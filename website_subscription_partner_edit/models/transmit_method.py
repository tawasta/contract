from odoo import fields, models


class TransmitMethod(models.Model):
    _inherit = "transmit.method"

    contract_target_type = fields.Selection(
        [('person', 'Person'), ('company', 'Company'), ('both', 'Both')],
        default='both',
        string="Target Type"
    )
