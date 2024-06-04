from odoo import fields, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    note = fields.Html("Terms and conditions")
