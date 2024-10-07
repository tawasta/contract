from odoo import api, fields, models


class SubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Related partner",
    )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if not res.partner_id:
            if res.product_id.subscription_commercial:
                res.partner_id = (
                    res.sale_subscription_id.partner_id.commercial_partner_id
                )
            else:
                res.partner_id = res.sale_subscription_id.partner_id

        return res

    @api.depends("product_id", "partner_id")
    def _compute_name(self):
        super()._compute_name()
        for record in self:
            if record.partner_id:
                record.name += ", {}".format(record.partner_id.name)
