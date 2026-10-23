import { describe, expect, it } from 'vitest';
import { renderToStaticMarkup } from 'react-dom/server';
import bank from '../../public/data/bank.json';
import QuestionText from './QuestionText';

function formatted(text: string) {
  const element = document.createElement('div');
  element.innerHTML = renderToStaticMarkup(<QuestionText text={text} />);
  return element;
}

describe('notation throughout the question bank', () => {
  it('formats untagged powers, recurrent indices, roots and nested rounding expressions', () => {
    const el = formatted('pass^k; h_t, h_(t-1); P_next=P+Q; sqrt(P_fused); floor((H_in+2p−d(k−1)−1)/s)+1; ceil(150/16); m^−2');
    expect([...el.querySelectorAll('sup')].map(n => n.textContent)).toEqual(['k', '−2']);
    expect([...el.querySelectorAll('sub')].map(n => n.textContent)).toEqual(['t', 't-1', 'next', 'fused', 'in']);
    expect(el.querySelector('.math-radicand')?.textContent).toBe('Pfused');
    expect(el.textContent).toContain('⌊(Hin+2p−d(k−1)−1)/s⌋+1');
    expect(el.textContent).toContain('⌈150/16⌉');
  });
  it('preserves Vietnamese words, API identifiers, code spans and URLs', () => {
    const text = 'muốn mua mô hình; max_tokens user_id Q4_K_M NEXT_PUBLIC_ usage.input_tokens; `x_next=2^3`; https://example.test/x_next?a=10^9';
    const el = formatted(text);
    expect(el.textContent).toBe(text);
    expect(el.querySelector('sup, sub')).toBeNull();
  });
  it('escapes imported HTML and preserves malformed expressions', () => {
    const el = formatted('<img src=x onerror=alert(1)> sqrt(P_fused');
    expect(el.querySelector('img')).toBeNull();
    expect(el.textContent).toContain('<img');
    expect(el.textContent).toContain('sqrt(');
  });
  it('renders every published question field without leaving raw mathematical scripts or functions', () => {
    let checked = 0;
    for (const q of bank.questions) {
      const fields = [q.question, q.context, q.explanation, ...q.options?.map(o => o.text) ?? [],
        ...(q.answer_format === 'rubric' ? [String(q.correct_answer)] : []),
        ...q.rubric?.flatMap(c => [c.description, c.full_credit, c.partial_credit, c.no_credit]) ?? []];
      for (const field of fields) {
        if (!field) continue;
        const el = formatted(field);
        expect(el.textContent, q.id).not.toMatch(/\^(?:[−+-]?\d|k\b)|\b(?:[A-Za-z]|sigma|bits)_(?:[A-Za-z]|\()|\b(?:sqrt|floor|ceil)\(/);
        for (const identifier of field.match(/\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+\b/g) ?? []) {
          if (!/^(?:[A-Za-z]|sigma|bits)_/.test(identifier)) expect(el.textContent, q.id).toContain(identifier);
        }
        checked++;
      }
    }
    expect(checked).toBeGreaterThan(6900);
  });
});
