from odoo import models


class ContractLine(models.Model):

    _inherit = "contract.line"

    def _prepare_invoice_line(self, move_form):
        invoice_line_vals = super()._prepare_invoice_line(move_form)

        lang_obj = self.env["res.lang"]
        lang = lang_obj.search([("code", "=", self.contract_id.partner_id.lang)])
        date_format = lang.date_format or "%m/%d/%Y"

        dates = self._get_period_to_invoice(
            self.last_date_invoiced, self.recurring_next_date
        )

        first_date_invoiced = dates[0].strftime(date_format)
        last_date_invoiced = dates[1].strftime(date_format)

        if self.contract_id.show_period_on_lines:

            # Add the invoicing period after line
            invoice_line_vals["name"] += " %s - %s" % (
                first_date_invoiced,
                last_date_invoiced,
            )

        return invoice_line_vals
