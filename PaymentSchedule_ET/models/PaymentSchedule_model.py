import zeep #(for web services)
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta
from .. import constants
import requests
import json



class DocumentType(models.Model):
    _name = 'model.payment_schedule.document_type'
    _order = 'name'
    name = fields.Char('Document type', required=True)
    payment_ids = fields.One2many('model.payment_schedule', 'document_type_id', string='Payments')


class BusinessDirection (models.Model):
    _name = 'model.payment_schedule.business_direction'
    name = fields.Char('Name')
    payment_ids = fields.One2many('model.payment_schedule', 'businessdirection_id', string='Payments')

class ConsumptionItem1 (models.Model):
    _name = 'model.payment_schedule.consumption_item1'
    name = fields.Char('Name')
    businessdirection_id = fields.Many2one('model.payment_schedule.business_direction', 'Business Direction', required=True)
    payment_ids = fields.One2many('model.payment_schedule', 'consumptionitem1_id', string='Payments')

class ConsumptionItem2 (models.Model):
    _name = 'model.payment_schedule.consumption_item2'
    name = fields.Char('Name')
    consumptionitem1_id = fields.Many2one('model.payment_schedule.consumption_item1','Consumption Item 1', required=True)
    payment_ids = fields.One2many('model.payment_schedule', 'consumptionitem2_id', string='Payments')



