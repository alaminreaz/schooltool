#
# SchoolTool - common information systems platform for school administration
# Copyright (c) 2006 Shuttleworth Foundation
#
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
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
Upgrade SchoolTool to generation 17.

Install catalog and reindex persons.

$Id: evolve17.py 6212 2006-06-08 13:01:04Z vidas $
"""

from zope.app.generations.utility import findObjectsProviding
from zope.app.publication.zopepublication import ZopePublication
from zope.lifecycleevent import ObjectModifiedEvent
from zope.app.container.contained import ObjectAddedEvent
from zope import event
from zope.app.component.hooks import setSite
from zope.app.intid import addIntIdSubscriber

from schooltool.demographics.utility import catalogSetUpSubscriber,\
     personFactorySetUpSubscriber
from schooltool.app.interfaces import ISchoolToolApplication

def evolve(context):
    root = context.connection.root()[ZopePublication.root_name]
    for app in findObjectsProviding(root, ISchoolToolApplication):
        # install the utilities
        catalogSetUpSubscriber(app, None)
        personFactorySetUpSubscriber(app, None)
        # catalog all persons
        setSite(app)
        for person in app['persons'].values():
            person.nameinfo.last_name = 'Last name unknown'
            addIntIdSubscriber(person, None)