
from odoo import fields, models


class ContractLineChangeProductVariant(models.TransientModel):

    _name = 'contract.line.change.product.variant'

    old_product_id = fields.Many2one('product.product', string="Previous membership")
    product_id = fields.Many2one('product.product',
        domain="[('id', 'in', available_variants)]",
        string="New membership"
    )
    contract_line = fields.Many2one('contract.line', readonly=True)
    contract_id = fields.Many2one('contract.contract', readonly=True)
    available_variants = fields.Many2many('product.product')

    def change_product_variant(self):
        self.ensure_one()
        contract = self.contract_id
        recurring_date = contract.recurring_next_date or fields.Datetime.now().date()

        contract_line_values = {
            'product_id': self.product_id.id,
            'price_unit': self.product_id.list_price,
            'name': self.product_id.display_name,
            'contract_id': contract.id,
            'recurring_next_date': recurring_date,
            'date_start': contract.recurring_next_date,
            'uom_id': self.contract_line.uom_id.id,
        }

        # Create a new contract line
        new_contract_line = self.env['contract.line'].create(contract_line_values)

        # Create a new invoice with a new contract line information
        invoice_values = []
        date_ref = contract.recurring_next_date
        invoice_vals, move_form = contract._prepare_invoice(date_ref)
        account_move_line = new_contract_line._prepare_invoice_line(
            move_form=move_form)
        invoice_vals["invoice_line_ids"] = []
        invoice_vals["invoice_line_ids"].append((0, 0, account_move_line))
        invoice_values.append(invoice_vals)
        del invoice_vals["line_ids"]
        new_contract_line._update_recurring_next_date()
        move_id = self.env['account.move'].create(invoice_values)
        contract._invoice_followers(move_id)
        contract._compute_recurring_next_date()

        # Stop a previous contract line
        stop_date = self.contract_line.last_date_invoiced or \
                    fields.Datetime.now().date()
        self.contract_line.recurring_next_date = stop_date
        self.contract_line.cancel()

        return move_id
