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
    from dc2.core.auth.decorators import needs_authentication, has_groups
except ImportError as e:
    raise e

try:
    from ...helpers.inputs.ipnetwork import type_ipv4_network
    from ...db.controllers import IPNetworkController
except ImportError as e:
    raise(e)

try:
    import ipaddress
except ImportError as e:
    raise(e)

_ipinfo_parser = RequestParser()
_ipinfo_parser.add_argument('ipnetwork', default=None, type=str, location="args")

class IPNetworkInfos(RestResource):

    def __init__(self, *args, **kwargs):
        super(IPNetworkInfos, self).__init__(*args, **kwargs)
        self._ctl_ipnetworks = IPNetworkController(DB.Session)

    @needs_authentication
    @has_groups(['admin', 'users'])
    def get(self):
        app.logger.info('hello')
        args = _ipinfo_parser.parse_args()
        if args.ipnetwork is not None:
            app.logger.info(args.ipnetwork)
            try:
                rec_ipnetwork = self._ctl_ipnetworks.find_by_network(args.ipnetwork)
                if rec_ipnetwork is not None:
                    ipnetwork = ipaddress.ip_network(rec_ipnetwork.ipnetwork)
                    ipnetwork_dict = dict(
                        ip_version=ipnetwork.version,
                        ip_is_private=ipnetwork.is_private,
                        ip_is_multicast=ipnetwork.is_multicast,
                        ip_network_address=str(ipnetwork.network_address),
                        ip_broadcast_address=str(ipnetwork.broadcast_address),
                        ip_netmask=str(ipnetwork.netmask),
                        ip_hostmask=str(ipnetwork.hostmask),
                        ip_max_usable_hosts=len(list(ipnetwork.hosts()))
                    )
                    return ipnetwork_dict, 200
            except Exception as e:
                app.logger.exception(msg="Exception Occured")
                return {'error': True, 'message': e.args}, 400
        return {'error': True, 'message': 'No Ip Address Given'}, 400


