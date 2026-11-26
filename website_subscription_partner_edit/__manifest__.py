##############################################################################
#
#    Author: Futural Oy
#    Copyright 2024 Futural Oy (https://futural.fi)
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
    "name": "Website subscription edit partner",
    "summary": "Website subscription edit partner",
    "version": "17.0.1.1.1",
    "category": "contract",
    "website": "https://github.com/tawasta/contract",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website",
        "website_subscription",
        "account_invoice_transmit_method",
        "website_sale_invoice_transmit_method",
        "partner_firstname",
        "l10n_fi_edicode",
        "l10n_fi_company_registry",
    ],
    "data": [
        "views/res_config_settings_views.xml",
        "views/templates.xml",
        "views/transmit_method.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_subscription_partner_edit/static/src/js/main.esm.js",
            "website_subscription_partner_edit/static/src/scss/contact_selection.scss",
        ],
    },
}
