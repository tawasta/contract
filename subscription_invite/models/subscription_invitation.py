from odoo import fields, models


class SubscriptionInvitation(models.Model):
    _name = "subscription.invitation"
    _description = "Subscription Invitation"
    _rec_name = "invite_email"

    subscription_id = fields.Many2one(
        "sale.subscription.line", string="Subscription", required=True
    )
    invite_email = fields.Char(string="Invite Email", required=True)
    invited_date = fields.Datetime(
        string="Invitation Date", default=fields.Datetime.now
    )
    is_used = fields.Boolean(string="Is Used", default=False)
    used_date = fields.Datetime(string="Used Date")
    access_token = fields.Char(
        string="Access Token", required=True, copy=False, index=True
    )
