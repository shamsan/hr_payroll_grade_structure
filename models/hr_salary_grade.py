from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrSalaryGrade(models.Model):
    _name = 'hr.salary.grade'
    _description = 'Salary Grade'
    _order = 'sequence, name'

    name = fields.Char(
        string='Grade Name',
        required=True,
        help='Name of the salary grade (e.g., Manager, Senior Developer)'
    )
    code = fields.Char(
        string='Code',
        required=True,
        help='Unique code for the salary grade'
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Order sequence for display and sorting'
    )
    grade_level_ids = fields.One2many(
        comodel_name='hr.grade.level',
        inverse_name='salary_grade_id',
        string='Grade Levels',
        help='Levels associated with this salary grade'
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'The salary grade code must be unique!'),
    ]

    @api.constrains('name')
    def _check_name(self):
        """Validate that name is not empty"""
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError(_('Grade name cannot be empty!'))

    def name_get(self):
        """Custom name display"""
        result = []
        for record in self:
            name = f'[{record.code}] {record.name}'
            result.append((record.id, name))
        return result
