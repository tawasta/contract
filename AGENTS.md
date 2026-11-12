# Development rules

These rules apply to every change in this repository. Reviews check the code against
these rules and [REVIEW.md](REVIEW.md).

## General

Quality before speed: the code is production-ready, clear, secure, efficient and as
simple as possible.

- **Do not assume the version.** Check it from the branch and the manifest version. Do
  not copy a solution from one version to another without checking.
- **Before implementing, investigate two things:**
  - Odoo core
  - other modules that change the same model

  Prove claims with `file:line` references.

- **Smallest correct change.** Implement only what was asked. Fix the root cause, not
  the symptom. Do not refactor or tidy the surrounding code without asking.
- **Do not modify core or OCA.** Extend an existing own module. Create a new module only
  if the functionality does not belong in any existing one.

## Permanent rules for every edited module

1. `i18n/fi.po` up to date (create it if missing)
2. README updated with the functionality changes
3. Own name and email (`Name <email>`) in the Contributors section
4. manifest version bumped.

`pre-commit run --all-files` passes. A pre-commit hook that does not support the
machine's Python version may be left failing.

## Quality

- The code is clear: descriptive names, small methods, early return, no duplicate, dead
  or commented-out code. Comments tell _why_.
- No hidden errors (`except Exception: pass`) and no `print` calls.
- ORM in batches, no searches or writes in loops. Support multiple records and
  multi-company.
- Security: every `sudo()` call has a reason. Never trust data or IDs coming from the
  browser. Assume the portal user misbehaves.
- Frontend: professional look, Bootstrap classes and components, no custom CSS without a
  justification, no `!important` rules and no inline styles (except in email and PDF
  templates).

## Limits

- **Tests are written only when requested.**

## Commit message

```
[FIX|IMP|ADD|MIG] <module>: <short description>

Assisted-by: <model name, e.g. Claude Opus 5.5>
```

# Coding conventions

## Code quality

- Write the simplest correct solution. Abstractions, helper modules or settings are
  added only for a real need.
- Methods are small (under ~30 lines) and do one thing. Names describe the action
  (`_prepare_contract_vals`, `_check_ecommerce_tax`).
- Prefer early return, not deep nesting.
- No duplicate, dead or commented-out code, `print` calls or debug logs.
- A comment tells _why_, not _what_. Code and comments are written in English.
- Errors are not hidden. No `except Exception: pass` construct. An expected error →
  `UserError` or `ValidationError` with a clear message.
- Translatable texts: `_("Order %(name)s failed", name=order.name)` (18+:
  `self.env._(...)`). Do not format the text inside the `_()` call.

## The Odoo way

- Inherit and call `super()`. Do not copy a core method and do not monkeypatch.
- Use the core extension points (`_prepare_invoice`, `_get_*`, `_compute_*`) before
  overriding large methods.
- `create`: `@api.model_create_multi` and `vals_list`. `write` and `unlink` work on a
  recordset.
- A compute field has the right `@api.depends` dependencies and a `for record in self`
  loop. `store=True` only with a justification (search, grouping, performance).
- Fields: consider `required`, `readonly`, `copy`, `index`, `tracking`,
  `company_dependent` and `check_company`.
- Onchange only as a user interface aid. Mandatory rules belong in the `@api.constrains`
  decorator or in a create/write method.
- Data: `noupdate="1"` for data that the customer can edit (templates, sequences,
  crons).

## ORM and performance

- No `search`, `browse`, `write` or `create` calls in a loop. Process in batches
  (`create(vals_list)`, `records.write(vals)`).
- Use `mapped`, `filtered` and `grouped` (17+) on recordsets. Prefetch handles reading.
- One search, not the same query again. `search_count` or `_read_group` for counting.
- SQL only with a justification (report views, mass update). Use parameters (`SQL()`
  17+), never string formatting.
- Scheduled task (cron):
  - Processes at most a limited number of records per run (`limit`). The rest are
    processed on the next run.
  - Selects only unprocessed records, so that a rerun does not do the same work twice.
  - Uses the `self.env.cr.commit()` call between batches only in long runs where the
    batches already processed should be saved even if a later batch fails.

