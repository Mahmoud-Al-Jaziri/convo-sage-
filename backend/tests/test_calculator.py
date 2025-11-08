"""Tests for the calculator tool."""
import pytest
from app.tools.calculator import CalculatorTool


def test_calculator_basic_addition():
    """Test basic addition."""
    calc = CalculatorTool()
    result = calc._run("5+3")
    assert "8" in result
    assert "5+3" in result


def test_calculator_multiplication():
    """Test multiplication."""
    calc = CalculatorTool()
    result = calc._run("10*2")
    assert "20" in result


def test_calculator_complex_expression():
    """Test complex expression with parentheses."""
    calc = CalculatorTool()
    result = calc._run("(5+3)*2")
    assert "16" in result


def test_calculator_division():
    """Test division."""
    calc = CalculatorTool()
    result = calc._run("10/2")
    assert "5" in result


def test_calculator_power():
    """Test power operation."""
    calc = CalculatorTool()
    result = calc._run("2**3")
    assert "8" in result


def test_calculator_division_by_zero():
    """Test division by zero error handling."""
    calc = CalculatorTool()
    result = calc._run("5/0")
    assert "Error" in result
    assert "zero" in result.lower()


def test_calculator_invalid_expression():
    """Test invalid expression error handling."""
    calc = CalculatorTool()
    result = calc._run("5+*3")
    assert "Error" in result


def test_calculator_invalid_characters():
    """Test security - reject invalid characters."""
    calc = CalculatorTool()
    result = calc._run("5+3; import os")
    assert "Error" in result
    assert "Invalid characters" in result


def test_calculator_with_spaces():
    """Test calculator handles spaces in expression."""
    calc = CalculatorTool()
    result = calc._run("5 + 3")
    assert "8" in result


def test_calculator_name_and_description():
    """Test that calculator has proper name and description."""
    calc = CalculatorTool()
    assert calc.name == "calculator"
    assert "mathematical" in calc.description.lower() or "calculation" in calc.description.lower()


@pytest.mark.asyncio
async def test_calculator_async():
    """Test async version of calculator."""
    calc = CalculatorTool()
    result = await calc._arun("10+5")
    assert "15" in result

