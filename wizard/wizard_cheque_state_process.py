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
import netsvc
import pooler
from osv.orm import browse_record

draft2posted_form = """<?xml version="1.0"?>
<form string="Draft To Posted">
    <separator colspan="4" string="change State : Draft to Posted " />
</form>
"""

draft2posted_fields = {

}
def _draft2posted(self, cr, uid, data, context):
        cheque_pool = pooler.get_pool(cr.dbname).get('account.loan.bank.cheque')
        wf_service = netsvc.LocalService("workflow")
        for o in cheque_pool.browse(cr, uid, data['ids'], context):
            if o.state=='draft':
                wf_service.trg_validate(uid, 'account.loan.bank.cheque', o.id, 'post_bank', cr)
        return {}

class change_cheque_state(wizard.interface):
    states = {
        'init' : {
            'actions' : [],
            'result' : {'type' : 'form',
                    'arch' : draft2posted_form,
                    'fields' : {},
                    'state' : [('end', 'Cancel'),('draft2posted', 'Draft To Posted') ]}
        },
        'draft2posted' : {
            'actions' : [],
            'result' : {'type' : 'action',
                    'action' : _draft2posted,
                    'state' : 'end'}
        },
    }
change_cheque_state('account.bank.cheque.process')