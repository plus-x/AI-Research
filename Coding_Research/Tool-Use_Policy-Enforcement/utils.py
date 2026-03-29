import re
import logging
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_input(user_input: str) -> bool:
    """Validate user input for potential prompt injection patterns."""
    # Check for common prompt injection patterns
    injection_patterns = [
        r'\b(ignore|forget|override)\s+(previous|all|these)\s+(instructions?|rules?)',
        r'\b(system|developer|admin)\s+(mode|prompt|instruction)',
        r'\bDAN\b',  # Common jailbreak
        r'\bYou are now\b.*\bAI\b',  # Role change attempts
        r'\bExecute\b.*\bas\b.*\broot\b',  # Privilege escalation
    ]

    for pattern in injection_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            logger.warning(f"Potential prompt injection detected: {pattern}")
            return False

    return True

def sanitize_input(user_input: str) -> str:
    """Sanitize user input by removing or escaping potentially dangerous content."""
    # Remove or escape special markers
    sanitized = re.sub(r'[<>]', '', user_input)  # Remove angle brackets
    sanitized = re.sub(r'\b(system|assistant|user):\s*', '', sanitized, flags=re.IGNORECASE)
    return sanitized.strip()

def log_agent_action(action: str, tool: str = None, parameters: Dict[str, Any] = None):
    """Log agent actions for monitoring."""
    log_entry = {
        "action": action,
        "tool": tool,
        "parameters": parameters,
        "timestamp": "2026-03-25T12:00:00Z"  # Mock timestamp
    }
    logger.info(f"Agent action logged: {log_entry}")

def check_tool_permissions(tool_name: str, user_role: str = "user") -> bool:
    """Check if the user has permission to use a specific tool."""
    # Define tool permissions
    restricted_tools = {
        "run_command": ["admin"],  # Only admin can run commands
        "write_file": ["user", "admin"],  # Users can write files
        "read_file": ["user", "admin"],
        "list_files": ["user", "admin"],
        "calculate": ["user", "admin"]
    }

    allowed_roles = restricted_tools.get(tool_name, [])
    return user_role in allowed_roles

def monitor_behavior_baseline(actions: List[str]) -> bool:
    """Monitor agent behavior against baseline."""
    # Simple baseline: no more than 5 actions in a session
    if len(actions) > 5:
        logger.warning("Agent behavior deviates from baseline: too many actions")
        return False

    # Check for suspicious patterns
    suspicious_patterns = ["delete", "rm", "format", "drop table"]
    for action in actions:
        if any(pattern in action.lower() for pattern in suspicious_patterns):
            logger.warning(f"Suspicious action detected: {action}")
            return False

    return True