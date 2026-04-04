# -*- coding: utf-8 -*-
from odoo import models
from odoo.http import request

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super().session_info()

        current_user = request.env.user

        if not current_user or current_user._is_public():
            result['can_switch_user'] = False
            result['switchable_users'] = []
            result['is_switched'] = False
            result['original_user_name'] = ''
            return result

        original_uid = request.session.get('original_uid')
        is_switched = bool(original_uid)

        can_switch = bool(current_user.sudo().any_userlogin) or is_switched

        result['can_switch_user'] = can_switch
        result['is_switched'] = is_switched

        if is_switched:
            original_user = request.env['res.users'].sudo().browse(original_uid)
            result['original_user_name'] = original_user.name if original_user.exists() else ''
        else:
            result['original_user_name'] = ''

        if not can_switch:
            result['switchable_users'] = []
            return result

        users = request.env['res.users'].sudo().search_read(
            domain=[
                ('active', '=', True),
                ('share', '=', False),
                ('id', '!=', current_user.id),
            ],
            fields=['id', 'name', 'login'],
            limit=100,
            order='name asc',
        )

        base_url = request.httprequest.host_url.rstrip('/')
        for u in users:
            u['avatar_url'] = f"{base_url}/web/image/res.users/{u['id']}/image_128"

        result['switchable_users'] = users
        return result
