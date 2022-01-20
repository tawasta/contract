##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
import logging

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import _, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class InvoiceMemberWizard(models.TransientModel):
    # 1. Private attributes
    _name = "invoice.member.wizard"
    _description = "Action to set default invoice address and create new invoice"

    # 2. Fields declaration
    contract_ids = fields.Many2many(
        "contract.contract",
        default=lambda self: self.env["contract.contract"].browse(
            self._context.get("active_ids")
        ),
        string="Contracts",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def action_invoice_member(self):
        for wizard in self:
            for contract in wizard.contract_ids:
                contract_line_names = []
                # set invoice address as partner/member
                contract.partner_invoice_id = contract.partner_id
                for contract_line in contract.contract_line_fixed_ids:
                    # check if contract line is not cancelled
                    if contract_line.state in ["upcoming", "in-progress", "to-renew"]:
                        # reset next invoicing date as today
                        contract_line.recurring_next_date = fields.Date.today()
                        contract_line_names.append(contract_line.name)
                if contract_line_names:
                    contract.recurring_next_date = fields.Date.today()
                    _logger.info(
                        _(
                            "Following contract lines invoiced for a contract %s:\n%s",
                            contract.name,
                            contract_line_names,
                        )
                    )
                contract.recurring_create_invoice()

    # 8. Business methods
