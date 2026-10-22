# Content maintenance

The current curated JSON files in `data/questions/drafts/` are the source of truth. Exact-revision independent decisions are in `reports/content/`; `release_bank.py` promotes only reviewed revisions. See the root README for release commands.

The `expand_a_*`, `expand_b*`, and editorial repair scripts preserve the initial authoring/revision history. They are one-time authoring utilities, not a repeatable build pipeline: some overwrite drafts or increment revisions. Do not rerun them over curated banks to rebuild the website. Any new content edit must increment its revision and receive a fresh independent source review before promotion.

`review_packet.py` creates read-only question packets and rendered PDF contact sheets for a reviewer. `expansion_audit.py` checks structure and exact-revision approval counts. `duplicate_candidates.py` screens lexical similarity only; neither tool can approve semantic correctness or establish complete semantic uniqueness.
