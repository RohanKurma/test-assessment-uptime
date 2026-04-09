"""Demo script for the payroll calculator.

Run with:
    python -m src.payroll.demo
"""

from decimal import Decimal

from .models import Employee, EmployeeType
from .payroll_processor import PayrollProcessor


def format_currency(amount: Decimal) -> str:
    """Return a currency string with two decimal places."""

    return f"${amount:.2f}"


def main() -> None:
    """Create sample employees and print their payslips."""

    processor = PayrollProcessor()

    employees_with_work = [
        (
            Employee(1, "Alice Johnson", EmployeeType.FULL_TIME, Decimal("4500.00"), False, True),
            Decimal("0"),
        ),
        (
            Employee(2, "Brian Smith", EmployeeType.FULL_TIME, Decimal("6200.00"), True, True),
            Decimal("0"),
        ),
        (
            Employee(3, "Catherine Lee", EmployeeType.PART_TIME, Decimal("25.00"), False, False),
            Decimal("80"),
        ),
        (
            Employee(4, "Daniel Brown", EmployeeType.PART_TIME, Decimal("18.50"), True, True),
            Decimal("120"),
        ),
        (
            Employee(5, "Eva Wilson", EmployeeType.CONTRACTOR, Decimal("300.00"), False, False),
            Decimal("12"),
        ),
        (
            Employee(6, "Frank Taylor", EmployeeType.CONTRACTOR, Decimal("425.00"), True, True),
            Decimal("15"),
        ),
    ]

    pay_slips = processor.process_monthly_payroll(employees_with_work)

    print("MONTHLY PAYROLL SUMMARY")
    print("=" * 80)

    for slip in pay_slips:
        print(f"Employee ID: {slip.employee.id}")
        print(f"Name      : {slip.employee.name}")
        print(f"Type      : {slip.employee.employee_type.value}")
        print(f"Gross Pay : {format_currency(slip.gross_pay)}")
        print(f"Tax       : {format_currency(slip.tax_amount)}")
        print("Deductions:")

        if slip.deductions:
            for deduction_name, amount in slip.deductions.items():
                print(f"  - {deduction_name}: {format_currency(amount)}")
        else:
            print("  - None")

        print(f"Net Pay   : {format_currency(slip.net_pay)}")
        print("-" * 80)


if __name__ == "__main__":
    main()
