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
from ..models import IPNetworks, IPAddresses
from dc2.core.modules.usersgroups.db.models import User

class IPAddressesController(BaseController):

    def __init__(self, session=None):
        super(IPAddressesController, self).__init__(session)

    def list(self, ipnetwork=None):
        try:
            result = IPAddresses.query.filter_by(ipnetwork=ipnetwork).all()
            return result
        except Exception as e:
            print(e)
            return None

    def find(self):
        pass

    def new(self):
        pass

    def get(self):
        pass

    def delelte(self):
        pass

    def update(self):
        pass
