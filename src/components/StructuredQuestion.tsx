import { ArrowDown, ArrowUp, Check, RotateCcw } from 'lucide-react';
import type { AnswerValue, AttemptQuestion } from '../domain/types';
import { isCorrect } from '../domain/grading';
import QuestionText from './QuestionText';
import ActivationPlot from './ActivationPlot';

type Props = { item: AttemptQuestion; answer: AnswerValue | undefined; disabled: boolean; submitted: boolean; onAnswer: (value: AnswerValue) => void };

export default function StructuredQuestion({ item, answer, disabled, submitted, onAnswer }: Props) {
  const q = item.question;
  const options = new Map(q.options?.map(o => [o.id, o.text]));
  if (q.answer_format === 'matching') {
    const chosen = answer && typeof answer === 'object' && !Array.isArray(answer) ? answer : {};
    const solution = q.correct_answer as Record<string, string>;
    const left = new Map(q.matching_items?.map(row => [row.id, row]));
    return <div className="matching-exercise">
      <p className="structured-policy">{q.matching_reuse ? 'Có thể dùng lại một phương án cho nhiều mục.' : 'Ghép một–một: mỗi phương án chỉ dùng một lần.'} Chọn chữ cái tương ứng. Đúng toàn bộ nhận đủ điểm; ghép thiếu hoặc sai nhận 0 điểm, không trừ điểm.</p>
      <div className="matching-layout">
        <section className="matching-key" aria-label="Các phương án ghép"><h2>Phương án</h2>{item.optionOrder.map((id, index) => <div className="matching-key-row" key={id}><b>{String.fromCharCode(65 + index)}</b><QuestionText text={options.get(id) ?? id} /></div>)}</section>
        <section className="matching-questions" aria-label="Các mục cần ghép"><h2>Ghép với phương án</h2>{(item.matchingOrder ?? [...left.keys()]).map((id, index) => {
          const row = left.get(id)!;
          const correct = chosen[id] === solution[id];
          return <div className={`matching-row ${submitted ? correct ? 'pair-correct' : 'pair-wrong' : ''}`} key={id}>
            <label htmlFor={`match-${q.id}-${id}`}><b>{index + 1}.</b> <QuestionText text={row.text} /></label>
            {row.graph && <ActivationPlot kind={row.graph} />}
            <select id={`match-${q.id}-${id}`} aria-label={`Ghép: ${row.text}`} disabled={disabled} value={chosen[id] ?? ''} onChange={event => {
              const next = { ...chosen };
              if (event.target.value) next[id] = event.target.value; else delete next[id];
              onAnswer(next);
            }}><option value="">Chưa ghép</option>{item.optionOrder.map((rightId, i) => <option key={rightId} value={rightId} disabled={!q.matching_reuse && Object.entries(chosen).some(([leftId, value]) => leftId !== id && value === rightId)}>Phương án {String.fromCharCode(65 + i)}</option>)}</select>
            {submitted && <div className="pair-feedback"><b>{correct ? 'Đúng' : chosen[id] ? 'Chưa đúng' : 'Chưa ghép'}</b><p>Ghép đúng: <QuestionText text={options.get(solution[id]) ?? solution[id]} /></p>{row.explanation && <p><QuestionText text={row.explanation} /></p>}</div>}
          </div>;
        })}</section>
      </div>
      {!submitted && <p className="structured-progress" role="status">Đã ghép {Object.keys(chosen).length}/{q.matching_items?.length} mục. <button className="text-link" disabled={disabled || !Object.keys(chosen).length} onClick={() => onAnswer({})}><RotateCcw size={14} /> Xóa các cặp</button></p>}
    </div>;
  }
  const selected = Array.isArray(answer) && answer.length ? answer : item.optionOrder;
  const recorded = Array.isArray(answer) && answer.length > 0;
  function move(index: number, change: number) {
    const next = [...selected];
    [next[index], next[index + change]] = [next[index + change], next[index]];
    onAnswer(next);
  }
  const validOrders = [q.correct_answer as string[], ...(q.accepted_orders ?? [])];
  return <div className="ordering-exercise">
    <p className="structured-policy">Dùng nút lên/xuống để sắp xếp. {validOrders.length > 1 ? 'Chấp nhận các thứ tự hợp lệ được nêu khi chấm.' : 'Thứ tự áp dụng cho quy trình và giả định trong đề.'} Đúng cả chuỗi nhận đủ điểm; sai hoặc bỏ trống nhận 0 điểm, không trừ điểm.</p>
    <ol className="ordering-list">{selected.map((id, index) => <li key={id}><span className="step-number">{index + 1}</span><div><QuestionText text={options.get(id) ?? id} /></div>{!submitted && <div className="step-actions"><button disabled={disabled || index === 0} aria-label={`Đưa bước ${index + 1} lên`} onClick={() => move(index, -1)}><ArrowUp size={16} /><span>Lên</span></button><button disabled={disabled || index === selected.length - 1} aria-label={`Đưa bước ${index + 1} xuống`} onClick={() => move(index, 1)}><ArrowDown size={16} /><span>Xuống</span></button></div>}</li>)}</ol>
    {!submitted ? <div className="ordering-confirm"><p role="status">{recorded ? 'Thứ tự đã được ghi nhận.' : 'Chưa trả lời. Thứ tự ban đầu chỉ là các bước đã xáo trộn.'}</p><button className="button button-secondary" disabled={disabled} onClick={() => onAnswer([...selected])}><Check size={15} /> Xác nhận thứ tự này</button>{recorded && <button className="text-link" disabled={disabled} onClick={() => onAnswer([])}>Xóa trả lời</button>}</div>
      : <div className="order-feedback"><b>{!recorded ? 'Bỏ trống' : isCorrect(item, answer) ? 'Thứ tự đúng' : 'Thứ tự chưa đúng'}</b>{validOrders.map((order, i) => <div key={i}><h3>{validOrders.length > 1 ? `Thứ tự hợp lệ ${i + 1}` : 'Thứ tự đúng'}</h3><ol>{order.map(id => <li key={id}><QuestionText text={options.get(id) ?? id} /></li>)}</ol></div>)}</div>}
  </div>;
}
