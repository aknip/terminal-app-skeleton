"""
Command Line Interface for Dexter AI Assistant.

Provides agent selection and interactive capabilities using the UI and Logger systems.
"""

from terminalapp.agent_demo import AgentDemo
from terminalapp.utils.intro import print_intro
from terminalapp.utils.ui import UI
from terminalapp.utils.logger import Logger
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory



def run_simple_agent():
    """Run the simple interactive agent."""
    agent = AgentDemo()
    agent.run()


def main():
    """Main CLI entry point with agent selection."""
    # Initialize UI and Logger for CLI interactions
    ui = UI()
    logger = Logger()
    
    # Show intro screen
    print_intro()

    run_simple_agent()


if __name__ == "__main__":
    main()
