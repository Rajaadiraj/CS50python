from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Emission Factors (in kg CO2e per unit) ---
# Sources are based on EPA and other environmental agencies.
# Converted to kg per mile or per unit for consistency.
EMISSION_FACTORS = {
    # Transportation (per mile)
    "personal_car": 0.404,  # kg CO2/mile for a typical passenger car
    "public_transit": 0.089, # kg CO2/mile (average for bus/train)
    "flights": 0.251,       # kg CO2/mile for domestic flights (per passenger)

    # Household Energy
    "electricity": 0.475,   # kg CO2/kWh (US average)
    "natural_gas": 5.3,     # kg CO2/therm
}

# --- Constants ---
KG_TO_TONS = 0.00110231
TONS_CO2_PER_TREE = 0.024 # Assumes one mature tree absorbs 48 lbs (0.024 tons) of CO2 per year

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    # --- Get Monthly Inputs ---
    personal_car_miles = float(data.get('personal_car', 0))
    public_transit_miles = float(data.get('public_transit', 0))
    flights_miles_yearly = float(data.get('flights', 0)) # This is a yearly input
    electricity_kwh = float(data.get('electricity', 0))
    natural_gas_therms = float(data.get('natural_gas', 0))

    # --- Annual Emission Calculations (in tons CO2) ---

    # 1. Transportation
    car_emissions = (personal_car_miles * 12) * EMISSION_FACTORS["personal_car"] * KG_TO_TONS
    transit_emissions = (public_transit_miles * 12) * EMISSION_FACTORS["public_transit"] * KG_TO_TONS
    flight_emissions = flights_miles_yearly * EMISSION_FACTORS["flights"] * KG_TO_TONS
    total_transport_emissions = car_emissions + transit_emissions + flight_emissions

    # 2. Household Energy
    electricity_emissions = (electricity_kwh * 12) * EMISSION_FACTORS["electricity"] * KG_TO_TONS
    natural_gas_emissions = (natural_gas_therms * 12) * EMISSION_FACTORS["natural_gas"] * KG_TO_TONS
    total_energy_emissions = electricity_emissions + natural_gas_emissions

    # 3. Total Annual Footprint
    total_annual_emissions = total_transport_emissions + total_energy_emissions

    # --- Trees to Offset ---
    trees_needed = 0
    if total_annual_emissions > 0:
        trees_needed = round(total_annual_emissions / TONS_CO2_PER_TREE)

    # --- Category Percentages ---
    transport_percentage = 0
    energy_percentage = 0
    if total_annual_emissions > 0:
        transport_percentage = round((total_transport_emissions / total_annual_emissions) * 100)
        energy_percentage = round((total_energy_emissions / total_annual_emissions) * 100)

    # --- Prepare JSON Response ---
    response_data = {
        "total_annual_footprint": round(total_annual_emissions, 2),
        "trees_to_offset": trees_needed,
        "transportation": {
            "total": round(total_transport_emissions, 2),
            "percentage": transport_percentage,
            "car": round(car_emissions, 2),
            "transit": round(transit_emissions, 2),
            "flights": round(flight_emissions, 2),
        },
        "household_energy": {
            "total": round(total_energy_emissions, 2),
            "percentage": energy_percentage,
            "electricity": round(electricity_emissions, 2),
            "natural_gas": round(natural_gas_emissions, 2),
        }
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
