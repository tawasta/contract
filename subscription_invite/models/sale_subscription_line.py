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

# 2. Known third party imports:


import logging

# 3. Odoo imports (openerp):
from odoo import fields, models, api, _

_logger = logging.getLogger(__name__)
# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleSubscriptionLine(models.Model):
    # 1. Private attributes
    _inherit = "sale.subscription.line"

    invite_id = fields.Many2one(
        string="Invitation", comodel_name="subscription.invitation"
    )

    def open_invite_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Send Invitation',
            'res_model': 'subscription.invite.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_subscription_line_id': self.id,
            }
        }

    invitation_status = fields.Char(
        string="Invitation Status",
        compute="_compute_invitation_status",
        store=False,
    )

    invitation_date_display = fields.Char(
        string="Invitation Date",
        compute="_compute_invitation_status",
        store=False,
    )

    @api.depends("invite_id", "invite_id.invited_date", "invite_id.used_date", "invite_id.is_used")
    def _compute_invitation_status(self):
        for line in self:
            if line.invite_id:
                if line.invite_id.is_used:
                    line.invitation_status = _("Accepted")
                    line.invitation_date_display = _(
                        "Accepted on %s"
                    ) % line.invite_id.used_date.strftime("%d.%m.%Y %H:%M:%S")
                else:
                    line.invitation_status = _("Pending")
                    line.invitation_date_display = _(
                        "Sent on %s, not yet accepted."
                    ) % line.invite_id.invited_date.strftime("%d.%m.%Y %H:%M:%S")
            else:
                line.invitation_status = ""
                line.invitation_date_display = ""
