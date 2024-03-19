from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    default_contract_terminate_reason_id = fields.Many2one(
        comodel_name="contract.terminate.reason",
        string="Default Contract Termination Reason",
    )
