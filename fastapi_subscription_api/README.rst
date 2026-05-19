.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================
Subscription API with FastAPI
=============================

* The module adds REST API endpoints for subscription-related integrations using FastAPI.
* Currently the only endpoint is:

  * Check if a partner has an ongoing subscription for one or more of configured products.
    Checking is done based on comparing supplied member ID against partner's ref field.
    Intended for situations where an external system verifies from Odoo if a specific
    person has an ongoing subscription or not.

Configuration
=============
* Authentication is handled via API keys (``auth.api.key``)
* API keys must belong to the *FastAPI Subscription API Group* group
* Go through the subscribable products and set the new 
  'API Check: Count as Having an Active Subscription' field where applicable.
  Only those subscribable products are taken into account when checking what 
  ongoing subscriptions a person has.

Usage
=====

Available endpoints:

**GET /subscription_api/members/<MEMBER-ID>/subscription_status**

* Returns boolean indicating if there is an ongoing subscription or not
* CURL call example:

  * curl -H "http-api-key: myexamplekey" "http://myodooinstallation.com/subscription_api/members/12345/subscription_status"


Known issues / Roadmap
======================
* Consider supporting checking for different types of memberships separately
  of each other (e.g. student member, honorary member...).


Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
