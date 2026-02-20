```python
"""
Shared guardrail policies for all examples.
"""

from typing import Tuple, Dict, Any

RESTRICTED_TOPICS = {"confidential", "internal secrets", "salary"}
RESTRICTED_TOOLS = {"read_customer_data"}

def input_policy(user_text: str) -> Tuple[bool, str]:
    text = user_text.lower()
    for token in RESTRICTED_TOPICS:
        if token in text:
            return False, "Request blocked by policy: sensitive topic."
    return True, "allowed"

def tool_policy(tool_name: str, args: Dict[str, Any], role: str = "user") -> Tuple[bool, str]:
    if tool_name in RESTRICTED_TOOLS and role != "admin":
        return False, f"Tool '{tool_name}' requires admin role."
    return True, "allowed"

```