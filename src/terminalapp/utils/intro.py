from pyfiglet import Figlet

def print_intro():
    """Display the welcome screen with ASCII art."""
    # ANSI color codes
    LIGHT_BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Clear screen effect with some spacing
    print("\n" * 2)
    
    # Welcome box with light blue border
    box_width = 80
    welcome_text = "Welcome to this app"
    padding = (box_width - len(welcome_text) - 2) // 2
    
    print(f"{LIGHT_BLUE}{'═' * box_width}{RESET}")
    print(f"{LIGHT_BLUE}║{' ' * padding}{BOLD}{welcome_text}{RESET}{LIGHT_BLUE}{' ' * (box_width - len(welcome_text) - padding - 2)}║{RESET}")
    print(f"{LIGHT_BLUE}{'═' * box_width}{RESET}")
    print()
    
    # Create 3D ASCII art using pyfiglet
    #f = Figlet(font='isometric1')
    f = Figlet(font='3D-ASCII')
    #f = Figlet(font='univers')
    ascii_art = f.renderText('HELLO')
    
    # Print the ASCII art in light blue
    for line in ascii_art.split('\n'):
        print(f"{LIGHT_BLUE}{line}{RESET}")
    
    print()
    print("Your AI assistant for financial analysis.")
    print("Ask me any questions. Type 'exit' or 'quit' to end.")
    print()

