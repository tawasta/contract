from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    contract_line_recurring_interval = fields.Integer(
        string="Default contract line interval",
        config_parameter="contract_line.recurring_interval",
        default=1,
    )

    contract_line_recurring_rule_type = fields.Selection(
        [
            ("daily", "Day(s)"),
            ("weekly", "Week(s)"),
            ("monthly", "Month(s)"),
            ("monthlylastday", "Month(s) last day"),
            ("quarterly", "Quarter(s)"),
            ("semesterly", "Semester(s)"),
            ("yearly", "Year(s)"),
        ],
        default="monthly",
        string="Default contract line recurrence",
        config_parameter="contract_line.recurring_rule_type",
    )
