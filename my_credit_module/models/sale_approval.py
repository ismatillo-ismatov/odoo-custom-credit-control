from odoo import models, fields, api, _

class SalesApprovalRequest(models.Model):
    _name = 'sale.approval.request'
    _description = 'Sotuvni tasdiqlash sorovi'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="So'rov raqami", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    sale_order_id = fields.Many2one('sale.order', string="Sotuv buyurtmasi", required=True, tracking=True)
    
    # Avtomatik hisoblanadigan maydonlar
    currency_id = fields.Many2one('res.currency', string="Valyuta", compute='_compute_sale_data', store=True)
    total_amount = fields.Monetary(string="Jami summa", currency_field='currency_id', compute='_compute_sale_data', store=True)
    
    state = fields.Selection([
        ('draft', 'Qoralaman'),
        ('submitted', 'Yuborilgan'),
        ('approved', 'Tasdiqlangan'), 
        ('rejected', 'Rad etilgan')
    ], default='draft', string='Holati', tracking=True)

    rejection_reason = fields.Text(string='Rad etish sababi', tracking=True)
    approved_by = fields.Many2one('res.users', string="Tasdiqladi", readonly=True, tracking=True)

    @api.depends('sale_order_id')
    def _compute_sale_data(self):
        for rec in self:
            if rec.sale_order_id:
                rec.currency_id = rec.sale_order_id.currency_id
                rec.total_amount = rec.sale_order_id.amount_total
            else:
                rec.currency_id = False
                rec.total_amount = 0.0

    def action_submit(self):
        for rec in self:
            rec.state = 'submitted'

    def action_approve(self):
        for rec in self:
            rec.write({
                'state': 'approved', 
                'approved_by': self.env.user.id
            })
            # Sale Order-ni ham tasdiqlash
            if rec.sale_order_id:
                rec.sale_order_id.action_confirm()

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'

    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            # Sequence o'rniga vaqt tamg'asidan foydalanamiz
            now = fields.Datetime.now()
            vals['name'] = f"REQ/{now.strftime('%Y%m%d')}/{self.env['ir.sequence'].next_by_code('sale.approval.request') or '001'}"
        return super(SalesApprovalRequest, self).create(vals)

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('New')) == _('New'):
    #         # Sequence o'rniga shunchaki vaqtinchalik nom beramiz
    #         vals['name'] = "REQ-" + str(fields.Datetime.now().timestamp())
    #     return super(SalesApprovalRequest, self).create(vals)