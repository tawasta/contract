from odoo import models, fields, api, exceptions
import base64
import csv
import re
import io
import logging
from odoo.tools.translate import _

class FileUploadWizard(models.TransientModel):
    _name = 'file.upload.wizard'
    file_data = fields.Binary('File', required=True)

    def create_partner_and_contract(self):
        if not self.file_data:
            raise exceptions.UserError(_("Tiedostoa ei ole ladattu."))

        # Purkaa tiedoston sisällön
        file_data = base64.b64decode(self.file_data)
        file_stream = io.StringIO(file_data.decode("utf-8"))
        rows = list(csv.DictReader(file_stream))

        previous_type = None  # Muuttuja edellisen rivin tyypin tallentamiseen
        previous_contract = None # Muuttuja edellisen sopimuksen tallentamiseen
        previous_product = None # Muuttuja edellisen sopimuksen tuotteen tallentamiseen
        # Käsittele tiedoston rivit
        for row in rows:
            logging.info(row);
            if any(row.values()):
                # Luo res.partner tietue
                partner_values = {
                    "name": f"{row.get('Etunimi')} {row.get('Sukunimi')}",
                    "email": row.get("Sähköposti").strip(),
                    "street": row.get("Osoite").strip(),
                    "zip": row.get("Postinumero").strip(),
                    "gender": row.get("Sukupuoli").strip(),
                    "company_type": "person",
                    "phone": row.get("Puhelin").strip(),
                    "city": row.get("Kaupunki").strip(),
                }
                logging.info(partner_values);
                partner = self.env['res.partner'].create(partner_values)

                # Luo contract.contract tietue
                contract_values = {
                    "partner_id": partner.id,
                    "name": partner.name,
                    "user_id": row.get("Vastuuhenkilo").strip(),
                    "line_recurrence": False,
                }
                contract = self.env['contract.contract'].create(contract_values)
                contract_template_id = int(row.get("Mallipohja").strip()) if row.get("Mallipohja") else False
                contract.sudo().write({"contract_template_id": contract_template_id})
                contract._onchange_contract_template_id()

                current_type = row.get("Tyyppi", "").strip()
                type_match = re.match(r"^[A-Za-z]+\d+$", current_type)

                # Onko tyyppi KIRJAIN + NUMEROSARJA...tämän avulla voidaan tehdään sopimuksien välillä kytkyjä
                if type_match:
                    logging.info("====TYPE MATCH======");
                    # Jos nykyinen tyyppi on sama kuin edellinen, luo kytky alkuperäiseen sopimukseen
                    if current_type == previous_type:
                        logging.info("=====ON SAMA ELI KYTKY TEHTAVA====");
                        # Tässä kohdassa tulisi luoda kytky sopimusten välille
                        contract.sudo().write({"parent_contract_id": previous_contract.id})

                        for product in previous_product.product_tmpl_id.free_products_ids:
                            contract_line_values = {
                                'contract_id': contract.id,
                                'product_id': product.id,
                                'name': product.name,
                                'price_unit': row.get("Hinta").strip(),
                            }

                            self.env['contract.line'].create(contract_line_values)

                    else:


                        previous_type = current_type  # Päivitä edellinen tyyppi nykyiseksi
                        previous_contract = contract # Päivitä edellinen sopimus nykyiseksi

                        # Luo contract.line tietueita
                        product_id = self.env["product.product"].sudo().search([
                            ('id', '=', int(row.get("Tuote").strip()))
                        ])
                        logging.info(product_id);

                        previous_product = product_id

                        contract_line_values = {
                            'contract_id': contract.id,
                            'product_id': product_id.id,
                            'name': product_id.name,
                            'price_unit': row.get("Hinta").strip(),
                        }

                        self.env['contract.line'].create(contract_line_values)

                else:

                    # Luo contract.line tietueita
                    product_id = self.env["product.product"].sudo().search([
                        ('id', '=', int(row.get("Tuote").strip()))
                    ])
                    logging.info(product_id);

                    contract_line_values = {
                        'contract_id': contract.id,
                        'product_id': product_id.id,
                        'name': product_id.name,
                        'price_unit': row.get("Hinta").strip(),
                    }

                    self.env['contract.line'].create(contract_line_values)


        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
