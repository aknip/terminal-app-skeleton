import time
from prompt_toolkit import prompt
from src.terminalapp.utils.ui import show_progress

@show_progress("Planning tasks...", "Tasks planned")
def func1():
    print("\033[?25l", end='')  # Hide cursor
    print("Step1", end='', flush=True)
    time.sleep(3)
    print("Step2...", end='', flush=True)
    time.sleep(3)
    print("\033[?25h", end='')  # Show cursor

text = prompt("Give me some input: ")
print(f"You said: {text}", end='', flush=True)
func1()



