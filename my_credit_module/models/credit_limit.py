from odoo import models, fields,api, _
from odoo.exceptions import ValidationError

class CustomerCreditLimit(models.Model):
    _name = 'customer.credit.limit'
    _discraption = 'Mijoz kredit limiti'
    partner_id = fields.Many2one('res.partner',string='Mijoz',required=True)
    credit_limit = fields.Monetary(string='Kiridit limit',required=True)
    currency_id = fields.Many2one('res.currency',string='Valyuta')
    active = fields.Boolean(default=True)
    total_due = fields.Monetary(compute='_compute_totals',store=True,string='Jami qarz')
    remaining_credit = fields.Monetary(compute='_compute_totals',store=True,string="Qolgan limit ")
    note = fields.Text(string="Eslatma")


    @api.depends('partner_id','credit_limit')
    def _compute_total(self):
        for record in self:
            invoices = self.env['account.move'].search([
                ('partner_id', '=', record.partner_id.id),
                ('state', '=', 'posted'),
                ('payment_state','not in',('paid','in_payment')),
            ])
            record.total_duo = sum(invoices.mapped('amount_residuel'))
            record.remaining_credit = record.credit_limit - record.total_due


    @api.constrains('partner_id','active')
    def _check_unique_active_limit(self):
        for record in self:
            if record.active:
                domain = [('partner_id', '=', record.partner_id.id),('active', '=', True), ('id', '!=',record.id)]
                if self.search_count(domain) > 0:
                    raise ValidationError(_("Ushbu mijozni allaqachon faol kiriditi mavjud!"))
            




