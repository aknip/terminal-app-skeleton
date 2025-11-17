"""
Logger module for Dexter AI assistant.

This module provides a logging interface that wraps the UI system to provide
consistent, formatted output for different types of agent activities and states.
"""

from terminalapp.utils.ui import UI


class Logger:
    """
    Logger that uses the interactive UI system for formatted output.
    
    This class acts as a bridge between the agent's logging needs and the UI system,
    providing semantic methods for different types of log messages while maintaining
    a consistent visual style throughout the application.
    
    Attributes:
        ui (UI): The UI instance used for formatted output
        log (list): Internal log storage for message history
    """
    
    def __init__(self):
        """Initialize the logger with a UI instance and empty log storage."""
        self.ui = UI()
        self.log = []  # Store log messages for potential later retrieval

    def _log(self, msg: str):
        """
        Print a message immediately and store it in the log history.
        
        Args:
            msg (str): The message to print and store
        """
        print(msg, flush=True)  # Immediate output with buffer flush
        self.log.append(msg)    # Store for history

    def log_header(self, msg: str):
        """
        Log a section header using the UI formatting.
        
        Args:
            msg (str): The header text to display
        """
        self.ui.print_header(msg)
    
    def log_user_query(self, query: str):
        """
        Log a user query with appropriate formatting and styling.
        
        Args:
            query (str): The user's query text
        """
        self.ui.print_user_query(query)

    def log_task_list(self, tasks):
        """
        Log a list of planned tasks in a formatted display.
        
        Args:
            tasks: List of task objects or task descriptions to display
        """
        self.ui.print_task_list(tasks)

    def log_task_start(self, task_desc: str):
        """
        Log the start of a task with visual indicators.
        
        Args:
            task_desc (str): Description of the task being started
        """
        self.ui.print_task_start(task_desc)

    def log_task_done(self, task_desc: str):
        """
        Log the completion of a task with success indicators.
        
        Args:
            task_desc (str): Description of the completed task
        """
        self.ui.print_task_done(task_desc)
        
    def log_tool_run(self, params: dict, result: dict):
        """
        Log the execution of a tool with its parameters and results.
        
        Args:
            params (dict): The parameters passed to the tool
            result (dict): The result returned by the tool
        """
        self.ui.print_tool_params(str(params))
        self.ui.print_tool_run(str(result))

    def log_risky(self, tool: str, input_str: str):
        """
        Log potentially risky actions that were auto-confirmed.
        
        This method is used to alert users when the system performs
        actions that could have side effects or security implications.
        
        Args:
            tool (str): Name of the tool being executed
            input_str (str): Input parameters for the risky action
        """
        self.ui.print_warning(f"Risky action {tool}({input_str}) — auto-confirmed")

    def log_summary(self, summary: str):
        """
        Log a final summary or answer in a prominent display box.
        
        Args:
            summary (str): The summary text to display prominently
        """
        self.ui.print_answer(summary)
    
    def progress(self, message: str, success_message: str = ""):
        """
        Return a progress context manager for showing loading states.
        
        This method provides a context manager that displays a spinner
        while long-running operations execute, with automatic cleanup
        and success/failure messaging.
        
        Args:
            message (str): The message to show during progress
            success_message (str): Optional success message to show on completion
            
        Returns:
            Context manager that handles spinner lifecycle
        """
        return self.ui.progress(message, success_message)
