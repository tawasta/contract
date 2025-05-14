from odoo import models, fields, api, tools
from odoo.exceptions import UserError
import secrets
from datetime import datetime
import re


class SubscriptionInviteWizard(models.TransientModel):
    _name = "subscription.invite.wizard"
    _description = "Subscription Invitation Wizard"

    subscription_line_id = fields.Many2one("sale.subscription.line", required=True)
    invite_email = fields.Char(string="Email", required=True)
    confirm_email = fields.Char(string="Confirm Email", required=True)

    def _is_valid_email(self, email):
        email = email.strip()
        return tools.email_split(email) and re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def action_send_invite(self):
        self.ensure_one()

        email = (self.invite_email or "").strip()
        confirm = (self.confirm_email or "").strip()

        if not self._is_valid_email(email):
            raise UserError("Please enter a valid email address.")

        if email != confirm:
            raise UserError("The email addresses do not match.")

        line = self.subscription_line_id
        if not line:
            raise UserError("Subscription line not found.")

        existing_user = (
            self.env["res.users"].sudo().search([("login", "=", email)], limit=1)
        )
        if not existing_user:
            partner = (
                self.env["res.partner"]
                .sudo()
                .create(
                    {
                        "name": email.split("@")[0],
                        "email": email,
                    }
                )
            )
            wizard = (
                self.env["portal.wizard"]
                .sudo()
                .create(
                    {
                        "partner_ids": [(6, 0, [partner.id])],
                    }
                )
            )
            portal_user = (
                self.env["portal.wizard.user"]
                .sudo()
                .create(
                    {
                        "wizard_id": wizard.id,
                        "partner_id": partner.id,
                        "email": email,
                    }
                )
            )
            portal_user.action_grant_access()

        if line.invite_id:
            line.invite_id.unlink()

        invite = (
            self.env["subscription.invitation"]
            .sudo()
            .create(
                {
                    "subscription_id": line.id,
                    "invite_email": email,
                    "invited_date": datetime.now(),
                    "is_used": False,
                    "access_token": secrets.token_urlsafe(32),
                }
            )
        )
        line.sudo().invite_id = invite.id

        template = self.env.ref(
            "subscription_invite.subscription_invitation_email_template"
        )
        if not template:
            raise UserError("Email template not found")

        template.sudo().send_mail(
            line.id, force_send=True, email_values={"email_to": email}
        )

        return {"type": "ir.actions.act_window_close"}
