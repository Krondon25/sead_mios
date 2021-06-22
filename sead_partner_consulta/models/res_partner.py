# -*- coding: utf-8 -*-
"""."""

from odoo import fields, models
from odoo.exceptions import ValidationError
import requests
import json


class ResPartner(models.Model):
    _inherit = 'res.partner'



    def button_consulta(self):
        token ={"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImNhbmFsZXMudmFyZ2FzLmx1aXNAZ21haWwuY29tIn0.HTNVWLENuwYKS_ndu8zImqstMfnU8ErXDKBupNFyxAo"}

        if self.l10n_latam_identification_type_id.name == "RUC":
            url = "https://dniruc.apisperu.com/api/v1/ruc/{0}".format(self.vat)
        elif self.l10n_latam_identification_type_id.name == "DNI":
            url = "https://dniruc.apisperu.com/api/v1/dni/{0}".format(self.vat)

        response = requests.get(url,token)
        if response.status_code == 200:
            data_response =response.content
            data_response = json.loads(data_response)
            self.name = data_response.get('razonSocial')
            self.street = data_response.get('direccion')
            self.phone = data_response.get('telefonos')
            self.zip = data_response.get('ubigeo')
            data_distrito = data_response.get('distrito').capitalize()
            data_provincia = data_response.get('provincia').capitalize()
            data_departamento = data_response.get('departamento').capitalize()
            data_departamento = data_response.get('departamento').capitalize()

            distrito = self.env['l10n_pe.res.city.district'].search([])
            provincia = self.env['res.city'].search([])
            departamento = self.env['res.country.state'].search([])

            for record_distrito in distrito:
                if record_distrito.name == data_distrito:
                    self.l10n_pe_district = record_distrito.id

            for record_provincia in provincia:
                if record_provincia.name == data_provincia:
                    self.city_id = record_provincia.id

            for record_departamneto in departamento:
                if record_departamneto.name == data_departamento:
                    self.state_id = record_departamneto.id 
            self.country_id = 173
        else:
            raise ValidationError("No Se Pudo encontrar la coicidencia, Verifique sus datos")





        

        # {
        #     "ruc":"20131312955",
        #     "razonSocial":"SUPERINTENDENCIA NACIONAL DE ADUANAS Y DE ADMINISTRACION TRIBUTARIA - SUNAT",
        #     "nombreComercial":null,
        #     "telefonos":[],
        #     "tipo":null,
        #     "estado":"ACTIVO",
        #     "condicion":"HABIDO",
        #     "direccion":"AV. GARCILASO DE LA VEGA NRO. 1472 LIMA LIMA LIMA",
        #     "departamento":"LIMA",
        #     "provincia":"LIMA",
        #     "distrito":"LIMA",
        #     "fechaInscripcion":null,
        #     "sistEmsion":null,
        #     "sistContabilidad":null,
        #     "actExterior":null,
        #     "actEconomicas":[],
        #     "cpPago":[],
        #     "sistElectronica":[],
        #     "fechaEmisorFe":null,
        #     "cpeElectronico":[],
        #     "fechaPle":null,
        #     "padrones":[],
        #     "fechaBaja":null,
        #     "profesion":null,
        #     "ubigeo":"150101",
        #     "capital":"LIMA"
        # }'