.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================================
Contract Invoice Address and force Commercial Partner
=====================================================

Add invoice address to contracts and assign its commercial partner to an invoice
if needed with a setting.

Configuration
=============
Go to Settings -> Invoicing and select "Force commercial partner on contracts"
to set commercial partner to an invoice to be created.

Usage
=====
Select a contract and test its invoice creation. Use "Force commercial partner
on contracts" setting to see that the invoice gets the commercial partner of
an invoice address of contract.

The invoice partner is the contract's invoice address. If it is empty, the
invoice-type address of the customer (``invoice_partner_id``) is used, and
finally the customer. With the "Force commercial partner on contracts" setting
the commercial partner is used whenever the selected invoice partner is not an
invoice-type address, also when the contract has no separate invoice address.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>
* Miika Nissi <miika.nissi@futural.fi>
* Timo Kekäläinen <timo.kekalainen@futural.fi>
* Joona Isoaho <joona.isoaho@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
