from project import calculate_emission, add_log_entry, get_summary
import os
import csv
import pytest

# Test for the calculation function
def test_calculate_emission():
    assert calculate_emission("transport", ("car", 100)) == pytest.approx(17.0)
    assert calculate_emission("transport", ("bus", 50)) == pytest.approx(4.0)
    assert calculate_emission("energy", (150,)) == pytest.approx(67.5)
    with pytest.raises(ValueError):
        calculate_emission("transport", ("plane", 1000)) # 'plane' is not in our factors

# Test for the log entry function
def test_add_log_entry():
    # Use a temporary test file
    test_log_file = "test_log.csv"
    if os.path.exists(test_log_file):
        os.remove(test_log_file)
    
    # Redefine the global LOG_FILE for testing purposes
    import project
    project.LOG_FILE = test_log_file
    project.initialize_log_file()
    
    add_log_entry("2025-11-06", "Test", 99.99)
    
    with open(test_log_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = next(reader)
        assert data == ["2025-11-06", "Test", "99.99"]
        
    os.remove(test_log_file)
    project.LOG_FILE = "footprint_log.csv" # Reset global variable

# Test for the summary function
def test_get_summary():
    # Use a temporary test file
    test_log_file = "test_summary.csv"
    with open(test_log_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Category", "Emission (kg CO2)"])
        writer.writerow(["2025-10-01", "Transport", "17.00"])
        writer.writerow(["2025-10-15", "Energy", "50.00"])
        writer.writerow(["2025-11-01", "Transport", "8.50"])
        
    import project
    project.LOG_FILE = test_log_file
    
    summary = get_summary()
    assert summary["2025-10"] == pytest.approx(67.00)
    assert summary["Transport"] == pytest.approx(25.50)
    assert summary["2025-11"] == pytest.approx(8.50)

    os.remove(test_log_file)
    project.LOG_FILE = "footprint_log.csv" # Reset
