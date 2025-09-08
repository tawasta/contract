from odoo import fields, models


class TransmitMethod(models.Model):
    _inherit = "transmit.method"

    contract_target_type = fields.Selection(
        [
            ("person", "Person"),
            ("company", "Company"),
            ("both", "Both"),
        ],
        default="both",
        string="Visible for Contact Type",
        help="Defines whether this transmit method is selectable for persons, companies, or both in the website subscription contact form.",
    )
