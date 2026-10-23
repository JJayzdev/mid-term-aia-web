import type { ReactNode } from 'react';

// Calculation notation is rendered as React text/elements, never interpreted as HTML.
// Scope this to numerical questions so code identifiers in other subjects stay literal.
export default function QuestionText({ text, calculation = false }: { text: string; calculation?: boolean }) {
  if (!calculation) return <>{text}</>;
  const tokens = text.split(/(\^[−+-]?\d+|[A-Za-z]+(?:_[A-Za-z]+)+|\b(?:[xyz][125]|[e][1-5]|[fc][xy])\b|[=×≈≤≥])/g);
  const parts: ReactNode[] = tokens.map((token, index) => {
    if (/^\^[−+-]?\d+$/.test(token)) return <sup key={index}>{token.slice(1)}</sup>;
    if (/^[=×≈≤≥]$/.test(token)) return <span key={index}> {token} </span>;
    if (token === 'y_hat') return <span key={index} className="math-symbol">ŷ</span>;
    if (token === 'c_tilde') return <span key={index} className="math-symbol">c̃</span>;
    if (/^[A-Za-z]+(?:_[A-Za-z]+)+$/.test(token)) {
      const [base, ...subscript] = token.split('_');
      return <span key={index} className="math-symbol">{base === 'sigma' ? 'σ' : base}<sub>{subscript.join(' ')}</sub></span>;
    }
    if (/^(?:[xyz][125]|e[1-5]|[fc][xy])$/.test(token)) return <span key={index} className="math-symbol">{token[0]}<sub>{token.slice(1)}</sub></span>;
    return token;
  });
  return <span className="question-text">{parts}</span>;
}
