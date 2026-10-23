export type AnswerFormat = 'single_choice' | 'multiple_choice' | 'boolean' | 'rubric';
export type Phase = 1 | 2;
export type Question = {
  id: string; revision: number; author_id: string; phase: Phase | null; track: 1 | 2 | 3 | 4 | null;
  day: string | null; topic: string; taxonomy_status: 'unresolved' | 'inferred' | 'verified';
  question_type: 'single_choice' | 'multiple_choice' | 'true_false' | 'short_answer' | 'scenario';
  answer_format: AnswerFormat; difficulty: 'easy' | 'medium' | 'hard'; cognitive_level: 'remember' | 'understand' | 'apply' | 'analyze';
  question: string; calculation?: boolean; context?: string; options?: { id: string; text: string }[]; shuffle_options?: boolean;
  correct_answer: string | string[] | boolean; rubric?: Criterion[]; explanation: string;
  source_reference: SourceReference[]; status: 'draft' | 'pending_review' | 'approved' | 'rejected';
  review?: { reviewer_id: string; reviewed_at: string; reviewed_revision: number; report_id: string };
  review_notes?: string[];
};
export type Criterion = { id: string; description: string; weight: number; full_credit: string; partial_credit: string; no_credit: string };
export type SourceReference = { document_id: string; sha256: string; pdf_page: number; printed_slide_label?: string | null; title: string; locator?: string; verification: 'needs_review' | 'verified' };
export type QuestionBank = { schema_version: '1.0.0'; bank_version: string; questions: Question[] };
export type Catalog = {
  schema_version: '1.0.0'; catalog_version: string;
  documents: { document_id: string; title: string; relative_path: string; page_count: number; sha256: string }[];
  topics: { id: string; label: string; phase: Phase; track: 1 | 2 | 3 | 4 | null; day: string | null; document_ids: string[]; question_count: number }[];
};
export type StudyMode = 'daily' | 'track' | 'phase' | 'mixed' | 'wrong' | 'bookmarked' | 'exam';
export type AttemptStatus = 'in_progress' | 'submitted_pending_grading' | 'graded';
export type RubricMarks = Record<string, 0 | 0.5 | 1>;
export type AttemptQuestion = { question: Question; points: number; optionOrder: string[] };
export type Attempt = {
  id: string; mode: StudyMode; status: AttemptStatus; label: string;
  startedAt: number; deadlineAt: number | null; submittedAt: number | null; finalizedAt: number | null;
  revision: number; writerToken: string; bankVersion: string; seed: string; questions: AttemptQuestion[];
  answers: Record<string, string | string[] | boolean>; rubricMarks: Record<string, RubricMarks>;
  flags: string[]; score: GradeSummary | null;
};
export type GradeSummary = {
  objectivePoints: number; rubricPoints: number; pendingPoints: number; totalPoints: number;
  maxPoints: number; byPhase: Record<string, { earned: number; max: number }>;
  byTrack: Record<string, { earned: number; max: number }>;
  byTopic: Record<string, { earned: number; max: number }>;
  wrongIds: string[]; pendingIds: string[];
};
export type ExamWeights = [number, number, number, number];
export type BucketNeed = { phase: Phase; track: 1 | 2 | 3 | 4 | null; format: 'objective' | 'rubric'; count: number; slotPoints: number[] };
