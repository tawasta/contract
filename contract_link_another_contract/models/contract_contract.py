from odoo import fields, models


class Contract(models.Model):

    _inherit = "contract.contract"

    related_contract_id = fields.Many2one(
        comodel_name="contract.contract",
        relation="related_contract_rel",
        string="Related contract",
        readonly=False,
    )

    all_related_contract_ids = fields.Many2many(
        comodel_name="contract.contract",
        relation="all_related_contracts_rel",
        string="All related batches",
        compute="_get_contracts",
        readonly=True,
    )

    def _get_contracts(self):
        for record in self:
            all_contracts_related = self.env["contract.contract"].sudo().search([
                ('related_contract_id', '=', record.id)
            ])
            if record.partner_id.is_company:
                company_contracts = self.env["contract.contract"].sudo().search([
                    ('partner_invoice_id', '=', record.partner_id.id),
                    ('partner_id.is_company', '=', False),
                ])

                record.all_related_contract_ids = all_contracts_related + company_contracts
            else:
                record.all_related_contract_ids = all_contracts_related
