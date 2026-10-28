import { useCallback, useEffect, useMemo, useState } from 'react';
import { Activity, ArrowDownToLine, ArrowRight, Award, BookOpen, Bookmark, CalendarDays, Check, CircleHelp, Clock3, FileJson2, Flame, GraduationCap, Layers3, ListChecks, LoaderCircle, Menu, Play, RefreshCw, Search, ShieldCheck, Sparkles, Target, Upload, X } from 'lucide-react';
import QuizSession from './components/QuizSession';
import FormulaLibrary from './components/FormulaLibrary';
import { focusLabels, kindLabels } from './components/practiceLabels';
import { DomainError } from './domain/errors';
import { formatDate, formatPoints } from './domain/format';
import { aggregateLearning } from './domain/analytics';
import { practicePool, selectExam, selectPractice, validateTrackWeights, type QuizFilter } from './domain/quiz';
import type { Attempt, ExamWeights, FocusTopic, PracticeKind, QuestionBank, StudyMode } from './domain/types';
import { loadContent, type ContentBundle } from './services/content';
import { claimAttempt, createAttempt, createBackup, getSetting, listAttempts, listBookmarks, listStagedImports, removeStagedImport, restoreBackup, setSetting, stageImport, submitAttempt, type AppBackup, type Bookmark as SavedBookmark, type StagedImport, validateBackup } from './storage/database';
import { stageImportedBank, validateBank } from './domain/validation';

type Page = 'home' | 'study' | 'exam' | 'history' | 'data' | 'formulas';
const pageTitle: Record<Page, string> = { home: 'Tổng quan', study: 'Ôn tập', exam: 'Thi thử', history: 'Lịch sử', data: 'Dữ liệu', formulas: 'Công thức' };
const navItems: { id: Page; icon: typeof Activity; label: string }[] = [
  { id: 'home', icon: Layers3, label: 'Tổng quan' }, { id: 'study', icon: BookOpen, label: 'Ôn tập' },
  { id: 'formulas', icon: BookOpen, label: 'Công thức' }, { id: 'exam', icon: Target, label: 'Thi thử' }, { id: 'history', icon: Activity, label: 'Lịch sử' }, { id: 'data', icon: FileJson2, label: 'Dữ liệu' },
];
const modes: { id: Exclude<StudyMode, 'exam'>; title: string; text: string; icon: typeof BookOpen; color: string }[] = [
  { id: 'focus', title: 'Ôn trọng tâm', text: 'Bảy nhóm kiến thức, nhiều dạng bài.', icon: Target, color: 'amber' },
  { id: 'daily', title: 'Ôn tập hôm nay', text: 'Một lượt ngắn, theo ngày học.', icon: CalendarDays, color: 'mint' },
  { id: 'track', title: 'Theo Track', text: 'Tập trung vào một track.', icon: Layers3, color: 'blue' },
  { id: 'phase', title: 'Theo Phase', text: 'Ôn theo giai đoạn học.', icon: GraduationCap, color: 'lavender' },
  { id: 'mixed', title: 'Luyện tổng hợp', text: 'Trộn câu từ ngân hàng.', icon: Sparkles, color: 'amber' },
  { id: 'wrong', title: 'Câu cần xem lại', text: 'Tập trung câu sai hoặc bỏ trống.', icon: RefreshCw, color: 'rose' },
  { id: 'bookmarked', title: 'Đã lưu', text: 'Quay lại câu hỏi đã đánh dấu.', icon: Bookmark, color: 'sky' },
];

