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
from ..models import IPNetworks
from dc2.core.modules.usersgroups.db.models import User

class IPNetworkController(BaseController):

    def __init__(self, session=None):
        super(IPNetworkController, self).__init__(session)

    def list(self):
        try:
            result = IPNetworks.query.all()
            return result
        except Exception as e:
            print(e)
            return None

    def find(self):
        pass


    def find_by_network(self, ipnetwork=None):
        if ipnetwork is not None:
            try:
                result = IPNetworks.query.filter_by(ipnetwork=ipnetwork).first()
                if result is not None:
                    return result
                else:
                    return None
            except Exception as e:
                return None
        return None

    def new(self, ipnetwork=None, description=None, username=None):
        if ipnetwork is not None and username is not None:
            try:
                user = User.query.filter_by(username=username).first()
                record = IPNetworks()
                record.ipnetwork = ipnetwork
                record.description = description
                record.created_by = user
                record.updated_by = user
                record = self.add(record)
                return record
            except Exception:
                print(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
                return None
        return None

    def get(self):
        pass

    def delelte(self):
        pass

    def update(self):
        pass
