"""
Interactive user interface module 

This module provides a comprehensive UI system with colors, animations, and
formatted output for creating a professional command-line interface. It includes
spinner animations, progress indicators, and styled message formatting.
"""

import sys
import time
import threading
from contextlib import contextmanager
from typing import Optional, Callable
from functools import wraps


class Colors:
    """
    ANSI color code constants for terminal output styling.
    
    Provides a centralized collection of color codes used throughout
    the Dexter UI for consistent theming and visual hierarchy.
    """
    BLUE = "\033[94m"        # Standard blue for headers and borders
    CYAN = "\033[96m"        # Cyan for progress indicators
    GREEN = "\033[92m"       # Green for success messages
    YELLOW = "\033[93m"      # Yellow for warnings and tool output
    RED = "\033[91m"         # Red for errors and failures
    MAGENTA = "\033[95m"     # Magenta for tool parameters
    ENDC = "\033[0m"         # Reset to default color
    BOLD = "\033[1m"         # Bold text formatting
    DIM = "\033[2m"          # Dimmed text for secondary info
    WHITE = "\033[97m"       # Bright white
    LIGHT_BLUE = "\033[94m"  # Light blue matching DEXTER ASCII art theme


class Spinner:
    """
    An animated spinner that runs in a separate thread for progress indication.
    
    Uses Unicode braille patterns to create a smooth spinning animation
    while long-running operations execute. Thread-safe and designed to
    provide visual feedback without blocking the main thread.
    
    Attributes:
        FRAMES (list): Unicode braille patterns for animation frames
        message (str): Text displayed alongside the spinner
        color (str): ANSI color code for the spinner
        running (bool): Flag to control animation state
        thread (Optional[threading.Thread]): Background animation thread
    """
    
    # Unicode braille patterns create smooth spinning effect
    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def __init__(self, message: str = "", color: str = Colors.CYAN):
        """
        Initialize a new spinner instance.
        
        Args:
            message (str): Text to display next to the spinner
            color (str): ANSI color code for spinner styling
        """
        self.message = message
        self.color = color
        self.running = False
        self.thread: Optional[threading.Thread] = None
        
    def _animate(self):
        """
        Internal animation loop that runs in a separate thread.
        
        Cycles through spinner frames at a consistent rate, updating
        the terminal display in-place to create animation effect.
        """
        idx = 0
        while self.running:
            frame = self.FRAMES[idx % len(self.FRAMES)]
            # Write spinner frame and message, overwriting previous line
            sys.stdout.write(f"\r{self.color}{frame}{Colors.ENDC} {self.message}")
            sys.stdout.flush()
            time.sleep(0.08)  # ~12 FPS for smooth animation
            idx += 1
    
    def start(self):
        """
        Start the spinner animation in a background thread.
        
        Creates and starts a daemon thread to handle animation,
        ensuring it won't prevent program exit.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._animate, daemon=True)
            self.thread.start()
    
    def stop(self, final_message: str = "", symbol: str = "✓", symbol_color: str = Colors.GREEN):
        """
        Stop the spinner and optionally show a completion message.
        
        Cleanly shuts down the animation thread, clears the spinner line,
        and optionally displays a final status message with symbol.
        
        Args:
            final_message (str): Optional completion message to display
            symbol (str): Symbol to show (default: checkmark for success)
            symbol_color (str): Color for the symbol
        """
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()  # Wait for animation thread to finish
            # Clear the spinner line by overwriting with spaces
            sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
            if final_message:
                print(f"{symbol_color}{symbol}{Colors.ENDC} {final_message}")
            sys.stdout.flush()
    
    def update_message(self, message: str):
        """
        Update the spinner message while it's running.
        
        Args:
            message (str): New message to display with the spinner
        """
        self.message = message


def show_progress(message: str, success_message: str = ""):
    """
    Decorator to show progress spinner while a function executes.
    
    Wraps a function to automatically display a spinner during execution,
    with success/failure handling and message display.
    
    Args:
        message (str): Message to show during execution
        success_message (str): Optional message to show on success
        
    Returns:
        Decorator function that wraps the target function
        
    Example:
        @show_progress("Processing data...", "Data processed successfully")
        def process_data():
            # Long-running operation
            time.sleep(5)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            spinner = Spinner(message, color=Colors.CYAN)
            spinner.start()
            try:
                result = func(*args, **kwargs)
                # Show success message or convert progress message to success
                success_msg = success_message or message.replace("...", " ✓")
                spinner.stop(success_msg, symbol="✓", symbol_color=Colors.GREEN)
                return result
            except Exception as e:
                # Show failure message with error details
                spinner.stop(f"Failed: {str(e)}", symbol="✗", symbol_color=Colors.RED)
                raise
        return wrapper
    return decorator


