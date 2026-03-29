# ASI02: Tool Misuse and Exploitation - Implementation

This implementation demonstrates the Tool Misuse and Exploitation vulnerability (ASI02) from the OWASP Top 10 for Agentic Applications 2026.

## Description

Agents can misuse legitimate tools due to prompt injection, misalignment, or unsafe delegation. This implementation shows:

1. A vulnerable agent that can be tricked into misusing tools via prompt injection
2. A secure agent with mitigations applied
3. Test cases demonstrating the vulnerability and mitigation effectiveness

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Run the vulnerable agent:
   ```bash
   python vulnerable_agent.py
   ```

4. Run the secure agent:
   ```bash
   python secure_agent.py
   ```

5. Run tests:
   ```bash
   python test_injection.py
   ```

## Files

- `vulnerable_agent.py`: Agent without proper safeguards
- `secure_agent.py`: Agent with ASI02 mitigations
- `test_injection.py`: Test script to demonstrate prompt injection attacks
- `tools.py`: Custom tools for the agent
- `utils.py`: Utility functions for input validation and monitoring