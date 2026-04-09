"""Unit tests for payroll processing logic."""

from decimal import Decimal

import pytest

from src.payroll.models import Employee, EmployeeType
from src.payroll.payroll_processor import PayrollProcessor


@pytest.fixture
def processor() -> PayrollProcessor:
    """Return a payroll processor instance for tests."""

    return PayrollProcessor()


@pytest.fixture
def full_time_employee() -> Employee:
    """Return a sample full-time employee."""

    return Employee(1, "Alice", EmployeeType.FULL_TIME, Decimal("4000.00"), True, True)


@pytest.fixture
def part_time_employee() -> Employee:
    """Return a sample part-time employee."""

    return Employee(2, "Bob", EmployeeType.PART_TIME, Decimal("20.00"), False, False)


@pytest.fixture
def contractor_employee() -> Employee:
    """Return a sample contractor."""

    return Employee(3, "Carol", EmployeeType.CONTRACTOR, Decimal("300.00"), False, True)


def test_calculate_gross_pay_for_full_time(processor: PayrollProcessor, full_time_employee: Employee) -> None:
    """Full-time gross pay should equal fixed monthly salary."""

    assert processor.calculate_gross_pay(full_time_employee, Decimal("0")) == Decimal("4000.00")


def test_calculate_gross_pay_for_part_time(processor: PayrollProcessor, part_time_employee: Employee) -> None:
    """Part-time gross pay should equal hourly rate times hours worked."""

    assert processor.calculate_gross_pay(part_time_employee, Decimal("100")) == Decimal("2000.00")


def test_calculate_gross_pay_for_contractor(processor: PayrollProcessor, contractor_employee: Employee) -> None:
    """Contractor gross pay should equal daily rate times days worked."""

    assert processor.calculate_gross_pay(contractor_employee, Decimal("10")) == Decimal("3000.00")


def test_part_time_hours_above_limit_raises_error(processor: PayrollProcessor, part_time_employee: Employee) -> None:
    """Part-time employees cannot exceed 120 hours."""

    with pytest.raises(ValueError, match="120 hours"):
        processor.calculate_gross_pay(part_time_employee, Decimal("121"))


def test_negative_work_quantity_raises_error(processor: PayrollProcessor, contractor_employee: Employee) -> None:
    """Negative hours or days should be rejected."""

    with pytest.raises(ValueError, match="cannot be negative"):
        processor.calculate_gross_pay(contractor_employee, Decimal("-1"))


def test_tax_below_or_equal_to_1000_is_zero(processor: PayrollProcessor) -> None:
    """No tax should apply to the first 1000 dollars."""

    assert processor.calculate_tax(Decimal("1000.00")) == Decimal("0.00")


def test_tax_at_2500(processor: PayrollProcessor) -> None:
    """Tax at 2500 should apply only the 10 percent bracket portion."""

    assert processor.calculate_tax(Decimal("2500.00")) == Decimal("150.00")


def test_tax_at_4500(processor: PayrollProcessor) -> None:
    """Tax at 4500 should include both 10 percent and 20 percent bracket portions."""

    assert processor.calculate_tax(Decimal("4500.00")) == Decimal("500.00")


def test_tax_at_7000(processor: PayrollProcessor) -> None:
    """Tax at 7000 should include all bracket portions progressively."""

    assert processor.calculate_tax(Decimal("7000.00")) == Decimal("1200.00")


def test_calculate_deductions_for_full_time_union_retirement(
    processor: PayrollProcessor,
    full_time_employee: Employee,
) -> None:
    """Full-time employee with union and retirement should get all applicable deductions."""

    deductions = processor.calculate_deductions(full_time_employee, Decimal("4000.00"))

    assert deductions == {
        "health_insurance": Decimal("150.00"),
        "retirement": Decimal("200.00"),
        "union_dues": Decimal("50.00"),
    }


def test_generate_pay_slip(processor: PayrollProcessor, full_time_employee: Employee) -> None:
    """Generated payslip should include gross pay, tax, deductions, and net pay."""

    payslip = processor.generate_pay_slip(full_time_employee, Decimal("0"))

    assert payslip.gross_pay == Decimal("4000.00")
    assert payslip.tax_amount == Decimal("400.00")
    assert payslip.deductions == {
        "health_insurance": Decimal("150.00"),
        "retirement": Decimal("200.00"),
        "union_dues": Decimal("50.00"),
    }
    assert payslip.net_pay == Decimal("3200.00")


def test_process_monthly_payroll_returns_multiple_payslips(
    processor: PayrollProcessor,
    full_time_employee: Employee,
    part_time_employee: Employee,
) -> None:
    """Monthly payroll processing should return one payslip per employee entry."""

    results = processor.process_monthly_payroll(
        [
            (full_time_employee, Decimal("0")),
            (part_time_employee, Decimal("50")),
        ]
    )

    assert len(results) == 2
    assert results[0].employee.name == "Alice"
    assert results[1].employee.name == "Bob"
