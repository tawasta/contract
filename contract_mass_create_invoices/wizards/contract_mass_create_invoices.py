import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ContractMassCreateInvoices(models.TransientModel):
    _name = "contract.mass.create.invoices"
    _description = "Mass create invoices"

    def action_mass_create_invoices(self):
        contract_ids = self.env["contract.contract"].browse(
            self._context.get("active_ids")
        )

        for contract in contract_ids:
            contract.recurring_create_invoice()
