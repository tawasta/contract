##############################################################################
#
#    Author: Futural Oy
#    Copyright 2021- Futural Oy (https://futural.fi)
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
    "version": "17.0.1.2.2",
    "category": "Contract",
    "website": "https://github.com/tawasta/contract",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "portal",
        "subscription_closing",
        "subscription_oca",
        "subscription_line_closing",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rules.xml",
        "views/subscription_portal_my.xml",
        "views/subscription_portal_page.xml",
        "views/subscription_portal_page_modals.xml",
        "views/subscription_portal_template_home.xml",
        "views/subscription_portal_template_menu.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_subscription/static/src/js/main.esm.js",
        ],
    },
}
