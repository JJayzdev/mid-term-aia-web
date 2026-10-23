# Formula display fix — 2026-10-23

Numerical question text now renders plain-text powers as superscripts and variable suffixes as subscripts, with spaced multiplication/equality signs. Context, choices, correct answers and explanations share the renderer. Non-calculation questions retain literal code identifiers. Rendering uses escaped React text; the reviewed bank and saved question snapshots are unchanged.

Answer and explanation text is now 14px before the existing desktop zoom. Narrow layouts wrap without horizontal overflow.

Validation: 54 unit tests passed; TypeScript/Vite build passed. All 13 existing browser scenarios passed against the production preview. The new screenshot-specific camera regression passed after fixing its test setup to select Phase 2 and the numerical-only filter. It verifies powers/subscripts, answer size, widths 1440/390/360, reload, submitted explanation and unchanged saved snapshots. Desktop and phone screenshots were visually inspected.

Initial browser runs could not reach the sandboxed preview server; verification succeeded with the local server and Chrome running in the same permitted environment.
