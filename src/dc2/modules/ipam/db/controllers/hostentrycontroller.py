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

import sys

try:
    from sqlalchemy.exc import IntegrityError
except ImportError as e:
    raise e

from dc2.core.database.controllers import BaseController
from ..models import IPNetworks, IPAddresses, HostEntry
from dc2.core.modules.usersgroups.db.models import User


class HostEntryController(BaseController):

    def __init__(self, session=None):
        super(HostEntryController, self).__init__(session)

    def list(self):
        try:
            result = HostEntry.query.all()
            return result
        except Exception as e:
            print(e)
            return None

    def find(self):
        pass

    def new(self, hostname=None, username=None):
        if hostname is not None and username is not None:
            try:
                user = User.query.filter_by(username=username).first()
                hostentry = HostEntry()
                hostentry.hostname = hostname
                hostentry.created_by = user
                record = self.add(hostentry)
                return record
            except Exception as e:
                print(e)
                return None
        return None

    def new_with_ipaddress(self, hostname=None, ipaddress=None, ipnetwork=None, username=None):
        if hostname is not None and ipaddress is not None and username is not None and ipnetwork is not None:
            try:
                user = User.query.filter_by(username=username).first()
                print(user.username)
                print(user.id)
                ipnetwork_rec = IPNetworks.query.filter_by(ipnetwork=ipnetwork).first()
                hostentry = HostEntry.query.filter_by(hostname=hostname).first()
                if hostentry is None:
                    hostentry = self.new(hostname, username)
                ipaddress_rec = IPAddresses()
                ipaddress_rec.ipaddress = ipaddress
                ipaddress_rec.created_by = user
                ipaddress_rec.ipnetwork = ipnetwork_rec
                ipaddress_rec.hostentry = hostentry
                result = self.add(ipaddress_rec)
                return hostentry, result
            except Exception as e:
                raise e

        return None, None

    def get(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass
