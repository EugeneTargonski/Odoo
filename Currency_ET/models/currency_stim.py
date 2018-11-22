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

class CurrencyRate(models.Model):

    """
    # Базовой валютой является белорусский рубль
    # Дополнительные настройки:
    # у пользователя Administrator часовой пояс должен соответствовать НБРБ
    # Dashboard/Users/Administrator/Preferences/Timezone=Europe/Minsk
    """

    # Private attributes
    # ------------------------------------------------------------------------------------------------------------------

    _name = 'res.currency.rate'
    _inherit = ['res.currency.rate']
    # База курса (пример - 3 рубля за 100 российских рублей. 100 - база)
    cur_scale = fields.Integer('Currency scale')
    # Курса (пример - 3 рубля за 100 российских рублей. 3 - курс)
    cur_official_rate = fields.Float('Currency rate using scale',(1,6))

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

    # Вызывается во вьюве currency_stim_cron.xml, по умолчанию - раз в час
    @api.multi
    def update_rates_on_date(self, var_update_date):
        update_date = str(var_update_date)
        # Ищем активные валюты
        currencys = self.env['res.currency'].search([('active', '=', True)])
        # Перебираем их
        for currency in currencys:
            # Проверяем наличие курса у данной валюты на сегодня
            if not self.env['res.currency.rate'].search([('name', '=', update_date),('currency_id', '=', currency.id)]):
                # Проверяем, что это базовая валюта. Если да, то создаем запись с курсом 1
                if currency.name == constants.BASE_CURRENCY:
                    # Создаем запись курсов валют, с полями: текущая дата, наша компания, ИД валюты, база курса, курс, курс в евро понимании
                    # (rate, который показывает сколько вражеской валюты мы можем купить за единицу нашей)
                    self.env['res.currency.rate'].create({'name': update_date,
                                                          'company_id': self.env.user.company_id.id,
                                                          'currency_id': currency.id,
                                                          'cur_scale': 1,
                                                          'cur_official_rate': 1,
                                                          'rate': 1
                                                          })
                else:
                    # Получаем список валют на сайте НБРБ
                    url = constants.CURRENCY_LIST_URL
                    response = requests.get(url, timeout=5)
                    parsed_string = json.loads(response.text)
                    for record in parsed_string:
                        # В списке находим валюту с нужным буквенным кодом (таких несколько) и активной датой(а такая одна)
                        if record[constants.RECORD_CUR_ABBR_NAME] == currency.name and str(record[constants.RECORD_CUR_DATE_END_NAME]) >= update_date and str(record[constants.RECORD_CUR_DATE_BEGIN_NAME]) < update_date:
                            # По внутреннему ИД НБРБ получаем курс валюты на дату
                            url2 = constants.CURRENCY_RATE_URL + str(record[constants.RECORD_CUR_ID_NAME]) + constants.ATTR_DATE + update_date
                            response2 = requests.get(url2, timeout=5)
                            parsed_string2 = json.loads(response2.text)
                            # Создаем запись курсов валют, с полями: текущая дата, наша компания, ИД валюты, база курса, курс, курс в евро понимании
                            # (rate, который показывает сколько вражеской валюты мы можем купить за единицу нашей)
                            self.env['res.currency.rate'].create({'name': update_date,
                                                                         'company_id': self.env.user.company_id.id,
                                                                         'currency_id': currency.id,
                                                                         'cur_scale': parsed_string2[constants.RECORD_CUR_SCALE_NAME],
                                                                         'cur_official_rate': parsed_string2[constants.RECORD_CUR_OFFRATE_NAME],
                                                                         'rate': 1/(parsed_string2[constants.RECORD_CUR_OFFRATE_NAME]/parsed_string2[constants.RECORD_CUR_SCALE_NAME])
                                                                         })
        return True

    # Вызывается во вьюве currency_stim_cron.xml, по умолчанию - раз в час
    @api.multi
    def cron_do_task(self):
        self.env['res.currency.rate'].update_rates_on_date(datetime.now())
        return True








