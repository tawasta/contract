from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    contract_force_commercial_partner = fields.Boolean(
        string="Force commercial partner on contracts",
        help="When creating invoice from Contract, always use commercial partner",
        config_parameter="contract_force_commercial_partner",
        default=False,
    )
