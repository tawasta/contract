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

# 3. Odoo imports (openerp):
from odoo import _, fields, models

# 2. Known third party imports:


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
    successful_contract_line_ids = fields.Many2many(
        "contract.line",
        "succesful_contract_rel",
        string="Succesfully Invoiced Contract Lines",
        readonly=1,
    )
    skipped_contract_line_ids = fields.Many2many(
        "contract.line",
        "skipped_contract_rel",
        string="Skipped Contract Lines",
        readonly=1,
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def action_invoice_member(self):
        for wizard in self:
            skipped_contract_lines = self.env["contract.line"]
            successful_contract_lines = self.env["contract.line"]
            for contract in wizard.contract_ids:
                skip_contract = True
                for contract_line in contract.contract_line_fixed_ids:
                    skip_contract_line = False
                    # check if contract line is not cancelled
                    if contract_line.state in ["upcoming", "in-progress", "to-renew"]:
                        # Skip contract_line if contract_line product
                        # membership date end matches with
                        # a paid membership_line date end
                        if any(
                            contract_line.product_id == membership_line.membership_id
                            and membership_line.date_to
                            == contract_line.product_id.membership_date_to
                            and membership_line.state == "paid"
                            for membership_line in contract.membership_line_ids
                        ):
                            skip_contract_line = True
                            skipped_contract_lines += contract_line
                        # If any line lis not skipped reset next_invoicing date as today
                        # and run contract.recurring_create_invoice()
                        if not skip_contract_line:
                            skip_contract = False
                            contract_line.recurring_next_date = fields.Date.today()
                            successful_contract_lines += contract_line
                # if contract is not skipped reset next_invoicing date as today \
                # and run contract.recurring_create_invoice()
                if not skip_contract:
                    # set invoice address as partner/member
                    contract.partner_invoice_id = contract.partner_id
                    contract.recurring_next_date = fields.Date.today()
                    contract.recurring_create_invoice()
            _logger.info(
                _(
                    "Invoice Member Wizard Without Company run succesfully.\n "
                    "Succesful Contract Lines: %s\n Skipped Contract Lines: %s"
                    % (successful_contract_lines, skipped_contract_lines)
                )
            )
            return {
                "type": "ir.actions.act_window",
                "name": _("Success"),
                "context": {
                    "default_successful_contract_line_ids": successful_contract_lines.ids,
                    "default_skipped_contract_line_ids": skipped_contract_lines.ids,
                },
                "view_type": "form",
                "view_mode": "form",
                "res_model": "invoice.member.wizard",
                "views": [
                    (
                        self.env.ref(
                            "contract_mass_action_invoice_member.contract_mass_action_invoice_member_form_log"
                        ).id,
                        "form",
                    )
                ],
                "target": "new",
            }


# 8. Business methods
