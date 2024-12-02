.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
Subscription user default
=========================

* This module sets a default user (user_id) for Subscription models whenever a new subscription is created. If no default user is configured in system settings, the module falls back to Odoo's core logic.

Configuration
=============
* Navigate to Settings > Technical > System Parameters.
* Add (or edit) the parameter key: sale_subscription.default_user_id.
* Set the value to the ID of an existing user.

Usage
=====
\-

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
