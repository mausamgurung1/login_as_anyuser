# -*- coding: utf-8 -*-
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class LoginAsUserController(http.Controller):

    @http.route('/web/login_as_user', type='json', auth='user', methods=['POST'])
    def login_as_user(self, user_id):
        current = request.env.user.sudo()
        # Must have permission OR already be in a switched state
        original_uid = request.session.get('original_uid')
        if not current.any_userlogin and not original_uid:
            return {'success': False, 'error': 'You do not have permission to switch users.'}

        target = request.env['res.users'].sudo().browse(int(user_id))

        if not target.exists() or not target.active:
            return {'success': False, 'error': 'Target user does not exist or is inactive.'}

        if target.share:
            return {'success': False, 'error': 'Cannot switch to a portal or public user.'}

        if target.id == current.id:
            return {'success': False, 'error': 'You are already logged in as this user.'}

        # Store original user the FIRST time only (not overwritten on re-switch)
        if not original_uid:
            request.session['original_uid'] = current.id

        # Perform session switch
        request.session.uid = target.id
        request.session.login = target.login
        request.session.session_token = target._compute_session_token(request.session.sid)

        _logger.info(
            "User %s (%s) switched session to %s (%s).",
            current.name, current.login, target.name, target.login,
        )
        return {'success': True}

    @http.route('/web/switch_back', type='json', auth='user', methods=['POST'])
    def switch_back(self):
        original_uid = request.session.get('original_uid')
        if not original_uid:
            return {'success': False, 'error': 'No original user to switch back to.'}

        original_user = request.env['res.users'].sudo().browse(int(original_uid))
        if not original_user.exists() or not original_user.active:
            return {'success': False, 'error': 'Original user no longer exists.'}

        current = request.env.user
        # Clear the stored original uid before switching back
        del request.session['original_uid']

        request.session.uid = original_user.id
        request.session.login = original_user.login
        request.session.session_token = original_user._compute_session_token(request.session.sid)

        _logger.info(
            "Switched back from %s (%s) to original user %s (%s).",
            current.name, current.login, original_user.name, original_user.login,
        )
        return {'success': True}
