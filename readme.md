# CarbonTrace CLI

#### Video Demo: <URL OF YOUR 3-MINUTE VIDEO PRESENTATION>

#### Description:
CarbonTrace CLI is a command-line application built in Python that empowers users to track and understand their personal carbon footprint. In an age where climate change is a pressing global issue, this tool provides a simple, accessible way for individuals to quantify their environmental impact from daily activities like transportation and energy use. The project was developed as the final project for Harvard's CS50's Introduction to Programming with Python course.

The application is designed to be lightweight and runs entirely in the terminal, requiring no graphical user interface. It stores all user data locally in a `footprint_log.csv` file, ensuring user privacy and data portability.

**Core Features:**
*   **Log Emissions:** Users can calculate and log their carbon footprint for two main categories:
    *   **Transport:** Based on the mode (car, bus, train) and distance traveled (in km).
    *   **Energy:** Based on household electricity consumption (in kWh).
    Emissions are calculated in kilograms of CO₂ using standard emission factors stored in `emission_factors.json`.
*   **View Log:** A complete history of all logged emissions can be viewed directly in the terminal, formatted for readability.
*   **Summarize Data:** The tool provides a powerful summary view that aggregates total emissions by both month (e.g., `2025-11`) and category (e.g., `Transport`), allowing users to easily spot trends in their carbon output.

**Project Structure and Design:**

This project is implemented in a single Python script, `project.py`, which contains the main application logic. The design is modular, with distinct functions for core functionalities:
*   `main()`: Serves as the main entry point and runs the primary user interaction loop.
*   `calculate_emission()`: A custom function that takes an activity category and value, reads from `emission_factors.json`, and returns the calculated CO₂ emissions.
*   `add_log_entry()`: A custom function that appends a new record to the `footprint_log.csv` file, demonstrating file I/O operations with the `csv` module.
*   `get_summary()`: A custom function that reads all records from the log file and performs data aggregation to calculate monthly and categorical totals.

A key design choice was to use a JSON file for emission factors. This decouples the data from the code, making it easy to update or add new factors without modifying the Python script. For data storage, a CSV file was chosen for its simplicity and universal compatibility, allowing users to open their log in any spreadsheet program.

The project is also thoroughly tested using `pytest`. The test suite, located in `test_project.py`, covers the three main custom functions, ensuring that calculations are correct, file writing is accurate, and data summarization works as expected. This focus on testing ensures the application is reliable and maintainable.
```
