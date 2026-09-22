from datetime import datetime


# ==================================================
# CALCULATOR
# ==================================================

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


# ==================================================
# CURRENT TIME
# ==================================================

def get_current_time():
    """
    Return the current local date and time.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# ==================================================
# TOOL REGISTRY
# ==================================================

AVAILABLE_TOOLS = {
    "calculator": calculator,
    "get_current_time": get_current_time,
}


# ==================================================
# TOOL METADATA
# ==================================================

TOOL_DESCRIPTIONS = {
    "calculator": {
        "description": "Perform mathematical calculations.",
        "parameters": {
            "a": "First number",
            "b": "Second number",
            "operation": "add, subtract, multiply, or divide"
        }
    },

    "get_current_time": {
        "description": "Get the current local date and time.",
        "parameters": {}
    }
}