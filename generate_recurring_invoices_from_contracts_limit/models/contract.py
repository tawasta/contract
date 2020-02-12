from odoo import api, fields, models


class RecurringContractLimitCompany(models.Model):
    _inherit = "res.company"
    contract_recurring_invoice_limit = fields.Integer(
        string="How many invoices to generate per run", default=5000, readonly=False
    )


class RecurringContractLimitSettings(models.TransientModel):
    _inherit = "res.config.settings"

    contract_recurring_invoice_limit = fields.Integer(
        related="company_id.contract_recurring_invoice_limit",
        help="How many invoices to generate per run",
        readonly=False,
    )


class RecurringContractLimit(models.Model):
    _inherit = "contract.contract"

    @api.model
    def cron_recurring_create_invoice(self):
        domain = self._get_contracts_to_invoice_domain()
        contracts_to_invoice = self.search(
            domain, limit=self.env.user.company_id.contract_recurring_invoice_limit
        )
        date_ref = fields.Date.context_today(contracts_to_invoice)
        contracts_to_invoice._recurring_create_invoice(date_ref)
