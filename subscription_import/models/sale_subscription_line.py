import logging

from odoo import api, models


_logger = logging.getLogger(__name__)


class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @api.model
    def _split_semicolon_parts(self, text):
        """Split by ';', trim, drop empties."""
        if not text:
            _logger.info("cron_split: Split empty text -> []")
            return []
        parts = [p.strip() for p in text.split(";")]
        result = [p for p in parts if p]
        _logger.info("cron_split: Split '%s' -> %s", text, result)
        return result

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
            stripped = part[: -len(", " + partner_name)].strip()
            _logger.info(
                "cron_split: Strip partner suffix '%s' - '%s' -> '%s'",
                part,
                partner_name,
                stripped,
            )
            return stripped

        suffix2 = ("," + partner_name).lower()
        if part_low.endswith(suffix2):
            stripped = part[: -len("," + partner_name)].strip()
            _logger.info(
                "cron_split: Strip partner suffix '%s' - '%s' -> '%s'",
                part,
                partner_name,
                stripped,
            )
            return stripped

        return part

    @api.model
    def _get_or_create_product_for_part(self, name):
        """
        Return product.product for given name.
        Avoid duplicates by searching product.template by exact name.
        """
        name = (name or "").strip()
        if not name:
            _logger.info("cron_split: Product name empty -> skip product creation")
            return False

        Template = self.env["product.template"].sudo()

        tmpl = Template.search([("name", "=", name)], limit=1)
        if tmpl:
            _logger.info(
                "cron_split: Product exists: '%s' (template_id=%s, variant_id=%s)",
                name,
                tmpl.id,
                tmpl.product_variant_id.id,
            )
            return tmpl.product_variant_id

        tmpl = Template.create(
            {
                "name": name,
                "type": "service",
                "subscribable": True,
            }
        )
        _logger.info(
            "cron_split: Product created: '%s' (template_id=%s, variant_id=%s)",
            name,
            tmpl.id,
            tmpl.product_variant_id.id,
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

        Safety:
        - Ensure subscription has company_id set,
        - taking it from the existing line (line.company_id).
        - This prevents OCA compute crash: company.ensure_one().
        """
        Line = self.sudo()

        _logger.info(
            "cron_split: START limit=%s line_id=%s",
            limit,
            line_id,
        )

        # If a specific line_id is provided -> process only that line
        if line_id:
            line = Line.browse(int(line_id))
            if not line.exists():
                _logger.info("cron_split: line_id=%s not found -> nothing to do", line_id)
                return True  # nothing to do

            # Only process if it really has ';'
            if not line.name or ";" not in line.name:
                _logger.info(
                    "cron_split: line_id=%s has no ';' in name ('%s') -> skip",
                    line_id,
                    line.name,
                )
                return True

            lines = line
            _logger.info(
                "cron_split: processing single line id=%s name='%s'",
                line.id,
                line.name,
            )
        else:
            lines = Line.search(
                [("name", "ilike", "%;%")],
                limit=limit,
                order="id asc",
            )
            _logger.info("cron_split: found %s lines matching ';'", len(lines))

        processed = 0
        skipped = 0
        created_copies = 0
        updated_lines = 0

        for line in lines:
            processed += 1

            subscription = line.sale_subscription_id
            if not subscription:
                skipped += 1
                _logger.info(
                    "cron_split: SKIP line_id=%s (no sale_subscription_id) name='%s'",
                    line.id,
                    line.name,
                )
                continue

            _logger.info(
                "cron_split: LINE line_id=%s sub_id=%s partner='%s' line_company_id=%s sub_company_id=%s name='%s'",
                line.id,
                subscription.id,
                subscription.partner_id.name or "",
                line.company_id.id if line.company_id else None,
                subscription.company_id.id if subscription.company_id else None,
                line.name or "",
            )

            # ---- FIX: take company from existing line
            target_company = line.company_id or subscription.company_id or self.env.company
            if not subscription.company_id and target_company:
                subscription.write({"company_id": target_company.id})
                _logger.info(
                    "cron_split: set subscription.company_id -> %s (sub_id=%s)",
                    target_company.id,
                    subscription.id,
                )

            # ---- normal processing
            original_name = (line.name or "").strip()
            parts = self._split_semicolon_parts(original_name)
            if len(parts) < 2:
                skipped += 1
                _logger.info(
                    "cron_split: SKIP line_id=%s parts=%s (<2) original='%s'",
                    line.id,
                    parts,
                    original_name,
                )
                continue

            partner_name = subscription.partner_id.name or ""
            taxes_ids = line.tax_ids.ids

            _logger.info(
                "cron_split: splitting line_id=%s into %s parts, taxes=%s partner='%s'",
                line.id,
                len(parts),
                taxes_ids,
                partner_name,
            )

            # Create copies so total lines == number of parts
            copies = []
            for i in range(len(parts) - 1):
                new_line = line.copy(default={})
                copies.append(new_line)
                created_copies += 1
                _logger.info(
                    "cron_split: created copy %s/%s -> new_line_id=%s from original_line_id=%s",
                    i + 1,
                    len(parts) - 1,
                    new_line.id,
                    line.id,
                )

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

                _logger.info(
                    "cron_split: write line_id=%s (orig_line_id=%s) desc='%s' product_name='%s' product_id=%s taxes=%s",
                    target_line.id,
                    line.id,
                    description,
                    product_name,
                    product.id if product else None,
                    taxes_ids,
                )

                target_line.write(vals)
                updated_lines += 1

        _logger.info(
            "cron_split: END processed=%s skipped=%s created_copies=%s updated_lines=%s",
            processed,
            skipped,
            created_copies,
            updated_lines,
        )
        return True
