# Pull Request Review Guide

Use the
[OCA contribution guidelines](https://github.com/OCA/odoo-community.org/blob/master/website/Contribution/CONTRIBUTING.rst)
as the baseline for reviews.

## Review process

1. Check the target branch to identify the Odoo version. This repository's Odoo 19
   workflow runs for pull requests and branches matching `19*`; verify that module
   versions and APIs are appropriate for that target.
2. Read the complete diff in context, including related modules, tests, and generated
   files. Confirm the change is focused and consistent with the pull request's stated
   intent.
3. Prioritize actionable defects: regressions, incorrect business behavior, data
   integrity problems, access-control issues, compatibility risks, and missing tests.
   Avoid comments that are only stylistic preferences unless they conflict with project
   conventions.
4. Check the relevant CI results and pre-commit checks. Do not treat a passing check as
   proof that the behavior is correct.
5. Report each finding with its location, the scenario that triggers it, and its impact.
   Distinguish required fixes from optional suggestions; if there are no actionable
   findings, say so.

## Odoo addon checklist

- **Manifest and dependencies:** Ensure each affected addon's manifest has the correct
  Odoo-versioned module version, declares every required addon dependency, and includes
  any new data files in the correct load order. Check that unrelated metadata and
  installability are unchanged.
- **ORM and business behavior:** Verify model fields, relations, compute dependencies,
  inverses, constraints, defaults, and create/write/unlink behavior. Consider
  multi-company, multi-record, empty-value, and upgrade scenarios where relevant. Avoid
  per-record queries or logic that only works for the current user's sample data.
- **Security and data access:** Check access control lists, record rules, elevated
  access, and user-facing actions. Confirm that the change neither exposes records nor
  blocks intended users.
- **Views and frontend:** Check view inheritance targets and priorities, field
  expressions, action/menu references, and behavior for the intended user groups. For
  JavaScript or styling changes, check compatibility with the Odoo web client and the
  affected interaction.
- **Data, upgrades, and integrations:** Consider existing databases, module upgrades,
  scheduled jobs, external integrations, and any required migration or configuration
  changes. Avoid destructive or non-repeatable data operations.
- **Tests and documentation:** Expect tests for changed behavior and regression coverage
  for fixed defects. Confirm addon documentation and user-visible help are updated when
  the behavior or setup changes; ensure translations are handled for new translatable
  text.
- **Generated and packaging files:** Check that generated README files, addon tables,
  external-dependency declarations, and other generated outputs are updated when their
  source changes. Do not hand-edit generated files when the configured generator should
  produce them.

## Repository checks

This branch configures Odoo 19 CI through the `odoo-19` and `build-test` workflows. The
pre-commit configuration includes Odoo module and translation checks, Ruff, pylint-odoo,
formatting, and repository-specific hooks. Review failures and applicable skipped
checks; request the relevant checks when results are missing.

# Other modules

Check https://github.com/odoo/odoo and https://github.com/OCA for existing functionality
and modules and mention them, if the PR is doing redundant work. OCA-modules should be
checked from other main branches too, as they can be migrated to the current version if
needed.
