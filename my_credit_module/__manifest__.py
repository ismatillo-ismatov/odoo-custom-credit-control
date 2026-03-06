{
    'name': 'My Credit Module',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Mijozlar uchun kredit limiti va sotuvni tasdiqlash tizimi',
    'description': """
        Ushbu modul orqali:
        - Mijozlar uchun kredit limitini belgilash
        - Sotuv buyurtmalarini tasdiqlash jarayonini boshqarish mumkin.
    """,
    'author': 'Osiyo',
    'depends': [
        'base', 
        'sale', 
        'mail', 
        'account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_approval_views.xml',  # Action-lar birinchi yuklanishi shart
        'views/credit_limit_views.xml',   # Menyu Action-ni shu yerdan qidiradi
        'views/sale_order_views.xml',    # Tugmalar va qo'shimcha maydonlar
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}