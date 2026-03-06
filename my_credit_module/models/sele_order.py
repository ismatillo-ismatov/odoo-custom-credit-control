from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    remaining_credit = fields.Float(string="Qolgan limit", compute="_compute_remaining_credit")

    def _compute_remaining_credit(self):
        for order in self:
            limit_rec = self.env['customer.credit.limit'].search([
                ('partner_id', '=', order.partner_id.id), ('active', '=', True)
            ], limit=1)
            order.remaining_credit = limit_rec.remaining_credit if limit_rec else 0.0

    def open_approval(self):
        """Approval tugmasi bosilganda so'rovlarni ochish"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Tasdiqlash so\'rovlari'),
            'res_model': 'sale.approval.request',
            'view_mode': 'tree,form',
            'domain': [('sale_order_id', '=', self.id)],
            'target': 'current',
        }
    

    def action_confirm(self):
        if self._context.get('skip_approval'):
            return super(SaleOrder, self).action_confirm()
        
        for order in self:
            # Avval tasdiqlangan so'rovni tekshirish
            approved_req = self.env['sale.approval.request'].search([
                ('sale_order_id', '=', order.id), ('state', '=', 'approved')
            ], limit=1)
            
            if approved_req:
                continue

            limit_rec = self.env['customer.credit.limit'].search([
                ('partner_id', '=', order.partner_id.id), ('active', '=', True)
            ], limit=1)
            
            limit_exceeded = limit_rec and (limit_rec.total_due + order.amount_total) > limit_rec.credit_limit
            amount_high = order.amount_total > 10000

            if limit_exceeded or amount_high:
                exist_req = self.env['sale.approval.request'].search([('sale_order_id', '=', order.id)], limit=1)
                if not exist_req:
                    # SO'ROVNI YARATAMIZ VA BAZAGA MAJBURIY YOZAMIZ
                    self.env['sale.approval.request'].create({
                        'sale_order_id': order.id, 
                        'state': 'submitted'
                    })
                    self.env.cr.commit()  # BU JUDA MUHIM: Xato chiqsa ham so'rov bazada qoladi!

                msg = "Kredit limiti oshib ketdi!" if limit_exceeded else "Summa 10,000 dan katta."
                raise ValidationError(_(f"{msg} Tasdiqlash so'rovi yuborildi. Iltimos, ma'suldan tasdiq kuting!"))
        
        return super(SaleOrder, self).action_confirm()

    # def action_confirm(self):
    #     # 1. Agar tasdiqlash jarayonini chetlab o'tish buyrug'i bo'lsa (context orqali)
    #     if self._context.get('skip_approval'):
    #         return super(SaleOrder, self).action_confirm()
        
    #     for order in self:
    #         # 2. Avval ushbu buyurtma uchun allaqachon TASDIQLANGAN so'rov bormi?
    #         approved_req = self.env['sale.approval.request'].search([
    #             ('sale_order_id', '=', order.id), 
    #             ('state', '=', 'approved')
    #         ], limit=1)
            
    #         # Agar tasdiqlangan so'rov bo'lsa, kredit limitini tekshirmasdan tasdiqlaymiz
    #         if approved_req:
    #             continue # Keyingi buyurtmaga o'tish (pastdagi ValidationError-larga tushmaydi)

    #         # 3. Kredit limitini tekshirish (faqat tasdiqlanmaganlar uchun)
    #         limit_rec = self.env['customer.credit.limit'].search([
    #             ('partner_id', '=', order.partner_id.id), 
    #             ('active', '=', True)
    #         ], limit=1)
            
    #         if limit_rec and (limit_rec.total_due + order.amount_total) > limit_rec.credit_limit:
    #             raise ValidationError(_("Kredit limiti oshib ketdi!"))
            
    #         # 4. Summa cheklovini tekshirish (10,000 dan oshsa)
    #         if order.amount_total > 10000:
    #             # Mavjud so'rovni tekshirish
    #             exist_req = self.env['sale.approval.request'].search([('sale_order_id', '=', order.id)], limit=1)
                
    #             if not exist_req:
    #                 # So'rov yo'q bo'lsa, yangi yaratish
    #                 self.env['sale.approval.request'].create({
    #                     'sale_order_id': order.id, 
    #                     'state': 'submitted'
    #                 })
                
    #             raise ValidationError(_("Summa 10,000 dan katta. Tasdiqlash so'rovi yuborildi!"))

    #     # Agar hamma tekshiruvlardan o'tsa yoki approved so'rov bo'lsa
    #     return super(SaleOrder, self).action_confirm()

# from odoo import models, fields, api
# from odoo.exceptions import ValidationError


# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#     _description = 'Sotuvni tasdiqlash so\'rovi'
    
#     def action_confirm(self):
#         if self._context.get('skip_approval'):
#             return super(SaleOrder,self).action_confirm()
        
#         for order in self:
#             limit_rec = self.env['customer.credit.limit'].search([
#                 ('partner_id', '=', order.partner_id.id),('active', '=', True)
#             ], limit=1)
#             if limit_rec and(limit_rec.total_due + order.amount_total) > limit_rec.credit_limit:
#                 raise ValidationError(_("Kredit limiti oshib ketdi!"))
            
#             if order.amount_total > 10000:
#                 approval = self.env['sale.approval.request'].search([
#                     ('sale_order_id', '=', order.id),('state', '=', 'approved')
#                 ], limit=1)
            
#                 if not approval:
#                     self.env['sale.approval.request'].create({'sale_order_id': order.id, 'state': 'submitted'})

#         raise ValidationError(_("Summa 10,000 dan katta. Tasdiqlash sorovi yuborildi"))