from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    contract_terminate_reason_default = fields.Many2one(
        related="company_id.default_contract_terminate_reason_id",
        string="Default Contract Termination Reason",
        readonly=False,
        store=True,
    )
