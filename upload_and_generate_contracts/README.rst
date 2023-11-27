.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

=============================
upload_and_generate_contracts
=============================

Tämä moduuli tarjoaa toiminnallisuuden CSV-tiedoston lataamiseen, jonka avulla voidaan luodaa res.partner, contract.contract ja contract.line tietueita

CSV-tiedoston vaatimukset:
- CSV-tiedostossa tulee olla otsikot, jotka vastaavat odotettuja kenttiä kumppaneille ja sopimuksille.
- Kumppaneille vaadittavat kentät sisältävät 'Etunimi', 'Sukunimi', 'Sähköposti', 'Osoite', 'Postinumero', 'Sukupuoli', 'Puhelin' ja 'Kaupunki'.
- Sopimuksille vaadittavat kentät sisältävät 'Vastuuhenkilö', 'Mallipohja', 'Tyyppi', 'Tuote' ja 'Hinta'.
- 'Tyyppi'-kenttää käytetään tunnistamaan ja linkittämään yhteen liittyvät sopimukset.


Configuration
=============
\-

Usage
=====
\-

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

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
        :alt: Oy Tawasta OS Technologies Ltd.
        :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
