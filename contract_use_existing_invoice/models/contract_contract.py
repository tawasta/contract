from odoo import models, fields


class Contract(models.Model):

    _inherit = "contract.contract"

    def _recurring_create_invoice(self, date_ref=False):
        """
        Overwrite the method to allow reusing existing invoices
        """
        account_move = self.env["account.move"]
        move_ids = []

        for record in self:
            invoices_values = record._prepare_recurring_invoices_values(date_ref)

            if len(invoices_values) == 1:
                # If the contract is creating multiple invoices at once, don't try to merge them to existing invoices
                existing_invoice = record._get_related_invoices().filtered(
                    lambda r: r.state == "draft"
                )

                if not existing_invoice:
                    # If there are no existing invoices, try to find an open invoice for this partner
                    if (
                        hasattr(self, "partner_invoice_id")
                        and record.partner_invoice_id
                    ):
                        # "contract_invoice_address" is installed
                        partner_id = record.partner_invoice_id
                    else:
                        partner_id = record.partner_id

                    existing_invoice = account_move.search(
                        [
                            ("partner_id", "=", partner_id.id),
                            ("state", "=", "draft"),
                            "|",
                            ("ref", "=", False),
                            ("ref", "=", record.code),
                        ]
                    )
            else:
                existing_invoice = False

            if existing_invoice:
                move = existing_invoice[0]
                invoice_line_ids = invoices_values[0]["invoice_line_ids"]
                move.write({"invoice_line_ids": invoice_line_ids})

                move_ids.append(move)
            else:
                moves = account_move.create(invoices_values)
                move_ids += moves.ids

        moves = account_move.browse(move_ids)
        self._invoice_followers(moves)
        self._compute_recurring_next_date()
        return moves
