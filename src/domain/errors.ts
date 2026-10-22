export class DomainError extends Error {
  constructor(message: string, readonly code: string, readonly detail?: unknown) { super(message); this.name = 'DomainError'; }
}
