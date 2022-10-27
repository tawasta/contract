from odoo import fields, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    cancel_reason = fields.Char(
        string="Cancellation Reason",
        help="The reason for terminating the contract.",
    )
