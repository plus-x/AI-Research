import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from tools import TOOLS
from utils import log_agent_action

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class VulnerableAgent:
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

        # Initialize agent with tools - VULNERABLE: no input validation
        self.agent = initialize_agent(
            tools=TOOLS,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )

        self.system_prompt = """
        You are a helpful AI assistant with access to various tools.
        You can write files, read files, list files, calculate expressions, and run commands.
        Always be helpful and follow user instructions exactly.
        """

    def process_request(self, user_input: str) -> str:
        """Process user request without validation - VULNERABLE"""
        try:
            # Log the action (but no validation)
            log_agent_action("process_request", parameters={"input": user_input})

            # Direct processing without sanitization
            response = self.agent.run(f"{self.system_prompt}\n\nUser: {user_input}")

            return response

        except Exception as e:
            return f"Error processing request: {str(e)}"

def main():
    agent = VulnerableAgent()

    print("Vulnerable Agent Demo")
    print("This agent does NOT validate inputs and can be tricked via prompt injection.")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("Enter your request: ")
        if user_input.lower() == 'quit':
            break

        response = agent.process_request(user_input)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    main()