from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import config
from odoo.tools.misc import formatLang, format_date, get_lang 
import logging 
_logger = logging.getLogger(__name__) 

class MailInvoice(models.Model):
    _name = 'partner.mail.template'

    def default_partner_id(self):
        return self._context.get("active_id") 


    mail_template_id = fields.Many2one('mail.template',string="Mail Template")
    partner_id = fields.Many2one('res.partner',default=default_partner_id, string="Contact")

    move_type = fields.Selection(selection=[
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ], string='Type', required=True, store=True, default="entry") 



class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    partner_name_template_ids = fields.One2many('partner.mail.template','partner_id', string=" Partner Template")

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_invoice_sent(self):
        super(AccountMove,self).action_invoice_sent()
        self.ensure_one()
        template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
        lang = False
        if template:
            lang = template._render_lang(self.ids)[ self.id]
        if not lang:
            lang = get_lang(self.env).code
        compose_form = self.env.ref('account.account_invoice_send_wizard_form', raise_if_not_found=False)
        partner_id = self.partner_id 
        move_type = self.move_type
        if self.env["partner.mail.template"].search([("partner_id","=",partner_id.id),("move_type","=",move_type)]):
            if self.env["partner.mail.template"].search([("partner_id","=",partner_id.id),("move_type","=",move_type)])[0].mail_template_id:
                template = self.env["partner.mail.template"].search([("partner_id","=",partner_id.id),("move_type","=",move_type)])[0].mail_template_id
        ctx = dict(
            default_model='account.move',
            default_res_id=self.id,
            # For the sake of consistency we need a default_res_model if
            # default_res_id is set. Not renaming default_model as it can
            # create many side-effects.
            default_res_model='account.move', default_use_template=bool(template),
            default_template_id=template and template.id or False, 
            default_composition_mode='comment', 
            mark_invoice_as_sent=True, 
            custom_layout="mail.mail_notification_paynow", 
            model_description=self.with_context(lang=lang).type_name, 
            force_email=True
        )
        return {
            'name': _('Send Invoice'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        } 


