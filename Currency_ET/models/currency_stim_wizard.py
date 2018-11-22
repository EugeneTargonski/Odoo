# -*- coding: utf-8 -*-

# 1 : imports of python lib
from datetime import datetime
import requests
import json

# 2 :  imports of odoo
from odoo import models, fields, api

# 3 :  imports of odoo modules

# 4 :  imports from custom modules
from .. import constants

class CurrencyWizard(models.TransientModel):
    """
    """

    _name = 'currency.rate.update.wizard'
    _description = 'Update wizard'
    update_date = fields.Date('Date')

    @api.multi
    def update_rates(self):
        update_date = self.update_date
        result = self.env['res.currency.rate'].update_rates_on_date(update_date)
        return result

