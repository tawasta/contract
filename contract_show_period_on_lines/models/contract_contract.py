from odoo import fields, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    show_period_on_lines = fields.Boolean(
        string="Show Invoice Period on Lines",
        help="If this is checked, each generated invoice line will \
        also show the time span of the invoice",
        default=True,
    )
