.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Sale Subscription Line Split
============================

Adds the ability to split subscription lines by quantity based on a setting on the product.

When a sale order is confirmed and a subscription is generated, products marked with
"Split Subscription Lines by Quantity" will create one subscription line per unit,
instead of a single line with a higher quantity.

Configuration
=============
- Go to **Sales > Products > Product Templates**
- Enable the checkbox **Split Subscription Lines by Quantity**
- Ensure the product is also marked as **Subscribable** and has a **Subscription Template**

Usage
=====
1. Create a Sale Order with a subscribable product that has "Split Subscription Lines by Quantity" enabled
2. Set quantity greater than 1
3. Confirm the Sale Order
4. A subscription will be created with one line per unit ordered

Example:
- Product A has the option enabled
- Sale order contains 5 units of Product A
- Result: 5 subscription lines, each with quantity = 1

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
