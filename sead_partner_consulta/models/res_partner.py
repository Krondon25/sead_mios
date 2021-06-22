# -*- coding: utf-8 -*-
"""."""

from odoo import fields, models
from odoo.exceptions import ValidationError
import requests
import json


class ResPartner(models.Model):
    _inherit = 'res.partner'


    partner_name = fields.Char(string='Nombre Completo',required=False)
    first_name = fields.Char(required=False)
    social_reason = fields.Char(string="Razón Social",required=False)
    tradename = fields.Char(string="Nombre Comercial",required=False)
    
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
            if 'success' not in data_response:
                self.name = data_response.get('razonSocial')
                self.tradename = data_response.get('razonSocial')
                self.social_reason = data_response.get('razonSocial')
                self.street = data_response.get('direccion')
                self.phone = data_response.get('telefonos')
                self.ubigeo = data_response.get('ubigeo')
                data_distrito = ''
                data_provincia = ''
                data_departamento = ''

                if data_response.get('distrito'):
                    data_distrito = data_response.get('distrito').capitalize()
                if data_response.get('provincia'):
                    data_provincia = data_response.get('provincia').capitalize()
                if data_response.get('departamento'):
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
                mensaje = data_response.get('message')
                raise ValidationError(mensaje)
        else:
            raise ValidationError("No Se Pudo encontrar la coicidencia, Verifique sus datos")
