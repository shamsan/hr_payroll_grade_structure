from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class HrContract(models.Model):
    _inherit = 'hr.contract'

    salary_grade_id = fields.Many2one(
        comodel_name='hr.salary.grade',
        string='Salary Grade',
        tracking=True,
        help='Select the salary grade for this contract'
    )
    grade_level_id = fields.Many2one(
        comodel_name='hr.grade.level',
        string='Grade Level',
        tracking=True,
        domain="[('salary_grade_id', '=', salary_grade_id)]",
        help='Select the grade level - must belong to the selected salary grade'
    )
    basic_salary = fields.Monetary(
        string='Basic Salary',
        currency_field='currency_id',
        tracking=True,
        help='Basic salary amount from grade level'
    )
    allowances = fields.Monetary(
        string='Allowances',
        currency_field='currency_id',
        tracking=True,
        help='Allowances amount from grade level'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        required=True
    )

    @api.onchange('salary_grade_id')
    def _onchange_salary_grade(self):
        """Clear grade level when salary grade changes"""
        if self.salary_grade_id:
            # Clear grade_level_id if it doesn't belong to the new salary_grade
            if self.grade_level_id and self.grade_level_id.salary_grade_id != self.salary_grade_id:
                self.grade_level_id = False
        else:
            # Clear grade_level_id if no salary_grade is selected
            self.grade_level_id = False

    @api.onchange('grade_level_id')
    def _onchange_grade_level(self):
        """Clear basic_salary and allowances when grade level changes"""
        # Don't show preview warning, user will click Apply button when ready
        pass

    @api.constrains('salary_grade_id', 'grade_level_id')
    def _check_grade_level_belongs_to_grade(self):
        """Ensure selected grade level belongs to selected salary grade"""
        for record in self:
            if record.grade_level_id and record.salary_grade_id:
                if record.grade_level_id.salary_grade_id != record.salary_grade_id:
                    raise ValidationError(_(
                        'The selected Grade Level does not belong to the selected Salary Grade!\n'
                        'Please select a valid grade level for the chosen salary grade.'
                    ))

    def action_apply_salary_structure(self):
        """Apply salary structure from grade level to contract"""
        self.ensure_one()
        
        # Validation: Check if both grade and level are selected
        if not self.salary_grade_id:
            raise UserError(_('Please select a Salary Grade first!'))
        
        if not self.grade_level_id:
            raise UserError(_('Please select a Grade Level first!'))
        
        # Validation: Ensure grade level belongs to selected grade
        if self.grade_level_id.salary_grade_id != self.salary_grade_id:
            raise UserError(_(
                'The selected Grade Level does not belong to the selected Salary Grade!\n'
                'Please select a valid combination.'
            ))
        
        # Get values from grade level BEFORE write
        basic_salary = self.grade_level_id.basic_salary
        allowances = self.grade_level_id.allowances
        total_wage = basic_salary + allowances
        
        # Apply the salary structure
        self.write({
            'basic_salary': basic_salary,
            'allowances': allowances,
            'wage': total_wage,
        })
        
        # Return True to refresh the form
        return True
