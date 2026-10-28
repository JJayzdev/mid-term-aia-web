import type { ReactNode } from 'react';

const greek: Record<string, string> = { sigma: 'σ', kappa: 'κ', mu: 'μ', gamma: 'γ', beta: 'β', epsilon: 'ε', alpha: 'α', theta: 'θ', eta: 'η', lambda: 'λ', delta: 'δ', sum: 'Σ' };
const superDigits = '⁰¹²³⁴⁵⁶⁷⁸⁹';
const mathBase = /^(?:[\p{L}∑∏]|d[A-Za-z]|sigma|bits|gamma|beta|theta|sum|delta|IoU|TP|FP|FN|HOTA|DetA|AssA|Dice|bytes|features|number|area|pad|range|voxel|count|time|batches|saturation|weight|active)$/u;

function notation(text: string): ReactNode[] {
  // Consume whole identifiers: an underscore in an API field is not a math subscript.
  // Code spans and URLs remain literal, including any embedded operators.
  const token = /https?:\/\/[^\s]+|`[^`\n]*`|\b(?:sqrt|floor|ceil)\(|[Σ∑Π∏](?!_)|[\p{L}∑∏][\p{L}\p{M}0-9]*(?:_(?:[\p{L}\p{M}0-9]+|\([^()\n]+\)|\{[^{}\n]+\}))*_?|(?<=\))_(?:[\p{L}\p{M}0-9]+|\{[^{}\n]+\})|\^(?:\{[^{}\n]+\}|\([^()\n]+\)|[−+-]?\d+|[A-Za-z]+)|[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ᵀ]+|[=×≈≤≥]/gu;
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
      parts.push(<sup key={key}>{notation(exponent)}</sup>);
    } else if (value.startsWith('_')) {
      parts.push(<sub key={key}>{notation(value.slice(1).replace(/^\{|\}$/g, ''))}</sub>);
    } else if (/^[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ᵀ]+$/.test(value)) {
      parts.push(<sup key={key}>{[...value].map(char => superDigits.includes(char) ? String(superDigits.indexOf(char)) : ({ '⁺': '+', '⁻': '−', 'ᵀ': 'T' }[char])).join('')}</sup>);
    } else if (/^[=×≈≤≥]$/.test(value)) {
      parts.push(<span key={key}> {value} </span>);
    } else if (/^(?:d)?[A-Za-z]_(?:hat|tilde)$/.test(value)) {
      const base = value.slice(0, value.indexOf('_'));
      parts.push(<span key={key}>{(base + (value.endsWith('_hat') ? '\u0302' : '\u0303')).normalize('NFC')}</span>);
    } else if (/^(?:alpha|beta|gamma|sigma|theta)\d+$/.test(value)) {
      const [, base, index] = value.match(/^([a-z]+)(\d+)$/)!;
      parts.push(<span key={key}>{greek[base]}<sub>{index}</sub></span>);
    } else if (value.includes('_') && mathBase.test(value.slice(0, value.indexOf('_'))) && !value.endsWith('_')) {
      const separator = value.indexOf('_');
      const base = value.slice(0, separator);
      const subscript = value.slice(separator + 1).replace(/^[({]|[)}]$/g, '').replaceAll('_', ' ');
      parts.push(<span key={key}>{greek[base] ?? base}<sub>{notation(subscript)}</sub></span>);
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