## Security

- Every new model has `ir.model.access.csv` rows. Multi-company data needs `company_id`,
  a record rule (`company_ids`) and `check_company=True`.
- `sudo()` only with a justification and narrowly. Comment the reason. Never
  `sudo().browse(id_from_browser)` without an ownership or token check.
- Controller: the right `auth`, and `csrf` off only for external webhooks that are
  otherwise authenticated. In the portal `_document_check_access()` and an access token.
  Do not trust the ID, price or state from the browser.
- `t-out` only for trusted content (Markup or an html field). No critical information in
  logs.

## Frontend (website, portal and backend views)

- The look is professional and in line with Odoo's own style: consistent spacing,
  typography, buttons and icons (`fa fa-*` / `oi`).
- **Bootstrap first:**
  - grid: `container`, `row`, `col-*`
  - utilities: `d-flex`, `gap-*`, `m*-*`, `p*-*`, `text-*`, `fw-*`, `bg-*`, `border`,
    `rounded`, `shadow-sm`
  - components: `card`, `alert`, `badge`, `btn`, `modal`, `list-group`, `table`
  - Odoo's classes and widgets (`o_*`, `widget="badge"`, `decoration-*`).
- **No custom CSS**, unless Bootstrap or Odoo solves the matter. If it is needed, it is
  a small SCSS file, tightly scoped with the module's own class, without `!important`
  rules and using Bootstrap variables.
- **No inline styles** (`style=`). Exception: email templates and PDF reports.
- Responsive (`col-12 col-md-6`) and accessible (`label for`, `aria-*`, `alt`). Keyboard
  focus stays visible (do not remove the focus outline), and motion respects
  `prefers-reduced-motion`. Animate only in response to a user action, not as
  decoration.
- Texts are translatable, and they are not hardcoded in JS without a `_t` call.
- **User-facing texts** (buttons, messages, empty states, portal and website copy,
  `UserError`):
  - A button says what happens ("Save changes", "Send request"), not "Submit" or "OK".
  - One action keeps one name through the whole flow: the button "Publish" gives the
    message "Published".
  - An error says what went wrong and how to fix it. It does not apologise and is not
    vague.
  - An empty state points to the next action.
  - Use the user's words, not internal names (a user manages notifications, not webhook
    settings). Active voice, sentence case.
  - Keep long running text under about 80 characters per line.
- QWeb inheritance with xpath (`hasclass()`, `@name`, `@id`), not by replacing a whole
  template and not with index-based selectors (`div[3]`).
- Bootstrap 5 (16+): `data-bs-*`. 17+: `invisible`, `readonly` and `required` as
  expressions, not `attrs`. 18+: `<list>`.
- JS: OWL and Odoo's services (`orm`, `rpc`, `notification`). No direct DOM manipulation
  and no business logic in the browser. Validation and calculation are done on the
  server.

## Backend views

- A new field is placed in a logical spot (`group`, `notebook` page), not at the end of
  the form.
- Group restriction `groups=` on a field or a button, if the information does not belong
  to everyone.
- In a list view only the essential columns. Others `optional="hide"`.

# Templates for a new module

Structure:

```
module/
  __init__.py
  __manifest__.py
  pyproject.toml
  README.rst
  i18n/fi.po
  models/ views/ security/ data/ controllers/ static/description/icon.png
```

## **manifest**.py

```python
##############################################################################
#
#    Author: Futural Oy
#    Copyright <year>- Futural Oy (https://futural.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

{
    "name": "Area: Feature",
    "summary": "One line description",
    "version": "<v>.0.1.0.0",
    "category": "<Category>",
    "website": "https://github.com/tawasta/<repo>",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [],
    "data": [],
}
```

`website` is the name of the repo (the same as in the other modules of the same repo).

## pyproject.toml

```toml
[build-system]
requires = ["whool"]
build-backend = "whool.buildapi"
```

## README.rst

```rst
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============
Area: Feature
=============

* What the module does, from the user's point of view.

Configuration
=============
\-

Usage
=====
* Where and how to use it.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* <User's name> <user's.email@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
```

