.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================================================================
Subscription: 'Products in Currently Ongoing Subscription Lines' Field for Partner
==================================================================================

* New computed field for easy programmatic access to partners' 
  subscribable products that are currenly a part of an ongoing
  subscription.
* The main use case is to combine this module with Futural `x_domain_filter` 
  modules, enabling to e.g. grant access to member-priced tickets only for 
  those persons with a specific type of subscripion ongoing (regular, 
  pensioner, student...)
* The field contents get recomputed automatically when subscription lines or their
  parent subscriptions' stage change
* Note that the module depends on `subscription_line_partner`, i.e. this 
  module uses the subscription line's partner info for all its checks. 
  This is to support the use case where the person who has a subscription is 
  different from the one who gets the invoice. We want to identify the persons, 
  to e.g. be able to deny their user accounts access to the member-priced tickets.
* Secondary optional feature: a "Currently Subscribed Products" notebook page on the contact form listing
  the products, with a shortcut to the subscription line list view filtered to
  the contact

Configuration
=============
* The visibility of the "Currently Subscribed Products" page can be toggled in
  Settings -> General Settings -> Contacts. The page is shown by default.

Usage
=====
* Create a subscription with lines for a contact and start it. The products
  appear on the contact's "Currently Subscribed Products" page and in the
  ``subscribable_product_ids_in_progress`` field. Closing the subscription
  removes them.

Known issues / Roadmap
======================
* None

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
