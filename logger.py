# Simple Logger System - Easy to understand version
# Uses Strategy and Factory patterns in the most basic way possible

from abc import ABC, abstractmethod
from datetime import datetime
import json

# ============================================================================
# STRATEGY PATTERN - Different ways to output logs
# ============================================================================

class LogStrategy(ABC):
    """Base class - all logging methods must have a 'write' function"""
    
    @abstractmethod
    def write(self, message: str):
        pass

class ConsoleLogger(LogStrategy):
    """Prints logs to the screen"""
    
    def write(self, message: str):
        print(message)

class FileLogger(LogStrategy):
    """Saves logs to a text file"""
    
    def write(self, message: str):
        with open("app.log", "a") as file:
            file.write(message + "\n")

class JSONLogger(LogStrategy):
    """Saves logs to a JSON file (like a simple database)"""
    
    def write(self, message: str):
        # Create log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        
        # Read existing logs (or create empty list)
        try:
            with open("logs.json", "r") as file:
                logs = json.load(file)
        except FileNotFoundError:
            logs = []
        
        # Add new log and save
        logs.append(log_entry)
        with open("logs.json", "w") as file:
            json.dump(logs, file, indent=2)

# ============================================================================
# FACTORY PATTERN - Easy way to create loggers
# ============================================================================

def create_logger(log_type: str):
    """Factory function - give it a type, get back a logger"""
    
    if log_type == "console":
        return ConsoleLogger()
    elif log_type == "file":
        return FileLogger()
    elif log_type == "json":
        return JSONLogger()
    else:
        raise ValueError(f"Unknown logger type: {log_type}")

# ============================================================================
# MAIN LOGGER - Uses different strategies to write logs
# ============================================================================

class Logger:
    """Main logger class - can switch between different output methods"""
    
    def __init__(self, strategy):
        self.strategy = strategy
    
    def change_output(self, new_strategy):
        """Switch to a different logging method"""
        self.strategy = new_strategy
    
    def log(self, level: str, message: str):
        """Write a log message with timestamp and level"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}"
        self.strategy.write(formatted_message)
    
    # Shortcut methods for common log levels
    def info(self, message: str):
        self.log("INFO", message)
    
    def error(self, message: str):
        self.log("ERROR", message)
    
    def warning(self, message: str):
        self.log("WARNING", message)

# ============================================================================
# DEMO - Show how it works
# ============================================================================

def demo():
    print("=== Simple Logger Demo ===\n")
    
    # 1. Console logging
    print("1. Logging to console:")
    console_strategy = create_logger("console")
    logger = Logger(console_strategy)
    
    logger.info("App started")
    logger.warning("Low memory")
    logger.error("File not found")
    
    print("\n" + "-"*30 + "\n")
    
    # 2. Switch to file logging
    print("2. Switching to file logging:")
    file_strategy = create_logger("file")
    logger.change_output(file_strategy)
    
    logger.info("Now logging to file")
    logger.error("Database connection failed")
    print("Check 'app.log' file!")
    
    print("\n" + "-"*30 + "\n")
    
    # 3. Switch to JSON logging
    print("3. Switching to JSON logging:")
    json_strategy = create_logger("json")
    logger.change_output(json_strategy)
    
    logger.info("Now logging to JSON")
    logger.warning("API rate limit reached")
    print("Check 'logs.json' file!")
    
    print("\n" + "-"*30 + "\n")
    
    # 4. Multiple loggers
    print("4. Using multiple loggers at once:")
    
    console_logger = Logger(create_logger("console"))
    file_logger = Logger(create_logger("file"))
    
    console_logger.info("This goes to console")
    file_logger.info("This goes to file")
    
    print("\nDone! Check the files to see the saved logs.")

# Run the demo
if __name__ == "__main__":
    demo()