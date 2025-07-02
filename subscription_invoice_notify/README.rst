.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Subscription Invoice Notify
===========================

This Odoo module extends the subscription management by sending an email notification to the responsible user whenever a new invoice is generated for a subscription. The notification email includes details about the latest invoice linked to the subscription.

Features
========

- Automatically sends email notification when a new invoice is created.
- Email is sent to the subscription's responsible user.
- Email includes a direct link to view the latest invoice in Odoo.
- Uses the subscription's `invoice_ids` One2many field to fetch the latest invoice, ensuring reliability.


Configuration
=============
No additional configuration is necessary. The module works out of the box once installed.

Usage
=====

When an invoice is generated for a subscription (via the standard `generate_invoice` method), the module sends an email notification to the responsible user associated with the subscription. The email template used is `subscription_invoice_notify.mail_template_invoice_notify_responsible`.

Email content includes:
- Subscription name
- Latest invoice details (customer, amount, and a direct link to the invoice form view)

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
