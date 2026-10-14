# NŪB — Living Atlas

NŪB is an independent, Arabic-first bilingual digital knowledge atlas designed as a companion layer to the existing Nubia Odyssey experiences. It does not replace, merge into, or modify the Odyssey projects.

## Pages
- `index.html` — cinematic entry point, project relationship, research paths, summary timeline and methodology.
- `atlas.html` — expanded knowledge layer: historical chronology, Nile geography, displacement, languages and oral tradition, architecture, contemporary continuity, open questions, and inline source links.
- `sources.html` — source register, source types, methodological boundaries, and editorial principles.
- `culture.html` — bilingual Living Heritage experience covering Nubia before/after displacement, architecture, language, music, food, community memory, source-linked archival collections and consent-aware contribution suggestions.
- `listening.html` — bilingual Listening Room with locally generated abstract synthetic sound (no autoplay), explicit distinction between sound design, archival recordings and consented oral history, plus a concise provenance and rights pathway.
- `fieldwork.html` — bilingual proposed fieldwork protocol for community-led documentation, granular consent, access levels, provenance metadata, interview prompts, and a downloadable JSON record template.
- `evidence.html` — searchable evidence register separating supported claims from limits, with institutional standards and scholarly research references.
- `research-map.html` — bilingual interactive research constellation connecting existing atlas topics to relevant evidence entries and open questions. It is a navigational layer, not a claim that linked topics form proven causal relationships.
- `research.html` — interactive research dossier for Mohamed Kasha’s *Nubian Archives Registry (v1.0)*, including dated findings, methodology, limitations, citation metadata, and next-work plan.
- `favicon.svg` — original project mark.
- `.github/workflows/deploy.yml` — isolated GitHub Pages deployment for this repository.

## Research foundations
The first release links to UNESCO World Heritage records and campaign history, the British Museum's Sudan/Egypt/Nubia chronology, Oxford Academic research on Nubian resettlement, an open-access linguistic study in *Dotawo*, UNESCO intangible-heritage materials, and studies of Nubian architecture. Each source is identified with a stated scope; institutional records, museum overviews and academic research are not treated as interchangeable.

## Cultural and academic integrity
- The site is an introductory knowledge prototype, not a peer-reviewed or community-reviewed archive.
- No invented quotations, testimony, vocabulary entries, map coordinates or ethnographic details are presented as evidence.
- Artistic river visuals are abstract metaphors, not accurate geographic or archaeological maps.
- New oral histories, language materials, photographs and community knowledge require source provenance, consent, appropriate attribution, licensing and context.
- Dates and period labels are approximate where indicated; Nubia is not presented as a homogeneous culture or one uninterrupted polity.

## Archival media and rights
The Living Heritage page links to original records and displays specific media under their stated licenses. The Tamit image is covered by Sapienza University of Rome’s `CC BY-NC-SA 4.0` terms unless the individual item says otherwise; the page links to the license record. Smithsonian archival descriptions are linked rather than reproduced where permission is required. Press reporting on family recipes is identified as journalism, not peer-reviewed research.

## Run locally
Open `index.html` in a browser. The project is static HTML/CSS/JavaScript and has no build step. Google Fonts are an optional external dependency; system fallbacks are provided.

## Deploy
GitHub Pages workflow deploys this repository independently. Do not connect or overwrite any unrelated project. External Nubia Odyssey links are navigation only.


## Research dossier: Nubian Archives Registry (v1.0)
The dedicated dossier presents the uploaded author manuscript as a preprint/data paper, dated 14 October 2026, with a registry snapshot verified 12 October 2026. It reports the paper’s sample counts and limitations explicitly; it does not describe the sample as a census, claim independent peer review, or invent a DOI. The manuscript notes that a DOI deposit was planned for the future.

## Record schema and responsible contribution
- `schemas/nub-record.schema.json` — draft JSON Schema for source provenance, claim scope, rights, consent, access restrictions, sensitivity flags, and review state.
- `schemas/README.md` — implementation guardrails: preserve UNKNOWN states, separate copyright from consent, restrict unresolved community material, and do not overstate review.
- The schema is not yet connected to ingestion or Supabase and is not a compliance claim, community approval, or evidence of permission for any item.

## Deterministic schema quality gate

- `scripts/validate_records.py` validates candidate JSON records against the draft schema and checks standard JSON Schema formats.
- `tests/test_record_schema.py` tests schema validity, required fields, strict enums, date formats, unknown-state preservation, and the distinction between rights and consent.
- `.github/workflows/validate-record-schema.yml` runs the validator and regression tests for relevant pull requests and main-branch changes.
- `tests/fixtures/record-valid-unknown.json` is synthetic test data only; it is not a historical item, testimony, or archival evidence.

Run locally with Python 3.12 or compatible:
```sh
python -m pip install "jsonschema>=4.23,<5"
python scripts/validate_records.py tests/fixtures/record-valid-unknown.json
python -m unittest discover -s tests -v
```

A passing schema check only establishes structural validity. It does not establish authenticity, rights, consent, permission to publish, community review, or scholarly verification. The fixture intentionally preserves unknown values rather than inventing missing metadata.
