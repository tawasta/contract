from odoo import api, fields, models


class ContractLine(models.Model):

    _inherit = "contract.line"

    contract_id_partner_invoice_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        related="contract_id.partner_invoice_id",
        store=True,
    )

    contract_id_invoice_name = fields.Char(
        related="contract_id.partner_invoice_id.name",
    )

    contract_id_invoice_name_conditional = fields.Char(
        string="Name", compute="_compute_contract_id_invoice_name_conditional"
    )

    contract_id_invoice_commercial_partner_id = fields.Many2one(
        comodel_name="res.partner",
        related="contract_id.partner_invoice_id.commercial_partner_id",
    )

    contract_id_invoice_street = fields.Char(
        string="Street",
        related="contract_id.partner_invoice_id.street",
    )

    contract_id_invoice_street2 = fields.Char(
        string="Street 2",
        related="contract_id.partner_invoice_id.street2",
    )

    contract_id_invoice_zip = fields.Char(
        string="Zip",
        related="contract_id.partner_invoice_id.zip",
    )

    contract_id_invoice_city = fields.Char(
        string="City",
        related="contract_id.partner_invoice_id.city",
        store=True,
    )

    contract_id_invoice_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        related="contract_id.partner_invoice_id.country_id",
        store=True,
    )

    contract_id_invoice_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        related="contract_id.partner_invoice_id.user_id",
        store=True,
    )

    @api.depends("contract_id_partner_invoice_id")
    def _compute_contract_id_invoice_name_conditional(self):
        for record in self:
            if (
                record.contract_id_partner_invoice_id
                != record.contract_id_invoice_commercial_partner_id
            ):
                record.contract_id_invoice_name_conditional = (
                    record.contract_id.partner_invoice_id.name
                )
            else:
                record.contract_id_invoice_name_conditional = False
