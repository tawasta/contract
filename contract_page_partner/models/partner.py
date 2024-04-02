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

import logging

# 3. Odoo imports (openerp):
from odoo import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ResPartner(models.Model):
    # 1. Private attributes
    _inherit = "res.partner"

    # 2. Fields declaration
    contract_lines = fields.One2many(
        comodel_name="contract.line", inverse_name="partner_id", string="Contract lines"
    )

    contract_start = fields.Date(
        compute="_compute_contract_state",
        string="Contract Start Date",
        store=True,
        help="Date from which contract becomes active.",
    )

    contract_stop = fields.Date(
        compute="_compute_contract_state",
        string="Contract End Date",
        store=True,
        help="Date until which contract remains active.",
    )

    contract_line_company_ids = fields.Many2many()
    # Many2many otetaan yritykset tuotteen takaa

    contract_line_product_ids = fields.Many2many(
        comodel_name="product.product",
        compute="_compute_contract_line_product_ids",
        string="Products",
        store=True,
    )

    contract_line_company_ids = fields.Many2many(
        comodel_name="res.company",
        compute="_compute_contract_line_company_ids",
        string="Companies",
        store=True,
    )

    @api.depends(
        "contract_lines",
        "contract_lines.contract_id.date_end",
        "contract_lines.product_id.variant_company_id",
        "contract_lines.product_id.product_tmpl_id.company_id",
    )
    def _compute_contract_line_company_ids(self):
        today = date.today()
        partners_with_lines = self.filtered(lambda p: p.contract_lines)
        for partner in partners_with_lines:
            # Filtteröi vain voimassa olevat sopimuslinjat
            valid_contract_lines = partner.contract_lines.filtered(
                lambda cl: cl.contract_id.date_end and cl.contract_id.date_end >= today
            )

            # Jos on voimassa olevia sopimuslinjoja
            if valid_contract_lines:
                # Kerää yhtiöt tuotteista ja tuotemalleista
                companies_from_products = valid_contract_lines.mapped(
                    "product_id.variant_company_id"
                ).filtered(lambda c: c)  # Varmista, että company_id on asetettu
                companies_from_templates = valid_contract_lines.mapped(
                    "product_id.product_tmpl_id.company_id"
                ).filtered(lambda c: c)  # Varmista, että company_id on asetettu

                # Yhdistä yhtiöiden joukot ja määritä partnerille
                partner.contract_line_company_ids = (
                    companies_from_products | companies_from_templates
                )
            else:
                # Jos ei löydy voimassa olevia sopimuslinjoja, tyhjennä kenttä
                partner.contract_line_company_ids = False

    @api.depends(
        "contract_lines",
        "contract_lines.product_id",
        "contract_lines.contract_id.date_end"
    )
    def _compute_contract_line_product_ids(self):
        today = date.today()
        for partner in self.filtered(lambda p: p.contract_lines):
            # Filtteröi vain voimassa olevat sopimuslinjat
            valid_contract_lines = partner.contract_lines.filtered(
                lambda line: line.contract_id.date_end and line.contract_id.date_end >= today
            )
            # Määritetään partnerin tuote-ID:t voimassa olevien sopimuslinjojen perusteella
            partner.contract_line_product_ids = valid_contract_lines.mapped("product_id")


    @api.depends(
        "contract_lines",
    )
    def _compute_contract_state(self):
        fields.Date.today()
        # Filter partners with contract_lines
        partners_with_lines = self.filtered(lambda p: p.contract_lines)
        for partner in partners_with_lines:
            logging.info("==")
            partner.contract_start = (
                self.env["contract.contract"]
                .search([("partner_id", "=", partner.id)], limit=1, order="date_start")
                .date_start
            )
            partner.contract_stop = (
                self.env["contract.contract"]
                .search(
                    [("partner_id", "=", partner.id)], limit=1, order="date_end desc"
                )
                .date_end
            )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
