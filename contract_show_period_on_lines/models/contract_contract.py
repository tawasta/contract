from odoo import api, fields, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    show_period_on_lines = fields.Boolean(
        string="Show Invoice Period on Lines",
        help="If this is checked, each generated invoice line will \
        also show the time span of the invoice",
    )

    invoicing_period_date_from = fields.Date(
        string="Next period start",
        compute="_compute_invoice_period",
    )
    invoicing_period_date_to = fields.Date(
        string="Next period end",
        compute="_compute_invoice_period",
    )

    @api.depends('contract_line_ids')
    def _compute_invoice_period(self):
        for record in self:
            if not record.contract_line_ids:
                record.invoicing_period_date_from = False
                record.invoicing_period_date_to = False

            for line in record.contract_line_ids:
                date_format = "%Y-%m-%d"

                self.env["contract.line"]

                dates = line._get_period_to_invoice(
                    record.last_date_invoiced, record.recurring_next_date
                )

                first_date_invoiced = dates[0].strftime(date_format)
                last_date_invoiced = dates[1].strftime(date_format)

                if record.show_period_on_lines:

                    # Add the invoicing period after line
                    record.invoicing_period_date_from = first_date_invoiced
                    record.invoicing_period_date_to = last_date_invoiced
                else:
                    record.invoicing_period_date_from = False
                    record.invoicing_period_date_to = False

                break