The underline of a heading is as long as the heading. If the repo uses a `readme/`
folder, update it there (`DESCRIPTION.md`, `CONTRIBUTORS.md` …).

## i18n/fi.po

```
# Translation of Odoo Server.
# This file contains the translation of the following modules:
# 	* module
#
msgid ""
msgstr ""
"Project-Id-Version: Odoo Server <v>.0\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: <date> 00:00+0000\n"
"PO-Revision-Date: <date> 00:00+0000\n"
"Last-Translator: \n"
"Language-Team: \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: \n"
"Plural-Forms: \n"

#. module: module
#: model:ir.model.fields,field_description:module.field_sale_order__x
msgid "Contract"
msgstr "Sopimus"
```

Included are the `string` and `help` of fields, selection values, the `_description` of
new models, `_()` texts and the texts of views, menus, actions and templates. The source
references (`#:`) follow Odoo's format: `model:`, `model_terms:ir.ui.view,arch_db:`,
`code:addons/module/models/x.py:0`.

# Odoo tests

Only when the user has asked for tests. Without the request no test is written,
suggested or extended.

## Before writing

1. **Version** from the branch and the manifest version. Read the test API of that
   version from `odoo/tests/common.py` in Odoo core. Do not copy a solution from another
   version without checking.
2. **What to test.** If the user did not name the behaviours, list the ones you propose
   (step 3) and let the user confirm them.
3. **An example:** the existing tests of the model in core or in the other modules
   (`tests/` folders), to follow their set-up.

## What makes a test good

- **Name the break.** Before writing a test, answer: which change in the code should
  make it fail, and is that change a bug? A test that only intentional changes can fail
  is not written. The name tells the behaviour:
  `test_portal_user_cannot_read_other_partner_invoice`.
- **Behaviour, not structure.** Do not assert private structure, constants or the exact
  wording of a message, unless the message is the behaviour.
- **Hand-derived expectations.** The expected value is a literal written by you, not
  computed by the code under test or its helpers.
- **Real records, not mocks.** Mock only an external service (HTTP, mail server), never
  the ORM.
- **Our code, not core.** Test what the module adds or changes.

## Scenarios to choose from

Pick those that apply to the change:

- the normal flow
- a boundary or empty case
- several records in one call (batch)
- a rerun: a cron or action run twice does not create duplicates
- access: a user without the right gets an `AccessError`. Test the roles that matter
  (internal, portal, public)
- multi-company: a user of company A does not see or change the data of company B

## Structure in Odoo

- Tests are in the module's `tests/` package. The file name starts with `test_` and
  `tests/__init__.py` imports it: core runs only the `test_*` modules that the package
  contains (`odoo/tests/loader.py:25-35` in 17, `56-66` in 19).
- `TransactionCase`: each test runs in its own rolled-back transaction. Shared data is
  created in `setUpClass` (`cls.env`).
- `HttpCase`: controllers, the portal and tours (`url_open`, `authenticate`,
  `start_tour`). It runs after the installation, so tag it
  `@tagged("post_install", "-at_install")`. Core warns otherwise (`common.py:2473`,
  version 19).
- Tags: a test is either `at_install` or `post_install` (`@tagged`,
  `common.py:2712-2732`, version 19). Check the rule in the version you work with.
- Users: `new_test_user(env, login, groups="base.group_user")`, for a portal user
  `groups="base.group_portal"` (`common.py:157` in 17, `common.py:195` in 19).
- Helpers: `assertRecordValues(records, expected_values)`, `assertQueryCount`, and
  `Form` (`odoo.tests.form`) for form and onchange behaviour.
- Code quality rules apply to tests: no `print`, no fixed `sleep`, no commented-out
  code.

## A test for a bug fix must fail on the old code

The new test is run against the code without the fix and must fail, then with the fix.
If this cannot be done, the handover says
`Not verified: the test fails without the fix`.

## Permanent module rules

Adding tests edits the module, so the permanent rules for every edited module apply:
fi.po (state that there are no new texts), README, Contributors and the manifest
version.
