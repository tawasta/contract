import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class SaleSubscriptionLine(models.Model):
    # 1. Private attributes
    _inherit = "sale.subscription.line"

    invite_id = fields.Many2one(
        string="Invitation", comodel_name="subscription.invitation"
    )

    def open_invite_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Send Invitation",
            "res_model": "subscription.invite.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_subscription_line_id": self.id,
            },
        }

    invitation_status = fields.Char(
        compute="_compute_invitation_status",
        store=False,
    )

    invitation_date_display = fields.Char(
        string="Invitation Date",
        compute="_compute_invitation_status",
        store=False,
    )

    @api.depends(
        "invite_id",
        "invite_id.invited_date",
        "invite_id.used_date",
        "invite_id.is_used",
    )
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
