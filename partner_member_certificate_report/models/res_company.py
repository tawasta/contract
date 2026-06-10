from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    member_certificate_signature = fields.Image(
        string="Member certificate signature",
        max_width=1024,
        max_height=1024,
    )
    member_certificate_signatory_name = fields.Char(
        string="Member certificate signatory name",
    )
    member_certificate_signatory_title = fields.Char(
        string="Member certificate signatory title",
    )
    member_certificate_signatory_place = fields.Char(
        string="Member certificate signatory place",
    )
    footer_company_definition = fields.Text(string="Footer company definition")
