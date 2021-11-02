# @author Fausto Jesus De La Cruz Caminero <fdelacruz@aviamltd.com>

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import config

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_reverse(self):
        res = super(AccountMove,self).action_reverse()
        res['context'] = "{'default_journal_id':"+str(self.journal_id.id)+"}"
        return res

    def action_debit_reverse(self):
        action = self.env["ir.actions.actions"]._for_xml_id("account_debit_note.action_view_account_move_debit") 
        action['context'] = "{'default_journal_id':"+str(self.journal_id.id)+"}"
        return action

    @api.onchange('date')
    def on_change(self):
        if self.move_type in ['in_invoice','out_invoice','out_refund', 'in_refund']:
#        if self.move_type == 'in_invoice':
            if self.date and self.invoice_date:
                if self.date.year != self.invoice_date.year:
                    raise ValidationError("La Fecha Contable no puede ser de un año diferente a la fecha de la Factura")
                if self.date.month < self.invoice_date.month:
                    raise ValidationError("La Fecha Contable no puede ser de un mes anterior a la fecha de la Factura")
        

class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"
