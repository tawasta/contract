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
- Choose Person or Company in a segmented control to reveal the correct form
  fields; the chosen option is raised and bold
- The contacts are selectable cards: the selected card gets a ring and a check
  mark. With the keyboard Enter or Space selects a card and the arrow keys
  move the selection. When the current invoice address is shown, its card
  starts selected
- The selections are drawn with the website theme's text and background
  colours, never with its primary or secondary colour, so they stay clear and
  readable whatever colours a website theme has
- Filter invoice transmit methods according to `contract_target_type`:
  - Person
  - Company
  - Both
- Handles specific logic for eInvoice and OCR methods
- Automatically updates the subscription's `partner_id`
- Optionally marks the invoice address currently used by the subscription
- Optionally lets the user edit their existing invoice addresses with the
  same restrictions as the checkout: the name cannot be changed once
  invoices or confirmed orders exist for the address, the name and email of
  another user's account cannot be changed, and an email that follows the
  username cannot be changed. Saving an edited address also sets it as the
  invoice address of the subscription
- The Business ID is validated in the same way as in the checkout
- The selection lists the contacts around the current invoice address of
  the subscription, of any type. Only these can be selected, and only for a
  subscription billed to the user's own contacts
- Of the listed contacts, the user's own contact and the invoice and other
  addresses can be edited, as in the checkout
- While saving, the save button shows the progress and cannot be clicked
  twice; errors are shown in a dialog

Configuration
=============

Go to **Website > Configuration > Settings** and, under **Subscriptions**,
enable the features you need. Both are off by default, so an existing
installation works as before:

- **Show current invoice address**: the address currently used by the
  subscription is shown first in the address selection with the label
  "In use", and the cards show the full address.
- **Allow editing invoice addresses**: the user's own contact and their
  invoice addresses get an "Edit address" button that opens the address
  form filled in.

To fully utilize the filtering logic, ensure that your `transmit.method` records
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
   - Edit an existing address with "Edit address", when enabled, **OR**
   - Add a new one by choosing "Person" or "Company" and filling out the form.
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
