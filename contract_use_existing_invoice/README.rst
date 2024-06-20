.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================================================
Contract: use an existing invoice when creating recurring invoices
==================================================================

Add lines to an existing invoice instead of creating a new invoice.

Warning! This will overwrite _recurring_create_invoice(), which will cause any module overriding the same
method stop working correctly.

The logic for finding an existing invoice:

- If there is an open invoice related to this contract, use that
- If not, try to find any open invoice for this partner with empty or matching customer reference


Configuration
=============
\-

Usage
=====
\-

Bug Tracker
===========
Bugs are tracked on `GitHub Issues
<https://github.com/tawasta/contract/issues>`_.

Credits
=======

Contributors
------------

* Jarmo Kortetjärvi <jarmo.kortetjarvi@tawasta.fi>
* Timo Kekäläinen <timo.kekalainen@tawasta.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
