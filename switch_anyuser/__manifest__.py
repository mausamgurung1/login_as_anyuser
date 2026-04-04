# -*- coding: utf-8 -*-
{
    'name': 'Login as Any User',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'summary': 'Systray user-switcher — icon only visible when current user has permission',
    'author': 'Mausam Gurung',
    'currency': 'USD',
    'price': '19.99',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'views/view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'login_as_anyuser/static/src/css/user_login_systray.css',
            'login_as_anyuser/static/src/components/user_login_systray/user_login_systray.xml',
            'login_as_anyuser/static/src/components/user_login_systray/user_login_systray.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
    'images':['static/description/banner.gif'],
}