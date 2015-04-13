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
import ir
from osv import osv
from report import report_sxw
import pooler

class loan_paper(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(loan_paper, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'merge' : self.__parse_paragraph__,
        })

    def __parse_paragraph__(self,content,loan):

        fetchval={
            '{p_name}':loan.name or '',
            '{p_loan_amount}':str(loan.loan_amount) or '',
            '{p_loan_period}':str(loan.loan_period) or '',
            '{p_process_fee}':str(loan.process_fee) or '',
            '{p_apply_date}':str(loan.apply_date) or '',
            '{p_approve_date}':str(loan.approve_date) or '',
            '{p_approve_amount}':str(loan.approve_amount) or '',
            '{p_contact}': str(loan.contact.name) + '\n' + str(loan.contact.street) + '\n ' + str(loan.contact.street2) + '\n ' + str(loan.contact.city) + '\n' + str(loan.contact.zip) or '',
        }
        for key in fetchval :
            content=content.replace(key,fetchval.get(key))
        return content;

report_sxw.report_sxw('report.letter.letter_info', 'account.loan', 'addons/loan/report/merge_letter.rml', parser=loan_paper)
