from datetime import datetime


def calculator(a: float, b: float, operation: str):
    """
    Perform a basic mathematical calculation.
    """

    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":

        if b == 0:
            return "Error: Cannot divide by zero."

        return a / b

    else:
        return f"Error: Unknown operation '{operation}'."


def get_current_time():
    """
    Return the current local date and time.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# Tool registry
AVAILABLE_TOOLS = {
    "calculator": calculator,
    "get_current_time": get_current_time,
}