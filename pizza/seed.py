# Import necessary modules
from app import Pizza, Restaurant, app, db

# Define a function to create and seed initial data
def create_seed_data():
    # Ensure the code runs within the Flask app context
    with app.app_context():
        # Delete any existing Pizza records (for a clean start)
        Pizza.query.delete()
        
        # Create the database tables (if not already created)
        db.create_all()

        # Create Pizza instances with name and ingredients
        margarita = Pizza(name="Margarita", ingredients="Dough, Tomato Sauce, Cheese")
        pepperoni = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")

        # Create Restaurant instances with name and address
        pizza_palace = Restaurant(name="Pizza Palace", address="123 Main St")
        dominion_pizza = Restaurant(name="Dominion Pizza", address="456 Elm St")

        # Add all Pizza and Restaurant instances to the database session
        db.session.add_all([margarita, pepperoni, pizza_palace, dominion_pizza])

        # Commit the changes to the database
        db.session.commit()

# Check if this script is the main entry point
if __name__ == "__main__":
    # Call the create_seed_data function to populate the database
    create_seed_data()
