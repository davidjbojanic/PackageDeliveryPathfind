# 011204547

# Import necessary libraries and modules
from datetime import datetime
from Hub import Hub
from Distance import*
from Truck import Truck

# Instantiate a Graph object and load locations and distances
g = Graph()
g.load_locations() # Loads the locations of the packages into the graph
g.load_distances() # Loads the distance data between the locations

# Instantiate a Hub object and load all package data
h = Hub()
h.load_packages() #Loads the package data (ID, address, etc.) into the Hub

# Create Truck 1 and load packages onto it for delivery
truck1 = Truck(datetime(2025,1,24,8,0,0)) # Instantiate Truck 1 with a departure time of 8:00 AM
truck1.load_package(h.get('15')) # Load packages onto Truck 1 by package ID
truck1.load_package(h.get('14'))
truck1.load_package(h.get('16'))
truck1.load_package(h.get('20'))
truck1.load_package(h.get('13'))
truck1.load_package(h.get('19'))
truck1.load_package(h.get('1'))
truck1.load_package(h.get('29'))
truck1.load_package(h.get('30'))
truck1.load_package(h.get('31'))
truck1.load_package(h.get('34'))
truck1.load_package(h.get('37'))
truck1.load_package(h.get('40'))
truck1.load_package(h.get('11'))
truck1.load_package(h.get('12'))
truck1.load_package(h.get('17'))
truck1.route_calculator() # Calculate the optimal delivery route for Truck 1

# Create Truck 2 and load packages ont it for delivery
truck2 = Truck(datetime(2025,1,24,9,5,0)) # Instantiate Truck 2 with departure time of 9:05 AM
truck2.load_package(h.get('6')) # Load packages onto Truck 2 by package ID
truck2.load_package(h.get('25'))
truck2.load_package(h.get('3'))
truck2.load_package(h.get('18'))
truck2.load_package(h.get('36'))
truck2.load_package(h.get('38'))
truck2.load_package(h.get('28'))
truck2.load_package(h.get('32'))
truck2.load_package(h.get('39'))
truck2.load_package(h.get('35'))
truck2.load_package(h.get('33'))
truck2.load_package(h.get('27'))
truck2.load_package(h.get('26'))
truck2.load_package(h.get('24'))
truck2.load_package(h.get('23'))
truck2.load_package(h.get('22'))
truck2.route_calculator() # Calculate the optimal delivery route for Truck 2

# Create Truck 3 and load packages onto it for delivery
truck3 = Truck(datetime(2025,1,24,10,40,0)) # Instantiate Truck 3 with a departure time of 10:40 AM
truck3.load_package(h.get('9')) # Load packages onto Truck 3 by package ID
truck3.load_package(h.get('10'))
truck3.load_package(h.get('21'))
truck3.load_package(h.get('8'))
truck3.load_package(h.get('7'))
truck3.load_package(h.get('5'))
truck3.load_package(h.get('4'))
truck3.load_package(h.get('2'))
truck3.route_calculator() # Calculate the optimal delivery route for Truck 3

# Set a default date for input validation
default_date = "2025-1-24"

# Start an interactive loop to accept user input and show delivery status
while True:
    time = input('Enter a time (ie. HH:MM): ') # Prompt user to enter a time in HH:MM format
    try:
        # Combine the default date with the user input time to create a datetime object
        combined_input = default_date + ' ' + time
        parsed_datetime = datetime.strptime(combined_input, "%Y-%m-%d %H:%M") # Parse the date and time input into datetime object
    except ValueError:
        # If the time format is incorrect, print error message and allow the user to exit or continue
        print("")
        print("Invalid time format. Please enter the time in HH:MM format.")
        exit = input('Do you want to exit? ("yes" to exit. Anything else will continue): ') # Ask the user if they want to exit
        print("")
        if exit.lower() == 'yes': # Exit the loop if user types "yes"
            break
        continue # Otherwise, continue prompting for the time input

    # If the datetime input is successfully parsed
    if parsed_datetime:
        # Prompt user for action: view all packages, view one package, or exit
        answer = input( "1. View all packages at selected time\n"
                        "2. View one package at selected time\n"
                        "3. Exit the program\n"
                        "> ")

        # Option 1: View all packages at the user selected time
        if answer == '1':
            print("")
            print(f"--------Status of all packages at {time}---------") # Print the status header
            print(f"Truck 1 - departure {truck1.departure_time.time()}")
            truck1.print_package_status(parsed_datetime) # Print the statuses of all packages for Truck 1 based on user selected time
            print(f"Truck 2 - departure {truck2.departure_time.time()}")
            truck2.print_package_status(parsed_datetime) # Print the statuses of all packages for Truck 2 based on user selected time
            print(f"Truck 3 - departure {truck3.departure_time.time()}")
            truck3.print_package_status(parsed_datetime) # Print the statuses of all packages for Truck 3 based on user selected time

            # Calculate and print the combined total mileage traveled for all trucks up to the user selected time
            total_mileage = truck1.mileage_calculator(parsed_datetime) + truck2.mileage_calculator(
                parsed_datetime) + truck3.mileage_calculator(parsed_datetime)
            print("Total mileage: " + str(round(total_mileage, 1))) # Print the rounded total mileage
            print("")

            # Reset the mileage for each truck after displaying the total mileage
            truck1.reset_mileage()
            truck2.reset_mileage()
            truck3.reset_mileage()
            continue # Loop again for another input

        # Option 2: View details of a single package by ID at the user selected time
        elif answer == '2':
            print("")
            package_id = input('Enter package ID: ') # Prompt user to enter package ID
            try:
                # Check if the package ID exists in the Hub, raise error if not found
                if not h.contains(package_id):
                    raise ValueError("Package ID not found.")

                print("")
                print(f"--------Status of package ID#{package_id} at {time}---------") # Print package status header
                truck1.print_package_status(parsed_datetime, package_id) # Check Truck 1 for user selected package and print package status at user selected time if found
                truck2.print_package_status(parsed_datetime, package_id) # Check Truck 2 for user selected package and print package status at user selected time if found
                truck3.print_package_status(parsed_datetime, package_id) # Check Truck 3 for user selected package and print package status at user selected time if found

                # Calculate and print the combined total mileage traveled for all trucks up to the user selected time
                total_mileage = truck1.mileage_calculator(parsed_datetime) + truck2.mileage_calculator(
                parsed_datetime) + truck3.mileage_calculator(parsed_datetime)
                print("Total mileage: " + str(round(total_mileage, 1))) # Print rounded total mileage
                print("")

                # Reset the mileage for each truck after displaying the total mileage
                truck1.reset_mileage()
                truck2.reset_mileage()
                truck3.reset_mileage()
            except ValueError as e:
                # If the package ID is not found, print error message
                print(str(e))
                print("")
            continue # Loop again for another input

        # Option 3: Exit the program
        elif answer == '3':
            break # Exit the loop and end the program



