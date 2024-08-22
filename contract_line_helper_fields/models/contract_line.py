from odoo import fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    contract_partner_name = fields.Char(related="partner_id.name")
    contract_partner_email = fields.Char(related="partner_id.email")
    contract_partner_ref = fields.Char(related="partner_id.ref")
    contract_product_name = fields.Char(related="product_id.name")
    contract_product_default_code = fields.Char(related="product_id.default_code")
