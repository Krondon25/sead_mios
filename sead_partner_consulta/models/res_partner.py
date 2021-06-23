# -*- coding: utf-8 -*-
"""."""

from odoo import fields, models
from odoo.exceptions import ValidationError
import requests
import json


class IdentificationQuery(models.TransientModel):
    
    _name = 'identification.query'

    type_identification = fields.Selection([
        ('RUC', 'RUC'),
        ('DNI', 'DNI'),],
        store=True,
        string="Tipo de Identificación"
    )

    number_identification = fields.Char('Numero de Identificación',)

    def button_consulta(self):
        token ={"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImNhbmFsZXMudmFyZ2FzLmx1aXNAZ21haWwuY29tIn0.HTNVWLENuwYKS_ndu8zImqstMfnU8ErXDKBupNFyxAo"}

        if self.type_identification == "RUC":
            tipo_identificacion = 1
            url = "https://dniruc.apisperu.com/api/v1/ruc/{0}".format(self.number_identification)
        elif self.type_identification == "DNI":
            tipo_identificacion = 5
            url = "https://dniruc.apisperu.com/api/v1/dni/{0}".format(self.number_identification)
        partner = self.env['res.partner']
        response = requests.get(url,token)
        if response.status_code == 200:
            data_response =response.content
            data_response = json.loads(data_response)
            print(data_response)
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
                    data_distrito = record_distrito.id

            for record_provincia in provincia:
                if record_provincia.name == data_provincia:
                    data_provincia = record_provincia.id

            for record_departamneto in departamento:
                if record_departamneto.name == data_departamento:
                    data_departamento = record_departamneto.id 

            if 'success' not in data_response:
                
                partner.create({
                    "name": data_response.get('razonSocial'),
                    "l10n_latam_identification_type_id": tipo_identificacion,
                    "vat": self.number_identification,
                    "tradename": data_response.get('razonSocial'),
                    "social_reason": data_response.get('razonSocial'),
                    "street": data_response.get('direccion'),
                    "phone": data_response.get('telefonos'),
                    "ubigeo": data_response.get('ubigeo'),
                    "l10n_pe_district":data_distrito,
                    "city_id":data_provincia,
                    "state_id":data_departamento,
                    "country_id": 173,
                    })
        
            else:
                mensaje = data_response.get('message')
                raise ValidationError(mensaje)
        else:
            raise ValidationError("No Se Pudo encontrar la coicidencia, Verifique sus datos")
