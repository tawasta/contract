.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================================
Website Subscription: Customer reference
========================================

* Shows the customer reference of a subscription on its portal page, below
  the invoice address.
* The customer can edit the reference in a dialog. The reference cannot be
  emptied and is at most 70 characters, the length that a Finvoice e-invoice
  carries.
* Only the customer of the subscription can edit it: the subscription must be
  billed to the user's own company or one of its addresses. Followers of the
  subscription see the reference but cannot change it.
* Changes are tracked in the chatter of the subscription in the name of the
  user who made them.

Configuration
=============
\-

Usage
=====
* Go to the portal, open a subscription and use the Edit button next to
  Customer reference.
* The new reference is used on the invoices created after the change. An
  invoice that is already in draft keeps its reference.

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
