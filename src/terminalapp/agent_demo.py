"""
Simple Agent Demo - A minimal interactive agent demonstration.

This agent showcases basic UI and Logger functionality with a simple
interaction pattern: greeting, waiting, and echoing user input.
"""

import time
from terminalapp.utils.logger import Logger
from terminalapp.utils.ui import UI


class AgentDemo:
    """
    A simple agent that demonstrates basic UI and Logger usage.
    
    This agent provides a minimal interactive experience:
    1. Says hello using the logger
    2. Waits for 3 seconds with a progress indicator
    3. Asks for user input
    4. Echoes back the user's input using formatted display
    
    Attributes:
        logger (Logger): Logger instance for formatted output
        ui (UI): UI instance for direct interface methods
    """
    
    def __init__(self):
        """Initialize the simple agent with logger and UI instances."""
        self.logger = Logger()
        self.ui = UI()
    
    def greet_user(self):
        """Display a greeting message using the logger."""
        self.logger.log_header("Agent Demo - Simple Interactive Demo")
        
        # Use UI for a friendly greeting with branding colors
        greeting = "Hello! I'm Agent Demo, a simple interactive assistant."
        self.ui.print_user_query(greeting)  # Uses the same styling as user queries
    
    def wait_with_progress(self):
        """Wait for 3 seconds with a progress indicator."""
        with self.logger.progress("Initializing system...", "System ready!"):
            time.sleep(3.0)
    
    def get_user_input(self):
        """
        Get input from the user and display it back.
        
        Returns:
            str: The user's input text
        """
        # Show an info message about what we're doing
        self.ui.print_info("I'm ready to listen to you!")
        
        # Get user input
        try:
            user_input = input(f"\n🤖 Please tell me something: ")
            return user_input
        except KeyboardInterrupt:
            self.ui.print_warning("Input interrupted by user")
            return ""
        except Exception as e:
            self.ui.print_error(f"Error getting input: {e}")
            return ""
    
    def echo_user_input(self, user_input: str):
        """
        Echo back the user's input using formatted display.
        
        Args:
            user_input (str): The text the user provided
        """
        if not user_input.strip():
            self.ui.print_warning("No input received or input was empty")
            return
        
        # Create a formatted response
        response = f"""You said: "{user_input}"

Thank you for sharing that with me! I received your message successfully.

Input analysis:
• Length: {len(user_input)} characters
• Word count: {len(user_input.split())} words
• Contains numbers: {'Yes' if any(c.isdigit() for c in user_input) else 'No'}
• Contains special chars: {'Yes' if any(not c.isalnum() and not c.isspace() for c in user_input) else 'No'}"""
        
        # Display the response in the prominent answer format
        self.logger.log_summary(response)
    
    def run(self):
        """
        Run the complete agent interaction flow.
        
        This method orchestrates the full interaction:
        1. Greet the user
        2. Wait with progress indicator
        3. Get user input
        4. Echo back the input with analysis
        """
        try:
            # Step 1: Greet the user
            self.greet_user()
            
            # Step 2: Wait for 3 seconds with progress
            self.wait_with_progress()
            
            # Step 3: Get user input
            user_input = self.get_user_input()
            
            # Step 4: Echo back the input
            self.echo_user_input(user_input)
            
            # Final message
            self.ui.print_info("Agent2 interaction complete. Thank you!")
            
        except Exception as e:
            self.ui.print_error(f"Agent2 encountered an error: {e}")
        finally:
            # Always show a final goodbye
            print(f"\n👋 Goodbye from Agent2!\n")


def main():
    """Main function to run Agent Demo independently."""
    print("Starting Agent Demo - Simple Interactive Demo")
    print("=" * 50)
    
    agent = AgentDemo()
    agent.run()


if __name__ == "__main__":
    main()