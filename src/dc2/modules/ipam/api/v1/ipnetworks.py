# -*- coding: utf-8 -*-
#
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

__author__ = 'stephan.adig'

try:
    from flask_restful import Resource as RestResource
    from flask_restful.reqparse import RequestParser
    from flask import g
except ImportError as e:
    raise e


try:
    from dc2.core.application import app
    from dc2.core.database import DB
    from dc2.core.helpers import hash_generator
    from dc2.core.database.errors import lookup_error
    from dc2.core.auth.decorators import needs_authentication, has_groups
except ImportError as e:
    raise e

try:
    from ...helpers.inputs.ipnetwork import type_ipv4_network
    from ...db.controllers import IPNetworkController
except ImportError as e:
    raise(e)

_ipnetwork_parser = RequestParser()
_ipnetwork_parser.add_argument('ipnetwork', type=type_ipv4_network, required=True, help="IPNetwork")
_ipnetwork_parser.add_argument('description', type=str, required=False, help="Description")


class IPNetworkCollection(RestResource):

    def __init__(self, *args, **kwargs):
        super(IPNetworkCollection, self).__init__(*args, **kwargs)
        self._ctl_ipnetworks = IPNetworkController(DB.session)

    @needs_authentication
    @has_groups(['admin','users'])
    def get(self):
        networklist = self._ctl_ipnetworks.list()
        print(g.auth_token)
        if networklist is not None:
            return [network.to_dict for network in networklist], 200

    @needs_authentication
    @has_groups(['admin','users'])
    def post(self):
        args = _ipnetwork_parser.parse_args()
        if g.auth_user is not None:
            try:
                ipnetwork = self._ctl_ipnetworks.new(args.ipnetwork, args.description, g.auth_user)
                if ipnetwork is not None:
                    return ipnetwork.to_dict, 201
            except Exception as e:
                app.logger.exception(msg="Exception occured")
                return {'error': True, 'error_code': e.error_code, 'error_message': e.error_message}, 400
        return {'error': True, 'message': 'Something went wrong'}, 400



