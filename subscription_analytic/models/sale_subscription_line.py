from odoo import api, models


class SaleSubscriptionLine(models.Model):
    _name = "sale.subscription.line"
    _inherit = ["sale.subscription.line", "analytic.mixin"]

    @api.depends("sale_subscription_id.partner_id", "product_id")
    def _compute_analytic_distribution(self):
        for line in self:
            line_partner = line.sale_subscription_id.partner_id
            vals = {
                "product_id": line.product_id.id,
                "product_categ_id": line.product_id.categ_id.id,
                "partner_id": line_partner.id,
                "partner_category_id": line_partner.category_id.ids,
                "company_id": line.company_id.id,
            }

            distribution = line.env[
                "account.analytic.distribution.model"
            ]._get_distribution(vals)
            line.analytic_distribution = distribution or line.analytic_distribution

    def _prepare_account_move_line(self):
        res = super()._prepare_account_move_line()

        res["analytic_distribution"] = self.analytic_distribution

        return res
