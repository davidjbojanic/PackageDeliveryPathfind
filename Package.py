class Package:
    def __init__(self, id, address, city, zip, delivery_deadline, weight):
        # Initialize the package with id, address, city, delivery_deadline, weight, status ('at the hub') and dropoff time as None
        self.id = id
        self.address = address
        self.city = city
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.status = "at the hub"
        self.dropoff = None

    # Method to print the package details
    def __str__(self):
        return (
            f"id: {self.id}\n"
            f"Address: {self.address}\n"
            f"City: {self.city}\n"
            f"Zip: {self.zip}\n"
            f"Delivery deadline: {self.delivery_deadline}\n"
            f"Weight: {self.weight}\n"
            f"Status: {self.status}\n"
            f"Dropoff time: {self.dropoff}\n"
        )
