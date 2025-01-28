from Distance import Graph
from datetime import datetime, timedelta
from Hub import Hub

# Create an instance of a Hub
h = Hub()
h.load_packages() # Load the Hub with packages

# Create an instance of a Graph
g = Graph()

class Truck:
    def __init__(self, departure_time):
        # Initialize truck properties
        self.speed_MPH = 18 # Fixed travel speed
        self.package_capacity = 0 # Counter for loaded packaged (max 16)
        self.departure_time = departure_time # Truck departure time
        self.packages = [] # List of (package ID, address) tuples
        self.route = {} # Dict mapping of route (e.g., {("id", "address"): miles})
        self.route_miles = 0 # Total miles traveled
        self.package_details = {} # Dict of delivery times (e.g., {id: (address, dropoff-time, miles)})

    # Method to load packages onto truck object
    def load_package(self, package):
        # Load a package if capacity < 16 and it's not already loaded
        if self.package_capacity < 16 and package.id not in self.packages:
            package_tuple = (package.id, package.address)
            self.packages.append(package_tuple)
            self.package_capacity += 1

    # Method to update package status and print package(s) based on user given time
    def print_package_status(self, time, user_package=None):
        hub_return = False
        for package in self.package_details.values():
            p = h.get(package[0]) # Fetch package details from Hub
            # Check if the package is delivered, en route, or at the hub
            if package[1] <= time:
                if package[0] == "4001 South 700 East":
                    hub_return = True
                    continue
                p.status = "delivered"
                p.dropoff = package[1]
            elif self.departure_time < time < package[1]:
                if package[0] == "4001 South 700 East":
                    continue
                p.status = "en route"
                p.dropoff = "NA"
            else:
                if package[0] == "4001 South 700 East":
                    continue
                p.status = "at the hub"
                p.dropoff = "NA"

        # Print statuses
        for package in self.package_details.keys():
            if user_package is None:
                if h.get(package) is not None:
                    print(f"id: {h.get(package).id}, address: {h.get(package).address}, status: {h.get(package).status}, dropoff: {h.get(package).dropoff}")
                elif package == "HUB" and hub_return: # Handle return to the hub
                    value = self.package_details.get(package)
                    print(f"id: {package}, address: {value[0]}, return: {value[1]}")
            else:
                if user_package == h.contains(package): # Print one user selected package
                    print(f"id: {h.get(package).id}, address: {h.get(package).address}, status: {h.get(package).status}, dropoff: {h.get(package).dropoff}")

    # Method to calculate total miles by truck up to 'user_time'
    def mileage_calculator(self, user_time):
        for package in self.package_details.values():
            miles = package[2]
            delivery_time = package[1]
            # Add miles if delivery occurred before 'user_time'
            if self.departure_time < user_time >= delivery_time:
                self.route_miles += miles
        return self.route_miles

    # Method to reset miles for new calculations
    def reset_mileage(self):
        self.route_miles = 0

    # Method to generate route using a nearest-neighbor algorithm
    def route_calculator(self):
        locations = self.packages
        start = "4001 South 700 East" # Hub address
        while locations:
            # Find the closest location to current 'start'
            if locations[0][1] == start: # If the fist locations address is the same as 'start' address
                self.route[locations[0]] = 0 # Add that location to route dict with (value) miles = 0
                locations.remove(locations[0]) # Remove the location from locations (packages) list
            closest_location = locations[0] # Default to first location in (packages) list as closest location
            closest_distance = g.get_distance(start, closest_location[1]) # Default the closest distance by checking the distance between current 'start' and closest location
            for location in locations:
                # If the first locations address is the same as current 'start' address add the location to the route and delete from the list
                if location[1] == start:
                    self.route[location] = 0
                    locations.remove(location)
                    continue
                # Loop through locations, if a location is closer than the current distance
                # Update closest_location and closest distance
                if g.get_distance(start, location[1]) < closest_distance:
                    closest_distance = g.get_distance(start, location[1])
                    closest_location = location
            # Update 'start' with closest_location's address
            start = closest_location[1]
            # Remove closest_location from the list
            locations.remove(closest_location)
            # Add the closest_location and closest_distance to route
            self.route[closest_location] = closest_distance

        # Add return to hub if departure time is 8:00 AM
        if self.departure_time == datetime(2025, 1, 24, 8, 0,0):
            last_key, last_value = list(self.route.items())[-1]
            hub_distance = g.get_distance(last_key[1], "4001 South 700 East")
            self.route[("HUB", "4001 South 700 East")] = hub_distance
        self.time_calculator() # Calculate delivery times

    # Method to compute delivery times for each package
    def time_calculator(self):
        start_time = self.departure_time
        for address in self.route:
            distance = self.route.get(address)
            travel_time_hours = distance/ self.speed_MPH
            travel_time = timedelta(hours=travel_time_hours)
            dropoff_time = travel_time + start_time
            start_time = dropoff_time # Update start time for next leg

            # Store delivery time details
            if address[0] == h.contains(address[0]):
                package = h.get(address[0])
                delivery_details = (address[0], dropoff_time, distance)
                self.package_details[package.id] = delivery_details
            if address[0] == "HUB":
                delivery_details = (address[1], dropoff_time, distance)
                self.package_details[address[0]] = delivery_details






