##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class RecurringContractLimitCompany(models.Model):
    # 1. Private attributes
    _inherit = "res.company"

    # 2. Fields declaration
    contract_recurring_invoice_limit = fields.Integer(
        string="How many invoices to generate per run", default=5000, readonly=False
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods


class RecurringContractLimitSettings(models.TransientModel):
    # 1. Private attributes
    _inherit = "res.config.settings"

    # 2. Fields declaration
    contract_recurring_invoice_limit = fields.Integer(
        related="company_id.contract_recurring_invoice_limit",
        help="How many invoices to generate per run",
        readonly=False,
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods


class RecurringContractLimit(models.Model):
    # 1. Private attributes
    _inherit = "contract.contract"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.model
    def cron_recurring_create_invoice(self, date_ref=None):
        if not date_ref:
            date_ref = fields.Date.context_today(self)
        domain = self._get_contracts_to_invoice_domain(date_ref)
        invoices = self.env["account.move"]
        # Invoice by companies, so assignation emails get correct context
        companies_to_invoice = self.read_group(domain, ["company_id"], ["company_id"])
        for row in companies_to_invoice:
            contracts_to_invoice = self.search(
                row["__domain"],
                limit=self.env.user.company_id.contract_recurring_invoice_limit,
            ).with_context(allowed_company_ids=[row["company_id"][0]])
            invoices |= contracts_to_invoice._recurring_create_invoice(date_ref)
        return invoices

    # 8. Business methods
