# -*- coding: utf-8 -*-

# 1 : imports of python lib
from datetime import datetime
import requests
import json

# 2 :  imports of odoo
from odoo import models, fields, api

# 3 :  imports of odoo modules

# 4 :  imports from custom modules


class Partner(models.Model):

    """
    We have inherited res.partner model and added some fields.
    Whenever create new field in res.partner and res.users then always open that module from app menu in browser so you can directly click on upgrade button, other wise it gives error as you mention.
    If you forget and error raised the you have to upgrade module from terminal.
    python openerp-server --config=give path of your config file --update=your module name
    """

    # Private attributes
    # ------------------------------------------------------------------------------------------------------------------


    _name = 'res.partner'
    _inherit = ['res.partner']

    is_company = fields.Boolean(default=True)
    gal_db1 = fields.Char('Gal1 Nrec')
    gal_db2 = fields.Char('Gal2 Nrec')
    gal_db3 = fields.Char('Gal3 Nrec')
    gal_db4 = fields.Char('Gal4 Nrec')
    full_name = fields.Char('Full Name')
    ext_id = fields.Char('External ID')
    kpp = fields.Char('RU code')

    # Default methods
    # ------------------------------------------------------------------------------------------------------------------

    # Fields declaration
    # ------------------------------------------------------------------------------------------------------------------

    # Compute and search fields, in the same order of fields declaration
    # ------------------------------------------------------------------------------------------------------------------

    # Constraints and onchanges
    # ------------------------------------------------------------------------------------------------------------------

    # Action methods
    # ------------------------------------------------------------------------------------------------------------------

    # Business methods
    # ------------------------------------------------------------------------------------------------------------------

    # CRUD methods
    # ------------------------------------------------------------------------------------------------------------------










