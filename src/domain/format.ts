export function formatPoints(units: number): string {
  const points = units / 100;
  return Number.isInteger(points) ? String(points) : points.toFixed(2).replace(/0+$/, '').replace(/\.$/, '');
}
export function formatDuration(milliseconds: number): string {
  const seconds = Math.max(0, Math.floor(milliseconds / 1000));
  const minutes = Math.floor(seconds / 60);
  return `${minutes} phút`;
}
export function formatDate(timestamp: number): string {
  return new Intl.DateTimeFormat('vi-VN', { dateStyle: 'medium', timeStyle: 'short' }).format(timestamp);
}
