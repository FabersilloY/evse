import requests
import csv

def fetch_evse_data(api_url):
    """
    Fetch EVSE data from the given API endpoint.
    Handles HTTP errors and JSON parsing errors gracefully.
    """

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e: 
        print("HTTP error occurred:", e) # HTTP request error.
        return []
    except ValueError as e:
        print("Error parsing JSON response:", e) # Failed to parse JSON error.
        return []

def save_to_csv(evse_data, filename="evse.csv"):
    """
    Save the EVSE data into a CSV file.
    Ensures file operations are handled safely to avoid corruption.
    """
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Parking Space", "Serial Number", "Energy Delivered"])
            
            for evse in evse_data:
                writer.writerow([evse.get("parking_space"), evse.get("serial_number"), evse.get("energy_delivered", 0)]) # Using .get() method to not need a bunch of if statements to avoiud empty field
    except IOError as e:
        print("Error writing to CSV file:", e)

def calculate_average_energy(evse_data):
    """
    Compute the average energy delivered across all stations.
    Handles scenarios where no valid data is available.
    """
    try:
        energy_values = [evse.get("energy_delivered", 0) for evse in evse_data if "energy_delivered" in evse]
        if energy_values:
            return sum(energy_values) / len(energy_values)
        return 0 # Return 0 on error
    except (ZeroDivisionError, TypeError) as e:
        print("Error calculating average energy:", e)
        return 0 # Return 0 on error

def main():
    """
    Main function to fetch data, save it, and compute statistics.
    """
    api_url = "https://api.example.com/evse"  # Mock API URL
    evse_data = fetch_evse_data(api_url)
    
    if evse_data:
        save_to_csv(evse_data)
        avg_energy = calculate_average_energy(evse_data)
        print(f"Average Energy Delivered: {avg_energy:.2f} kWh")
        print("Take home task for PowerFlex - By Krijn Faber")


main()
