from odoo import fields, models


class AccountAnalyticContract(models.Model):

    _inherit = "account.analytic.contract"

    partner_id_street = fields.Char(string="Street", related="partner_id.street")

    partner_id_street2 = fields.Char(string="Street2", related="partner_id.street2")

    partner_id_zip = fields.Char(string="Zip", related="partner_id.zip")

    partner_id_city = fields.Char(string="City", related="partner_id.city")

    partner_id_country_id = fields.Many2one(
        comodel_name="res.country", string="Country", related="partner_id.country_id"
    )
