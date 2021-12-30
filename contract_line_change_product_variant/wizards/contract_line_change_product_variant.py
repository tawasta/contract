from datetime import datetime

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class ContractLineChangeProductVariant(models.TransientModel):

    _name = "contract.line.change.product.variant"

    old_product_id = fields.Many2one("product.product", string="Previous membership")
    product_id = fields.Many2one(
        "product.product",
        domain="[('id', 'in', available_variants)]",
        string="New membership",
    )
    contract_line = fields.Many2one("contract.line", readonly=True)
    contract_id = fields.Many2one("contract.contract", readonly=True)
    available_variants = fields.Many2many("product.product")

    def change_product_variant(
        self, contract_id=None, new_product_id=None, contract_line=None
    ):
        """ This function creates a new contract line and a new invoice with
        appropriate values based on a chosen product and the old contract
        line. """

        contract = contract_id or self.contract_id
        contract_line = contract_line or self.contract_line
        product = new_product_id or self.product_id
        old_product = contract_line and contract_line.product_id
        now_date = datetime.now()
        recurring_date = contract_line.recurring_next_date or now_date.date()
        if contract_line.recurring_next_date < now_date.date():
            raise ValidationError(
                _(
                    "You cannot change a contract line '%s' membership after "
                    "Date of Next Invoice '%s'. Please create an invoice from "
                    "this contract line "
                )
                % (contract_line.name, contract_line.recurring_next_date)
            )

        new_line_price = 0
        old_line_price = 0

        # Get price for a product
        if contract.pricelist_id:
            new_line_price = contract.pricelist_id.get_product_price(
                product=product,
                quantity=contract_line.quantity,
                partner=contract.partner_id.id,
                date=now_date,
                uom_id=contract_line.uom_id.id,
            )

            old_line_price = contract.pricelist_id.get_product_price(
                product=old_product,
                quantity=contract_line.quantity,
                partner=contract.partner_id.id,
                date=now_date,
                uom_id=contract_line.uom_id.id,
            )

        # Check the price difference and set the new price for invoice line
        # to zero, if the difference is negative
        new_line_price = new_line_price - old_line_price
        new_line_price = 0 if new_line_price < 0 else new_line_price

        contract_line_values = {
            "product_id": product.id,
            "price_unit": product.lst_price,
            "name": product.display_name,
            "contract_id": contract.id,
            "recurring_next_date": recurring_date,
            "date_start": now_date,
            "uom_id": contract_line.uom_id.id,
            "recurring_interval": 1,
            "recurring_rule_type": "monthly",
        }

        # Create a new contract line
        new_contract_line = self.env["contract.line"].create(contract_line_values)

        # Create a new invoice with a new contract line information
        invoice_values = []
        date_ref = contract.recurring_next_date
        invoice_vals, move_form = contract._prepare_invoice(date_ref)
        account_move_line = new_contract_line._prepare_invoice_line(move_form=move_form)
        # Set invoice line's price as the difference between old contract
        # line's and new contract line's price based on contract's pricelist
        # rule.
        account_move_line["price_unit"] = new_line_price
        invoice_vals["invoice_line_ids"] = []
        invoice_vals["invoice_line_ids"].append((0, 0, account_move_line))
        invoice_values.append(invoice_vals)
        del invoice_vals["line_ids"]
        move_id = self.env["account.move"].sudo().create(invoice_values)
        contract._invoice_followers(move_id)
        contract._compute_recurring_next_date()

        # This line of code can cause errors, so check it first in case some
        # problems appear when using this module.
        new_contract_line._update_recurring_next_date()

        new_contract_line.last_date_invoiced = now_date

        # Stop a previous contract line
        if (
            contract_line.last_date_invoiced
            and now_date.date() >= contract_line.last_date_invoiced
            or not contract_line.last_date_invoiced
        ):
            stop_date = now_date.date()
        else:
            stop_date = contract_line.last_date_invoiced

        contract_line.stop(stop_date)

        return move_id
