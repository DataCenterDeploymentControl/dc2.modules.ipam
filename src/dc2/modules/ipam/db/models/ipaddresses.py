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
    from dc2.core.database import DB
except ImportError as e:
    raise(e)

try:
    from sqlalchemy.dialects.postgresql import CIDR, INET, ENUM
except ImportError as e:
    raise(e)

import datetime


class IPAddresses(DB.Model):
    __tablename__ = 'ipaddresses'

    id = DB.Column(DB.Integer, primary_key=True)
    ipaddress = DB.Column(INET, nullable=True, unique=True)
    ipnetwork_id = DB.Column(DB.Integer, DB.ForeignKey('ipnetworks.id'))
    ipnetwork = DB.relationship('IPNetworks', uselist=False, foreign_keys="IPAddresses.ipnetwork_id")
    hostentry_id = DB.Column(DB.Integer, DB.ForeignKey('hostentries.id'))
    hostentry = DB.relationship('HostEntry', uselist=False, foreign_keys="IPAddresses.hostentry_id")
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.now())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.now())
    created_by_user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    updated_by_user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    created_by = DB.relationship("User", uselist=False, foreign_keys="IPAddresses.created_by_user_id")
    updated_by = DB.relationship("User", uselist=False, foreign_keys="IPAddresses.updated_by_user_id")

    @property
    def to_dict(self):
        return dict(id=self.id,
                    ipaddress=self.ipaddress,
                    ipnetwork=self.ipnetwork.ipnetwork,
                    hostname=self.hostentry.hostname,
                    created_at=self.created_at.isoformat() if self.created_at is not None else None,
                    updated_at=self.updated_at.isoformat() if self.updated_at is not None else None,
                    created_by=self.created_by.username if self.created_by is not None else None,
                    updated_by=self.updated_by.username if self.updated_by is not None else None
                    )
