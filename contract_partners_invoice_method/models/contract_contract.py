from odoo import fields, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    customer_invoice_transmit_method_id = fields.Many2one(
        comodel_name="transmit.method",
        related="partner_id.customer_invoice_transmit_method_id",
    )
