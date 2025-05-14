.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Subscription: Invite Others
===========================

This module adds functionality to send email invitations related to `sale.subscription.line` records.

It allows portal users and internal users to invite external users via email to join a subscription, such as events, SaaS products, or service contracts.

Key Features
============

- Invite users to a specific subscription line by email.
- Both backend (admin) and portal (frontend) views are supported.
- Invitation emails include a secure token link to accept.
- Email verification with "Confirm Email" field.
- Prevents re-inviting the same address unintentionally.
- Tracks invitation status and acceptance date.
- Fully translatable strings (invitation status, messages).
- Configuration to enable/disable invitations per product.


Configuration
=============
1. Ensure your products have the **"Allow Subscription Invitations"** field enabled (`Product Template` form view).
2. Configure the **Email Template** if needed (`subscription_invitation_email_template`).


Usage
=====

Backend (Administrator):
------------------------

- Go to a Subscription record.
- In the **Subscription Lines** tab, click the 📧 *Invite* button on a line.
- Fill out both email fields and click "Send Invitation".

Portal (Website User):
----------------------

- Go to *My Subscriptions*.
- Click the 📧 *Send Invitation* button on a line that allows invites.
- Confirm the recipient's email and send.
- A badge shows whether the invitation has been sent or accepted.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@tawasta.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
