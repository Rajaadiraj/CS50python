document.addEventListener('DOMContentLoaded', function() {

    // --- Element Selections ---
    const heroCtaButton = document.getElementById('hero-cta-button');
    const calculatorSection = document.getElementById('calculator-section');
    const resultsSection = document.getElementById('results-section');
    const carbonForm = document.getElementById('carbon-form');
    const startOverButton = document.getElementById('start-over-button');
    const recalculateButton = document.getElementById('recalculate-button');

    // --- Event Listeners ---

    // Smooth scroll from hero button to calculator
    heroCtaButton.addEventListener('click', () => {
        calculatorSection.scrollIntoView({ behavior: 'smooth' });
    });

    // Handle form submission
    carbonForm.addEventListener('submit', function(e) {
        e.preventDefault();
        calculateFootprint();
    });

    // Handle 'Start Over' and 'Recalculate' buttons
    startOverButton.addEventListener('click', resetForm);
    recalculateButton.addEventListener('click', showForm);

    // --- Functions ---

    function calculateFootprint() {
        const formData = new FormData(carbonForm);
        const data = Object.fromEntries(formData.entries());

        // Send data to the backend
        fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(results => {
            updateResultsUI(results);
            showResults();
        })
        .catch(error => {
            console.error('Error calculating footprint:', error);
            alert('An error occurred. Please try again.');
        });
    }

    function updateResultsUI(data) {
        // Total Footprint
        document.getElementById('total-footprint').textContent = data.total_annual_footprint;
        document.getElementById('trees-offset').textContent = data.trees_to_offset;

        // Transportation Breakdown
        document.getElementById('transport-total').textContent = data.transportation.total;
        document.getElementById('transport-percentage').textContent = data.transportation.percentage;
        document.getElementById('car-emissions').textContent = data.transportation.car;
        document.getElementById('transit-emissions').textContent = data.transportation.transit;
        document.getElementById('flight-emissions').textContent = data.transportation.flights;

        // Household Energy Breakdown
        document.getElementById('energy-total').textContent = data.household_energy.total;
        document.getElementById('energy-percentage').textContent = data.household_energy.percentage;
        document.getElementById('electricity-emissions').textContent = data.household_energy.electricity;
        document.getElementById('natural-gas-emissions').textContent = data.household_energy.natural_gas;

        // Progress Bars
        const transportProgress = document.getElementById('transport-progress');
        const energyProgress = document.getElementById('energy-progress');
        transportProgress.style.width = `${data.transportation.percentage}%`;
        energyProgress.style.width = `${data.household_energy.percentage}%`;
        document.getElementById('transport-progress-label').textContent = `${data.transportation.percentage}%`;
        document.getElementById('energy-progress-label').textContent = `${data.household_energy.percentage}%`;
    }

    function showResults() {
        calculatorSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function showForm() {
        resultsSection.classList.add('hidden');
        calculatorSection.classList.remove('hidden');
        calculatorSection.scrollIntoView({ behavior: 'smooth' });
    }

    function resetForm() {
        carbonForm.reset();
        showForm();
    }
});
