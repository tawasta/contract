.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Website subscription edit partner
=================================

This module adds functionality to edit the partner associated with a subscription
directly through the website portal.

It allows portal users to:
- Select an existing contact as invoice partner
- Add a new contact (person or company)
- Dynamically filter "Invoice Transmit Method" options based on contact type
- Add EDI and operator info for eInvoice methods
- Update the subscription's invoice partner accordingly

Features
========

- Portal users can view and manage their subscription partner details
- Add new contact with fields: name, address, email, phone
- Toggle between person/company to reveal the correct form fields
- Filter invoice transmit methods according to `contract_target_type`:
  - Person
  - Company
  - Both
- Handles specific logic for eInvoice and OCR methods
- Automatically updates the subscription's `partner_id`

Configuration
=============

No specific configuration is required after installation.

However, to fully utilize the filtering logic, ensure that your `transmit.method` records
have the `contract_target_type` field set accordingly:
- `person`: for private individuals
- `company`: for business contacts
- `both`: visible to all

Usage
=====

1. Go to the **Customer Portal** and open any active subscription.
2. Click the **Edit** button under the Customer Information section.
3. In the modal window:
   - Select an existing contact **OR**
   - Add a new one by toggling "Person / Company" and filling out the form.
4. Transmit method options are filtered based on type.
5. Submit the form to update the partner for the subscription.

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

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
