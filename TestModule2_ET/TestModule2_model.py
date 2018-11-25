import random, zeep
from datetime import datetime
from odoo import models, fields, api
import requests
import json
import xmlrpc.client
import pyodbc


class Pwd:

    def __init__(self): #empty function
        pass

    def newpwd(self): #generating new pass function 
        sequence = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM09876543210987654321'
        i = 1
        maxpwd = 8 #normally must be const
        pwd = ''
        while i <= maxpwd:
            pwd = pwd + random.choice(sequence)
            i = i+1
        return pwd

class TestModule2Wizard(models.TransientModel): #testing wizard class
    _name = 'testmodule2.wizard'
    _description = 'testing wizard'
    new_date = fields.Date('New date')

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

    @api.multi
    def massbutton1(self): #empty function for button on wizard
        return self._reopen_form()

    @api.multi
    def action1(self): #empty function for button on wizard
        return True







class TestModule2(models.Model): #testing class. conteins some tech on button functions
    _name = 'testmodule2'
    _description = 'TestModule2'
    name = fields.Char('Name', required=True)
    sf1 = fields.Char('string field 1')
    sf2 = fields.Char('string field 2')
    sf3 = fields.Char('string field 3')
    #sf3 = fields.Char('string field 3', compute="_compute_sf3")
    sf4 = fields.Char('string field 4')
    company_id = fields.Many2one('res.company', 'Company')
    user_id = fields.Many2one('res.users', 'Responsible')
    bool1 = fields.Boolean('boolean 1')
    bool2 = fields.Boolean('boolean 2')
    bool3 = fields.Boolean('boolean 3')
    bool4 = fields.Boolean('boolean 4')
    active = fields.Boolean('Active?', default=True)
    datetime_create = fields.Datetime('Document created', default=datetime.now())

    PwdGen = Pwd

    @api.model
    def create(self, vals): #fills sf1 field with 'aaaaa, blin' value on create
        vals['sf1']='aaaaa, blin'
        new_record = super(TestModule2, self).create(vals)
        return new_record

    @api.multi
    def write(self, vals):
        vals['sf2'] = 'a tut nixrena ne soxranitsia'
        super(TestModule2, self).write(vals)
        return True

    @api.multi
    def btn1(self):

        pwd = Pwd.newpwd(self)

        for test in self:
            test.sf1 = pwd
            test.bool1 = True
        return True

    @api.multi
    def btn2(self):

        currencys = self.env['res.currency'].search([('active', '=', True)])
        newstr = ""
        for currency in currencys:
            if not self.env['res.currency.rate'].search([('name', '=', datetime.now()), ('currency_id', '=', currency.id)]):
                url = 'http://www.nbrb.by/API/ExRates/Currencies'
                response = requests.get(url, timeout=5)
                parsed_string = json.loads(response.text)
                for record in parsed_string:
                    if record["Cur_Abbreviation"] == currency.name and str(record["Cur_DateEnd"]) > str(datetime.now()):# and record["Cur_Abbreviation"] != 'BYN':
                        newstr = newstr + currency.name + str(record["Cur_ID"])

        for task in self:
            task.sf3 = newstr
        return True

    @api.multi
    def btn3(self):
        url = 'http://www.nbrb.by/API/ExRates/Rates/145'
        #payload = (('key1', 'value1'), ('key2', 'value2'))
        #r = requests.get("http://httpbin.org/get", params=payload)

        response = requests.get(url, timeout=5)
        parsed_string = json.loads(response.text)
        for task in self:
            task.sf3 = str(parsed_string["Cur_OfficialRate"])+str(datetime.now())
        return True

    @api.multi
    def btn4(self):
        usd = 'USD'

        url = 'http://www.nbrb.by/API/ExRates/Currencies'
        response = requests.get(url, timeout=5)
        parsed_string = json.loads(response.text)
        for record in parsed_string:
            if record["Cur_Abbreviation"] == usd:
                url2 = 'http://www.nbrb.by/API/ExRates/Rates/'+str(record["Cur_ID"])
                response2 = requests.get(url2, timeout=5)
                parsed_string2 = json.loads(response2.text)
                for task in self:
                    task.sf4 = parsed_string2["Cur_OfficialRate"]
        return True

    #    sample:
    #    @api.onchange('first_field')
    #    def _first_field_onchange(self):
    #        res = {}
    #        res['domain'] = {'second_field': [('first_field', '=', self.first_field.id)]}
    #        return res


    @api.multi
    def btn5(self):

        wsdl = 'http://10.30.100.102/SyncDirectum/SyncDirectum.svc?wsdl'
        client = zeep.Client(wsdl=wsdl)
        #print(client.service.SyncR('54830207589427985273908888'))
        for test in self:
            test.sf4 = client.service.SyncR('Hello from Odoo!!!8888')
            test.bool4 = True
        return True

    @api.multi
    def btn6(self):
        #kurs = self.env['res.currency.rate'].search([('name', '=', datetime.now())])

        test = self.env['testmodule2'].create({'name': 'Created from button6','sf4':datetime.now()})

