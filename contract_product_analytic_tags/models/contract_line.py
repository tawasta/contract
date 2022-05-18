##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
from odoo import api, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ContractLine(models.Model):

    # 1. Private attributes
    _inherit = "contract.line"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.onchange("product_id")
    def onchange_product_id_update_analytic_tags(self):
        for rec in self:
            if rec.product_id and rec.product_id.get_analytic_tags():
                rec.analytic_tag_ids += rec.product_id.get_analytic_tags()

    @api.model
    def create(self, vals):
        if "analytic_tag_ids" not in vals:
            product_id = vals.get("product_id")
            product = self.env["product.product"].browse([product_id])
            vals["analytic_tag_ids"] = [(6, 0, product.analytic_tag_ids.ids)]

        return super(ContractLine, self).create(vals)

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
