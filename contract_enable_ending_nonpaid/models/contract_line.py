from odoo import fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    last_date_invoiced = fields.Date(
        string='Invoiced until',
        readonly=False,
        copy=False,
    )
