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
import wizard


loan_form = '''<?xml version="1.0"?>
<form string="Select partner">
    <field name="partner_id"/>
</form>'''

loan_fields = {
    'partner_id': {'string':'Partner', 'type':'many2one', 'relation': 'res.partner', 'required':True},
}

class wizard_report(wizard.interface):
    states = {
        'init': {
            'actions': [],
            'result': {'type':'form', 'arch':loan_form, 'fields':loan_fields, 'state':[('end','Cancel'),('report','Print Loan Report.')]}
        },
        'report': {
            'actions': [],
            'result': {'type':'print', 'report':'account.partner.loan', 'state':'end'}
        }
    }
wizard_report('account.partner.loan')