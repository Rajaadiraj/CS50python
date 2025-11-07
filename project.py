import csv
import json
import datetime
import os

LOG_FILE = "footprint_log.csv"
FACTORS_FILE = "emission_factors.json"

def main():
    """Main function to run the CarbonTrace CLI."""
    initialize_log_file()
    
    print("\n--- CarbonTrace CLI ---")
    print("Your Personal Carbon Footprint Tracker")

    while True:
        print("\nOptions: log | view | summary | quit")
        choice = input("Enter command: ").strip().lower()

        if choice == "log":
            log_emission()
        elif choice == "view":
            view_log()
        elif choice == "summary":
            display_summary()
        elif choice == "quit":
            print("Thank you for using CarbonTrace. Stay green!")
            break
        else:
            print("Invalid command. Please try again.")

def calculate_emission(category, value):
    """
    Calculates CO2 emissions in kg based on category and value.
    'category' can be 'transport' or 'energy'.
    'value' is a tuple, e.g., ('car', 100) for 100km by car, or (120,) for 120 kWh.
    """
    with open(FACTORS_FILE, 'r') as f:
        factors = json.load(f)
    
    if category == "transport":
        mode, distance = value
        factor = factors["transport"].get(mode.lower())
        if factor is None:
            raise ValueError("Invalid mode of transport.")
        return distance * factor
    elif category == "energy":
        kwh, = value
        factor = factors["energy"]["default_factor"]
        return kwh * factor
    else:
        raise ValueError("Invalid category.")

def add_log_entry(date, category, emission_kg):
    """Adds a calculated emission entry to the log file."""
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, category, f"{emission_kg:.2f}"])
    return True

def get_summary():
    """Reads the log file and returns a summary of emissions by category and month."""
    summary = {}
    with open(LOG_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                month = row["Date"][:7] # Format YYYY-MM
                category = row["Category"]
                emissions = float(row["Emission (kg CO2)"])
                
                # Sum by month
                summary[month] = summary.get(month, 0) + emissions
                # Sum by category
                summary[category] = summary.get(category, 0) + emissions
            except (ValueError, KeyError):
                continue # Skip malformed rows
    return summary

# Helper Functions for CLI
def initialize_log_file():
    """Creates the log file with a header if it doesn't exist."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "Emission (kg CO2)"])

def log_emission():
    """CLI wrapper to get user input and log an emission."""
    category = input("Enter category (transport/energy): ").strip().lower()
    try:
        if category == "transport":
            mode = input("Mode of transport (car/bus/train): ")
            distance = float(input("Distance (km): "))
            emission = calculate_emission("transport", (mode, distance))
        elif category == "energy":
            kwh = float(input("Electricity usage (kWh): "))
            emission = calculate_emission("energy", (kwh,))
        else:
            print("Invalid category.")
            return

        date = datetime.date.today().isoformat()
        add_log_entry(date, category.capitalize(), emission)
        print(f"Successfully logged {emission:.2f} kg of CO2.")

    except (ValueError, TypeError) as e:
        print(f"Error: Invalid input. {e}")

def view_log():
    """Displays all entries from the log file."""
    print("\n--- Emission Log ---")
    with open(LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(f"{row[0]:<12} | {row[1]:<12} | {row[2]:>10}")
    print("--------------------")

def display_summary():
    """Displays the emission summary."""
    print("\n--- Emission Summary ---")
    summary = get_summary()
    if not summary:
        print("No data to summarize.")
        return
    for key, value in summary.items():
        print(f"{key}: {value:.2f} kg CO2")
    print("------------------------")

if __name__ == "__main__":
    main()
