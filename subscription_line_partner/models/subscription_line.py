from odoo import api, fields, models


class SubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Related partner",
        compute="_compute_partner_id",
        precompute=True,
        store=True,
        readonly=False,
    )

    def _compute_partner_id(self):
        for line in self:
            if line.product_id.subscription_commercial:
                line.partner_id = (
                    line.sale_subscription_id.partner_id.commercial_partner_id
                )
            else:
                line.partner_id = line.sale_subscription_id.partner_id

    @api.depends("product_id", "partner_id")
    def _compute_name(self):
        super()._compute_name()
        for record in self:
            if record.partner_id:
                record.name += ", {}".format(record.partner_id.name)
