import { validateBank, validateCatalog } from '../domain/validation';
import type { Catalog, QuestionBank } from '../domain/types';

export type ContentBundle = { bank: QuestionBank; catalog: Catalog };
async function readJson(path: string): Promise<unknown> {
  const response = await fetch(`${import.meta.env.BASE_URL}${path}`, { cache: 'no-cache' });
  if (!response.ok) throw new Error(response.status === 404 ? `Chưa tìm thấy ${path}.` : `Không tải được ${path} (HTTP ${response.status}).`);
  return response.json();
}
export async function loadContent(): Promise<ContentBundle> {
  const [bankRaw, catalogRaw] = await Promise.all([readJson('data/bank.json'), readJson('data/catalog.json')]);
  validateCatalog(catalogRaw);
  const bank = validateBank(bankRaw, catalogRaw, true);
  return { bank, catalog: catalogRaw };
}
