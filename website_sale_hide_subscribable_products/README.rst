.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================
Website Sale Hide Subscribable Products
=======================================

This module hides products marked as *subscribable* from the webshop
(`website_sale`).

Products that have the field ``subscribable = True`` will not be shown
in the website shop or product listings.

This is useful when subscription-based products are managed separately
(e.g. via subscription flows) and should not be directly purchasable
from the standard webshop.

Configuration
=============
No configuration is required.

Make sure that the module providing the ``subscribable`` field on
products is installed.

Usage
=====
1. Go to *Products*.
2. Mark a product as *Subscribable product*.
3. The product will automatically be hidden from the webshop.

To make a product visible again, simply uncheck the *Subscribable product*
flag.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
