import os
import tempfile
from langchain.tools import tool
from langchain_community.tools import ShellTool

# Create a temporary directory for safe file operations
TEMP_DIR = tempfile.mkdtemp()

@tool
def write_file(content: str, filename: str) -> str:
    """Write content to a file in the temporary directory."""
    filepath = os.path.join(TEMP_DIR, filename)
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@tool
def read_file(filename: str) -> str:
    """Read content from a file in the temporary directory."""
    filepath = os.path.join(TEMP_DIR, filename)
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool
def list_files() -> str:
    """List files in the temporary directory."""
    try:
        files = os.listdir(TEMP_DIR)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {str(e)}"

@tool
def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    try:
        # Use eval with restricted globals for safety
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error calculating: {str(e)}"

# Dangerous tool - simulated shell command (for demo only)
@tool
def run_command(command: str) -> str:
    """Run a shell command - DANGEROUS - for demonstration only."""
    # In a real scenario, this would be restricted or sandboxed
    # For safety, we'll just simulate and log
    return f"Simulated command execution: {command}\nOutput: Command would run but is blocked for safety."

TOOLS = [write_file, read_file, list_files, calculate, run_command]