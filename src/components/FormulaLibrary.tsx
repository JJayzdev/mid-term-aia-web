import { useState } from 'react';
import type { Question } from '../domain/types';
import { focusLabels } from './practiceLabels';
import QuestionText from './QuestionText';
import QuestionSources from './QuestionSources';

export default function FormulaLibrary({ questions, loading = false, error = '' }: { questions: Question[]; loading?: boolean; error?: string }) {
  const [search, setSearch] = useState('');
  const [focus, setFocus] = useState('');
  const [track, setTrack] = useState('');
  const cards = questions.filter(q => q.formula_reference);
  const shown = cards.filter(q => (!focus || q.focus_topics?.some(t => t === focus)) && (!track || (track === 'p1' ? q.phase === 1 : q.track === Number(track))) && `${Object.values(q.formula_reference!).join(' ')} ${q.id}`.toLocaleLowerCase('vi-VN').includes(search.toLocaleLowerCase('vi-VN')));
  return <div className="formula-page"><div className="page-intro"><span className="eyebrow">TRA CỨU KHI ÔN TẬP</span><h1>Công thức và cách áp dụng</h1><p>Ký hiệu, giả định, ví dụ và lỗi dễ nhầm từ nội dung đã duyệt. Dùng để luyện tập; không phải danh sách công thức chắc chắn có trong đề thi.</p></div>
    {(loading || error) && <p className="content-notice" role="status">{loading ? 'Đang tải công thức…' : error}</p>}
    <div className="section-card formula-filters"><label className="field-label">Tìm công thức<input type="search" value={search} onChange={e => setSearch(e.target.value)} placeholder="Kalman, softmax, CNN…" /></label><label className="field-label">Nhóm trọng tâm<select value={focus} onChange={e => setFocus(e.target.value)}><option value="">Tất cả nhóm</option>{Object.entries(focusLabels).map(([id, label]) => <option value={id} key={id}>{label}</option>)}</select></label><label className="field-label">Phạm vi tài liệu<select value={track} onChange={e => setTrack(e.target.value)}><option value="">Tất cả Phase / Track</option><option value="p1">Phase 1</option>{[1, 2, 3, 4].map(n => <option key={n} value={n}>Phase 2 · Track {n}</option>)}</select></label></div>
    <p className="formula-count" role="status">{shown.length} / {cards.length} mục công thức</p>
    <div className="formula-grid">{shown.map(q => { const f = q.formula_reference!; return <article className="section-card formula-card" key={q.id}>
      <div className="question-meta"><span className="tag">Phase {q.phase}{q.track ? ` · Track ${q.track}` : ''}</span><span className="tag tag-muted">Ngày {Number(q.day?.split('-d').at(-1))}</span></div><h2>{f.title}</h2>
      <div className="formula-expression"><QuestionText text={f.formula} /></div>
      <dl><dt>Ký hiệu</dt><dd><QuestionText text={f.symbols} /></dd><dt>Điều kiện áp dụng</dt><dd><QuestionText text={f.conditions} /></dd><dt>Ví dụ thay số</dt><dd><QuestionText text={f.example} /></dd><dt>Lỗi thường gặp</dt><dd><QuestionText text={f.common_mistakes} /></dd></dl>
      <QuestionSources question={q} />
    </article>; })}</div>{!loading && !error && !shown.length && <p className="section-card">Chưa có công thức phù hợp với bộ lọc này.</p>}
  </div>;
}
