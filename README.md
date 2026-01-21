# HR Payroll Grade Structure

## Overview

This **Odoo 18** module provides a comprehensive salary grade structure system integrated with HR contracts.

## Features

### Core Models

1. **Salary Grade (hr.salary.grade)**
   - Name, Code, Sequence fields
   - One2many relationship to Grade Levels
   - Unique code constraint

2. **Grade Level (hr.grade.level)**
   - Four levels: A, B, C, D
   - Basic Salary and Allowances
   - Unique constraint: one level per grade
   - Validation: prevents negative salary values
   - Auto-computed display name

3. **HR Contract Extension**
   - Salary Grade and Grade Level fields
   - Basic Salary and Allowances fields
   - Domain constraint: Grade Level must belong to selected Salary Grade
   - Professional XPath view inheritance

### Business Constraints

- ✅ Prevent duplicate Levels (A/B/C/D) within the same Salary Grade
- ✅ Prevent selecting a Grade Level that does not belong to the selected Salary Grade
- ✅ Prevent invalid data (negative salary values, empty names)
- ✅ Unique code for each Salary Grade

### User Interface

- **List and Form views** for Salary Grades (Odoo 18 compatible)
- **List and Form views** for Grade Levels (Odoo 18 compatible)
- Grade Levels displayed inside Salary Grade form using editable list
- Clean, logical field layout with proper grouping
- Professional XPath inheritance for contract views
- Menu items under **HR → Salary Structure**

### Apply Salary Structure Button

- Button in HR Contract form (appears only when both Grade and Level are selected)
- Automatically populates Basic Salary and Allowances
- Calculates total Wage (Basic Salary + Allowances)
- Validates all data before applying
- Shows success notification with applied values

## Installation

1. Copy the module to your Odoo addons directory
2. Restart Odoo server
3. Update the app list: **Apps → Update Apps List**
4. Search for "HR Payroll Grade Structure"
5. Click **Install**

## Usage

### Creating Salary Grades

1. Go to **HR → Salary Structure → Salary Grades**
2. Create a new grade (e.g., "Senior Developer" with code "SD")
3. Add levels in the Grade Levels tab:
   - Level A: Basic Salary 80,000, Allowances 10,000
   - Level B: Basic Salary 70,000, Allowances 8,000
   - Level C: Basic Salary 60,000, Allowances 6,000
   - Level D: Basic Salary 50,000, Allowances 5,000

### Applying to Contracts

1. Go to **HR → Contracts**
2. Open or create an HR Contract
3. Scroll to **Salary Structure** section
4. Select a **Salary Grade**
5. Select a **Grade Level** (only levels from selected grade will appear)
6. Click **"Apply Salary Structure"** button
7. Basic Salary, Allowances, and Wage will be automatically populated
8. Save the contract

## Technical Details

### Module Structure

```
hr_payroll_grade_structure/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── hr_salary_grade.py
│   ├── hr_grade_level.py
│   └── hr_contract.py
├── views/
│   ├── hr_salary_grade_views.xml
│   ├── hr_grade_level_views.xml
│   ├── hr_contract_views.xml
│   └── menu_items.xml
├── security/
│   └── ir.model.access.csv
└── README.md
```

### Dependencies

- `base` - Odoo base module
- `hr` - Human Resources
- `hr_contract` - HR Contracts

### Security Groups

- **HR User**: Read-only access to Salary Grades and Grade Levels
- **HR Manager**: Full CRUD access to Salary Grades and Grade Levels

### Odoo 18 Compatibility

This module is fully compatible with **Odoo 18** and includes:

- ✅ List views (instead of deprecated tree views)
- ✅ Professional XPath view inheritance
- ✅ Modern UI/UX patterns
- ✅ Proper field positioning and grouping

## Version

- **Version**: 1.0.0
- **Odoo**: 18.0
- **License**: LGPL-3

## Author

Shamsan Mohammed

## Support

For issues or questions, please contact sm777822275@gmail.com.
