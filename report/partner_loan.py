# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

import time
import datetime
from report import report_sxw
from osv import osv
from datetime import date
import pooler

import mx.DateTime
from mx.DateTime import RelativeDateTime, now, DateTime, localtime

class partner_loan(report_sxw.rml_parse):
    s=0.0
    _capital=0.0
    _interest=0.0
    _subtotal=0.0

    def __init__(self, cr, uid, name, context):

        super(partner_loan, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'get_loan':self.__get_loan__,
            'ending_date' : self.__ending_date__,
            'installment': self.__installment__,
            #'amount_total' : self.__amount_total__,
            'get_capital': self.__get_capital__,
            'get_interest':self.__get_interest__,
            'get_subtotal':self.__get_subtotal__,
        })
    def __get_loan__(self, partner_id):

        tc = self.pool.get('account.loan')
        ids = tc.search(self.cr, self.uid, [('partner_id','=',partner_id)])
        res = []
        for loan in tc.browse(self.cr, self.uid, ids, {'partner_id':partner_id}):
            res.append(loan)

        return res

    def __installment__(self,install):

        #self._capital=self._capital+ install.capital
        #self._interest= self._interest+install.interest
        #self._subtotal= self._subtotal + install.capital + install.interest

        return install.total

#    def __amount_total__(self,install):
#        self.s = self.s + install.capital
#        return self.s

    def __get_capital__(self,loan):
        self.cr.execute("SELECT SUM(capital) from account_loan_installment where \
                        account_loan_installment.loan_id=" +str(loan.id))
        return self.cr.fetchone()[0] or 0.0

        #return self._capital

    def __get_interest__(self,loan):
        self.cr.execute("SELECT SUM(interest) from account_loan_installment where \
                        account_loan_installment.loan_id=" +str(loan.id))
        return self.cr.fetchone()[0] or 0.0

        #return self._interest

    def __get_subtotal__(self,loan):
        self.cr.execute("SELECT SUM(total) from account_loan_installment where \
                        account_loan_installment.loan_id=" +str(loan.id))
        return self.cr.fetchone()[0] or 0.0

#        self.cr.execute("SELECT SUM(total) from account_loan_installment, account_loan where \
#        account_loan_installment.loan_id=account_loan.id and account_loan.id=" +str(loan.id)+" group by account_loan_installment.loan_id")

        #return self._subtotal

    def __ending_date__(self,loan):

        start_date = loan.approve_date
        total_inst = loan.total_installment

        i = 366
        j = 12
        if j == total_inst:
            end_date = mx.DateTime.strptime(start_date, '%Y-%m-%d') + RelativeDateTime(days=i)
        else:
            while j < total_inst:
                j = j + 12
                i = i + 365

                end_date = mx.DateTime.strptime(start_date, '%Y-%m-%d') + RelativeDateTime(days=i)

        return end_date.date

#    def __amount_total__(self,loan):
#
#         self.cr.execute("SELECT SUM(total) from account_loan_installment where loan_id=%d" % (1))
#         self.cr.execute("SELECT SUM(total) from account_loan_installment, account_loan where \
#                        account_loan_installment.loan_id=account_loan.id and account_loan.id=" +str(loan.id)+" group by account_loan_installment.loan_id")
#         res = self.cr.fetchone()[0]
#         return res

report_sxw.report_sxw('report.account.partner.loan',
                       'account.loan',
                        'addons/loan/report/partner_loan.rml',
                        parser=partner_loan)
