from odoo import fields, models


class ContractLine(models.Model):

    _inherit = "contract.line"

    contract_id_partner_shipping_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        related="contract_id.partner_shipping_id",
        store=True,
    )

    contract_id_date_end = fields.Date(
        string="End date",
        related="contract_id.date_end",
        store=True,
    )

    contract_id_shipping_name = fields.Char(
        related="contract_id.partner_shipping_id.name",
    )

    contract_id_shipping_name_conditional = fields.Char(
        string="Name",
        compute=lambda self: self._compute_contract_id_shipping_name_conditional(),
    )

    contract_id_shipping_commercial_partner_id = fields.Many2one(
        comodel_name="res.partner",
        related="contract_id.partner_shipping_id.commercial_partner_id",
    )

    contract_id_shipping_street = fields.Char(
        string="Street",
        related="contract_id.partner_shipping_id.street",
    )

    contract_id_shipping_street2 = fields.Char(
        string="Street 2",
        related="contract_id.partner_shipping_id.street2",
    )

    contract_id_shipping_zip = fields.Char(
        string="Zip",
        related="contract_id.partner_shipping_id.zip",
    )

    contract_id_shipping_city = fields.Char(
        string="City",
        related="contract_id.partner_shipping_id.city",
        store=True,
    )

    contract_id_shipping_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        related="contract_id.partner_shipping_id.country_id",
        store=True,
    )

    contract_id_shipping_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        related="contract_id.partner_shipping_id.user_id",
        store=True,
    )

    def _compute_contract_id_shipping_name_conditional(self):
        for line in self:
            if (
                line.contract_id_partner_shipping_id
                != line.contract_id_shipping_commercial_partner_id
            ):
                line.contract_id_shipping_name_conditional = (
                    line.contract_id.partner_shipping_id.name
                )
            else:
                line.contract_id_shipping_name_conditional = ""
