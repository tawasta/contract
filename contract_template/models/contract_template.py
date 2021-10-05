from odoo import fields, models


class ContractTemplate(models.Model):

    _inherit = "contract.template"

    recurring_rule_type = fields.Selection(
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
        string="Recurrence",
        help="Specify Interval for automatic invoice generation.",
    )
    recurring_interval = fields.Integer(
        default=1,
        string="Invoice Every",
        help="Invoice every (Days/Week/Month/Year)",
    )

    payment_term_id = fields.Many2one(
        comodel_name="account.payment.term", string="Payment Terms", index=True
    )
