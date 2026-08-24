.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================================
Use Recipient Bank on Contract and its Invoices
===============================================

Add a required field, Recipient Bank, to a contract. Recurring created
invoices inherit recipient bank from the contract.

Configuration
=============
Contracts and invoices are being used by this module.

Usage
=====
Create a contract and define Recipient bank to it. Then create recurring
invoices to inherit Recipient bank from the contract.

Known issues / Roadmap
======================
Note from TimoK: I decided to set the technical field name as partner_bank_id
for possible later use. Other 3rd party modules might use the same techincal
field name, but hopefully this only helps, because the field definition can
then be removed from this module if this will not create any issues.

Credits
=======

Contributors
------------

* Timo Kekäläinen <timo.kekalainen@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