class UI:
    """
    Interactive user interface for displaying agent progress and results.
    
    Provides a comprehensive set of methods for formatted terminal output,
    including headers, task progress, tool execution feedback, and final
    results display. Maintains consistent visual styling throughout.
    
    Attributes:
        current_spinner (Optional[Spinner]): Currently active spinner instance
    """
    
    def __init__(self):
        """Initialize the UI with no active spinner."""
        self.current_spinner: Optional[Spinner] = None
        
    @contextmanager
    def progress(self, message: str, success_message: str = ""):
        """
        Context manager for showing progress with a spinner.
        
        Automatically manages spinner lifecycle within a context,
        ensuring proper cleanup even if exceptions occur.
        
        Args:
            message (str): Message to display during progress
            success_message (str): Optional success message on completion
            
        Yields:
            Spinner: The spinner instance for potential message updates
            
        Example:
            with ui.progress("Loading data...") as spinner:
                # Long-running operation
                data = load_data()
                spinner.update_message("Processing data...")
                process_data(data)
        """
        spinner = Spinner(message, color=Colors.CYAN)
        self.current_spinner = spinner
        spinner.start()
        try:
            yield spinner
            # Show success message or convert progress message
            success_msg = success_message or message.replace("...", " ✓")
            spinner.stop(success_msg, symbol="✓", symbol_color=Colors.GREEN)
        except Exception as e:
            spinner.stop(f"Failed: {str(e)}", symbol="✗", symbol_color=Colors.RED)
            raise
        finally:
            self.current_spinner = None
    
    def print_header(self, text: str):
        """
        Print a section header with decorative border styling.
        
        Args:
            text (str): The header text to display
        """
        print(f"\n{Colors.BOLD}{Colors.BLUE}╭─ {text}{Colors.ENDC}")
    
    def print_user_query(self, query: str):
        """
        Print the user's query with consistent branding styling.
        
        Uses the same light blue color as the DEXTER ASCII art
        to maintain visual consistency throughout the interface.
        
        Args:
            query (str): The user's input query
        """
        print(f"\n{Colors.BOLD}{Colors.LIGHT_BLUE}You: {query}{Colors.ENDC}\n")
    
    def print_task_list(self, tasks):
        """
        Print a formatted list of planned tasks with borders.
        
        Creates a bordered box containing all planned tasks,
        providing users with clear visibility into upcoming work.
        
        Args:
            tasks: List of task objects or descriptions to display
        """
        if not tasks:
            return
        self.print_header("Planned Tasks")
        for i, task in enumerate(tasks):
            status = "+"  # Plus symbol indicates planned task
            color = Colors.DIM
            # Handle both dict objects and simple strings
            desc = task.get('description', task) if hasattr(task, 'get') else task
            print(f"{Colors.BLUE}│{Colors.ENDC} {color}{status}{Colors.ENDC} {desc}")
        print(f"{Colors.BLUE}╰{'─' * 50}{Colors.ENDC}\n")
    
    def print_task_start(self, task_desc: str):
        """
        Print a task start indicator with play symbol.
        
        Args:
            task_desc (str): Description of the task being started
        """
        print(f"\n{Colors.BOLD}{Colors.CYAN}▶ Task:{Colors.ENDC} {task_desc}")
    
    def print_task_done(self, task_desc: str):
        """
        Print a task completion indicator with checkmark.
        
        Args:
            task_desc (str): Description of the completed task
        """
        print(f"{Colors.GREEN}  ✓ Completed{Colors.ENDC} {Colors.DIM}│ {task_desc}{Colors.ENDC}")
    
    def print_tool_params(self, params: str):
        """
        Print tool parameters before execution for transparency.
        
        Args:
            params (str): String representation of tool parameters
        """
        params_display = f" {Colors.DIM}{params}{Colors.ENDC}" if params and len(params) > 0 else ""
        print(f"  {Colors.MAGENTA}→{Colors.ENDC}  Parameters: {params_display}")
    
    def print_tool_run(self, result: str):
        """
        Print tool execution result with truncation for long outputs.
        
        Args:
            result (str): String representation of tool result
        """
        # Truncate long results to keep output manageable
        result_display = f" {Colors.DIM}({result[:150]}...){Colors.ENDC}" if result and len(result) > 0 else ""
        print(f"  {Colors.YELLOW}⚡{Colors.ENDC} Result: {result_display}")
    
    def print_answer(self, answer: str):
        """
        Print the final answer in a prominent bordered box.
        
        Creates an attractive, attention-grabbing display for final
        answers with proper word wrapping and consistent formatting.
        
        Args:
            answer (str): The answer text to display prominently
        """
        width = 80
        
        # Top border with double line style
        print(f"\n{Colors.BOLD}{Colors.BLUE}╔{'═' * (width - 2)}╗{Colors.ENDC}")
        
        # Centered title
        title = "ANSWER"
        padding = (width - len(title) - 2) // 2
        print(f"{Colors.BOLD}{Colors.BLUE}║{' ' * padding}{title}{' ' * (width - len(title) - padding - 2)}║{Colors.ENDC}")
        
        # Separator line
        print(f"{Colors.BLUE}╠{'═' * (width - 2)}╣{Colors.ENDC}")
        
        # Answer content with proper line wrapping
        print(f"{Colors.BLUE}║{Colors.ENDC}{' ' * (width - 2)}{Colors.BLUE}║{Colors.ENDC}")
        for line in answer.split('\n'):
            if len(line) == 0:
                # Empty line
                print(f"{Colors.BLUE}║{Colors.ENDC}{' ' * (width - 2)}{Colors.BLUE}║{Colors.ENDC}")
            else:
                # Word wrap long lines to fit within box
                words = line.split()
                current_line = ""
                for word in words:
                    # Check if adding this word would exceed width
                    if len(current_line) + len(word) + 1 <= width - 6:
                        current_line += word + " "
                    else:
                        if current_line:
                            print(f"{Colors.BLUE}║{Colors.ENDC} {current_line.ljust(width - 4)} {Colors.BLUE}║{Colors.ENDC}")
                        current_line = word + " "
                if current_line:
                    print(f"{Colors.BLUE}║{Colors.ENDC} {current_line.ljust(width - 4)} {Colors.BLUE}║{Colors.ENDC}")
        
        print(f"{Colors.BLUE}║{Colors.ENDC}{' ' * (width - 2)}{Colors.BLUE}║{Colors.ENDC}")
        
        # Bottom border
        print(f"{Colors.BOLD}{Colors.BLUE}╚{'═' * (width - 2)}╝{Colors.ENDC}\n")
    
    def print_info(self, message: str):
        """
        Print an informational message in dimmed text.
        
        Args:
            message (str): The informational message to display
        """
        print(f"{Colors.DIM}{message}{Colors.ENDC}")
    
    def print_error(self, message: str):
        """
        Print an error message with error symbol and red styling.
        
        Args:
            message (str): The error message to display
        """
        print(f"{Colors.RED}✗ Error:{Colors.ENDC} {message}")
    
    def print_warning(self, message: str):
        """
        Print a warning message with warning symbol and yellow styling.
        
        Args:
            message (str): The warning message to display
        """
        print(f"{Colors.YELLOW}⚠ Warning:{Colors.ENDC} {message}")

