from odoo import fields, models


class SubscriptionInvitation(models.Model):
    _name = "subscription.invitation"
    _description = "Subscription Invitation"
    _rec_name = "invite_email"

    subscription_id = fields.Many2one(
        "sale.subscription.line", string="Subscription", required=True
    )
    invite_email = fields.Char(required=True)
    invited_date = fields.Datetime(default=fields.Datetime.now)
    is_used = fields.Boolean(default=False)
    used_date = fields.Datetime()
    access_token = fields.Char(required=True, copy=False, index=True)
