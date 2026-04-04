# -*- coding: utf-8 -*-
from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    any_userlogin = fields.Boolean(
        string="Allow To Login Other User",
        default=False,
        help=(
            "When enabled:\n"
            "  • This user CAN use the Switch User icon in the systray.\n"
            "  • This user APPEARS in other permitted users' switcher list."
        ),
    )
