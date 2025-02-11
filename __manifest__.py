# servicio_mantenimiento/__manifest__.py
{
    'name': 'Alquiler de Productos',
    'version': '1.0',
    'author': 'Emilio Neva',
    'category': 'Custom',
    'summary': 'Gestión de Alquileres de Productos',
    'depends': ['base', 'garantias'],
    'data': [
        'security/ir.model.access.csv',
        'views/alquiler_producto_views.xml',
    ],
    'icon': '/servicio_mantenimiento/static/description/icon56.png',
    'installable': True,
    'application': True,
}