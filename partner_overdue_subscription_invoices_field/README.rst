.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================================
Subscription: Overdue Invoices Indicator Field for Partner
==========================================================

* New computed field for easy programmatic access to partners with 
  overdue subscription-related invoices
* The main use case is to combine this module with Futural `x_domain_filter` 
  modules, enabling to e.g. deny access to member-priced tickets for 
  those persons who have not yet paid their subscription invoice (but 
  the subscription has not yet been closed)
* A scheduled action checks for overdue invoices and flags partners 
  automatically. Status changes to invoice and its payments adjust 
  the flag also. 
* Note that the module depends on `subscription_line_partner`, i.e. this 
  module uses the subscription line's partner info for all its checks. 
  This is to support the use case where the person who has a subscription is 
  different from the one who gets the invoice. We want to identify the persons, 
  to e.g. be able to deny their user accounts access to the member-priced tickets.

  * i.e. a partner is considered having overdue invoices if they are listed 
    on a subscription line whose parent subscription has unpaid, overdue
    invoices linked to it.

Configuration
=============
* None needed

Usage
=====
* Create an subscription that is in progress, and create an invoice for it.
  Mark the invoice's due date to be in the past and confirm the invoice. The
  partner's 'Has Overdue Subscription Invoices?' field gets checked and is
  searchable/filterable.

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
