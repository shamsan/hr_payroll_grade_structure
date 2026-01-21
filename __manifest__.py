{
    'name': 'HR Payroll Grade Structure',
    'version': '18.0.1.0.0',
    'category': 'Human Resources/Payroll',
    'summary': 'Salary Grade Structure & HR Contract Integration',
    'description': """
HR Payroll Grade Structure
===========================
This module provides:
- Salary Grade management with hierarchical levels (A/B/C/D)
- Business constraints for data integrity
- Integration with HR contracts
- Automatic salary structure application
    """,
    'author': 'Shamsan Mohammed',
    'website': 'https://github.com/shamsan',
    'depends': [
        'base',
        'hr',
        'hr_contract',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_salary_grade_views.xml',
        'views/hr_grade_level_views.xml',
        'views/hr_contract_views.xml',
        'views/menu_items.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
