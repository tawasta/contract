from odoo import api, models


class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @api.model
    def _split_semicolon_parts(self, text):
        """Split by ';', trim, drop empties."""
        if not text:
            return []
        parts = [p.strip() for p in text.split(";")]
        return [p for p in parts if p]

    @api.model
    def _strip_partner_suffix(self, part, partner_name):
        """
        Remove trailing ', <partner_name>' from part if present.

        Example:
        'Säätiö - JCI Finland Foundation, Testi Kayttaja'
        -> 'Säätiö - JCI Finland Foundation'
        """
        part = (part or "").strip()
        partner_name = (partner_name or "").strip()
        if not part or not partner_name:
            return part

        part_low = part.lower()

        suffix = (", " + partner_name).lower()
        if part_low.endswith(suffix):
            return part[: -len(", " + partner_name)].strip()

        suffix2 = ("," + partner_name).lower()
        if part_low.endswith(suffix2):
            return part[: -len("," + partner_name)].strip()

        return part

    @api.model
    def _get_or_create_product_for_part(self, name):
        """
        Return product.product for given name.
        Avoid duplicates by searching product.template by exact name.
        """
        name = (name or "").strip()
        if not name:
            return False

        Template = self.env["product.template"].sudo()

        tmpl = Template.search([("name", "=", name)], limit=1)
        if tmpl:
            return tmpl.product_variant_id

        tmpl = Template.create(
            {
                "name": name,
                "type": "service",
                "subscribable": True,
            }
        )
        return tmpl.product_variant_id

    # -------------------------------------------------------------------------
    # Cron
    # -------------------------------------------------------------------------

    @api.model
    def cron_split_lines_by_semicolon(self, limit=500, line_id=None):
        """
        Cron job:
        - If line_id is provided: process ONLY that line (if it contains ';')
        - Otherwise: find subscription lines where name contains ';' (up to limit)

        Process logic:
        - Split name into parts
        - Keep original line for first part, create copies for remaining parts
        - Description (line.name) keeps full part text
        - Product name strips ', Partner' if present
        - Attach existing product or create new (no duplicates by name)
        """
        Line = self.sudo()

        # If a specific line_id is provided -> process only that line
        if line_id:
            line = Line.browse(int(line_id))
            if not line.exists():
                return True  # nothing to do

            # Only process if it really has ';'
            if not line.name or ";" not in line.name:
                return True

            lines = line
        else:
            lines = Line.search(
                [("name", "ilike", "%;%")],
                limit=limit,
                order="id asc",
            )

        for line in lines:
            original_name = (line.name or "").strip()
            parts = self._split_semicolon_parts(original_name)
            if len(parts) < 2:
                continue

            partner_name = line.sale_subscription_id.partner_id.name or ""
            taxes_ids = line.tax_ids.ids

            # Create copies so total lines == number of parts
            copies = []
            for _ in range(len(parts) - 1):
                copies.append(line.copy(default={}))

            target_lines = [line] + copies

            for target_line, part in zip(target_lines, parts):  # NOQA: B905
                description = part
                product_name = self._strip_partner_suffix(part, partner_name)

                product = self._get_or_create_product_for_part(product_name)

                vals = {
                    "name": description,
                    "product_id": product.id if product else False,
                    "tax_ids": [(6, 0, taxes_ids)],
                }

                # If you want copies to be non-billing lines, uncomment:
                # if target_line.id != line.id:
                #     vals.update({"price_unit": 0.0, "discount": 0.0})

                target_line.write(vals)

        return True
