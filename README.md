# W34D2_Assignment

# Logger System Technical Documentation

## Overview

This document explains the implementation of a flexible logging system that supports multiple output formats (console, file, and database). The system uses two key design patterns to achieve flexibility, maintainability, and extensibility.

## Design Patterns Used

### 1. Strategy Pattern

**What it is:** The Strategy pattern allows you to define a family of algorithms (in this case, logging methods), encapsulate each one, and make them interchangeable at runtime.

**Why I chose it:** Different applications need different logging approaches. Some need console output for development, others need file logging for production, and enterprise applications might need database logging for analytics. The Strategy pattern lets us switch between these approaches without changing the main Logger class.

**How it works in our code:**
- `LogStrategy` is the abstract base class that defines the interface
- `ConsoleLogStrategy`, `FileLogStrategy`, and `DatabaseLogStrategy` are concrete implementations
- The `Logger` class uses whatever strategy is given to it, without knowing the details

**Benefits:**
- Easy to add new logging formats without modifying existing code
- Can switch logging methods at runtime
- Each logging method is isolated and testable

### 2. Factory Pattern  

**What it is:** The Factory pattern provides a way to create objects without specifying their exact class. Instead, you ask the factory for what you want, and it gives you the right object.

**Why I chose it:** Creating the right logging strategy could get complicated, especially with different configuration options. The Factory pattern centralizes this logic and makes it easy to add new strategies.

**How it works in our code:**
- `LogStrategyFactory.create_strategy()` takes a string like "console" or "file"
- It returns the appropriate strategy object
- Additional parameters can be passed for configuration (like filename)

**Benefits:**
- Simple interface for creating complex objects
- Centralized creation logic
- Easy to extend with new strategy types

## SOLID Principles Compliance

### Single Responsibility Principle (SRP) ✅
Each class has one reason to change:
- `ConsoleLogStrategy` only handles console output
- `FileLogStrategy` only handles file operations  
- `Logger` only coordinates logging, doesn't know output details
- `LogStrategyFactory` only creates strategy objects

### Open/Closed Principle (OCP) ✅
The system is open for extension but closed for modification:
- To add a new logging format (like email alerts), you create a new strategy class
- No need to modify existing `Logger` or strategy classes
- Factory can be extended to create new strategies

### Liskov Substitution Principle (LSP) ✅
All strategy classes can be used interchangeably:
- Any `LogStrategy` subclass works with the `Logger`
- They all follow the same interface contract
- Switching strategies doesn't break functionality

### Interface Segregation Principle (ISP) ✅
The `LogStrategy` interface is focused and minimal:
- Only defines the `log()` method that strategies need
- No unnecessary methods that some strategies wouldn't use
- Clean, focused interface

### Dependency Inversion Principle (DIP) ✅
High-level modules don't depend on low-level modules:
- `Logger` depends on the abstract `LogStrategy`, not concrete implementations
- This allows easy testing and flexibility
- Strategies can be injected from outside

## Trade-offs and Alternatives Considered

### Trade-offs Made

**Complexity vs Flexibility:**
- **Pro:** Very flexible and extensible
- **Con:** More complex than a simple logging function
- **Decision:** Chose flexibility because logging requirements often change

**Memory vs Features:**
- **Pro:** Rich feature set with multiple output formats
- **Con:** Uses more memory than basic logging
- **Decision:** Modern applications can afford this overhead for better maintainability

### Alternatives Considered

**1. Simple Function Approach**
```python
def log(message, output_type="console"):
    if output_type == "console":
        print(message)
    elif output_type == "file":
        # file logic
```
**Rejected because:** Hard to extend, violates Open/Closed Principle

**2. Inheritance-Based Approach**
```python
class Logger:
    def log(self): pass

class ConsoleLogger(Logger):
    def log(self): # console logic
```
**Rejected because:** Less flexible than composition, harder to switch at runtime

**3. Observer Pattern**
Could notify multiple outputs simultaneously.
**Rejected because:** Overkill for this use case, Strategy pattern is simpler

## Future Extensibility

The design makes several extensions easy:

### Adding New Output Formats
```python
class EmailLogStrategy(LogStrategy):
    def log(self, level, message, timestamp):
        # Send email for critical errors
        pass

class SlackLogStrategy(LogStrategy):
    def log(self, level, message, timestamp):
        # Post to Slack channel
        pass
```

### Adding Log Filtering
```python
class FilteredLogger(Logger):
    def __init__(self, strategy, min_level="INFO"):
        super().__init__(strategy)
        self.min_level = min_level
    
    def _log(self, level, message):
        if self._should_log(level):
            super()._log(level, message)
```

### Adding Log Formatting
```python
class FormattedLogStrategy(LogStrategy):
    def __init__(self, base_strategy, formatter):
        self.base_strategy = base_strategy
        self.formatter = formatter
    
    def log(self, level, message, timestamp):
        formatted_message = self.formatter.format(message)
        self.base_strategy.log(level, formatted_message, timestamp)
```

### Configuration-Driven Setup
```python
def create_logger_from_config(config):
    strategy_type = config["output_type"]
    strategy_params = config["params"]
    strategy = LogStrategyFactory.create_strategy(strategy_type, **strategy_params)
    return Logger(strategy)
```

## Usage Examples

**Basic Usage:**
```python
# Create logger with console output
logger = Logger(LogStrategyFactory.create_strategy("console"))
logger.info("Hello, World!")
```

**Runtime Strategy Switching:**
```python
# Start with console, switch to file
logger = Logger(LogStrategyFactory.create_strategy("console"))
logger.info("Starting application")

logger.set_strategy(LogStrategyFactory.create_strategy("file"))
logger.info("Switched to file logging")
```

**Multiple Loggers:**
```python
# Different loggers for different purposes
error_logger = Logger(LogStrategyFactory.create_strategy("database"))
debug_logger = Logger(LogStrategyFactory.create_strategy("console"))

error_logger.error("Critical database error")
debug_logger.debug("User clicked button")
```

## Conclusion

This logging system demonstrates how design patterns can create flexible, maintainable code. The Strategy and Factory patterns work together to provide a system that's easy to use, extend, and test. While more complex than a simple logging function, the investment in good design pays off when requirements change or the system needs to scale.