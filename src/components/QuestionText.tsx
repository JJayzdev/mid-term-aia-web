import type { ReactNode } from 'react';

const greek: Record<string, string> = { sigma: 'σ', kappa: 'κ', mu: 'μ' };
const superDigits = '⁰¹²³⁴⁵⁶⁷⁸⁹';

function notation(text: string): ReactNode[] {
  // Consume whole identifiers: an underscore in an API field is not a math subscript.
  // Code spans and URLs remain literal, including any embedded operators.
  const token = /https?:\/\/[^\s]+|`[^`\n]*`|\b(?:sqrt|floor|ceil)\(|[\p{L}][\p{L}\p{M}0-9]*(?:_(?:[\p{L}\p{M}0-9]+|\([^()\n]+\)))*_?|\^(?:\{[^{}\n]+\}|\([^()\n]+\)|[−+-]?\d+|[A-Za-z])|[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ᵀ]+|[=×≈≤≥]/gu;
  const parts: ReactNode[] = [];
  let cursor = 0;
  for (let match = token.exec(text); match; match = token.exec(text)) {
    const value = match[0];
    parts.push(text.slice(cursor, match.index));
    cursor = token.lastIndex;
    const key = match.index;
    if (/^(?:https?:|`)/.test(value)) { parts.push(value); continue; }
    if (/^(sqrt|floor|ceil)\($/.test(value)) {
      let depth = 1;
      let end = cursor;
      for (; end < text.length && depth; end++) {
        if (text[end] === '(') depth++;
        if (text[end] === ')') depth--;
      }
      if (depth) { parts.push(value); continue; }
      const inner = notation(text.slice(cursor, end - 1));
      parts.push(value === 'sqrt('
        ? <span key={key} className="math-root"><span>√</span><span className="math-radicand">{inner}</span></span>
        : <span key={key}>{value === 'floor(' ? '⌊' : '⌈'}{inner}{value === 'floor(' ? '⌋' : '⌉'}</span>);
      cursor = end;
      token.lastIndex = end;
    } else if (value.startsWith('^')) {
      const exponent = value.slice(1).replace(/^[{(]|[})]$/g, '');
      parts.push(<sup key={key}>{exponent}</sup>);
    } else if (/^[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ᵀ]+$/.test(value)) {
      parts.push(<sup key={key}>{[...value].map(char => superDigits.includes(char) ? String(superDigits.indexOf(char)) : ({ '⁺': '+', '⁻': '−', 'ᵀ': 'T' }[char])).join('')}</sup>);
    } else if (/^[=×≈≤≥]$/.test(value)) {
      parts.push(<span key={key}> {value} </span>);
    } else if (value === 'y_hat' || value === 'c_tilde') {
      parts.push(<span key={key}>{value === 'y_hat' ? 'ŷ' : 'c̃'}</span>);
    } else if (/^(?:[A-Za-z]|sigma|bits)_(?:[A-Za-z0-9_]+|\([^()]+\))$/.test(value)) {
      const separator = value.indexOf('_');
      const base = value.slice(0, separator);
      const subscript = value.slice(separator + 1).replace(/^\(|\)$/g, '').replaceAll('_', ' ');
      parts.push(<span key={key}>{greek[base] ?? base}<sub>{subscript}</sub></span>);
    } else if (/^(?:[xyz]\d+|e[1-5]|[fc][xy]|F1|IDF1)$/.test(value)) {
      const base = value === 'IDF1' ? 'IDF' : value[0];
      parts.push(<span key={key}>{base}<sub>{value.slice(base.length)}</sub></span>);
    } else {
      parts.push(greek[value] ?? value);
    }
  }
  parts.push(text.slice(cursor));
  return parts;
}

// Presentation only: works for every bank and saved snapshot without rewriting content.
// React escapes all text, including imported content. No HTML evaluation is used.
export default function QuestionText({ text }: { text: string }) {
  return <span className="question-text">{notation(text)}</span>;
}
