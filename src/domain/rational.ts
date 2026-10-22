type Fraction = { n: bigint; d: bigint };
function gcd(a: bigint, b: bigint): bigint { while (b !== 0n) [a, b] = [b, a % b]; return a < 0n ? -a : a; }
function fraction(value: number): Fraction {
  if (!Number.isFinite(value)) throw new Error('Expected finite decimal value.');
  const [mantissa, exponentText] = String(value).toLowerCase().split('e');
  const exponent = exponentText ? Number(exponentText) : 0;
  const negative = mantissa.startsWith('-');
  const unsigned = mantissa.replace(/^[+-]/, '');
  const [whole, fractional = ''] = unsigned.split('.');
  let n = BigInt(`${negative ? '-' : ''}${whole}${fractional}`);
  let scale = fractional.length - exponent;
  let d = 1n;
  if (scale > 0) d = 10n ** BigInt(scale);
  else if (scale < 0) { n *= 10n ** BigInt(-scale); scale = 0; }
  const factor = gcd(n, d) || 1n;
  return { n: n / factor, d: d / factor };
}
export function decimalSumEquals(values: number[], target: number): boolean {
  let sum = { n: 0n, d: 1n };
  for (const value of values) {
    const next = fraction(value);
    sum = { n: sum.n * next.d + next.n * sum.d, d: sum.d * next.d };
    const factor = gcd(sum.n, sum.d) || 1n;
    sum = { n: sum.n / factor, d: sum.d / factor };
  }
  const expected = fraction(target);
  return sum.n * expected.d === expected.n * sum.d;
}
export function decimalProductIsInteger(value: number, multiplier: number): boolean {
  const a = fraction(value), b = fraction(multiplier);
  return (a.n * b.n) % (a.d * b.d) === 0n;
}
export function weightedDecimalRoundHalfUp(weights: number[], factors: number[], multiplier: number): number {
  if (weights.length !== factors.length || !Number.isFinite(multiplier) || multiplier < 0) throw new Error('Invalid weighted decimal input.');
  let sum: Fraction = { n: 0n, d: 1n };
  for (let index = 0; index < weights.length; index++) {
    const weight = fraction(weights[index]); const factor = fraction(factors[index]);
    const product = { n: weight.n * factor.n, d: weight.d * factor.d };
    sum = { n: sum.n * product.d + product.n * sum.d, d: sum.d * product.d };
    const divisor = gcd(sum.n, sum.d) || 1n;
    sum = { n: sum.n / divisor, d: sum.d / divisor };
  }
  const scale = fraction(multiplier);
  const n = sum.n * scale.n, d = sum.d * scale.d;
  return Number((2n * n + d) / (2n * d));
}
