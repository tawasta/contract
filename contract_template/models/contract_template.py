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
        required=True,
    )
    recurring_interval = fields.Integer(
        default=1,
        string="Invoice Every",
        help="Invoice every (Days/Week/Month/Year)",
        required=True,
    )

    payment_term_id = fields.Many2one(
        comodel_name="account.payment.term",
        string="Payment Terms",
        required=True,
        index=True,
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        index=True,
    )