function routeFromHash(): Page {
  const key = window.location.hash.replace(/^#\/?/, '').split('/')[0] as Page;
  return ['home', 'study', 'exam', 'history', 'data', 'formulas'].includes(key) ? key : 'home';
}
function safeId(prefix: string) { return `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`; }
function errorText(error: unknown) { return error instanceof Error ? error.message : 'Có lỗi xảy ra. Vui lòng thử lại.'; }
function dayLabel(day: string) {
  const match = day.match(/^p([12])(?:-t([1-4]))?-d(\d+)$/);
  if (!match) return day;
  return `Ngày ${Number(match[3])} · ${match[2] ? `Track ${match[2]}` : `Phase ${match[1]}`}`;
}

export default function App() {
  const [page, setPage] = useState<Page>(() => routeFromHash());
  const [writerToken] = useState(() => crypto.randomUUID());
  const [content, setContent] = useState<ContentBundle | null>(null);
  const [contentError, setContentError] = useState('');
  const [attempts, setAttempts] = useState<Attempt[]>([]);
  const [bookmarks, setBookmarks] = useState<SavedBookmark[]>([]);
  const [staged, setStaged] = useState<StagedImport[]>([]);
  const [weights, setWeights] = useState<ExamWeights>([25, 25, 25, 25]);
  const [active, setActive] = useState<Attempt | null>(null);
  const [toast, setToast] = useState('');
  const [mobileOpen, setMobileOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [importPreview, setImportPreview] = useState<{ backup?: AppBackup; stage?: StagedImport; conflicts?: string[] } | null>(null);
  const [weightWarning, setWeightWarning] = useState('');

  const refreshLocal = useCallback(async () => {
    const [a, b, s, w] = await Promise.all([listAttempts(), listBookmarks(), listStagedImports(), getSetting<ExamWeights>('examWeights', [25, 25, 25, 25])]);
    setAttempts(a); setBookmarks(b); setStaged(s); setWeights(w);
  }, []);
  const notifyError = useCallback((message: string) => { setToast(message); window.setTimeout(() => setToast(''), 5000); }, []);
  const refreshContent = useCallback(async () => {
    setLoading(true); setContentError('');
    try { const bundle = await loadContent(); setContent(bundle); }
    catch (e) { setContent(null); setContentError(errorText(e)); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => {
    const onHash = () => { setPage(routeFromHash()); setMobileOpen(false); };
    window.addEventListener('hashchange', onHash);
    if (!window.location.hash) window.location.hash = '#/home';
    void refreshContent();
    void (async () => {
      try {
        await refreshLocal();
        const inProgress = (await listAttempts()).find(a => a.status === 'in_progress');
        if (inProgress) {
          if (inProgress.deadlineAt !== null && Date.now() >= inProgress.deadlineAt) {
            const submitted = await submitAttempt(inProgress.id, undefined, Date.now(), true);
            setActive(submitted); await refreshLocal();
          } else setActive(await claimAttempt(inProgress.id, writerToken));
        }
      } catch (e) { notifyError(errorText(e)); }
    })();
    return () => window.removeEventListener('hashchange', onHash);
  }, [refreshContent, refreshLocal, notifyError, writerToken]);

  const bookmarkedSet = useMemo(() => new Set(bookmarks.map(b => b.questionId)), [bookmarks]);
  const wrongIds = useMemo(() => [...new Set(attempts.flatMap(a => a.status !== 'in_progress' ? a.score?.wrongIds ?? [] : []))], [attempts]);
  const recent = attempts.filter(a => a.status !== 'in_progress').slice(0, 4);
  const completed = attempts.filter(a => a.status !== 'in_progress');
  const graded = attempts.filter(a => a.status === 'graded');
  const average = graded.length ? graded.reduce((sum, a) => sum + ((a.score?.totalPoints ?? 0) / Math.max(1, a.score?.maxPoints ?? 1)), 0) / graded.length : null;
  const topicById = useMemo(() => new Map(content?.catalog.topics.map(t => [t.id, t.label]) ?? []), [content]);

  const navigate = useCallback((next: Page) => { if (window.location.hash !== `#/${next}`) window.location.hash = `#/${next}`; setPage(next); setMobileOpen(false); }, []);
  const launch = useCallback(async (mode: Exclude<StudyMode, 'exam'>, filter: LaunchFilter = {}) => {
    if (!content) { notifyError('Chưa có ngân hàng câu hỏi đã duyệt để mở phiên.'); return; }
    try {
      const review = mode === 'wrong' ? wrongIds : mode === 'bookmarked' ? [...bookmarkedSet] : [];
      const available = practicePool(content.bank.questions, mode, filter, review).length;
      const count = mode === 'wrong' || mode === 'bookmarked' ? filter.count : filter.count ?? Math.min(10, available);
      const selected = selectPractice(content.bank.questions, mode, { ...filter, count, seed: safeId(mode) }, review);
      const created = await createAttempt({ mode, label: selected.label, seed: selected.seed, bankVersion: content.bank.bank_version, questions: selected.items, writerToken });
      setActive(created); setAttempts(await listAttempts());
    } catch (e) { notifyError(errorText(e)); }
  }, [content, notifyError, wrongIds, bookmarkedSet, writerToken]);
  const launchExam = useCallback(async () => {
    if (!content) { notifyError('Chưa có ngân hàng câu hỏi đã duyệt để tạo đề.'); return; }
    try {
      validateTrackWeights(weights);
      const selected = selectExam(content.bank.questions, content.catalog, weights, safeId('mock'));
      await setSetting('examWeights', weights);
      const created = await createAttempt({ mode: 'exam', label: selected.label, seed: selected.seed, bankVersion: content.bank.bank_version, questions: selected.items, writerToken });
      setActive(created); setAttempts(await listAttempts());
    } catch (e) { notifyError(errorText(e)); }
  }, [content, weights, notifyError, writerToken]);
  const acceptWeights = useCallback((next: ExamWeights) => {
    setWeights(next);
    try { validateTrackWeights(next); setWeightWarning(''); }
    catch (e) { setWeightWarning(errorText(e)); }
  }, []);
  const onAttemptChange = useCallback((next: Attempt) => {
    setActive(next); setAttempts(old => [next, ...old.filter(a => a.id !== next.id)].sort((a, b) => (b.finalizedAt ?? b.startedAt) - (a.finalizedAt ?? a.startedAt)));
  }, []);
  const openAttempt = useCallback(async (attempt: Attempt) => {
    try { setActive(attempt.status === 'in_progress' || attempt.status === 'submitted_pending_grading' ? await claimAttempt(attempt.id, writerToken) : attempt); }
    catch (e) { notifyError(errorText(e)); }
  }, [writerToken, notifyError]);
  const onBookmarkChange = useCallback((id: string, saved: boolean) => setBookmarks(old => saved ? [...old, { questionId: id, createdAt: Date.now() }] : old.filter(b => b.questionId !== id)), []);

  async function handleImport(file?: File) {
    if (!file) return;
    if (file.size > 10 * 1024 * 1024) { notifyError('Tệp vượt giới hạn 10 MB.'); return; }
    try {
      const parsed: unknown = JSON.parse(await file.text());
      if (parsed && typeof parsed === 'object' && (parsed as { kind?: string }).kind === 'aia-study-backup') {
        const backup = validateBackup(parsed);
        const [existingAttempts, existingBookmarks] = await Promise.all([listAttempts(), listBookmarks()]);
        const attemptMap = new Map(existingAttempts.map(a => [a.id, a])); const bookmarkMap = new Map(existingBookmarks.map(bm => [bm.questionId, bm]));
        const conflicts = [
          ...backup.attempts.filter(a => attemptMap.has(a.id) && JSON.stringify(attemptMap.get(a.id)) !== JSON.stringify(a)).map(a => `Phiên ${a.id}`),
          ...backup.bookmarks.filter(bm => bookmarkMap.has(bm.questionId) && JSON.stringify(bookmarkMap.get(bm.questionId)) !== JSON.stringify(bm)).map(bm => `Bookmark ${bm.questionId}`),
        ];
        setImportPreview({ backup, conflicts }); return;
      }
      if (!content) throw new DomainError('Cần tải được catalog trước để kiểm tra câu hỏi nhập vào.', 'catalog_missing');
      if (!parsed || typeof parsed !== 'object' || !Array.isArray((parsed as Partial<QuestionBank>).questions) || (parsed as QuestionBank).questions.length > 5000) throw new DomainError('Tệp ngân hàng vượt giới hạn 5.000 câu hoặc sai định dạng.', 'import_size');
      const bank = validateBank(parsed, content.catalog, false);
      const stagedBank = stageImportedBank(bank);
      const batch: StagedImport = { id: safeId('import'), createdAt: Date.now(), sourceVersion: bank.bank_version, questions: stagedBank.questions };
      setImportPreview({ stage: batch });
    } catch (e) { notifyError(errorText(e)); }
  }
  async function confirmStageImport() {
    if (!importPreview?.stage) return;
    try { await stageImport(importPreview.stage); setImportPreview(null); setStaged(await listStagedImports()); notifyError('Đã đưa batch vào vùng chờ duyệt.'); }
    catch (e) { notifyError(errorText(e)); }
  }
  async function confirmBackupRestore() {
    if (!importPreview?.backup) return;
    try { await restoreBackup(importPreview.backup); setImportPreview(null); await refreshLocal(); notifyError('Đã nhập bản sao lưu vào thiết bị.'); }
    catch (e) { notifyError(errorText(e)); }
  }
  async function downloadBackup() {
    try {
      const backup = await createBackup(); const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob); const anchor = document.createElement('a'); anchor.href = url; anchor.download = `aia-study-backup-${new Date().toISOString().slice(0, 10)}.json`; anchor.click(); URL.revokeObjectURL(url);
    } catch (e) { notifyError(errorText(e)); }
  }
  function downloadQuestionBank() {
    if (!content) { notifyError('Ngân hàng câu hỏi chưa tải được để xuất.'); return; }
    const blob = new Blob([JSON.stringify(content.bank, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob); const anchor = document.createElement('a'); anchor.href = url; anchor.download = `aia-question-bank-${content.bank.bank_version}.json`; anchor.click(); URL.revokeObjectURL(url);
  }

  if (active) return <QuizSession initial={active} writerToken={writerToken} topicLabels={topicById} bookmarked={bookmarkedSet} onChange={onAttemptChange} onExit={() => { setActive(null); navigate(active.status === 'in_progress' ? 'study' : 'history'); }} onBookmarkChange={onBookmarkChange} onError={notifyError} />;

  return <div className="app-shell">
    <aside className={`sidebar ${mobileOpen ? 'sidebar-open' : ''}`}>
      <a href="#/home" className="brand" onClick={() => navigate('home')}><span className="brand-mark"><GraduationCap size={23} strokeWidth={2.2} /></span><span><b>AIA Study</b><small>LEARN WITH INTENTION</small></span></a>
      <div className="workspace-label">KHÔNG GIAN HỌC TẬP</div>
      <nav className="side-nav" aria-label="Điều hướng chính">{navItems.map(item => { const Icon = item.icon; return <a href={`#/${item.id}`} key={item.id} className={`nav-link ${page === item.id ? 'active' : ''}`} onClick={e => { e.preventDefault(); navigate(item.id); }}><Icon size={18} strokeWidth={1.9} /><span>{item.label}</span></a>; })}</nav>
      <div className="sidebar-bottom"><div className="sidebar-callout"><span className="callout-icon"><Sparkles size={17} /></span><b>Học đều mỗi ngày</b><p>Một bước nhỏ hôm nay tạo khác biệt lớn ngày mai.</p><button onClick={() => navigate('study')}>Bắt đầu học <ArrowRight size={14} /></button></div><div className="local-status"><span className="status-dot" /> Dữ liệu lưu trên thiết bị</div></div>
    </aside>
    {mobileOpen && <button className="scrim" aria-label="Đóng menu" onClick={() => setMobileOpen(false)} />}
    <div className="main-column"><header className="topbar"><button className="mobile-menu" aria-label="Mở điều hướng" onClick={() => setMobileOpen(v => !v)}><Menu size={21} /></button><div className="breadcrumb"><span>Không gian học tập</span><span className="crumb-slash">/</span><b>{pageTitle[page]}</b></div><div className="topbar-right"><span className="today-label"><CalendarDays size={16} /> {new Intl.DateTimeFormat('vi-VN', { weekday: 'long', day: 'numeric', month: 'long' }).format(new Date())}</span><button className="avatar" aria-label="Hồ sơ cá nhân">A</button></div></header>
      <div className="page-content">
        {page === 'home' && <Dashboard content={content} contentError={contentError} loading={loading} onRefresh={refreshContent} totalQuestions={content?.bank.questions.length ?? 0} attempts={completed} average={average} bookmarks={bookmarks.length} recent={recent} onNavigate={navigate} onLaunch={launch} onExam={launchExam} />}
        {page === 'study' && <StudyPage content={content} contentError={contentError} loading={loading} onLaunch={launch} wrongIds={wrongIds} bookmarkedIds={[...bookmarkedSet]} />}
        {page === 'formulas' && <FormulaLibrary questions={content?.bank.questions ?? []} loading={loading} error={contentError} />}
        {page === 'exam' && <ExamPage weights={weights} onWeights={acceptWeights} warning={weightWarning} content={content} loading={loading} onLaunch={launchExam} attempts={completed.filter(a => a.mode === 'exam')} />}
        {page === 'history' && <HistoryPage attempts={attempts} topicById={topicById} onOpen={openAttempt} />}
        {page === 'data' && <DataPage content={content} error={contentError} attempts={completed.length} bookmarks={bookmarks.length} staged={staged} onDownload={downloadBackup} onDownloadBank={downloadQuestionBank} onFile={handleImport} onRemoveStage={async id => { await removeStagedImport(id); setStaged(await listStagedImports()); }} />}
      </div>
      <footer className="app-footer"><span>© 2026 AIA Study</span><span><ShieldCheck size={14} /> Riêng tư theo mặc định</span></footer>
    </div>
    {toast && <div className="toast" role="status"><CircleHelp size={17} /> {toast}<button onClick={() => setToast('')} aria-label="Đóng thông báo"><X size={16} /></button></div>}
    {importPreview && <div className="modal-scrim" role="presentation"><section className="modal" role="dialog" aria-modal="true" aria-labelledby="import-title"><button className="modal-close" onClick={() => setImportPreview(null)} aria-label="Đóng"><X size={18} /></button><span className="eyebrow">XEM TRƯỚC TỆP</span><h2 id="import-title">{importPreview.backup ? 'Khôi phục dữ liệu cá nhân' : 'Xem trước câu hỏi nhập vào'}</h2>{importPreview.backup ? <><p>Tệp gồm {importPreview.backup.attempts.length} phiên đã nộp và {importPreview.backup.bookmarks.length} bookmark. Dữ liệu trùng khớp sẽ được giữ nguyên; dữ liệu cùng ID nhưng khác nội dung sẽ bị từ chối để tránh ghi đè.</p>{Boolean(importPreview.conflicts?.length) && <div className="validation-warning" role="status">Có {importPreview.conflicts?.length} mục trùng ID nhưng khác dữ liệu. Khôi phục sẽ dừng và không thay đổi dữ liệu hiện có.</div>}<div className="modal-actions"><button className="button button-secondary" onClick={() => setImportPreview(null)}>Hủy</button><button className="button button-primary" onClick={() => void confirmBackupRestore()}>Khôi phục dữ liệu <ArrowRight size={16} /></button></div></> : <><p>{importPreview.stage?.questions.length} câu đã được kiểm tra schema và taxonomy, rồi chuyển sang trạng thái chờ duyệt. Chúng không thể xuất hiện trong phiên học hay đề thi.</p><div className="modal-actions"><button className="button button-secondary" onClick={() => setImportPreview(null)}>Hủy</button><button className="button button-primary" onClick={() => void confirmStageImport()}>Đưa vào vùng chờ <ArrowRight size={16} /></button></div></>}</section></div>}
  </div>;
}

type LaunchFilter = QuizFilter;
type LaunchFn = (mode: Exclude<StudyMode, 'exam'>, filter?: LaunchFilter) => void;
type DashboardProps = { content: ContentBundle | null; contentError: string; loading: boolean; onRefresh: () => void; totalQuestions: number; attempts: Attempt[]; average: number | null; bookmarks: number; recent: Attempt[]; onNavigate: (page: Page) => void; onLaunch: LaunchFn; onExam: () => void };
function Dashboard({ content, contentError, loading, onRefresh, totalQuestions, attempts, average, bookmarks, recent, onNavigate, onLaunch, onExam }: DashboardProps) {
  const topics = content?.catalog.topics ?? [];
  const analytics = aggregateLearning(attempts);
  const topicLabels = new Map(topics.map(topic => [topic.id, topic.label]));
  const topicScores = Object.entries(analytics.byTopic).sort((a, b) => a[1].earned / Math.max(1, a[1].max) - b[1].earned / Math.max(1, b[1].max));
  return <>
    <div className="welcome-row"><div><span className="eyebrow">{new Intl.DateTimeFormat('vi-VN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }).format(new Date()).toLocaleUpperCase('vi-VN')}</span><h1>Chào bạn, bắt đầu<br className="desktop-only" /> từ điều nhỏ nhất.</h1><p>Mỗi lượt học là một bước gần hơn đến sự tự tin.</p><small className="coverage-note">Ngân hàng gồm các câu hỏi ôn tập theo tài liệu hiện có, không thay thế việc đọc đầy đủ học phần.</small></div><div className="welcome-illustration" aria-hidden="true"><div className="illustration-sun" /><div className="illustration-book"><span /><span /><span /></div><div className="illustration-leaf leaf-one" /><div className="illustration-leaf leaf-two" /><span className="illustration-star">✦</span></div></div>
    {(loading || !content) && <div className={`content-notice ${content ? '' : 'notice-empty'}`}>{loading ? <><LoaderCircle className="spin" size={18} /> Đang tải ngân hàng câu hỏi…</> : <><div className="notice-icon"><BookOpen size={20} /></div><div><b>Ngân hàng câu hỏi chưa sẵn sàng</b><p>{contentError || 'Cần có bộ câu hỏi đã duyệt để bắt đầu luyện tập.'} Khi có dữ liệu, trang sẽ tự tải lại bằng nút bên cạnh.</p></div><button className="button button-secondary" onClick={onRefresh}><RefreshCw size={15} /> Tải lại</button></>}</div>}
    <section className="hero-panel"><div className="hero-copy"><span className="hero-kicker"><span className="hero-kicker-dot" /> NHỊP HỌC CỦA BẠN</span><h2>Kiến thức vững<br />bắt đầu từ hôm nay.</h2><p>Ôn tập theo chủ đề hoặc thử sức với đề thi 90 phút.</p><div className="hero-actions"><button className="button button-light" onClick={() => onNavigate('study')}>Chọn chế độ học <ArrowRight size={16} /></button><button className="hero-link" onClick={onExam}>Thi thử ngay <ArrowRight size={15} /></button></div></div><div className="hero-art" aria-hidden="true"><div className="hero-orbit orbit-one" /><div className="hero-orbit orbit-two" /><div className="hero-bubble bubble-top"><Sparkles size={17} /></div><div className="hero-book"><div className="book-spine" /><div className="book-lines"><i /><i /><i /><i /></div><div className="book-seal"><Check size={20} /></div></div><div className="hero-bubble bubble-bottom"><Flame size={16} /><b>{attempts.length ? `${attempts.length} phiên đã học` : 'Bắt đầu ngày đầu tiên'}</b></div></div><div className="hero-index">01 <span>/ 04</span></div></section>
    <section className="stats-grid" aria-label="Tiến độ học tập"><StatCard icon={BookOpen} label="Câu hỏi đã duyệt" value={loading ? '—' : totalQuestions.toLocaleString('vi-VN')} foot="Sẵn sàng để ôn luyện" color="mint" /><StatCard icon={Award} label="Phiên đã hoàn thành" value={attempts.length.toString()} foot="Lịch sử trên thiết bị này" color="lavender" /><StatCard icon={Target} label="Điểm trung bình" value={average === null ? '—' : `${Math.round(average * 100)}%`} foot="Dựa trên phiên đã nộp" color="amber" /><StatCard icon={Bookmark} label="Câu hỏi đã lưu" value={bookmarks.toString()} foot="Dành cho lần xem lại sau" color="rose" /></section>
    <section className="section-card analytics-card"><div className="section-heading"><div><span className="eyebrow">TIẾN ĐỘ THEO NỘI DUNG</span><h2>Điểm mạnh và phần cần ôn</h2><p>Thống kê dựa trên các phiên đã chấm; câu tự luận chờ tự đánh giá chưa được tính.</p></div></div><div className="analytics-columns"><AnalyticsGroup title="Theo Phase" rows={analytics.byPhase} /><AnalyticsGroup title="Theo Track" rows={analytics.byTrack} /><AnalyticsGroup title="Theo chủ đề" rows={Object.fromEntries(topicScores.slice(0, 5))} labels={topicLabels} /></div><details className="topic-analytics-more"><summary>Xem thống kê tất cả {topicScores.length} chủ đề</summary><div className="topic-analytics-list">{topicScores.map(([id, score]) => <AnalyticsRow key={id} label={topicLabels.get(id) ?? id} score={score} />)}</div></details><div className="review-topics"><div><span className="eyebrow">CÂU SAI HOẶC BỎ TRỐNG</span><h3>Gợi ý ôn tập tiếp theo</h3></div>{analytics.topicsToReview.length ? <div className="review-topic-list">{analytics.topicsToReview.slice(0, 5).map(topic => <button key={topic.id} className="review-topic-row" onClick={() => onLaunch('wrong', { topic: topic.id })}><span><b>{topicLabels.get(topic.id) ?? topic.id}</b><small>{topic.misses} câu cần xem lại · {topic.sessions} phiên</small></span><ArrowRight size={16} /></button>)}</div> : <p className="analytics-empty">Các chủ đề có câu sai hoặc bỏ trống sẽ xuất hiện sau khi hoàn thành một phiên.</p>}</div></section>
    <div className="dashboard-columns"><section className="section-card"><div className="section-heading"><div><span className="eyebrow">LỰA CHỌN CỦA BẠN</span><h2>Bắt đầu một lượt học</h2></div><button className="text-link" onClick={() => onNavigate('study')}>Tất cả chế độ <ArrowRight size={15} /></button></div><div className="mode-tiles">{modes.slice(0, 4).map(mode => <ModeTile key={mode.id} mode={mode} onClick={() => mode.id === 'track' || mode.id === 'phase' ? onNavigate('study') : onLaunch(mode.id)} />)}</div></section><section className="section-card topic-card"><div className="section-heading"><div><span className="eyebrow">BẢN ĐỒ NỘI DUNG</span><h2>Chủ đề học tập</h2></div><span className="small-count">{topics.length} chủ đề</span></div>{topics.length ? <div className="topic-list">{topics.slice(0, 4).map(topic => <button className="topic-row" key={topic.id} onClick={() => onLaunch('mixed', { topic: topic.id })}><span className="topic-dot" /><span className="topic-copy"><b>{topic.label}</b><small>Phase {topic.phase}{topic.track ? ` · Track ${topic.track}` : ''}{topic.day ? ` · ${dayLabel(topic.day)}` : ''}</small></span><span className="topic-qty">{topic.question_count} câu</span><ArrowRight size={15} /></button>)}</div> : <EmptyInline text="Danh mục chủ đề sẽ xuất hiện khi có catalog." />}</section></div>
    <section className="section-card recent-card"><div className="section-heading"><div><span className="eyebrow">TIẾP NỐI HÀNH TRÌNH</span><h2>Hoạt động gần đây</h2></div><button className="text-link" onClick={() => onNavigate('history')}>Xem lịch sử <ArrowRight size={15} /></button></div>{recent.length ? <div className="recent-list">{recent.map(a => <button key={a.id} className="recent-row" onClick={() => onNavigate('history')}><span className={`recent-symbol ${a.mode === 'exam' ? 'symbol-exam' : ''}`}>{a.mode === 'exam' ? <Target size={18} /> : <BookOpen size={18} />}</span><span className="recent-title"><b>{a.label}</b><small>{formatDate(a.finalizedAt ?? a.startedAt)} · {a.questions.length} câu</small></span><span className="recent-score">{a.score ? `${formatPoints(a.score.totalPoints)} / ${formatPoints(a.score.maxPoints)}` : 'Đang chấm'}</span><ArrowRight size={15} /></button>)}</div> : <EmptyInline text="Các phiên đã hoàn thành sẽ được lưu tại đây." />}</section>
    <div className="dashboard-bottom"><div className="quote-card"><span>“</span><p>Học tập không phải là tích lũy câu trả lời, mà là rèn luyện cách đặt câu hỏi tốt hơn.</p><small>MỘT GHI CHÚ NHỎ CHO HÔM NAY</small></div><div className="quick-exam"><div className="quick-exam-icon"><Clock3 size={18} /></div><div><b>Thử đề mô phỏng</b><p>60 câu · 90 phút · lưu tiến độ tự động</p></div><button onClick={onExam} aria-label="Mở thiết lập thi thử"><ArrowRight size={18} /></button></div></div>
  </>;
}
function StatCard({ icon: Icon, label, value, foot, color }: { icon: typeof Activity; label: string; value: string; foot: string; color: string }) { return <article className="stat-card"><div className={`stat-icon ${color}`}><Icon size={18} /></div><span>{label}</span><b>{value}</b><small>{foot}</small></article>; }
function ModeTile({ mode, onClick }: { mode: typeof modes[number]; onClick: () => void }) { const Icon = mode.icon; return <button className="mode-tile" onClick={onClick}><span className={`mode-icon ${mode.color}`}><Icon size={18} /></span><b>{mode.title}</b><small>{mode.text}</small><span className="mode-arrow"><ArrowRight size={15} /></span></button>; }
function EmptyInline({ text }: { text: string }) { return <div className="empty-inline"><CircleHelp size={16} />{text}</div>; }

type StudyPageProps = { content: ContentBundle | null; contentError: string; loading: boolean; onLaunch: LaunchFn; wrongIds: string[]; bookmarkedIds: string[] };
function StudyPage({ content, contentError, loading, onLaunch, wrongIds, bookmarkedIds }: StudyPageProps) {
  const [mode, setMode] = useState<Exclude<StudyMode, 'exam'>>('daily');
  const [phase, setPhase] = useState<1 | 2>(1);
  const [track, setTrack] = useState<1 | 2 | 3 | 4>(1);
  const [day, setDay] = useState('');
  const [topic, setTopic] = useState('');
  const [mixedPhase, setMixedPhase] = useState<'both' | 1 | 2>('both');
  const [mixedTracks, setMixedTracks] = useState<(1 | 2 | 3 | 4)[]>([1, 2, 3, 4]);
  const [count, setCount] = useState(10);
  const [practiceKind, setPracticeKind] = useState<PracticeKind | ''>('');
  const [focusTopic, setFocusTopic] = useState<FocusTopic | ''>('');
  const [difficulty, setDifficulty] = useState<'' | 'easy' | 'medium' | 'hard'>('');
  const days = [...new Map((content?.catalog.topics ?? []).filter(t => t.day && t.phase === phase).map(t => [t.day!, t.day!])).values()].sort();
  const currentMode = modes.find(m => m.id === mode)!;
  const Icon = currentMode.icon;
  const reviewIds = mode === 'wrong' ? wrongIds : mode === 'bookmarked' ? bookmarkedIds : [];
  const selectedFilter: QuizFilter = { practiceKind: practiceKind || undefined, focusTopic: focusTopic || undefined, phase: mode === 'phase' || mode === 'daily' ? phase : mode === 'mixed' && mixedPhase !== 'both' ? mixedPhase : undefined, track: mode === 'track' ? track : undefined, tracks: mode === 'mixed' && mixedPhase !== 1 ? mixedTracks : undefined, day: mode === 'daily' && day ? day : undefined, topic: topic || undefined, difficulty: difficulty || undefined };
  const available = content ? practicePool(content.bank.questions, mode, selectedFilter, reviewIds).length : 0;
  const targetCount = Math.min(count, available);
  const countOptions = [...new Set([5, 10, ...(mode === 'focus' ? [14] : []), 15, 20, 30, 60, targetCount, ...(available <= 60 ? [available] : [])])].filter(n => n > 0 && n <= available).sort((a, b) => a - b);
  const actionable = Boolean(content) && !loading && available > 0;
  return <div className="study-page">
    <PageIntro eyebrow="HỌC THEO CÁCH CỦA BẠN" title="Chọn một chế độ ôn tập" subtitle="Mỗi chế độ giữ đúng phạm vi đã chọn. Phiên học không lặp câu và lưu tiến độ ngay trên thiết bị." />
    {!content && <div className="content-notice notice-empty"><div className="notice-icon"><BookOpen size={20} /></div><div><b>{loading ? 'Đang tải câu hỏi…' : 'Ngân hàng chưa sẵn sàng'}</b><p>{contentError || 'Hãy tải dữ liệu đã duyệt để mở phiên học.'}</p></div></div>}
    <div className="study-layout"><section className="mode-picker"><div className="mode-picker-head"><span className="eyebrow">CHỌN PHẠM VI</span><span className="small-count">{modes.length} chế độ</span></div>{modes.map(m => { const MIcon = m.icon; const badge = m.id === 'wrong' ? wrongIds.length : m.id === 'bookmarked' ? bookmarkedIds.length : null; return <button key={m.id} className={`mode-choice ${mode === m.id ? 'active' : ''}`} onClick={() => { setMode(m.id); setTopic(''); setFocusTopic(''); if (m.id === 'focus') { setPracticeKind(''); setCount(14); } }}><span className={`mode-icon ${m.color}`}><MIcon size={17} /></span><span><b>{m.title}</b><small>{m.text}</small></span>{badge !== null && <span className="choice-count">{badge}</span>}</button>; })}</section>
      <section className="section-card mode-detail"><div className="mode-detail-heading"><span className={`mode-icon large ${currentMode.color}`}><Icon size={21} /></span><div><span className="eyebrow">CHẾ ĐỘ HỌC</span><h2>{currentMode.title}</h2><p>{currentMode.text}</p></div></div>
        {mode === 'focus' && <p className="focus-note">Luyện ReAct, tham số sinh, Kalman, cảm biến, vòng kín, hàm kích hoạt và chuẩn hóa; phân bổ đều các nhóm và dạng bài có sẵn trong bộ lọc. Đây là định hướng ôn tập, không phải đề thi chính thức hay tỷ lệ đã xác minh. Đề thi thử 60 câu vẫn giữ cấu hình riêng.</p>}
        <div className="filter-grid">{(mode === 'phase' || mode === 'daily') && <label className="field-label">Phase<select value={phase} onChange={e => { setPhase(Number(e.target.value) as 1 | 2); setDay(''); setTopic(''); }}><option value={1}>Phase 1</option><option value={2}>Phase 2</option></select></label>}{mode === 'mixed' && <label className="field-label">Phạm vi Phase<select value={mixedPhase} onChange={e => { setMixedPhase(e.target.value === 'both' ? 'both' : Number(e.target.value) as 1 | 2); setTopic(''); }}><option value="both">Cả hai Phase</option><option value={1}>Phase 1</option><option value={2}>Phase 2</option></select></label>}{mode === 'track' && <label className="field-label">Track<select value={track} onChange={e => { setTrack(Number(e.target.value) as 1 | 2 | 3 | 4); setTopic(''); }}>{[1, 2, 3, 4].map(n => <option key={n} value={n}>Track {n}</option>)}</select></label>}{mode === 'mixed' && mixedPhase !== 1 && <fieldset className="field-label track-filter"><legend>Track trong Phase 2</legend>{([1, 2, 3, 4] as const).map(n => <label key={n}><input type="checkbox" checked={mixedTracks.includes(n)} onChange={e => setMixedTracks(v => e.target.checked ? [...v, n].sort() : v.filter(x => x !== n))} />Track {n}</label>)}</fieldset>}{mode === 'daily' && <label className="field-label">Ngày học<select value={day} onChange={e => { setDay(e.target.value); setTopic(''); }}><option value="">Tự chọn một ngày có câu hỏi</option>{days.map(d => <option key={d} value={d}>{dayLabel(d)}</option>)}</select></label>}<label className="field-label">Chủ đề<select value={topic} onChange={e => setTopic(e.target.value)}><option value="">Tất cả chủ đề phù hợp</option>{(content?.catalog.topics ?? []).filter(t => (!selectedFilter.phase || t.phase === selectedFilter.phase) && (!selectedFilter.track || t.track === selectedFilter.track) && (!selectedFilter.tracks || t.phase !== 2 || selectedFilter.tracks.includes(t.track as 1 | 2 | 3 | 4)) && (!selectedFilter.day || t.day === selectedFilter.day)).map(t => <option value={t.id} key={t.id}>{t.label}</option>)}</select></label><label className="field-label">Nhóm trọng tâm<select value={focusTopic} onChange={e => setFocusTopic(e.target.value as FocusTopic | '')}><option value="">Tất cả nhóm</option>{Object.entries(focusLabels).map(([id, label]) => <option key={id} value={id}>{label}</option>)}</select></label><label className="field-label">Dạng bài<select value={practiceKind || 'all'} onChange={e => setPracticeKind(e.target.value === 'all' ? '' : e.target.value as PracticeKind)}><option value="all">Tất cả dạng bài</option>{Object.entries(kindLabels).map(([id, label]) => <option key={id} value={id}>{label}</option>)}</select></label><label className="field-label">Độ khó<select value={difficulty} onChange={e => setDifficulty(e.target.value as typeof difficulty)}><option value="">Tất cả độ khó</option><option value="easy">Dễ</option><option value="medium">Trung bình</option><option value="hard">Khó</option></select></label>{mode !== 'wrong' && mode !== 'bookmarked' && <label className="field-label">Số câu mục tiêu<select value={targetCount || count} onChange={e => setCount(Number(e.target.value))}>{countOptions.map(n => <option value={n} key={n}>{n} câu</option>)}</select></label>}</div>
        {(mode === 'wrong' || mode === 'bookmarked') && <div className="review-count-panel"><div className="review-count-number">{available}</div><div><b>{mode === 'wrong' ? 'câu cần xem lại' : 'câu hỏi đã lưu'}</b><p>{mode === 'wrong' ? 'Bao gồm câu sai hoặc bỏ trống trong các phiên đã nộp. Tự luận đang chờ chấm không được tính là sai.' : 'Các câu đã bookmark sẽ được đưa vào một lượt luyện riêng.'}</p></div></div>}
        <div className="mode-summary"><div><ListChecks size={17} /><span>{mode === 'wrong' || mode === 'bookmarked' ? `Bao gồm ${available} câu trong danh sách` : `Có ${available} câu phù hợp · mục tiêu ${targetCount}`}</span></div><div><ShieldCheck size={17} /><span>Chỉ câu hỏi đã duyệt độc lập</span></div><div><Clock3 size={17} /><span>Không giới hạn thời gian</span></div></div>
        <button className="button button-primary button-wide" disabled={!actionable || (mode === 'mixed' && mixedPhase !== 1 && !mixedTracks.length)} onClick={() => void onLaunch(mode, { ...selectedFilter, count: mode === 'wrong' || mode === 'bookmarked' ? undefined : targetCount })}><Play size={17} fill="currentColor" /> Bắt đầu lượt học <ArrowRight size={16} /></button>
        {!actionable && content && <small className="disabled-note">Chưa có câu phù hợp trong nhóm này.</small>}
      </section></div>
  </div>;
}

type ExamPageProps = { weights: ExamWeights; onWeights: (weights: ExamWeights) => void; warning: string; content: ContentBundle | null; loading: boolean; onLaunch: () => void; attempts: Attempt[] };
function ExamPage({ weights, onWeights, warning, content, loading, onLaunch, attempts }: ExamPageProps) {
  return <div className="exam-page"><PageIntro eyebrow="MÔ PHỎNG CÓ CẤU TRÚC" title="Làm quen với nhịp thi thật" subtitle="Một đề 90 phút với phân bổ điểm rõ ràng theo Phase, Track và dạng câu hỏi." />
    <div className="exam-hero"><div className="exam-hero-copy"><span className="exam-pill"><Clock3 size={14} /> THỜI LƯỢNG 90 PHÚT</span><h2>60 câu hỏi.<br />Một bức tranh toàn diện.</h2><p>Track 4 có ít nhất 2 câu tính toán để luyện với máy tính Casio. Câu hỏi được giữ nguyên trong suốt bài thi. Đồng hồ tiếp tục chạy nếu bạn tải lại trang; câu trả lời được lưu tự động.</p><div className="exam-facts"><span><b>60%</b> Phase 1 · 36 câu</span><i /><span><b>40%</b> Phase 2 · 24 câu</span><i /><span><b>10%</b> tự luận · 6 câu</span></div></div><div className="exam-graphic" aria-hidden="true"><div className="exam-ring ring-back" /><div className="exam-ring ring-front" /><div className="exam-center"><Target size={27} /><b>100</b><small>ĐIỂM</small></div><div className="ring-label ring-label-one">P1</div><div className="ring-label ring-label-two">P2</div><div className="ring-label ring-label-three">10%</div></div></div>
    <section className="section-card weight-card"><div className="section-heading"><div><span className="eyebrow">CẤU HÌNH PHASE 2</span><h2>Phân bổ trọng số Track</h2><p>Bốn tỷ trọng cần là số dương và cộng đúng 100%. Mỗi câu sẽ nhận điểm theo tỷ trọng đã chọn.</p></div><span className="total-weight">Tổng <b>{weights.reduce((a, b) => a + (Number.isFinite(b) ? b : 0), 0)}%</b></span></div><div className="weight-grid">{weights.map((weight, index) => <label className="weight-input" key={index}><span>Track {index + 1}</span><div><input type="number" min="0.25" max="99.25" step="0.25" value={weight} aria-label={`Trọng số Track ${index + 1}`} onChange={e => { const next = [...weights] as ExamWeights; next[index] = Number(e.target.value); onWeights(next); }} /><b>%</b></div><small>{Math.round(40 * weight) / 100} điểm Phase 2</small></label>)}</div>{warning && <div className="validation-warning" role="alert"><CircleHelp size={16} />{warning}</div>}
      <div className="blueprint-table"><div className="blueprint-row blueprint-head"><span>Phân bổ</span><span>Trắc nghiệm</span><span>Tự luận</span><span>Tổng điểm</span></div><div className="blueprint-row"><span>Phase 1</span><span>34 câu · 54 điểm</span><span>2 câu · 6 điểm</span><b>60</b></div>{weights.map((w, i) => <div className="blueprint-row" key={i}><span>Phase 2 · Track {i + 1}</span><span>5 câu · {formatPoints(36 * w)} điểm</span><span>1 câu · {formatPoints(4 * w)} điểm</span><b>{formatPoints(40 * w)}</b></div>)}<div className="blueprint-row blueprint-total"><span>Tổng đề</span><span>54 câu · 90 điểm</span><span>6 câu · 10 điểm</span><b>100</b></div></div>
      <div className="exam-bottom"><div className="exam-note"><ShieldCheck size={17} /><span>Đề chỉ bắt đầu khi đủ câu đã duyệt cho mọi nhóm. Không lặp câu và không lấy câu từ Track khác để bù thiếu.</span></div><button className="button button-primary" disabled={!content || loading || Boolean(warning)} onClick={onLaunch}><Play size={16} fill="currentColor" /> Bắt đầu thi thử <ArrowRight size={16} /></button></div>
    </section>
    <div className="exam-history-hint"><Award size={17} /><span>{attempts.length ? `Bạn đã hoàn thành ${attempts.length} bài thi thử trên thiết bị này.` : 'Kết quả thi thử sẽ lưu vào lịch sử sau khi nộp bài.'}</span></div>
  </div>;
}

function PageIntro({ eyebrow, title, subtitle }: { eyebrow: string; title: string; subtitle: string }) { return <div className="page-intro"><span className="eyebrow">{eyebrow}</span><h1>{title}</h1><p>{subtitle}</p></div>; }

function HistoryPage({ attempts, topicById, onOpen }: { attempts: Attempt[]; topicById: Map<string, string>; onOpen: (a: Attempt) => void }) {
  const [search, setSearch] = useState('');
  const filtered = attempts.filter(a => `${a.label} ${a.mode}`.toLowerCase().includes(search.toLowerCase()));
  return <div className="history-page"><PageIntro eyebrow="TIẾN ĐỘ CỦA BẠN" title="Lịch sử học tập" subtitle="Mỗi phiên đã nộp được lưu cùng đáp án và nội dung câu hỏi để bạn xem lại bất cứ lúc nào." />
    <section className="section-card history-card"><div className="history-toolbar"><div><span className="eyebrow">TẤT CẢ PHIÊN</span><h2>{attempts.length} phiên học</h2></div><label className="search-box"><Search size={16} /><input value={search} onChange={e => setSearch(e.target.value)} placeholder="Tìm phiên học" /></label></div>{filtered.length ? <div className="history-list">{filtered.map(a => { const result = a.score; const pct = result?.maxPoints ? Math.round(result.totalPoints / result.maxPoints * 100) : 0; const isActive = a.status === 'in_progress'; return <article className="history-row" key={a.id}><div className={`history-icon ${a.mode === 'exam' ? 'history-exam' : ''}`}>{a.mode === 'exam' ? <Target size={19} /> : <BookOpen size={19} />}</div><div className="history-main"><b>{a.label}</b><span>{formatDate(a.finalizedAt ?? a.startedAt)} <i>·</i> {a.questions.length} câu <i>·</i> {a.mode === 'exam' ? 'Thi thử' : 'Ôn tập'}</span><div className="history-tags">{isActive ? <em className="status-active">Đang làm</em> : a.status === 'submitted_pending_grading' ? <em className="status-pending">Chờ tự chấm</em> : <em className="status-done">Đã hoàn thành</em>}<span>{new Set(a.questions.map(q => topicById.get(q.question.topic)).filter(Boolean)).size} chủ đề</span></div></div><div className="history-result">{result && <><b>{formatPoints(result.totalPoints)}<small>/{formatPoints(result.maxPoints)}</small></b><span>{pct}%</span></>}</div><button className="button button-secondary history-open" onClick={() => onOpen(a)}>{isActive ? 'Tiếp tục' : a.status === 'submitted_pending_grading' ? 'Tiếp tục tự chấm' : 'Xem lại'} <ArrowRight size={15} /></button></article>; })}</div> : <EmptyState icon={Activity} title={search ? 'Không tìm thấy phiên phù hợp' : 'Chưa có phiên học'} text={search ? 'Thử một từ khóa khác.' : 'Khi hoàn thành lượt ôn tập hoặc đề thi, kết quả sẽ xuất hiện ở đây.'} />}</section>
  </div>;
}

function DataPage({ content, error, attempts, bookmarks, staged, onDownload, onDownloadBank, onFile, onRemoveStage }: { content: ContentBundle | null; error: string; attempts: number; bookmarks: number; staged: StagedImport[]; onDownload: () => void; onDownloadBank: () => void; onFile: (file?: File) => void; onRemoveStage: (id: string) => void }) {
  return <div className="data-page"><PageIntro eyebrow="DỮ LIỆU CỦA BẠN" title="Giữ dữ liệu luôn trong tầm tay" subtitle="Câu trả lời, dấu trang và lịch sử được lưu cục bộ. Xuất bản sao lưu định kỳ để chuyển thiết bị hoặc khôi phục." />
    <div className="data-summary"><div><BookOpen size={18} /><span><b>{content?.bank.questions.length ?? 0}</b> câu đã duyệt khả dụng</span></div><div><Activity size={18} /><span><b>{attempts}</b> phiên đã nộp</span></div><div><Bookmark size={18} /><span><b>{bookmarks}</b> bookmark</span></div></div>
    {!content && <div className="content-notice notice-empty"><div className="notice-icon"><BookOpen size={20} /></div><div><b>Chưa tải được ngân hàng tĩnh</b><p>{error || 'Bạn vẫn có thể sao lưu lịch sử cá nhân.'} Tệp câu hỏi nhập riêng sẽ được kiểm tra rồi đưa vào vùng chờ duyệt.</p></div></div>}
    <div className="data-actions-grid"><section className="section-card data-action-card"><span className="data-action-icon mint"><ArrowDownToLine size={21} /></span><span className="eyebrow">SAO LƯU CÁ NHÂN</span><h2>Xuất dữ liệu của bạn</h2><p>Tải về tệp JSON gồm lịch sử phiên đã nộp và bookmark để khôi phục về sau.</p><button className="button button-primary" onClick={onDownload}>Tải bản sao lưu <ArrowDownToLine size={16} /></button></section><section className="section-card data-action-card"><span className="data-action-icon blue"><Upload size={21} /></span><span className="eyebrow">NHẬP TỆP JSON</span><h2>Khôi phục hoặc kiểm tra</h2><p>Bản sao lưu cá nhân được xem trước trước khi nhập. Câu hỏi từ bên ngoài sẽ vào vùng chờ, không tự được dùng làm đề.</p><label className="button button-secondary file-button"><Upload size={16} /> Chọn tệp JSON<input type="file" accept="application/json,.json" onChange={e => { onFile(e.target.files?.[0]); e.currentTarget.value = ''; }} /></label></section></div>
    <section className="section-card bank-export"><div><span className="eyebrow">NGÂN HÀNG ĐÃ DUYỆT</span><h2>Xuất tệp câu hỏi</h2><p>Tải JSON của ngân hàng đang phát hành để dùng làm tài liệu ngoại tuyến.</p></div><button className="button button-secondary" disabled={!content} onClick={onDownloadBank}>Xuất ngân hàng JSON <ArrowDownToLine size={16} /></button></section>
    <section className="section-card staged-section"><div className="section-heading"><div><span className="eyebrow">CÁCH LY NỘI DUNG NHẬP</span><h2>Vùng chờ duyệt</h2><p>Nhập câu hỏi không thể làm thay đổi ngân hàng phát hành đang dùng.</p></div><span className="small-count">{staged.reduce((n, batch) => n + batch.questions.length, 0)} câu</span></div>{staged.length ? <div className="staged-list">{staged.map(batch => <article className="staged-row" key={batch.id}><span className="staged-icon"><FileJson2 size={17} /></span><div><b>{batch.sourceVersion}</b><small>{batch.questions.length} câu · {formatDate(batch.createdAt)} · trạng thái chờ duyệt</small></div><button className="icon-button" aria-label="Xóa batch nhập" onClick={() => onRemoveStage(batch.id)}><X size={17} /></button></article>)}</div> : <EmptyInline text="Chưa có batch nào được nhập." />}</section>
    <section className="privacy-note"><ShieldCheck size={19} /><div><b>Lưu trữ trên thiết bị này</b><p>Dữ liệu không được gửi lên máy chủ. Xóa dữ liệu trang web hoặc đổi trình duyệt có thể làm mất lịch sử nếu chưa xuất sao lưu.</p></div></section>
  </div>;
}
function EmptyState({ icon: Icon, title, text }: { icon: typeof Activity; title: string; text: string }) { return <div className="empty-state"><span><Icon size={22} /></span><b>{title}</b><p>{text}</p></div>; }
function AnalyticsGroup({ title, rows, labels }: { title: string; rows: Record<string, { earned: number; max: number }>; labels?: Map<string, string> }) {
  return <div className="analytics-group"><h3>{title}</h3>{Object.entries(rows).length ? Object.entries(rows).map(([id, score]) => <AnalyticsRow key={id} label={labels?.get(id) ?? (id === '—' ? 'Phase 1' : id)} score={score} />) : <p className="analytics-empty">Chưa có phiên đã chấm.</p>}</div>;
}
function AnalyticsRow({ label, score }: { label: string; score: { earned: number; max: number } }) {
  const percent = score.max ? Math.round(100 * score.earned / score.max) : 0;
  return <div className="analytics-row"><span>{label}</span><b>{formatPoints(score.earned)} / {formatPoints(score.max)}</b><div className="analytics-bar"><i style={{ width: `${percent}%` }} /></div></div>;
}
