.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================================
Substriction Line Change product variant
========================================

Opens up a wizard to choose a different product variant for subscription line.
Line values are changed according to the pricelist set on the subscription and
a new invoice is created with the price difference between the previous and
a new product variant.

Configuration
=============
Product template with different variants needs to exist to use this module
properly. Also it is good to have a pricelist that uses those variants,
because price differences are calculated based on that.

Usage
=====
On a subscription line click "Change Membership" button to open up a wizard.
Select a new product variant and click "Confirm". Check the new created invoice.

Known issues / Roadmap
======================
Track the changes on subscription lines from chatter.

Credits
=======

Contributors
------------

* Aleksi Savijoki <aleksi.savijoki@tawasta.fi>
* Jarmo Kortetjärvi <jarmo.kortetjarvi@tawasta.fi>
* Miika Nissi<miika.nissi@tawasta.fi>
* Timo Kekäläinen <timo.kekalainen@tawasta.fi>
* Valtteri Lattu <valtteri.lattu@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
