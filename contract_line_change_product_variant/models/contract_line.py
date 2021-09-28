
from odoo import fields, models


class ContractLine(models.Model):

    _inherit = 'contract.line'

    def change_product_variant_wizard(self):
        product = self.product_id
        contract_line = self.id
        contract_id = self.contract_id.id
        available_variants = product.product_tmpl_id.product_variant_ids
        view_id = self.env.ref(
            'contract_line_change_product_variant.'
            'contract_line_change_product_variant_wizard').id
        wiz = self.env['contract.line.change.product.variant'].sudo().create({
            'old_product_id': product.id,
            'product_id': product.id,
            'contract_line': contract_line,
            'contract_id': contract_id,
            'available_variants': available_variants,
        })

        return {
            'name': 'Change member product',
            'view_mode': 'form',
            'res_model': 'contract.line.change.product.variant',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': wiz.id,
            'target': 'new',
        }
