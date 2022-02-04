from odoo import fields, models


class Contract(models.Model):

    _inherit = "contract.contract"

    related_contract_id = fields.Many2one(
        comodel_name="contract.contract",
        relation="related_contract_rel",
        string="Related contract",
        readonly=False,
    )
