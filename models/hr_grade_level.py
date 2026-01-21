from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrGradeLevel(models.Model):
    _name = 'hr.grade.level'
    _description = 'Grade Level'
    _order = 'salary_grade_id, level'

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True,
        help='Auto-computed display name (Grade + Level)'
    )
    salary_grade_id = fields.Many2one(
        comodel_name='hr.salary.grade',
        string='Salary Grade',
        required=True,
        ondelete='cascade',
        help='Parent salary grade'
    )
    level = fields.Selection(
        selection=[
            ('A', 'Level A'),
            ('B', 'Level B'),
            ('C', 'Level C'),
            ('D', 'Level D'),
        ],
        string='Level',
        required=True,
        help='Grade level indicator (A/B/C/D)'
    )
    basic_salary = fields.Monetary(
        string='Basic Salary',
        required=True,
        currency_field='currency_id',
        help='Base salary amount for this grade level'
    )
    allowances = fields.Monetary(
        string='Allowances',
        currency_field='currency_id',
        default=0.0,
        help='Additional allowances for this grade level'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        required=True,
        help='Currency for monetary fields'
    )

    _sql_constraints = [
        (
            'unique_grade_level',
            'UNIQUE(salary_grade_id, level)',
            'Level must be unique within the same Salary Grade! Each grade can have only one level of each type (A/B/C/D).'
        ),
    ]

    @api.depends('salary_grade_id', 'level')
    def _compute_name(self):
        """Auto-compute display name from grade and level"""
        for record in self:
            if record.salary_grade_id and record.level:
                record.name = f'{record.salary_grade_id.name} - Level {record.level}'
            else:
                record.name = 'New Grade Level'

    @api.constrains('basic_salary', 'allowances')
    def _check_salary_values(self):
        """Validate that salary values are not negative"""
        for record in self:
            if record.basic_salary < 0:
                raise ValidationError(_('Basic Salary cannot be negative!'))
            if record.allowances < 0:
                raise ValidationError(_('Allowances cannot be negative!'))

    @api.constrains('salary_grade_id', 'level')
    def _check_grade_level_combination(self):
        """Additional validation for grade-level combination"""
        for record in self:
            if not record.salary_grade_id:
                raise ValidationError(_('Salary Grade is required!'))
            if not record.level:
                raise ValidationError(_('Level is required!'))

    def name_get(self):
        """Custom name display"""
        result = []
        for record in self:
            if record.salary_grade_id and record.level:
                name = f'{record.salary_grade_id.name} - Level {record.level}'
            else:
                name = 'New Grade Level'
            result.append((record.id, name))
        return result
