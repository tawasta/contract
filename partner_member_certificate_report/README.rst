.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================================
Subscriptions: Partner Member Certificate Report
================================================

* Adds a certificate report PDF for partners, containing
  the partner's active subscriptions.
* Use case: members need a PDF proving that they have an ongoing membership,
  no matter which one it is. In addition, some of the ongoing membership 
  products need to be listed on the PDF report.

Configuration
=============
* Go to company settings to configure

  * Which subscribable products should shown on the report, if the partner
    has an active subscription for them.
  * Signature/signer information
  * Report HTML contents (main title and main contents)
  * Whether printing also via portal by the member themselves is allowed

* Also needs basic company information (logo, name, address etc.) to be filled.
* Note that this functionality is based on OCA's module `subscription_oca`

Usage
=====
* Print the report from Contact form, and if portal printing is allowed, from 
  portal's sidebar in `/my` page.

Known issues / Roadmap
======================
* Possible layout tweaks still needed if there are many subscriptions 
  shown on the PDF
* Portal user is currently allowed to print the PDF if they have 
  an ongoing subscription to whatever subscribable product. 
  A limiting configuration for this may be useful for other use cases
  so that only certain subscribable products grant this right.

Credits
=======

Contributors
------------
* Joonas Lahtinen <joonas.lahtinen@futural.fi>
* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
