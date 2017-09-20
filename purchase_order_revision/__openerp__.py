# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    @author Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': "Purchase order revisions",
    'version': '7.0.1.0.1',
    'category': 'Purchase Management',
    'description': """
Revisions for purchase orders (and requests for quotation)
==========================================================

On canceled orders, you can click on "New revision" button. This
will create a new revision of the quotation, with the same base number and a
'-revno' suffix appended. A message is added in the chatter saying that a new
revision was created.

In the form view, a new tab is added that lists the previous revisions, with
the date they were made obsolete and the user who performed the action.

The old revisions of a purchase order are flagged as inactive, so they don't
clutter up searches.
""",
    'author': "Agile Business Group,Odoo Community Association (OCA)",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends": ['purchase'],
    "data": [
        'purchase_view.xml',
    ],
    "demo": [],
    "test": [
        'test/purchase_order.yml',
    ],
    "active": False,
    "installable": True
}
