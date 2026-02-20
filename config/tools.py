```python
"""
Simulated enterprise tools.
"""

def send_email(email: str, message: str) -> str:
    return f"Email sent to {email}: {message}"

def read_customer_data(customer_id: str) -> str:
    return f"Customer {customer_id}: [RESTRICTED DATA]"

TOOL_REGISTRY = {
    "send_email": send_email,
    "read_customer_data": read_customer_data,
}

OPENAI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email to a customer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "message": {"type": "string"},
                },
                "required": ["email", "message"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_customer_data",
            "description": "Read customer data by id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                },
                "required": ["customer_id"],
            },
        },
    },
]

```