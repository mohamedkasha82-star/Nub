# Supabase integration boundary

NŪB's public GitHub Pages site is currently static. The live Supabase project `nubian-memory-network` contains an existing village/person/family/memory schema; it is not yet wired to the website's evidence catalogue. Do not assume that existing records are consented for public display.

## Proposed next layer

`proposals/nub-private-evidence-vault.sql` is a **proposal only**. It has not been applied to the live Supabase project. It creates a separate, non-public schema for candidate evidence records, with:
- owner-bound records and row-level security;
- no anonymous access and no public read policy;
- required provenance, rights, access, and review metadata in the payload;
- an update timestamp trigger with a fixed `search_path`;
- no seeded historical records, names, oral histories, or media.

## Before applying

1. Create or use an isolated Supabase development branch; do not test schema changes directly against production.
2. Confirm the `nub_archive` schema is not included in exposed Data API schemas.
3. Apply the proposal only to the isolated branch and inspect the resulting grants, policies, triggers, and security advisors.
4. Run two-user isolation tests: owner A can only read/write A's records; owner B cannot read, update, or delete A's records; anonymous requests cannot access records.
5. Validate candidate payloads with `schemas/nub-record.schema.json` before insert. Database structural checks complement but do not replace the JSON Schema validator.
6. Add editorial/community review and consent/withdrawal workflows before any public-facing archive UI.
7. Only after successful review and explicit deployment approval should a reviewed migration be applied to production.

## Current audit observations

- Existing public tables have RLS enabled, but some use public read policies and authenticated insert policies that are broad. Review each existing table against its actual intended access model before changing it.
- `public.search_log` has RLS enabled but no policies. This blocks normal role-based access by default; do not add a policy until its intended readers/writers and privacy requirements are specified.
- Security advisors flagged mutable `search_path` settings on `public.get_lineage` and `public.match_person`, plus the `pg_trgm` extension in `public`. These are audit findings, not authorization to modify the existing functions or extension. Review dependencies and regression-test before remediation.
- The live project currently reports no migration history through the migrations listing tool. Establish a reliable migration baseline before treating future schema files as deployable history.

## Research integrity and community safeguards

A valid JSON record is not proof of source authenticity, copyright permission, informed consent, community review, or scholarly verification. Keep unknown values explicit. Rights and consent are separate. Do not publicly expose living-person details, restricted knowledge, or recordings with unresolved consent/access decisions.
