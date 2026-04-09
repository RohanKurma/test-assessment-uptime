"""Business logic for payroll calculation.

The processor keeps all payroll rules in one place so that the models stay
simple and the rules are easy to test.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Iterable, List, Tuple

from .models import Employee, EmployeeType, PaySlip


class PayrollProcessor:
    """Processes payroll calculations for employees.

    This class contains methods for gross pay, progressive tax, deductions,
    payslip generation, and monthly payroll processing.
    """

    @staticmethod
    def _to_decimal(value: Decimal | int | float | str) -> Decimal:
        """Convert an input value to Decimal safely.

        Converting through `str` helps avoid binary floating-point precision
        issues when users pass floats.
        """

        return Decimal(str(value))

    @staticmethod
    def _round_money(amount: Decimal) -> Decimal:
        """Round a currency amount to 2 decimal places."""

        return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def calculate_gross_pay(self, employee: Employee, hours_or_days: Decimal | int | float | str) -> Decimal:
        """Calculate gross pay based on employee type.

        Args:
            employee: Employee whose pay is being calculated.
            hours_or_days: Hours worked for part-time employees or days worked
                for contractors. For full-time employees, the value is ignored
                after validation.

        Returns:
            Gross pay rounded to 2 decimal places.

        Raises:
            ValueError: If work quantity is negative or part-time hours exceed 120.
        """

        quantity = self._to_decimal(hours_or_days)

        if quantity < 0:
            raise ValueError("Hours or days worked cannot be negative.")

        if employee.employee_type == EmployeeType.FULL_TIME:
            gross_pay = employee.pay_rate
        elif employee.employee_type == EmployeeType.PART_TIME:
            if quantity > Decimal("120"):
                raise ValueError("Part-time employees cannot work more than 120 hours per month.")
            gross_pay = employee.pay_rate * quantity
        elif employee.employee_type == EmployeeType.CONTRACTOR:
            gross_pay = employee.pay_rate * quantity
        else:
            raise ValueError("Unsupported employee type.")

        return self._round_money(gross_pay)

    def calculate_tax(self, gross_pay: Decimal | int | float | str) -> Decimal:
        """Calculate progressive tax using the provided salary brackets.

        Brackets:
            - 0% for first 1000
            - 10% for 1001 to 3000
            - 20% for 3001 to 5000
            - 30% above 5000

        Args:
            gross_pay: Gross salary amount.

        Returns:
            Progressive tax rounded to 2 decimal places.

        Raises:
            ValueError: If gross pay is negative.
        """

        gross = self._to_decimal(gross_pay)

        if gross < 0:
            raise ValueError("Gross pay cannot be negative.")

        tax = Decimal("0")

        # Tax on the amount between 1000 and 3000.
        if gross > Decimal("1000"):
            taxable_at_10 = min(gross, Decimal("3000")) - Decimal("1000")
            tax += taxable_at_10 * Decimal("0.10")

        # Tax on the amount between 3000 and 5000.
        if gross > Decimal("3000"):
            taxable_at_20 = min(gross, Decimal("5000")) - Decimal("3000")
            tax += taxable_at_20 * Decimal("0.20")

        # Tax on the amount above 5000.
        if gross > Decimal("5000"):
            taxable_at_30 = gross - Decimal("5000")
            tax += taxable_at_30 * Decimal("0.30")

        return self._round_money(tax)

    def calculate_deductions(self, employee: Employee, gross_pay: Decimal | int | float | str) -> Dict[str, Decimal]:
        """Calculate all applicable deductions for an employee.

        Deductions included:
            - Health insurance: 150 flat, only for full-time employees
            - Retirement: 5% of gross pay if enabled
            - Union dues: 50 flat if employee is a union member

        Args:
            employee: Employee whose deductions are being calculated.
            gross_pay: Gross pay used for percentage-based deductions.

        Returns:
            Dictionary mapping deduction names to rounded values.
        """

        gross = self._to_decimal(gross_pay)
        deductions: Dict[str, Decimal] = {}

        if employee.employee_type == EmployeeType.FULL_TIME:
            deductions["health_insurance"] = self._round_money(Decimal("150"))

        if employee.has_retirement:
            deductions["retirement"] = self._round_money(gross * Decimal("0.05"))

        if employee.is_union_member:
            deductions["union_dues"] = self._round_money(Decimal("50"))

        return deductions

    def generate_pay_slip(self, employee: Employee, hours_or_days: Decimal | int | float | str) -> PaySlip:
        """Generate a payslip for one employee.

        Args:
            employee: Employee whose payroll is being processed.
            hours_or_days: Work quantity used for part-time and contractor pay.

        Returns:
            A populated PaySlip instance.
        """

        gross_pay = self.calculate_gross_pay(employee, hours_or_days)
        tax_amount = self.calculate_tax(gross_pay)
        deductions = self.calculate_deductions(employee, gross_pay)
        total_deductions = sum(deductions.values(), Decimal("0"))
        net_pay = gross_pay - tax_amount - total_deductions

        return PaySlip(
            employee=employee,
            gross_pay=self._round_money(gross_pay),
            tax_amount=self._round_money(tax_amount),
            deductions={key: self._round_money(value) for key, value in deductions.items()},
            net_pay=self._round_money(net_pay),
        )

    def process_monthly_payroll(self, employee_data: Iterable[Tuple[Employee, Decimal | int | float | str]]) -> List[PaySlip]:
        """Process payroll for multiple employees.

        The assessment specifies `processMonthlyPayroll(employeeList)`, but
        part-time and contractor payroll requires work quantity. For that
        reason, this implementation accepts an iterable of `(employee, hours_or_days)`.

        Args:
            employee_data: Iterable of tuples containing an employee and the
                associated work quantity for that month.

        Returns:
            List of generated payslips.
        """

        pay_slips: List[PaySlip] = []

        for employee, hours_or_days in employee_data:
            pay_slips.append(self.generate_pay_slip(employee, hours_or_days))

        return pay_slips
