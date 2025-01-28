import csv

# Class that represents a Location, which holds the Location's name and address
class Location:
    def __init__(self, location_name, address):
        self.location_name = location_name # The name of the location
        self.address = address # The address of the location

# Class to represent the Graph which stores Locations (vertices) and distances (edges)
class Graph:
    vertices = {} # Dictionary to hold the locations (key: address, value: Location object)
    edges = [] # Adjacency matrix to hold distances between locations (2D list)
    edge_indices = {} # Dictionary to map location addresses to index positions in the adjacency matrix

    # Method to add a location to the graph
    def add_vertex(self, location):
        if isinstance(location, Location) and location.address not in self.vertices:
            # If location is valid and not already in graph, add it as a vertex
            self.vertices[location.address] = location # Add location to vertices dictionary
            for row in self.edges:
                row.append(0) # Add a new column (initialize to 0) for the new vertex in the edge matrix
            self.edges.append([0] * (len(self.edges)+1)) # Add a new row (initialize to 0) for the new vertex
            self.edge_indices[location.address] = len(self.edge_indices) # Add location to the edge index map
            return True
        else:
            # If the location is invalid or already exists, return False
            return False

    # Method to add an edge between two locations with specified weight (distance)
    def add_edge(self, location1, location2, weight):
        if isinstance(location1, Location) and isinstance(location2, Location):
            # Ensure both locations are valid Location objects
            if location1.address in self.vertices and location2.address in self.vertices:
                weight = float(weight) # Convert weight to float for distance
                # Add distance (weight) in both directions of the adjacency matrix (undirected graph)
                self.edges[self.edge_indices[location1.address]][self.edge_indices[location2.address]] = weight
                self.edges[self.edge_indices[location2.address]][self.edge_indices[location1.address]] = weight
                return True
            else:
                return False # One or both locations are not in the graph, return False

    # Method to retrieve the distance between two locations
    def get_distance(self, location1, location2):
        # Return the distance using the edge_indices to locate the correct position in the adjacency matrix
        return self.edges[self.edge_indices[location1]][self.edge_indices[location2]]

    # Method to load locations from a CSV file and add them ad vertices to the graph
    def load_locations(self):
        # Open and read the 'WGUPS Location list.csv' file
        with open("data/WGUPS Location list.csv", encoding='utf-8-sig') as fp:
            reader = csv.reader(fp, delimiter=',') # Read the CSV file
            for row in reader:
                location_name = row[0] # Get the location name from the CSV row
                address = row[1] # Get the location address from the CSV row

                location = Location(location_name, address) # Create a location object with the row data

                self.add_vertex(location) # Add the location to the graph as a vertex

    # Method to load distances (edges) between locations from a CSV file
    def load_distances(self):
        # Open and read the 'WGUPS Distance Table.csv' file
        with open("data/WGUPS Distance Table.csv", encoding='utf-8-sig') as fp:
            reader = csv.reader(fp, delimiter=',') # Read the CSV data
            for row_index, row in enumerate(reader):
                for column_index, dist in enumerate(row):
                    if dist not in ['0.0', '']: # If distance is not 0.0 or empty
                        # Get the addresses for the two locations (row and column)
                        location1_address = list(self.vertices.keys())[row_index]
                        location2_address = list(self.vertices.keys())[column_index]
                        location1 = self.vertices[location1_address] # Retrieve the location object for location1
                        location2 = self.vertices[location2_address] # Retrieve the location object for location2
                        self.add_edge(location1, location2, float(dist)) # Add the edge (distance) between the two locations