# -*- coding: utf-8 -*-
from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    any_userlogin = fields.Boolean(
        string="Allow To Login Other User",
        default=False,
        help="When enabled, this user will appear in the systray user-switcher "
             "dropdown so that other users can switch into this account."
    )
