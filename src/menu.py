# src/menu.py
class MenuItem:
    def __init__(self, name, price, image):
        self.name = name
        self.price = price
        self.image = image

def get_menu():
    # Définition du menu avec plusieurs éléments
    return [
        MenuItem("Burger", 40.00, "images/burger.png"),
        MenuItem("Pizza", 60.00, "images/pizza.png"),
        MenuItem("Soda", 10.00, "images/soda.png"),
        MenuItem("Salade César", 30.00, "images/salad.png"),
        MenuItem("Spaghetti Bolognaise", 50.00, "images/spaghetti.png"),
        MenuItem("Café", 15.00, "images/coffee.png"),
        MenuItem("Thé à la menthe", 12.00, "images/tea.png"),
        MenuItem("Jus d’orange", 20.00, "images/orange_juice.png"),
        MenuItem("Sandwich", 25.00, "images/sandwich.png"),
        MenuItem("Glace", 18.00, "images/ice_cream.png")
    ]
