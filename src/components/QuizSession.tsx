import { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, Bookmark, Check, CircleHelp, Clock3, Flag, Send, ShieldCheck, RotateCcw } from 'lucide-react';
import type { AnswerValue, Attempt, RubricMarks } from '../domain/types';
import QuestionText from './QuestionText';
import StructuredQuestion from './StructuredQuestion';
import QuestionSources from './QuestionSources';
import { formatPoints } from '../domain/format';
import { isCorrect, isBlankAnswer } from '../domain/grading';
import { getAttempt, gradeRubric, saveAnswer, submitAttempt, toggleBookmark, toggleFlag } from '../storage/database';

type Props = { initial: Attempt; writerToken: string; topicLabels: Map<string, string>; bookmarked: Set<string>; onChange: (attempt: Attempt) => void; onExit: () => void; onBookmarkChange: (id: string, saved: boolean) => void; onError: (message: string) => void };
export default function QuizSession({ initial, writerToken, topicLabels, bookmarked, onChange, onExit, onBookmarkChange, onError }: Props) {
  const [attempt, setAttempt] = useState(initial);
  const [index, setIndex] = useState(0);
  const [pendingWrites, setPendingWrites] = useState(0);
  const [saveError, setSaveError] = useState(false);
  const [unsavedAnswer, setUnsavedAnswer] = useState<{ questionId: string; answer: AnswerValue } | null>(null);
  const [sessionError, setSessionError] = useState('');
  const [now, setNow] = useState(Date.now());
  const [marks, setMarks] = useState<RubricMarks>({});
  const [essayDraft, setEssayDraft] = useState('');
  const answerQueue = useRef(Promise.resolve());
  const pendingWritesRef = useRef(0);
  const saveErrorRef = useRef(false);
  const latestEssayRef = useRef(new Map<string, string>());
  function reportError(message: string) { setSessionError(message); onError(message); }
  function saveFailure(error: unknown) {
    return error instanceof DOMException && error.name === 'QuotaExceededError'
      ? 'Không đủ dung lượng để lưu câu trả lời. Hãy giải phóng bộ nhớ rồi thử lại.'
      : error instanceof Error ? error.message : 'Chưa lưu được câu trả lời.';
  }
  useEffect(() => { setAttempt(initial); }, [initial.id]);
  useEffect(() => { const timer = window.setInterval(() => setNow(Date.now()), 500); return () => window.clearInterval(timer); }, []);
  useEffect(() => {
    const onVisibility = () => { if (document.visibilityState === 'visible') setNow(Date.now()); };
    document.addEventListener('visibilitychange', onVisibility);
    return () => document.removeEventListener('visibilitychange', onVisibility);
  }, []);
  useEffect(() => {
    let channel: BroadcastChannel | undefined;
    try {
      channel = new BroadcastChannel('aia-study-attempts');
      channel.onmessage = event => { if (event.data?.id === attempt.id) void getAttempt(attempt.id).then(fresh => { const currentId = attempt.questions[index]?.question.id; if (fresh) { setAttempt(fresh); if (fresh.writerToken !== writerToken && currentId && typeof fresh.answers[currentId] === 'string') setEssayDraft(fresh.answers[currentId] as string); onChange(fresh); } }); };
    } catch { /* IndexedDB remains the source of truth */ }
    return () => channel?.close();
  }, [attempt.id, attempt.questions, index, writerToken, onChange]);
  useEffect(() => {
    if (attempt.status === 'in_progress' && attempt.deadlineAt !== null && now >= attempt.deadlineAt) {
      void submitAttempt(attempt.id, undefined, now, true).then(next => { setAttempt(next); onChange(next); if (saveErrorRef.current) { setSessionError('Đã hết giờ. Các thay đổi chưa lưu không được tính trong bài đã nộp.'); } }).catch(e => reportError(e instanceof Error ? e.message : 'Không thể tự nộp bài.'));
    }
  }, [attempt.id, attempt.deadlineAt, attempt.status, now, onChange, onError]);
  const item = attempt.questions[index];
  const q = item.question;
  useEffect(() => { setEssayDraft(typeof attempt.answers[q.id] === 'string' ? attempt.answers[q.id] as string : ''); setMarks({}); }, [q.id]);
  const remaining = Math.max(0, attempt.deadlineAt === null ? 0 : attempt.deadlineAt - now);
  const submitted = attempt.status !== 'in_progress';
  const readOnly = attempt.status !== 'graded' && attempt.writerToken !== writerToken;
  const saving = pendingWrites > 0;
  useEffect(() => {
    if (submitted || (!saving && !saveError)) return;
    const warn = (event: BeforeUnloadEvent) => { event.preventDefault(); event.returnValue = ''; };
    window.addEventListener('beforeunload', warn);
    return () => window.removeEventListener('beforeunload', warn);
  }, [submitted, saving, saveError]);
  const answer = attempt.answers[q.id];
  const savedMarks = attempt.rubricMarks[q.id] ?? {};
  const currentMarks = { ...savedMarks, ...marks };
  const progress = useMemo(() => Object.values(attempt.answers).filter(value => !isBlankAnswer(value)).length, [attempt.answers]);

  function persistAnswer(nextAnswer: AnswerValue, questionId = q.id): Promise<boolean> {
    if (submitted) return Promise.resolve(false);
    if (typeof nextAnswer === 'string' && attempt.questions.find(part => part.question.id === questionId)?.question.answer_format === 'rubric') latestEssayRef.current.set(questionId, nextAnswer);
    pendingWritesRef.current += 1;
    setPendingWrites(pendingWritesRef.current);
    const work = answerQueue.current.then(async () => {
      try {
        const fresh = await getAttempt(attempt.id);
        if (!fresh) throw new Error('Phiên học không còn tồn tại.');
        const next = await saveAnswer(attempt.id, questionId, nextAnswer, fresh.revision, Date.now(), writerToken);
        if (next.status !== 'in_progress' && JSON.stringify(next.answers[questionId]) !== JSON.stringify(nextAnswer)) {
          setAttempt(next); onChange(next); saveErrorRef.current = true; setSaveError(true);
          setUnsavedAnswer({ questionId, answer: typeof nextAnswer === 'string' ? latestEssayRef.current.get(questionId) ?? nextAnswer : nextAnswer });
          reportError('Đã hết giờ trước khi lưu xong. Thay đổi chưa lưu không được tính trong bài đã nộp.'); return false;
        }
        const isEssay = attempt.questions.find(part => part.question.id === questionId)?.question.answer_format === 'rubric';
        if (!isEssay || latestEssayRef.current.get(questionId) === nextAnswer) {
          saveErrorRef.current = false; setSaveError(false); setUnsavedAnswer(null); setSessionError('');
        }
        setAttempt(next); onChange(next); return true;
      } catch (e) {
        const fresh = await getAttempt(attempt.id).catch(() => undefined);
        if (fresh) { setAttempt(fresh); onChange(fresh); }
        saveErrorRef.current = true; setSaveError(true);
        setUnsavedAnswer({ questionId, answer: typeof nextAnswer === 'string' ? latestEssayRef.current.get(questionId) ?? nextAnswer : nextAnswer });
        reportError(fresh && fresh.status !== 'in_progress' ? 'Đã hết giờ trước khi lưu xong. Thay đổi chưa lưu không được tính trong bài đã nộp.' : saveFailure(e)); return false;
      }
    });
    answerQueue.current = work.then(() => undefined).finally(() => {
      pendingWritesRef.current = Math.max(0, pendingWritesRef.current - 1);
      setPendingWrites(pendingWritesRef.current);
    });
    return work;
  }
  async function retryUnsavedAnswer() {
    if (!unsavedAnswer) return;
    await persistAnswer(unsavedAnswer.answer, unsavedAnswer.questionId);
  }
  async function toggleCurrentFlag() {
    try { const next = await toggleFlag(attempt.id, q.id, attempt.revision, Date.now(), writerToken); setAttempt(next); onChange(next); }
    catch (e) { const fresh = await getAttempt(attempt.id).catch(() => undefined); if (fresh) { setAttempt(fresh); onChange(fresh); } reportError(e instanceof Error ? e.message : 'Không thể đánh dấu.'); }
  }
  async function toggleCurrentBookmark() {
    try { const saved = await toggleBookmark(q.id); onBookmarkChange(q.id, saved); }
    catch (e) { reportError(e instanceof Error ? e.message : 'Không thể lưu bookmark.'); }
  }
  async function manualSubmit() {
    if (attempt.deadlineAt !== null && Date.now() >= attempt.deadlineAt) {
      try { const next = await submitAttempt(attempt.id, undefined, Date.now(), true); setAttempt(next); onChange(next); if (saveErrorRef.current) setSessionError('Đã hết giờ. Các thay đổi chưa lưu không được tính trong bài đã nộp.'); }
      catch (e) { reportError(e instanceof Error ? e.message : 'Không thể tự nộp bài.'); }
      return;
    }
    if (pendingWritesRef.current > 0) { reportError('Đang lưu câu trả lời. Hãy đợi lưu xong rồi nộp bài.'); return; }
    if (saveErrorRef.current) { reportError('Câu trả lời chưa lưu được. Hãy thử lưu lại trước khi nộp bài.'); return; }
    if (window.confirm('Nộp bài ngay bây giờ? Bạn sẽ không thể sửa đáp án sau khi nộp.')) {
      try { await answerQueue.current; const fresh = await getAttempt(attempt.id); if (!fresh) throw new Error('Phiên học không còn tồn tại.'); const next = await submitAttempt(attempt.id, fresh.revision, Date.now(), false, writerToken); setAttempt(next); onChange(next); }
      catch (e) { reportError(e instanceof Error ? e.message : 'Không nộp được bài.'); }
    }
  }
  async function navigateTo(nextIndex: number) {
    if (submitted) { setIndex(nextIndex); return; }
    if (attempt.deadlineAt !== null && Date.now() >= attempt.deadlineAt) {
      try { const next = await submitAttempt(attempt.id, undefined, Date.now(), true); setAttempt(next); onChange(next); if (saveErrorRef.current) setSessionError('Đã hết giờ. Các thay đổi chưa lưu không được tính trong bài đã nộp.'); }
      catch (e) { reportError(e instanceof Error ? e.message : 'Không thể tự nộp bài.'); }
      return;
    }
    if (pendingWritesRef.current > 0) { await answerQueue.current; }
    if (pendingWritesRef.current > 0 || saveErrorRef.current) { reportError('Câu trả lời chưa lưu được. Hãy thử lưu lại trước khi chuyển câu.'); return; }
    setIndex(nextIndex);
  }
  async function exitSession() {
    if (!submitted && pendingWritesRef.current > 0) await answerQueue.current;
    if (!submitted && (pendingWritesRef.current > 0 || saveErrorRef.current)) { reportError('Câu trả lời chưa lưu được. Hãy thử lưu lại trước khi rời phiên.'); return; }
    onExit();
  }
  async function submitMarks() {
    try { const next = await gradeRubric(attempt.id, q.id, currentMarks, attempt.revision, writerToken); setAttempt(next); onChange(next); setMarks({}); }
    catch (e) { reportError(e instanceof Error ? e.message : 'Không lưu được phần tự chấm.'); }
  }
  function setChoice(optionId: string) {
    if (q.answer_format === 'multiple_choice') {
      const values = Array.isArray(answer) ? answer : [];
      void persistAnswer(values.includes(optionId) ? values.filter(v => v !== optionId) : [...values, optionId]);
    } else void persistAnswer(optionId);
  }
  const answeredCount = progress;
  const objectiveItems = attempt.questions.filter(part => part.question.answer_format !== 'rubric');
  const correctCount = objectiveItems.filter(part => isCorrect(part, attempt.answers[part.question.id])).length;
  const blankCount = attempt.questions.filter(part => isBlankAnswer(attempt.answers[part.question.id])).length;
  const wrongAnsweredCount = (attempt.score?.wrongIds ?? []).filter(id => {
    const answer = attempt.answers[id];
    return !isBlankAnswer(answer);
  }).length;
  const objectiveMax = objectiveItems.reduce((sum, part) => sum + part.points, 0);
  const suggestedTopics = [...new Set((attempt.score?.wrongIds ?? []).map(id => attempt.questions.find(part => part.question.id === id)?.question.topic).filter((topic): topic is string => Boolean(topic)))];
  const optionRows = item.optionOrder.map(id => q.options?.find(o => o.id === id)).filter((o): o is NonNullable<typeof o> => Boolean(o));

  return <main className="session-page">
    {sessionError && <div className="session-alert" role="alert"><CircleHelp size={17} /><span>{sessionError}</span>{unsavedAnswer && !submitted && <button onClick={() => void retryUnsavedAnswer()} disabled={saving}><RotateCcw size={15} /> Thử lưu lại</button>}{!unsavedAnswer && <button aria-label="Đóng thông báo" onClick={() => setSessionError('')}>Đóng</button>}</div>}
    {readOnly && <div className="content-notice notice-empty" role="status"><div className="notice-icon"><ShieldCheck size={20} /></div><div><b>Phiên đang mở ở tab khác</b><p>Tab này chỉ xem được dữ liệu. Hãy tiếp tục ở tab đang chỉnh sửa để tránh ghi đè câu trả lời.</p></div></div>}
    <div className="session-top"><button className="back-button" onClick={() => void exitSession()}><ArrowLeft size={17} /> Tất cả chế độ</button><div className="session-heading"><span className="eyebrow">{attempt.mode === 'exam' ? 'THI THỬ' : 'PHIÊN ÔN TẬP'}</span><strong>{attempt.label}</strong></div><div className="session-tools"><div className={`timer ${remaining < 5 * 60_000 && attempt.deadlineAt !== null ? 'timer-warning' : ''}`}>{attempt.deadlineAt === null ? <span className="timer-practice">Không giới hạn giờ</span> : <><Clock3 size={16} /><b>{Math.floor(remaining / 60000).toString().padStart(2, '0')}:{Math.floor(remaining % 60000 / 1000).toString().padStart(2, '0')}</b></>}</div>{attempt.mode === 'exam' && !submitted && <button className="quick-submit" disabled={readOnly || saving || saveError} onClick={() => void manualSubmit()}>Nộp bài</button>}</div></div>
    <div className="session-progress"><div><span>Câu {index + 1} / {attempt.questions.length}</span><span>{answeredCount} đã trả lời{saving ? ' · Đang lưu…' : saveError ? ' · Chưa lưu được' : ' · Đã lưu'}</span></div><div className="progress-track"><span style={{ width: `${100 * (index + 1) / attempt.questions.length}%` }} /></div></div>
    {submitted && attempt.score && <section className="section-card result-summary"><div className="section-heading"><div><span className="eyebrow">KẾT QUẢ PHIÊN</span><h2>{attempt.status === 'submitted_pending_grading' ? 'Điểm tạm tính' : 'Kết quả đã chấm'}</h2></div><div className="result-total"><b>{formatPoints(attempt.score.totalPoints)}<small> / {formatPoints(attempt.score.maxPoints)}</small></b><span>{Math.round(attempt.score.totalPoints / Math.max(1, attempt.score.maxPoints) * 100)}%</span></div></div><div className="result-counts"><div><b>{correctCount}</b><span>đúng / {objectiveItems.length} câu khách quan</span></div><div><b>{wrongAnsweredCount}</b><span>sai hoặc chưa đạt</span></div><div><b>{blankCount}</b><span>bỏ trống</span></div><div><b>{attempt.score.pendingIds.length}</b><span>tự luận chờ tự chấm</span></div></div>{attempt.mode === 'exam' && <p className="result-note">Điểm trắc nghiệm: {formatPoints(attempt.score.objectivePoints)} / {formatPoints(objectiveMax)}. {attempt.score.pendingIds.length ? `Còn ${attempt.score.pendingIds.length} câu tự luận chưa có điểm.` : 'Điểm đã bao gồm phần tự luận bạn tự đánh giá.'}</p>}<div className="result-breakdown"><div><h3>Theo Phase</h3>{Object.entries(attempt.score.byPhase).map(([key, value]) => <p key={key}><span>{topicLabels.get(key) ?? key}</span><b>{formatPoints(value.earned)} / {formatPoints(value.max)}</b></p>)}</div><div><h3>Theo Track</h3>{Object.entries(attempt.score.byTrack).map(([key, value]) => <p key={key}><span>{key === '—' ? 'Phase 1' : key}</span><b>{formatPoints(value.earned)} / {formatPoints(value.max)}</b></p>)}</div><div><h3>Theo chủ đề</h3>{Object.entries(attempt.score.byTopic).map(([key, value]) => <p key={key}><span>{topicLabels.get(key) ?? key}</span><b>{formatPoints(value.earned)} / {formatPoints(value.max)}</b></p>)}</div></div></section>}
    {submitted && attempt.score && <p className="result-note">{suggestedTopics.length ? `Gợi ý ôn tập: ${suggestedTopics.map(topic => topicLabels.get(topic) ?? topic).join(' · ')}.` : 'Không có chủ đề cần xem lại từ các câu đã chấm.'} Câu tự luận đang chờ tự đánh giá chưa được tính.</p>}
    <div className="session-grid"><aside className="question-map card"><span className="eyebrow">TIẾN ĐỘ</span><div className="map-grid">{attempt.questions.map((part, i) => <button key={part.question.id} aria-label={`Đi đến câu ${i + 1}`} className={`map-cell ${i === index ? 'current' : ''} ${!isBlankAnswer(attempt.answers[part.question.id]) ? 'answered' : ''} ${attempt.flags.includes(part.question.id) ? 'flagged' : ''}`} onClick={() => void navigateTo(i)}>{i + 1}</button>)}</div><p className="map-legend"><span className="legend-dot answered" /> Đã trả lời <span className="legend-dot flagged" /> Đánh dấu</p><div className="map-note"><ShieldCheck size={16} /> Đáp án chỉ lưu trên thiết bị của bạn.</div></aside>
      <section className="question-card card" data-question-id={q.id}>
        <div className="question-meta"><span className="tag">Phase {q.phase}{q.track ? ` · Track ${q.track}` : ''}</span><span className="tag tag-muted">{q.answer_format === 'matching' ? 'Ghép cặp' : q.answer_format === 'ordering' ? 'Sắp xếp' : q.answer_format === 'rubric' ? 'Tự luận' : q.answer_format === 'multiple_choice' ? 'Chọn nhiều' : 'Trắc nghiệm'}</span><span className="question-points">{formatPoints(item.points)} điểm</span></div>
        {q.context && <div className="question-context"><QuestionText text={q.context} /></div>}
        <h1><QuestionText text={q.question} /></h1>
        <p className="answer-hint">{q.answer_format === 'matching' ? 'Ghép các mục theo quan hệ trong đề.' : q.answer_format === 'ordering' ? 'Sắp xếp các bước theo quy trình được mô tả.' : q.answer_format === 'multiple_choice' ? 'Chọn tất cả đáp án đúng.' : q.answer_format === 'rubric' ? 'Viết câu trả lời của bạn. Phần tự luận được tự chấm sau khi nộp.' : 'Chọn một đáp án phù hợp nhất.'}</p>
        {q.answer_format === 'matching' || q.answer_format === 'ordering' ? <StructuredQuestion item={item} answer={answer} submitted={submitted} disabled={submitted || saving || readOnly} onAnswer={value => void persistAnswer(value)} /> : q.answer_format === 'rubric' ? <textarea aria-label="Câu trả lời tự luận" className="essay-input" disabled={submitted || readOnly} value={essayDraft} onChange={e => { setEssayDraft(e.target.value); void persistAnswer(e.target.value); }} placeholder="Nhập câu trả lời của bạn…" /> : <div className="answer-options">{q.answer_format === 'boolean' ? [true, false].map(value => <button key={String(value)} className={`answer-option ${answer === value ? 'selected' : ''}`} disabled={submitted || saving || readOnly} onClick={() => void persistAnswer(value)}><span className="option-check">{answer === value && <Check size={15} />}</span><span>{value ? 'Đúng' : 'Sai'}</span></button>) : optionRows.map((option, i) => {
          const chosen = q.answer_format === 'multiple_choice' ? Array.isArray(answer) && answer.includes(option.id) : answer === option.id;
          return <button key={option.id} className={`answer-option ${chosen ? 'selected' : ''}`} disabled={submitted || saving || readOnly} onClick={() => setChoice(option.id)}><span className="option-letter">{String.fromCharCode(65 + i)}</span><span className="option-copy"><QuestionText text={option.text} /></span>{chosen && <Check className="option-checkmark" size={17} />}</button>;
        })}</div>}
        {submitted && q.answer_format === 'rubric' && typeof answer === 'string' && answer.trim() && <div className="self-grade"><div className="self-grade-title"><div><span className="eyebrow">TỰ ĐÁNH GIÁ</span><h2>Đối chiếu câu trả lời</h2></div><span className="tag tag-muted">Tối đa {formatPoints(item.points)} điểm</span></div><p className="grade-note">Chọn mức phù hợp với từng tiêu chí. Điểm tự chấm giúp bạn theo dõi tiến độ cá nhân.</p>{q.rubric?.map(c => <div className="criterion" key={c.id}><div><b><QuestionText text={c.description} /></b><small><QuestionText text={currentMarks[c.id] === 1 ? c.full_credit : currentMarks[c.id] === 0.5 ? c.partial_credit : c.no_credit} /></small></div><div className="grade-choices">{([0, 0.5, 1] as const).map(value => <button key={value} disabled={attempt.status !== 'submitted_pending_grading' || readOnly} onClick={() => setMarks(prev => ({ ...prev, [c.id]: value }))} className={currentMarks[c.id] === value ? 'chosen' : ''}>{value === 0 ? 'Chưa đạt' : value === 0.5 ? 'Một phần' : 'Đạt'}</button>)}</div></div>)}{attempt.status === 'submitted_pending_grading' && <button className="button button-primary" onClick={() => void submitMarks()} disabled={readOnly || Object.keys(currentMarks).length !== (q.rubric?.length ?? 0)}>Lưu tự đánh giá <Check size={16} /></button>}</div>}
        {submitted && <div className="explanation"><span className="eyebrow">ĐÁP ÁN & GIẢI THÍCH</span>{q.answer_format !== 'matching' && q.answer_format !== 'ordering' && <p><b>Đáp án đúng:</b> <QuestionText text={String(q.answer_format === 'rubric' ? q.correct_answer : q.answer_format === 'boolean' ? (q.correct_answer ? 'Đúng' : 'Sai') : q.options?.filter(o => Array.isArray(q.correct_answer) ? q.correct_answer.includes(o.id) : q.correct_answer === o.id).map(o => o.text).join(' · ') ?? '')} /></p>}<p><QuestionText text={q.explanation} /></p><QuestionSources question={q} /></div>}
        <div className="question-actions"><div><button className={`subtle-button ${bookmarked.has(q.id) ? 'is-bookmarked' : ''}`} disabled={readOnly} onClick={() => void toggleCurrentBookmark()}><Bookmark size={16} fill={bookmarked.has(q.id) ? 'currentColor' : 'none'} /> {bookmarked.has(q.id) ? 'Đã lưu' : 'Lưu câu hỏi'}</button><button className={`subtle-button ${attempt.flags.includes(q.id) ? 'is-flagged' : ''}`} disabled={submitted || readOnly} onClick={() => void toggleCurrentFlag()}><Flag size={16} /> {attempt.flags.includes(q.id) ? 'Đã đánh dấu' : 'Đánh dấu xem lại'}</button></div><div className="question-nav"><button className="button button-secondary" disabled={index === 0} onClick={() => void navigateTo(index - 1)}><ArrowLeft size={16} /> Trước</button>{index === attempt.questions.length - 1 ? <button className="button button-primary" disabled={submitted || saving || saveError || readOnly} onClick={() => void manualSubmit()}><Send size={16} /> Nộp bài</button> : <button className="button button-primary" disabled={saving || saveError} onClick={() => void navigateTo(index + 1)}>Tiếp <ArrowRight size={16} /></button>}</div></div>
      </section></div>
    {submitted && <div className="submission-banner"><CircleHelp size={17} /><span>{attempt.status === 'submitted_pending_grading' ? `Đã nộp. Còn ${attempt.score?.pendingIds.length ?? 0} câu tự luận đang chờ tự đánh giá.` : 'Đã nộp và chấm xong phiên này.'}</span><button onClick={onExit}>Xem lịch sử <ArrowRight size={15} /></button></div>}
  </main>;
}
