-- PROPOSAL ONLY: review and test in an isolated Supabase development branch before applying.
-- This file has NOT been applied to the live project.
-- Private-by-default storage for candidate NŪB evidence records. No records are seeded.

begin;

create schema if not exists nub_archive;
revoke all on schema nub_archive from public;
revoke all on schema nub_archive from anon;
grant usage on schema nub_archive to authenticated;

create table if not exists nub_archive.records (
  record_id text primary key,
  owner_id uuid not null references auth.users(id) on delete restrict,
  payload jsonb not null,
  created_at timestamptz not null default pg_catalog.now(),
  updated_at timestamptz not null default pg_catalog.now(),

  constraint records_payload_is_object
    check (pg_catalog.jsonb_typeof(payload) = 'object'),
  constraint records_payload_record_id_matches
    check (payload ->> 'record_id' = record_id),
  constraint records_payload_title_present
    check (nullif(pg_catalog.btrim(payload ->> 'title'), '') is not null),
  constraint records_payload_kind_present
    check (nullif(pg_catalog.btrim(payload ->> 'record_kind'), '') is not null),
  constraint records_payload_provenance_present
    check (
      pg_catalog.jsonb_typeof(payload -> 'provenance') = 'object'
      and nullif(payload -> 'provenance' ->> 'origin_type', '') is not null
      and nullif(payload -> 'provenance' ->> 'source_status', '') is not null
    ),
  constraint records_payload_rights_present
    check (
      pg_catalog.jsonb_typeof(payload -> 'rights') = 'object'
      and nullif(payload -> 'rights' ->> 'status', '') is not null
    ),
  constraint records_payload_access_present
    check (
      pg_catalog.jsonb_typeof(payload -> 'access') = 'object'
      and nullif(payload -> 'access' ->> 'level', '') is not null
    ),
  constraint records_payload_review_state_present
    check (
      pg_catalog.jsonb_typeof(payload -> 'review_state') = 'object'
      and nullif(payload -> 'review_state' ->> 'status', '') is not null
    )
);

create index if not exists records_owner_updated_idx
  on nub_archive.records (owner_id, updated_at desc);

alter table nub_archive.records enable row level security;

drop policy if exists "record owners manage their own records" on nub_archive.records;
create policy "record owners manage their own records"
  on nub_archive.records
  for all
  to authenticated
  using ((select auth.uid()) = owner_id)
  with check ((select auth.uid()) = owner_id);

revoke all on nub_archive.records from public;
revoke all on nub_archive.records from anon;
grant select, insert, update, delete on nub_archive.records to authenticated;

create or replace function nub_archive.set_updated_at()
returns trigger
language plpgsql
set search_path = pg_catalog
as $function$
begin
  new.updated_at := pg_catalog.now();
  return new;
end;
$function$;

revoke all on function nub_archive.set_updated_at() from public;
revoke all on function nub_archive.set_updated_at() from anon;
revoke all on function nub_archive.set_updated_at() from authenticated;

drop trigger if exists set_records_updated_at on nub_archive.records;
create trigger set_records_updated_at
  before update on nub_archive.records
  for each row execute function nub_archive.set_updated_at();

commit;

-- Important boundaries:
-- 1. This schema should remain absent from Supabase's exposed Data API schemas.
-- 2. The JSON Schema validator remains the full application-level contract.
-- 3. RLS owner isolation does not itself establish consent, rights, authenticity, or review.
-- 4. Do not seed real testimony or media until consent, rights, access, and review workflows exist.
-- 5. Test cross-user isolation and the intended API exposure configuration before production use.
