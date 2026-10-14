# NŪB record schema — implementation notes

**Status: draft contract, not an operational archive or a certification.**

`schemas/nub-record.schema.json` defines a common structure for source records and community-contributed heritage materials. It is designed to make provenance, claim scope, rights, consent, access, and review state explicit rather than inferred.

## Non-negotiable data rules

- **Unknown is a valid state.** Do not fill missing rights, consent, dates, authorship, or access decisions with guesses.
- **Rights and consent are different.** A public URL or open license does not automatically authorize recording, translation, display of a living person's testimony, or disclosure of sensitive knowledge.
- **A source link is not verification.** Record whether the original item, repository landing page, or only a citation was checked.
- **Review labels are scoped.** `editorially_checked` is not peer review; `community_reviewed` must only be used when an actual, documented community review took place and its scope is recorded.
- **Default to no public display when consent or access is unresolved.** Keep sensitive records out of public outputs until a responsible, documented decision is made.
- **Minimize personal data.** Store only the information needed for provenance and permission; do not place private contact details or consent forms in public JSON.
- **Respect withdrawal.** A withdrawal or correction request should trigger a documented review and removal or restriction where appropriate, without erasing the audit trail needed to explain the change.
- **Do not expose credentials.** This schema is a data contract only; it contains no keys and does not configure Supabase, authentication, or access policies.

## Validation and use

1. Validate a candidate JSON record against the schema before ingesting it.
2. Have a human reviewer check the source and every claim the record is used to support.
3. Verify the exact license and rights-holder terms for the specific item, not merely the hosting website.
4. For community-contributed material, document the contributor's choices about public display, translation, editing, sensitive knowledge, and withdrawal.
5. Review access and consent again before publishing a page, excerpt, transcript, or derivative.
6. Keep corrections and review decisions traceable; never silently convert `unknown` to a positive status.

This schema has not yet been wired to a database, tested in a production ingestion pipeline, or reviewed by Nubian community representatives, an archivist, or a legal specialist. It must not be described as evidence that NŪB is compliant with a standard or that any item has permission for reuse.
