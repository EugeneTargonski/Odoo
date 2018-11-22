import zeep #(for web services)
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta
import requests
import json

class Test0(models.Model):

    _name                = 'test0'

    name                 = fields.Char('Name')
    stringfield1         = fields.Char('String field 1')
    stringfield2         = fields.Char('String field 2')
    bool1 = fields.Boolean('Bool')