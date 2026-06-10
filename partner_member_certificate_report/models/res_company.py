from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    member_certificate_title_content = fields.Html(
        string="Member Certificate: Title Content",
        translate=True,
        default="<h2>Certificate of membership</h2>",
        help="Main title on the membership certificate, shown just below the logo",
    )

    member_certificate_main_content = fields.Html(
        string="Member Certificate: Main Content",
        translate=True,
        default="<p>We hereby state that the aforementioned is currently a "
        "member of our organization.</p>",
        help="Main text paragraph on the membership certificate, shown just below the "
        "person's name.",
    )

    member_certificate_products_subheading_content = fields.Html(
        string="Member Certificate: Subheading Before Subscribable Products",
        translate=True,
        default="<p>Active subscriptions:</p>",
        help="Subheading shown on the membership certificate, just above the list of"
        "subscribable products. This subheading is left out, if there are no "
        "matching subscribable products shown.",
    )

    member_certificate_shown_subscription_product_ids = fields.Many2many(
        comodel_name="product.template",
        domain=[("subscribable", "=", True)],
        string="Member Certificate: Shown Subscription Products",
        help="Subscribable products listed under the main content on the "
        "membership certificate, if the person has a matching membership for them.",
    )

    member_certificate_allow_portal_printing = fields.Boolean(
        string="Member Certificate: Allow Printing from Portal",
        help="If enabled, members can print their own membership certificate "
        "from the customer portal.",
    )

    member_certificate_signature = fields.Image(
        string="Member certificate: Signature Image",
        max_width=1024,
        max_height=1024,
    )
    member_certificate_signatory_name = fields.Char(
        string="Member certificate: Signatory Name",
    )
    member_certificate_signatory_title = fields.Char(
        string="Member Certificate: Signatory Title", translate=True
    )
    member_certificate_signatory_place = fields.Char(
        string="Member Certificate: Signatory Place", translate=True
    )

    footer_company_definition = fields.Text(
        string="Member Certificate: Custom Text for Footer",
        translate=True,
        help="Custom text to show on the footer's top-left column.",
    )
