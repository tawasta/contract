from odoo import api, fields, models


class Contract(models.Model):

    _inherit = "contract.contract"

    partner_invoice_id = fields.Many2one(
        comodel_name="res.partner", string="Invoice Address"
    )
    invoice_for_company = fields.Boolean(
        "Invoice for a company",
        compute="_compute_invoice_for_company",
        help="Invoice goes for a company",
        store=True,
    )

    separate_invoice_address = fields.Boolean(
        "Separate invoice address",
        help="Customer and invoice address differ",
        compute="_compute_separate_invoice_address",
        store=True,
    )

    @api.depends("partner_id", "partner_invoice_id")
    def _compute_invoice_for_company(self):
        for record in self:
            partner = record.partner_invoice_id or record.partner_id
            record.invoice_for_company = partner.is_company

    @api.depends("partner_invoice_id", "partner_id")
    def _compute_separate_invoice_address(self):
        for record in self:
            record.separate_invoice_address = (
                record.partner_invoice_id
                and record.partner_id != record.partner_invoice_id
            )

    def _prepare_invoice(self, *args, **kwargs):
        # Super will handle ensure_one() and other validation
        invoice_vals, move_form = super()._prepare_invoice(*args, **kwargs)

        # Add shipping address to writable values
        if self.partner_invoice_id:
            partner = self.partner_invoice_id
        else:
            partner = self.partner_id

        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("contract_force_commercial_partner")
        ):
            # Force commercial partner
            partner = partner.commercial_partner_id

        invoice_vals["partner_id"] = partner.id

        return invoice_vals, move_form
