import csv
from datetime import datetime

from HashMap import HashMap
from Package import Package


class Hub:
    def __init__(self):
        # Initialize a hash map to store package objects with package IDs as keys
        self.package_list = HashMap()

    # Method to load packages from a CSV file
    def load_packages(self):
        # Open and read the "WGUPS Package File.csv" file
        with open("data/WGUPS Package File.csv", encoding='utf-8-sig') as fp:
            reader = csv.reader(fp, delimiter=',') # Read the CSV data
            for row in reader:
                id = row[0]       # Get the id from the CSV row
                address = row[1]  # Get the id from the CSV row
                city = row[2]     # Get the id from the CSV row
                zipcode = row[4]  # Get the id from the CSV row
                deadline = row[5] # Get the id from the CSV row
                weight = row[6]   # Get the id from the CSV row

                # Convert deadline string to a datetime object
                if deadline == "EOD":
                    # Default to 5:00 PM for the "EOD" packages
                    converted_deadline = datetime(2025, 1, 24, 17, 0, 0)
                elif deadline == "10:30 AM":
                    converted_deadline = datetime(2025, 1, 24, 10, 30, 0)
                else:
                    # Assume 9:00 AM for all other cases
                    converted_deadline = datetime(2025, 1, 24, 9, 0, 0)

                # Special case: Override address for Package ID 9
                if id == "9":
                    address = "410 S State St"

                # Create a Package object with parsed data
                package = Package(id, address, city, zipcode, converted_deadline.time(), weight)

                # Add to hash map using package ID as the key
                self.package_list.add(id, package)

    # Method to retrieve package by its ID (key)
    def get(self, key):
        return self.package_list.get(key)

    # Method to check key exists in hash map
    def contains(self, key):
        return self.package_list.get_key(key)

