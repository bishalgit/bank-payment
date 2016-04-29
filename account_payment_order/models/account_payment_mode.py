# -*- coding: utf-8 -*-
# © 2009 EduSense BV (<http://www.edusense.nl>)
# © 2011-2013 Therp BV (<http://therp.nl>)
# © 2014-2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountPaymentMode(models.Model):
    """This corresponds to the object payment.mode of v8 with some
    important changes"""
    _inherit = "account.payment.mode"

    payment_order_ok = fields.Boolean(
        string='Selectable in Payment Orders', default=True)
    # Default options for the "payment.order.create" wizard
    default_payment_mode = fields.Selection([
        ('same', 'Same'),
        ('same_or_null', 'Same or empty'),
        ('any', 'Any'),
        ], string='Payment Mode on Invoice', default='same')
    default_journal_ids = fields.Many2many(
        'account.journal', string="Journals Filter")
    default_invoice = fields.Boolean(
        string='Linked to an Invoice or Refund', default=False)
    default_date_type = fields.Selection([
        ('due', 'Due'),
        ('move', 'Move'),
        ], default='due', string="Type of Date Filter")
    group_lines = fields.Boolean(
        string="Group lines in payment orders", default=True,
        help="If this mark is checked, the payment order lines will be "
             "grouped when validating the payment order before exporting the "
             "bank file. The grouping will be done only if the following "
             "fields matches:\n"
             "* Partner\n"
             "* Currency\n"
             "* Destination Bank Account\n"
             "* Communication Type (structured, free)\n"
             "* Payment Date\n"
             "(other modules can set additional fields to restrict the "
             "grouping.)")

    @api.onchange('payment_method_id')
    def payment_method_id_change(self):
        if self.payment_method_id:
            ajo = self.env['account.journal']
            aj_ids = []
            if self.payment_method_id.payment_type == 'outbound':
                aj_ids = ajo.search([
                    ('type', 'in', ('purchase_refund', 'purchase'))]).ids
            elif self.payment_method_id.payment_type == 'inbound':
                aj_ids = ajo.search([
                    ('type', 'in', ('sale_refund', 'sale'))]).ids
            self.default_journal_ids = [(6, 0, aj_ids)]
