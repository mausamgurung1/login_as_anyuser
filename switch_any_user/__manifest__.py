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
            'switch_any_user/static/src/css/user_login_systray.css',
            'switch_any_user/static/src/components/user_login_systray/user_login_systray.xml',
            'switch_any_user/static/src/components/user_login_systray/user_login_systray.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
    'images':['static/description/banner.gif'],
}