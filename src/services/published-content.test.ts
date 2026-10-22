import { describe, expect, it } from 'vitest';
import { validateBank, validateCatalog } from '../domain/validation';
import type { Catalog } from '../domain/types';
import catalogRaw from '../../public/data/catalog.json';
import bankRaw from '../../public/data/bank.json';

describe('published static content', () => {
  it('validates the release bank against its catalog and contains only independently approved questions', () => {
    validateCatalog(catalogRaw);
    const bank = validateBank(bankRaw, catalogRaw as Catalog, true);
    expect(bank.questions.length).toBeGreaterThan(0);
    expect(bank.questions.every(q => q.status === 'approved' && q.review?.reviewer_id !== q.author_id && q.review?.reviewed_revision === q.revision)).toBe(true);
  });
});
