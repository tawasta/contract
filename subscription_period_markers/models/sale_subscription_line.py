from dateutil.relativedelta import relativedelta
from odoo import models


class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    def _prepare_account_move_line(self):
        res = super()._prepare_account_move_line()

        subscription_id = self.sale_subscription_id

        lang_obj = self.env["res.lang"]
        lang = lang_obj.search([("code", "=", subscription_id.partner_id.lang)])
        date_format = lang.date_format or "%d.%m.%Y"

        name = res.get("name")
        if "#START" in name or "#END#" in name:
            type_interval = subscription_id.template_id.recurring_rule_type
            interval = int(subscription_id.template_id.recurring_interval)

            first_date_invoiced = subscription_id.recurring_next_date
            last_date_invoiced = first_date_invoiced + relativedelta(
                **{type_interval: interval}
            )

            if subscription_id.recurring_invoicing_type == "post-paid":
                # When subscription is paid after the period
                last_date_invoiced = first_date_invoiced
                first_date_invoiced = last_date_invoiced - relativedelta(
                    **{type_interval: interval}
                )

            # End the period before the next period starts
            last_date_invoiced = last_date_invoiced - relativedelta(days=1)

            name = name.replace("#START#", first_date_invoiced.strftime(date_format))
            name = name.replace("#END#", last_date_invoiced.strftime(date_format))

            res["name"] = name

        return res
