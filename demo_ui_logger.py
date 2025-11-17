#!/usr/bin/env python3
"""
Demo script showcasing the Dexter UI and Logger functionality.

This script simulates a typical agent workflow to demonstrate all the different
UI components and logging capabilities available in the Dexter utils package.
"""

import time
import random
from src.terminalapp.utils.ui import UI, show_progress, Colors
from src.terminalapp.utils.logger import Logger
from src.terminalapp.utils.intro import print_intro


def simulate_typing_delay():
    """Add a small random delay to simulate realistic interaction timing."""
    time.sleep(random.uniform(0.5, 1.5))


def simulate_processing_delay():
    """Add a longer delay to simulate processing time."""
    time.sleep(random.uniform(1.0, 3.0))


@show_progress("Analyzing financial data...", "Financial analysis complete")
def simulate_data_analysis():
    """Simulate a long-running data analysis task."""
    time.sleep(2.5)
    return {"analysis": "Stock shows positive trend", "confidence": 0.85}


def demo_basic_ui():
    """Demonstrate basic UI functionality."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}=== BASIC UI DEMO ==={Colors.ENDC}\n")
    
    ui = UI()
    
    # Test different message types
    ui.print_info("This is an informational message")
    simulate_typing_delay()
    
    ui.print_warning("This is a warning message")
    simulate_typing_delay()
    
    ui.print_error("This is an error message")
    simulate_typing_delay()
    
    # Test header
    ui.print_header("Financial Analysis Section")
    simulate_typing_delay()


def demo_task_workflow():
    """Demonstrate task workflow with UI feedback."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}=== TASK WORKFLOW DEMO ==={Colors.ENDC}\n")
    
    ui = UI()
    
    # Simulate planned tasks
    tasks = [
        {"description": "Fetch stock prices for AAPL"},
        {"description": "Calculate technical indicators"},
        {"description": "Generate investment recommendation"},
        {"description": "Create summary report"}
    ]
    
    ui.print_task_list(tasks)
    simulate_typing_delay()
    
    # Execute tasks one by one
    for task in tasks:
        task_desc = task["description"]
        ui.print_task_start(task_desc)
        simulate_processing_delay()
        ui.print_task_done(task_desc)
        simulate_typing_delay()


def demo_progress_context():
    """Demonstrate progress context manager."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}=== PROGRESS CONTEXT DEMO ==={Colors.ENDC}\n")
    
    ui = UI()
    
    # Context manager progress
    with ui.progress("Loading market data...") as spinner:
        time.sleep(1.5)
        spinner.update_message("Processing market data...")
        time.sleep(1.5)
        spinner.update_message("Finalizing analysis...")
        time.sleep(1.0)
    
    simulate_typing_delay()
    
    # Progress with custom success message
    with ui.progress("Connecting to financial API...", "Connected successfully"):
        time.sleep(2.0)
    
    simulate_typing_delay()


def demo_tool_execution():
    """Demonstrate tool execution logging."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}=== TOOL EXECUTION DEMO ==={Colors.ENDC}\n")
    
    ui = UI()
    
    # Simulate tool parameter display and results
    tool_params = {"symbol": "AAPL", "period": "1y", "interval": "1d"}
    ui.print_tool_params(str(tool_params))
    simulate_typing_delay()
    
    tool_result = {
        "status": "success", 
        "data_points": 252, 
        "last_price": 175.43,
        "volume": 45782190
    }
    ui.print_tool_run(str(tool_result))
    simulate_typing_delay()


def demo_user_interaction():
    """Demonstrate user query display."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}=== USER INTERACTION DEMO ==={Colors.ENDC}\n")
    
    ui = UI()
    
    # Simulate user queries
    queries = [
        "What's the current price of Apple stock?",
        "Show me the performance of tech stocks this quarter",
        "Should I invest in renewable energy ETFs?"
    ]
    
    for query in queries:
        ui.print_user_query(query)
        simulate_typing_delay()


def demo_final_answer():
    """Demonstrate final answer display."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}=== FINAL ANSWER DEMO ==={Colors.ENDC}\n")
    
    ui = UI()
    
    answer = """Based on my analysis of Apple Inc. (AAPL), here are my findings:

Current Stock Price: $175.43 (+2.3% today)

Technical Analysis:
• 50-day MA: $168.50 (bullish crossover)
• RSI: 62 (neutral to slightly overbought)
• MACD: Positive momentum

Fundamental Highlights:
• P/E Ratio: 28.5 (reasonable for tech)
• Revenue Growth: 8.1% YoY
• Strong cash position: $166B

Recommendation: BUY
Target Price: $185-190 (12-month outlook)

Risk Factors: Market volatility, regulatory concerns, supply chain disruptions."""
    
    ui.print_answer(answer)
    simulate_typing_delay()


