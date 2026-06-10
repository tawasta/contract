##############################################################################
#
#    Author: Futural Oy
#    Copyright 2026 Futural Oy (https://futural.fi)
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
    "name": "Partner member certificate report",
    "summary": "Partner member certificate report",
    "version": "17.0.1.0.1",
    "category": "Partner Management",
    "website": "https://github.com/tawasta/contract",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": [
        "contacts",
        "web",
        "sale",
        "subscription_oca",
        "subscription_line_partner",
    ],
    "data": [
        "reports/signature_company.xml",
        "reports/paperformat.xml",
        "reports/report_template.xml",
        "reports/report.xml",
        "views/res_partner_views.xml",
    ],
    "demo": [],
}
