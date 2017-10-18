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

from openerp.osv import fields, orm
from openerp.tools.translate import _


class purchase_order(orm.Model):

    _inherit = "purchase.order"

    _columns = {
        'current_revision_id': fields.many2one(
            'purchase.order', 'Current revision', readonly=True),
        'old_revision_ids': fields.one2many(
            'purchase.order', 'current_revision_id',
            'Old revisions', context={'active_test': False}, readonly=True),
        'revision_number': fields.integer('Revision'),
        'unrevisioned_name': fields.char(
            'Order Reference', readonly=True),
        'active': fields.boolean('Active', readonly=True),
    }

    _defaults = {
        'active': True,
    }

    _sql_constraints = [
        ('revision_unique',
         'unique(unrevisioned_name, revision_number, company_id)',
         'Order Reference and revision must be unique per Company.'),
    ]

    def new_revision(self, cr, uid, ids, context=None):
        if len(ids) > 1:
            raise orm.except_orm(
                _('Error'), _('This only works for 1 PO at a time'))
        po = self.browse(cr, uid, ids[0], context)
        old_name = po.name
        revno = po.revision_number
        po.write({'name': '%s-%02d' % (po.unrevisioned_name, revno + 1),
                 'revision_number': revno + 1})
        # 'orm.Model.copy' is called instead of 'self.copy' in order to avoid
        # 'purchase.order' method to overwrite our values, like name and state
        defaults = {'name': old_name,
                    'revision_number': revno,
                    'active': False,
                    'state': 'cancel',
                    'current_revision_id': po.id,
                    'unrevisioned_name': po.unrevisioned_name,
                    'shipped': False,
                    'invoiced': False,
                    'picking_ids': [],
                    'old_revision_ids': [],
                    }
        old_revision_id = orm.Model.copy(
            self, cr, uid, po.id, default=defaults, context=context)
        self.action_cancel_draft(cr, uid, [po.id], context=context)
        msg = _('New revision created: %s') % po.name
        self.message_post(cr, uid, [po.id], body=msg, context=context)
        self.message_post(
            cr, uid, [old_revision_id], body=msg, context=context)
        return True

    def create(self, cr, uid, vals, context=None):
        if 'unrevisioned_name' not in vals:
            if vals.get('name', '/') == '/':
                seq = self.pool['ir.sequence']
                vals['name'] = seq.next_by_code(
                    cr, uid, 'purchase.order', context=context) or '/'
            vals['unrevisioned_name'] = vals['name']
        return super(purchase_order, self).create(
            cr, uid, vals, context=context)

    def copy_data(self, cr, uid, id, default=None, context=None):
        """ This trick is meant to allow duplication
        preventing the copy of the following fields: old_revision_ids,
        revision_number and unrevisioned_name
        considering that in old API "copy=False" doesn't work
        """
        res = super(purchase_order, self).copy_data(
            cr, uid, id, default=default, context=context)
        if 'old_revision_ids' in res and res['old_revision_ids']:
            del res['old_revision_ids']
        if 'revision_number' in res and res['revision_number']:
            del res['revision_number']
        if 'unrevisioned_name' in res and res['unrevisioned_name']:
            del res['unrevisioned_name']
        return res
