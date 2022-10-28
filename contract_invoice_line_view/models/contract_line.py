from odoo import fields, models


class ContractLine(models.Model):

    _inherit = "contract.line"

    contract_id_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        related="contract_id.partner_id",
        store=True,
    )

    contract_id_date_end = fields.Date(
        string="End date", related="contract_id.date_end", store=True
    )

    contract_id_code = fields.Char(string="Reference", related="contract_id.code")

    contract_id_street = fields.Char(
        string="Street", related="contract_id.partner_id_street"
    )

    contract_id_street2 = fields.Char(
        string="Street 2", related="contract_id.partner_id_street2"
    )

    contract_id_zip = fields.Char(string="Zip", related="contract_id.partner_id_zip")

    contract_id_city = fields.Char(
        string="City", related="contract_id.partner_id_city", store=True
    )

    contract_id_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        related="contract_id.partner_id_country_id",
        store=True,
    )
