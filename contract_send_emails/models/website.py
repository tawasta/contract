from odoo import api, fields, models,

class Website(models.Model):

    _inherit = "website"

    contract_email = fields.Char(string="Contract email", help="When the contract line is terminated or updated, a message will be sent to this email")