class PaymentSchedule(models.Model):

    #"""
    @api.multi
    def get_date_desired(self):

        today = datetime.now()
        delta_week = timedelta(days=7)
        delta_day_of_week = timedelta(days=today.weekday())
        newdate = today-delta_day_of_week+delta_week

        return newdate
    #"""

    _name = 'model.payment_schedule'
    _description = 'Payment Schedule'
    name                 = fields.Char('Document number')
    document_type_id     = fields.Many2one('model.payment_schedule.document_type', 'Document type', required=True)
    company_id           = lambda self: self.env.user.company_id.id
    our_company_id       = fields.Many2one('res.company', 'Company', required=True, domain=lambda self: ['|',('id','=', self.env.user.company_id.id),('parent_id','=', self.env.user.company_id.id)])
    company_id           = fields.Many2one('res.partner', 'Company', required=True, domain=[('is_company', '=', True)])
    date_desired         = fields.Date(string='Desired date of payment'
                                       , default=get_date_desired
                                       )
    date_transfer        = fields.Date('Transfer date of payment')
    #date_payment         = fields.Date('Date of payment', depends="compute_date_payment")
    date_payment         = fields.Date('Date of payment', compute="compute_date_payment", store=True)
    date_document        = fields.Date('Document date')
    sum_payment          = fields.Float('total', (3, 2), required=True)
    sum_payment_recount  = fields.Float(constants.RECOUNT_CURRENCY, (3, 2), readonly=True)
    currency_id          = fields.Many2one('res.currency', 'Currency', required=True)
    payment_approved     = fields.Boolean('Payment approved')
    user_id              = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.uid)
    datetime_create      = fields.Datetime('Document created', default=datetime.now())
    businessdirection_id = fields.Many2one('model.payment_schedule.business_direction', 'Business Direction', required=True)
    consumptionitem1_id  = fields.Many2one('model.payment_schedule.consumption_item1', 'Consumption Item 1', required=True)
    consumptionitem2_id  = fields.Many2one('model.payment_schedule.consumption_item2', 'Consumption Item 2')
    reason               = fields.Char('Reason')

    # @api.depends('date_transfer','date_desired')
    @api.depends('date_transfer','date_desired')
    def compute_date_payment(self):
        for paymant in self:
            if paymant.date_transfer is False:
                paymant.date_payment = paymant.date_desired
            else:
                paymant.date_payment = paymant.date_transfer


    """
    @api.multi
    def get_date_desired(self):

        today = datetime.now()
        delta_week = timedelta(days=7)
        delta_day_of_week = timedelta(days=today.weekday())
        newdate = today-delta_day_of_week+delta_week

        return newdate
    """

    #TestButton1
    @api.multi
    def button1(self):
        #payments = self.env['model.payment_schedule'].search([('date_payment', '>=', datetime.now().date())])
        for paymant in self:
            paymant_day = datetime.now().date()
            #if fields.Datetime.from_string(paymant.date_payment).date() < paymant_day:
            #    paymant_day = paymant.date_payment

            recount_currency_id  = self.env['res.currency'].search([('name', '=', constants.RECOUNT_CURRENCY)])

            recount_currencyrate = self.env['res.currency.rate'].search([('name', '=', paymant_day),('currency_id', '=', recount_currency_id.id)])
            paymant_currencyrate = self.env['res.currency.rate'].search([('name', '=', paymant_day), ('currency_id', '=', paymant.currency_id.id)])

            paymant.reason = str(recount_currencyrate)
            if recount_currencyrate:
                paymant.reason = "without not"
            if not recount_currencyrate:
                paymant.reason = "with not"
        return True

    # TestButton2
    @api.multi
    def button2(self):
        for paymant in self:
            today = datetime.now()
            delta_week = timedelta(days=7)
            delta_day_of_week = timedelta(days=today.weekday())
            newdate = today-delta_day_of_week+delta_week
            paymant.reason = str(newdate.date())
        return newdate.date()


    # TestButton2
    @api.multi
    def button3(self):
        #payments = self.env['model.payment_schedule'].search([('date_payment', '>=', datetime.now().date())])
        for paymant in self:
            paymant_day = datetime.now().date()+timedelta(days=7)
            #if fields.Datetime.from_string(paymant.date_payment).date() < paymant_day:
            #    paymant_day = paymant.date_payment

            recount_currency_id  = self.env['res.currency'].search([('name', '=', constants.RECOUNT_CURRENCY)])

            recount_currencyrate = self.env['res.currency.rate'].search([('name', '=', paymant_day),('currency_id', '=', recount_currency_id.id)])
            paymant_currencyrate = self.env['res.currency.rate'].search([('name', '=', paymant_day), ('currency_id', '=', paymant.currency_id.id)])

            paymant.reason = str(recount_currencyrate)
            if recount_currencyrate:
                paymant.reason = "without not"
            if not recount_currencyrate:
                paymant.reason = "with not"
            #paymant.reason = str(paymant_currencyrate.cur_official_rate)
            #if recount_currencyrate != False and paymant_currencyrate != False:
            #    sum_payment_in_base_cur = paymant.sum_payment * paymant_currencyrate.cur_official_rate / paymant_currencyrate.cur_scale
            #    paymant.sum_payment_recount = sum_payment_in_base_cur*recount_currencyrate.cur_scale/recount_currencyrate.cur_official_rate

        return True


    @api.onchange('date_desired')
    def _onchange_date_desired(self):
        for paymant in self:
            if fields.Datetime.from_string(paymant.date_desired).date() < paymant.get_date_desired().date():
            #if paymant.date_desired < str(paymant.get_date_desired()):
                paymant.date_desired = paymant.get_date_desired()
                #paymant.reason = str(fields.Datetime.from_string(paymant.date_desired))+'___'+str(paymant.get_date_desired())
                #raise ValidationError('Must have 5 chars!')
                return {
                        'warning': {
                        'title': 'Ошибка ввода',
                        'message': 'Дата завершения должна быть больше даты начала'
                                    }
                        }


    @api.multi
    def cron_do_task(self):
        payments = self.env['model.payment_schedule'].search([('date_payment', '>=', datetime.now().date())])
        for paymant in payments:
            paymant_day = datetime.now().date()
            if fields.Datetime.from_string(paymant.date_payment).date() < paymant_day:
                paymant_day = paymant.date_payment

            recount_currency_id  = self.env['res.currency'].search([('name', '=', constants.RECOUNT_CURRENCY)])

            recount_currencyrate = self.env['res.currency.rate'].search([('name', '=', paymant_day),('currency_id', '=', recount_currency_id.id)])
            paymant_currencyrate = self.env['res.currency.rate'].search([('name', '=', paymant_day), ('currency_id', '=', paymant.currency_id.id)])
            if recount_currencyrate and paymant_currencyrate:
                sum_payment_in_base_cur = paymant.sum_payment * paymant_currencyrate.cur_official_rate / paymant_currencyrate.cur_scale
                paymant.sum_payment_recount = sum_payment_in_base_cur*recount_currencyrate.cur_scale/recount_currencyrate.cur_official_rate
        return True