def demo_logger_workflow():
    """Demonstrate Logger class functionality."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}=== LOGGER WORKFLOW DEMO ==={Colors.ENDC}\n")
    
    logger = Logger()
    
    # User query logging
    logger.log_user_query("Analyze Tesla's stock performance and provide investment advice")
    simulate_typing_delay()
    
    # Task planning
    tasks = [
        "Fetch TSLA stock data",
        "Calculate volatility metrics", 
        "Compare with sector peers",
        "Generate recommendation"
    ]
    logger.log_task_list(tasks)
    simulate_typing_delay()
    
    # Execute workflow with logging
    for task in tasks:
        logger.log_task_start(task)
        simulate_processing_delay()
        
        # Simulate tool execution
        if "Fetch" in task:
            params = {"symbol": "TSLA", "range": "6mo"}
            result = {"status": "success", "records": 126}
            logger.log_tool_run(params, result)
        elif "volatility" in task:
            params = {"method": "historical", "window": 30}
            result = {"volatility": 0.42, "percentile": 78}
            logger.log_tool_run(params, result)
        
        logger.log_task_done(task)
        simulate_typing_delay()
    
    # Risky action simulation
    logger.log_risky("execute_trade", "symbol=TSLA, quantity=100, type=market_buy")
    simulate_typing_delay()
    
    # Progress context from logger
    with logger.progress("Generating final report...", "Report generated successfully"):
        time.sleep(2.0)
    
    # Final summary
    summary = """Tesla (TSLA) Investment Analysis Summary:

Current Price: $238.45 (-1.2% today)
Volatility: High (42% annualized)
Sector Ranking: 3rd out of 12 EV companies

Key Metrics:
• Market Cap: $758B
• P/E Ratio: 54.2 (high growth premium)
• Delivery Growth: +35% YoY

Investment Recommendation: HOLD
• Strong fundamentals but high volatility
• Consider dollar-cost averaging
• Monitor Q4 delivery numbers

Risk Level: MODERATE-HIGH"""
    
    logger.log_summary(summary)


def demo_progress_decorator():
    """Demonstrate the progress decorator."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}=== PROGRESS DECORATOR DEMO ==={Colors.ENDC}\n")
    
    # Use the decorator function we defined earlier
    result = simulate_data_analysis()
    
    print(f"Analysis result: {result}")
    simulate_typing_delay()


def main():
    """Run all UI and Logger demos."""
    print(f"{Colors.BOLD}{Colors.LIGHT_BLUE}")
    print("╔" + "═" * 60 + "╗")
    print("║" + " " * 15 + "UI & LOGGER DEMO" + " " * 22 + "║") 
    print("╚" + "═" * 60 + "╝")
    print(f"{Colors.ENDC}\n")
    
    # Show intro screen
    print_intro()
    input("Press Enter to start the demo...")
    
    # Run all demos
    demo_basic_ui()
    input("\nPress Enter to continue to task workflow demo...")
    
    demo_task_workflow()
    input("\nPress Enter to continue to progress context demo...")
    
    demo_progress_context()
    input("\nPress Enter to continue to tool execution demo...")
    
    demo_tool_execution()
    input("\nPress Enter to continue to user interaction demo...")
    
    demo_user_interaction()
    input("\nPress Enter to continue to final answer demo...")
    
    demo_final_answer()
    input("\nPress Enter to continue to logger workflow demo...")
    
    demo_logger_workflow()
    input("\nPress Enter to continue to progress decorator demo...")
    
    demo_progress_decorator()
    
    # Final message
    print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 Demo completed! All UI and Logger features demonstrated.{Colors.ENDC}")
    print(f"{Colors.DIM}This demo showed:")
    print("• Basic UI messages (info, warning, error)")
    print("• Task workflow management")
    print("• Progress indicators and spinners") 
    print("• Tool execution logging")
    print("• User interaction display")
    print("• Final answer formatting")
    print("• Logger class integration")
    print(f"• Progress decorators{Colors.ENDC}\n")


if __name__ == "__main__":
    main()