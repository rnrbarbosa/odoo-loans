#!/usr/bin/env python
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
from openerp.osv import fields, osv

class account_loan_installment(osv.osv):
    _name = 'account.loan.installment'
    _columns = {
        'name': fields.char('Description',size=64 ),
        'loan_id': fields.many2one('account.loan', 'Loan'),
        'capital': fields.float('Installment'),
        'interest': fields.float('Interest'),
        'total': fields.float('Installment'),
        'cheque_id' : fields.many2one('account.loan.bank.cheque','Bank Transfer')
    }
account_loan_installment()

class loan_installment_period(osv.osv):
    _name = 'loan.installment.period'
    _columns ={
        'name':fields.char('Period Name', size=64, required=True),
        'period':fields.integer('Loan Period', required = True),
   }
loan_installment_period()
