import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL_PATH = ROOT / "supabase" / "proposals" / "nub-private-evidence-vault.sql"
README_PATH = ROOT / "supabase" / "README.md"


class SupabaseProposalSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sql = SQL_PATH.read_text(encoding="utf-8").lower()
        cls.readme = README_PATH.read_text(encoding="utf-8").lower()

    def test_proposal_is_explicitly_not_live_applied(self):
        self.assertIn("proposal only", self.sql)
        self.assertIn("has not been applied", self.sql)

    def test_separate_schema_and_rls_are_required(self):
        self.assertIn("create schema if not exists nub_archive", self.sql)
        self.assertIn("alter table nub_archive.records enable row level security", self.sql)

    def test_anonymous_and_public_grants_are_revoked(self):
        self.assertIn("revoke all on schema nub_archive from public", self.sql)
        self.assertIn("revoke all on schema nub_archive from anon", self.sql)
        self.assertIn("revoke all on nub_archive.records from public", self.sql)
        self.assertIn("revoke all on nub_archive.records from anon", self.sql)

    def test_owner_policy_checks_both_using_and_with_check(self):
        self.assertIn("for all", self.sql)
        self.assertIn("to authenticated", self.sql)
        self.assertIn("using ((select auth.uid()) = owner_id)", self.sql)
        self.assertIn("with check ((select auth.uid()) = owner_id)", self.sql)

    def test_no_public_read_policy_or_seed_data(self):
        self.assertNotIn("to anon", self.sql.split("create policy", 1)[-1])
        self.assertNotIn("using (true)", self.sql)
        self.assertNotIn("insert into nub_archive.records", self.sql)

    def test_trigger_function_pins_search_path(self):
        self.assertIn("set search_path = pg_catalog", self.sql)
        self.assertIn("revoke all on function nub_archive.set_updated_at() from public", self.sql)

    def test_rollout_requires_isolation_tests_and_exposure_review(self):
        self.assertIn("two-user isolation tests", self.readme)
        self.assertIn("not included in supabase's exposed data api schemas", self.readme)
        self.assertIn("explicit deployment approval", self.readme)


if __name__ == "__main__":
    unittest.main()
