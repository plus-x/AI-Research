import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from tools import TOOLS
from utils import validate_input, sanitize_input, log_agent_action, check_tool_permissions, monitor_behavior_baseline

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class SecureAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            openai_api_key=OPENAI_API_KEY,
            model="gpt-4"
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Initialize agent with tools
        self.agent = initialize_agent(
            tools=TOOLS,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )

        self.system_prompt = """
        You are a secure AI assistant with access to limited tools.
        You can write files, read files, list files, and calculate expressions.
        You CANNOT run shell commands or perform dangerous operations.
        Always validate user inputs and follow security guidelines.
        If something seems suspicious, ask for clarification or deny the request.
        """

        self.action_history = []
        self.user_role = "user"  # Could be "admin" for elevated permissions

    def process_request(self, user_input: str) -> str:
        """Process user request with security validations"""
        try:
            # Step 1: Validate input for prompt injection
            if not validate_input(user_input):
                return "Input validation failed. Request contains potentially malicious content."

            # Step 2: Sanitize input
            sanitized_input = sanitize_input(user_input)

            # Step 3: Check behavior baseline
            if not monitor_behavior_baseline(self.action_history):
                return "Request denied due to suspicious behavior pattern."

            # Step 4: Log the action
            log_agent_action("process_request", parameters={"input": sanitized_input})

            # Step 5: Process with agent
            full_prompt = f"{self.system_prompt}\n\nUser: {sanitized_input}"
            response = self.agent.run(full_prompt)

            # Step 6: Update action history
            self.action_history.append(sanitized_input)

            return response

        except Exception as e:
            return f"Error processing request: {str(e)}"

    def execute_tool_with_permission_check(self, tool_name: str, **kwargs) -> str:
        """Execute a tool only if user has permission"""
        if not check_tool_permissions(tool_name, self.user_role):
            return f"Access denied: You don't have permission to use {tool_name}"

        # Find the tool
        tool = next((t for t in TOOLS if t.name == tool_name), None)
        if not tool:
            return f"Tool {tool_name} not found"

        try:
            result = tool.run(**kwargs)
            log_agent_action("tool_execution", tool=tool_name, parameters=kwargs)
            return result
        except Exception as e:
            return f"Error executing tool: {str(e)}"

def main():
    agent = SecureAgent()

    print("Secure Agent Demo")
    print("This agent validates inputs and checks permissions to prevent tool misuse.")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("Enter your request: ")
        if user_input.lower() == 'quit':
            break

        response = agent.process_request(user_input)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    main()