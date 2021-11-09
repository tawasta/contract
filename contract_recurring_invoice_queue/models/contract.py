from odoo import api, fields, models


class RecurringContractLimit(models.Model):
    _inherit = "contract.contract"

    @api.model
    def cron_recurring_create_invoice(self, date_ref=None):
        if not date_ref:
            date_ref = fields.Date.context_today(self)
        domain = self._get_contracts_to_invoice_domain(date_ref)
        invoices = self.env["account.move"]
        # Invoice by companies, so assignation emails get correct context
        companies_to_invoice = self.read_group(domain, ["company_id"], ["company_id"])
        for row in companies_to_invoice:
            contracts_to_invoice = self.search(row["__domain"]).with_context(
                allowed_company_ids=[row["company_id"][0]]
            )

            for contract in contracts_to_invoice:
                contract.with_delay()._recurring_create_invoice(date_ref)

        # The original method will return the created invoices, but as it's not possible here,
        # let's just return an empty recordset (so the result type is correct even when it's empty)
        return invoices