#        wsdl = 'http://10.30.100.102/SyncDirectum/SyncDirectum.svc?wsdl'
#        client = zeep.Client(wsdl=wsdl)
    @api.multi
    def btn7(self):
        url = "http://10.10.222.224:8069" #"http://10.10.222.222:8069"
        db = "testbase"#"testbase2"
        username = "admin"
        password = "admin"
        models = xmlrpc.client.ServerProxy(url+'/xmlrpc/2/obiect')
        common = xmlrpc.client.ServerProxy(url+'/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        id = models.execute_kw(db, uid, password, 'test0'
                                                  '', 'create', [{'name': "Created from biliat!!!!!!", }])
        #id = models.execute_kw(db, uid, password, 'testmodule2', 'create', [{'name': "Created from biliat!!!!!!",}])


        #models.execute_kw(db, uid, password,
        #                  'res.partner', 'check_access_rights',
        #                  ['read'], {'raise_exception': False})
    @api.multi
    def testwebserv(self):
        json = '{"url":"http://10.10.222.224:8069/xmlrpc/2",' \
               '"db":"testbase",' \
               '"username":"admin",' \
               '"password":"admin",' \
               '"module":"test0",' \
               '"action":"create",' \
               '"param_names":["name","stringfield1"],' \
               '"param_values":["name_value","stringfield1_value"]}'
        wsdl = 'http://10.30.100.102/SyncDirectum/SyncDirectum.svc?wsdl'
        wsdl = 'http://10.10.222.222/SyncDirectum/SyncDirectum.svc?wsdl'
        client = zeep.Client(wsdl=wsdl)

        for test in self:
            test.sf4 = client.service.Odoo(json)
            #test.bool4 = True

        pass

    @api.multi
    def test_act(self): #def test_act(self, cr, uid, ids, context={}):
        test = self.env['testmodule2'].create({'name': 'Created from menu', 'sf4': datetime.now()})
        return True

    @api.multi
    def btn8(self):
        return {
               'type': 'ir.actions.act_window',
               'res_model': self.env['testmodule2.wizard']._name,
                   #'wizzard.wizzard_model',
               'src_model': 'testmodule2.wizard',
               'res_id': self.env['testmodule2.wizard'].id,
               'view_type': 'form',
               'view_mode': 'form',
               'context': {},
               'views': [(self.env.ref('TestModule2.testmodule2_wizard_form').id, 'form')],
               'view_id': self.env.ref('TestModule2.testmodule2_wizard_form').id,
               'target': 'new'
            }

    @api.multi
    def btn9(self):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.30.100.102;DATABASE=directum;UID=sa;PWD=Qwaser082')
		
		#conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.30.100.102;DATABASE=tel.dbo;UID=sa;PWD=Qwaser082')
		#cnxn = pyodbc.connect("Driver = {SQL Server Native Client 11.0};Server = 10.30.100.102;Database = tel.dbo;username = sa;password = Qwaser082;Trusted_Connection = yes;")
        cursor = conn.cursor()
        #cursor.execute('SELECT * FROM numbers')
        #cursor.execute('select * from MBAnalit where MBAnalit.Vid = 3704')
        cursor.execute("""select DateOper, Dop, NameAn, DrobnoeChislo1 from MBAnalit 
                          where MBAnalit.Vid = 3704 
                                and Date2 = CONVERT(datetime,'20.11.2018',103)""")
        for test in self:
            test.sf4 = ''
        for row in cursor:
            for test in self:
                test.sf4 =test.sf4 + str(row.Dop)
        return True

    @api.multi
    def btn10(self):
        return True

    #работает, отрабатывает только по Enter
    #@api.onchange('sf4')
    #def _onchange_sf4(self):
    #    for test in self:
    #        test.sf2 = test.sf4
    #    return True

    #@api.depends('sf4')
    #def _compute_sf3(self):
    #    for test in self:
    #        if len(test.sf4) < 6:
    #            test.sf3 = test.sf4
    #        else:
    #            test.sf3 = "313211"
    #    return True



    #@api.depends('sf4')
    #def _compute_sf4(self):
    #    for task in self:
    #        task.sf3 = task.sf4

    #@api.depends('sf4')
    #def _write_sf4(self):
    #    self.sf3 = self.sf4


    #@api.depends('stage_id.fold')
    #def _write_stage_fold(self):
    #    self.stage_id.fold = self.stage_fold
