# -*- coding: utf-8 -*-

# 1 : imports of python lib
#import requests #import json #import xmlrpc.client #import random, zeep #from datetime import datetime 
import pyodbc #Инструкция по установке: https://debian.pkgs.org/9/debian-main-i386/python3-pyodbc_3.0.10-2_i386.deb.html


# 2 :  imports of odoo
from odoo import api, fields, models
from odoo import exceptions

# 3 :  imports of odoo modules

# 4 :  imports from custom modules
from .. import constants





class MSSQLConnectWizard(models.TransientModel):

    """ 
    Модель, в которой будут отображаться данные, сохраненные в модели MSSQLConnect
    Нужна для кнопок и дополнительных вычислений
    """ 

    # Private attributes
    # ------------------------------------------------------------------------------------------------------------------
    _name = 'mssql.connect.wizard'
    _description = 'no descr'

    # Default methods
    # ------------------------------------------------------------------------------------------------------------------

    # Fields declaration
    # ------------------------------------------------------------------------------------------------------------------    
    request_date = fields.Date('Date')
    mssql_ids = fields.Many2many('mssql.connect',string='Table')


    # Compute and search fields, in the same order of fields declaration
    # ------------------------------------------------------------------------------------------------------------------

    # Constraints and onchanges
    # ------------------------------------------------------------------------------------------------------------------

    # Action methods
    # ------------------------------------------------------------------------------------------------------------------
        
    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,  # this model
            'res_id': self.id,  # the current wizard record
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'}
    
    # Business methods
    # ------------------------------------------------------------------------------------------------------------------
    @api.multi
    def get_data(self):
        #проверка пустой даты
        if not (self.request_date): raise exceptions.ValidationError('Input date first!')
        
        #подключаюсь к базе
        conn = pyodbc.connect('DRIVER={'+constants.DRIVER+'};SERVER='+constants.SERVER+';DATABASE='+constants.DATABASE+
                                ';UID='+constants.UID+';PWD='+constants.PWD+'')
        cursor = conn.cursor()
        
        #выполняю запрос
        cursor.execute(constants.QUERY+"'%s'"%str(self.request_date))
        
        #чищу данные в модели
        self.env['mssql.connect'].search([]).unlink()
        
        #записываю данные из SQL в модель
        for row in cursor:
            rec_id = self.env['mssql.connect'].create({'name': row.NameAn,'date_field1': row.DateOper
                                                        ,'string1': row.Dop, 'float1': row.DrobnoeChislo1})                            
        
        #Из книжного примера (Todo wizard, v11.0)
        self.ensure_one()
        Task = self.env['mssql.connect']
        all_tasks = Task.search([])
        # Fill the wizard list with all tasks
        self.mssql_ids = all_tasks
        # reopen wizard form on same wizard record
        return self._reopen_form()
        
    # CRUD methods
    # ------------------------------------------------------------------------------------------------------------------
    

    

        
        



class MSSQLConnect(models.TransientModel): #TransientModel

    """ 
    Модель, в которую будут записываться данные, импортированные из SQL
    """ 

    # Private attributes
    # ------------------------------------------------------------------------------------------------------------------
    _name = 'mssql.connect'
    _description = 'MSSQL Connect'

    # Default methods
    # ------------------------------------------------------------------------------------------------------------------

    # Fields declaration
    # ------------------------------------------------------------------------------------------------------------------
    
    #Набор произвольных полей, подходящих для данных, загружаемых из SQL
    name = fields.Char('Name')
    date_field1 = fields.Date('Date')
    float1 = fields.Float('Float',(1,6))
    int1 = fields.Integer('Integer')
    string1 = fields.Char('string1')
    string2 = fields.Char('string2')
    
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

