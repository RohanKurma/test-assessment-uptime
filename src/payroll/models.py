"""Data models used by the payroll calculator.

This module defines the core data structures for the payroll assignment.
The objects are intentionally small and focused so the business logic can
stay inside the payroll processor.
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Dict


class EmployeeType(Enum):
    """Supported employee categories for payroll processing."""

    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACTOR = "CONTRACTOR"


@dataclass(frozen=True)
class Employee:
    """Represents an employee and the payroll settings tied to that employee.

    Attributes:
        id: Unique employee identifier.
        name: Employee name.
        employee_type: Category of employee that determines pay logic.
        pay_rate: Monthly salary, hourly rate, or daily rate depending on type.
        is_union_member: Whether union dues should be applied.
        has_retirement: Whether retirement deduction should be applied.
    """

    id: int
    name: str
    employee_type: EmployeeType
    pay_rate: Decimal
    is_union_member: bool
    has_retirement: bool


@dataclass
class PaySlip:
    """Represents the result of payroll calculation for one employee.

    Attributes:
        employee: Employee whose payroll was processed.
        gross_pay: Pay before tax and deductions.
        tax_amount: Progressive tax amount.
        deductions: Dictionary of deduction names to amounts.
        net_pay: Final pay after tax and deductions.
    """

    employee: Employee
    gross_pay: Decimal
    tax_amount: Decimal
    deductions: Dict[str, Decimal]
    net_pay: Decimal
