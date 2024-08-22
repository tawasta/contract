##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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
    "name": "Website Subscriptions",
    "summary": "Subscriptions in website portal",
    "version": "17.0.1.0.0",
    "category": "Contract",
    "website": "https://gitlab.com/tawasta/odoo/contract",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "portal",
        "subscription_oca",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/subscription_portal_my.xml",
        "views/subscription_portal_page.xml",
        "views/subscription_portal_template_home.xml",
        "views/subscription_portal_template_menu.xml",
    ],
    # "assets": {
    #     "web.assets_frontend": [
    #         "website_subscription/static/src/js/main.esm.js",
    #     ],
    # },
}