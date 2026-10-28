// Fixed, shared axes let learners compare the curve itself rather than auto-scaling.
export default function ActivationPlot({ kind }: { kind: 'sigmoid' | 'tanh' | 'relu' }) {
  const xPixel = (x: number) => 28 + (x + 4) / 8 * 250;
  const yPixel = (y: number) => 158 - (y + 1.5) / 6 * 140;
  const value = (x: number) => kind === 'sigmoid' ? 1 / (1 + Math.exp(-x)) : kind === 'tanh' ? Math.tanh(x) : Math.max(0, x);
  const points = Array.from({ length: 129 }, (_, i) => { const x = -4 + i / 16; return `${xPixel(x)},${yPixel(value(x))}`; }).join(' ');
  return <svg className="activation-plot" viewBox="0 0 300 185" aria-hidden="true">
    {[-1, 1, 4].map(y => <g key={y}><line x1="28" x2="278" y1={yPixel(y)} y2={yPixel(y)} stroke="#e1e9e4" /><text x="21" y={yPixel(y) + 4} textAnchor="end">{y}</text></g>)}
    <line x1="28" x2="284" y1={yPixel(0)} y2={yPixel(0)} stroke="#778f84" />
    <line x1={xPixel(0)} x2={xPixel(0)} y1="15" y2="162" stroke="#778f84" />
    {[-4, 0, 4].map(x => <text key={x} x={xPixel(x)} y="177" textAnchor="middle">{x}</text>)}
    <text x="286" y={yPixel(0) - 5}>x</text><text x={xPixel(0) + 6} y="13">y</text>
    <polyline points={points} fill="none" stroke="#147763" strokeWidth="2.5" strokeLinejoin="round" />
  </svg>;
}
