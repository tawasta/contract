from odoo import models
from odoo.exceptions import AccessError


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def create_invoice(self):
        if not self.env["account.move"].check_access_rights("create", False):
            try:
                self.check_access_rights("write")
                self.check_access_rule("write")
            except AccessError:
                return self.env["account.move"]

        account_move = self.env["account.move"]

        for record in self:
            # Invoices linked to this subcription
            existing_invoices = self.invoice_ids.filtered(lambda r: r.state == "draft")
            if not existing_invoices:
                # If there are no linked invoices,
                # try to find an open invoice for this partner
                existing_invoices = account_move.search(
                    [
                        ("partner_id", "=", self.partner_id.id),
                        ("state", "=", "draft"),
                        "|",
                        ("ref", "=", False),
                        ("ref", "=", record.invoice_ref),
                    ]
                )

            if existing_invoices:
                # Create new lines for existing invoice
                invoice_id = existing_invoices[0]
                line_ids = []
                for line in self.sale_subscription_line_ids:
                    line_values = line._prepare_account_move_line()
                    line_ids.append((0, 0, line_values))

                invoice_id.invoice_line_ids = line_ids
                if hasattr(self, "partner_shipping_id"):
                    # Remove separate shipping address from combined invoices
                    invoice_id.partner_shipping_id = self.partner_id

                self.write({"invoice_ids": [(4, invoice_id.id)]})
            else:
                # Create new invoice
                invoice_id = super().create_invoice()

        return invoice_id
