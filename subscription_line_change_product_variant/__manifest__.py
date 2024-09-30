##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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

{
    "name": "Substriction Line Change product variant",
    "summary": "Substriction Line Change product variant and create invoice",
    "version": "17.0.1.0.0",
    "category": "Contract Management",
    "website": "https://gitlab.com/tawasta/odoo/contract",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
        "subscription_oca",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_subscription_view.xml",
        "wizards/subscription_line_change_product_variant.xml",
    ],
}
