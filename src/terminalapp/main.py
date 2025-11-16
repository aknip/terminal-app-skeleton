import time
from terminalapp.utils.ui import Spinner
from prompt_toolkit.filters import is_done
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice
from prompt_toolkit.styles import Style

class Agent:
    def __init__(self):
        pass
    
    def run(self, query: str = None):
        """
        Process user input with a choice dialog followed by a 5-second spinner animation.
        This is a skeleton implementation for a new terminal application.
        """
        # Show choice dialog
        style = Style.from_dict(
            {
                "frame.border": "#ff4444",
                "selected-option": "bold",
                # ('noreverse' because the default toolbar style uses 'reverse')
                "bottom-toolbar": "#ffffff bg:#333333 noreverse",
            }
        )

        result = choice(
            message=HTML("<u>Please select a dish</u>:"),
            options=[
                ("pizza", "Pizza with mushrooms"),
                ("salad", "Salad with tomatoes"),
                ("sushi", "Sushi"),
            ],
            style=style,
            bottom_toolbar=HTML(
                " Press <b>[Up]</b>/<b>[Down]</b> to select, <b>[Enter]</b> to accept."
            ),
            show_frame=~is_done,
        )
        print(f"You have chosen: {result}")
        
        # Show spinner for 5 seconds
        spinner = Spinner("Processing your input...", color="\033[96m")
        spinner.start()
        
        # Wait for 5 seconds
        time.sleep(5)
        
        # Stop spinner with completion message
        spinner.stop("Processing complete!", symbol="✓", symbol_color="\033[92m")
        
        # Return the chosen dish instead of the query parameter
        return f"Processed: {result}"