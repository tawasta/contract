from odoo import _, fields, models


class Contract(models.Model):

    _inherit = "contract.contract"

    latest_paid_invoice_id = fields.Many2one(
        string="Latest paid invoice",
        comodel_name="account.move",
        help="The latest invoice that has been paid",
        compute="_compute_latest_paid_invoice_id",
        store=True,
        copy=False,
        readonly=1,
    )
    latest_paid_invoice_due_date = fields.Date(
        "Latest paid invoice due date",
        compute="_compute_latest_paid_invoice_id",
        store=True,
        copy=False,
        readonly=1,
    )

    def _compute_latest_paid_invoice_id(self):
        for record in self:
            # Fetch latest paid invoice and link the latest paid invoice to it
            invoices = record._get_related_invoices()
            paid_invoices = invoices.filtered(lambda i: i.payment_state == "paid")
            latest_paid_invoice_id = False
            latest_paid_invoice_due_date = False

            if paid_invoices:
                latest_paid_invoice = paid_invoices[0]
                latest_paid_invoice_id = latest_paid_invoice.id
                latest_paid_invoice_due_date = latest_paid_invoice.invoice_date_due

            record.write(
                {
                    "latest_paid_invoice_id": latest_paid_invoice_id,
                    "latest_paid_invoice_due_date": latest_paid_invoice_due_date,
                }
            )

    def action_cron_update_latest_paid_invoice(self):
        contracts = self.search([])
        for contract in contracts:
            job_desc = _("Compute latest paid invoice for {}".format(contract.name))
            contract.with_delay(description=job_desc)._compute_latest_paid_invoice_id()
