##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models, api
import logging

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ResPartner(models.Model):
    # 1. Private attributes
    _inherit = "res.partner"

    # 2. Fields declaration
    contract_lines = fields.One2many(comodel_name="contract.line", inverse_name='partner_id', string='Contract lines')

    contract_start = fields.Date(compute='_compute_contract_state', # OTETAANKIN HEADERISTA
        string ='Contract Start Date', store=True,
        help="Date from which contract becomes active.")

    contract_stop = fields.Date(compute='_compute_contract_state', # OTETAANKIN HEADERISTA
        string ='Contract End Date', store=True,
        help="Date until which contract remains active.")

    contract_line_company_ids = fields.Many2many()
    #Many2many otetaan yritykset tuotteen takaa

    contract_line_product_ids = fields.Many2many(
        comodel_name='product.product',
        compute='_compute_contract_line_product_ids',
        string='Products',
        store=True,
    )

    contract_line_company_ids = fields.Many2many(
        comodel_name='res.company',
        compute='_compute_contract_line_company_ids',
        string='Companies',
        store=True,
    )

    @api.depends('contract_lines','contract_lines.product_id.company_id', 'contract_lines.product_id.product_tmpl_id.company_id')
    def _compute_contract_line_company_ids(self):
        for partner in self:
            companies = self.env['res.company']
            for contract_line in partner.contract_lines:
                # Add the company from the product of each contract line to the recordset
                if contract_line.product_id.company_id:
                    companies |= contract_line.product_id.company_id
                
                # Also add the company from the product template of each contract line to the recordset
                if contract_line.product_id.product_tmpl_id.company_id:
                    companies |= contract_line.product_id.product_tmpl_id.company_id

            partner.contract_line_company_ids = companies

    @api.depends('contract_lines','contract_lines.product_id')
    def _compute_contract_line_product_ids(self):
        for partner in self:
            products = self.env['product.product']
            # Iterate over all contract lines related to the partner
            for contract_line in partner.contract_lines:
                # Add the product from each contract line to the recordset
                products |= contract_line.product_id

            partner.contract_line_product_ids = products


    @api.depends('contract_lines',)
    def _compute_contract_state(self):
        today = fields.Date.today()
        for partner in self:
            logging.info("==");
            partner.contract_start = self.env['contract.contract'].search([
                ('partner_id', '=', partner.id)
            ], limit=1, order='date_start').date_start
            partner.contract_stop = self.env['contract.contract'].search([
                ('partner_id', '=', partner.id)
            ], limit=1, order='date_end desc').date_end

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
