# main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Restaurant, Customer, Review
from seed import seed_data

# Create an SQLite in-memory database for testing
engine = create_engine('sqlite:///:memory:', echo=True)

# Create the tables based on the models
Base.metadata.create_all(engine)

# Create a session to interact with the database
session = Session(engine)

# Seed the database with sample data
seed_data(session)

# Example usage of the methods
# Retrieve the first customer from the database
customer = session.query(Customer).first()

# Print the full name of the customer
print(f"Customer Full Name: {customer.full_name()}")

# Print the reviews left by the customer
print(f"Customer Reviews: {customer.get_reviews()}")

# Print the restaurants reviewed by the customer
print(f"Customer Reviewed Restaurants: {customer.restaurants()}")

# Print the customer's favorite restaurant
print(f"Customer's Favorite Restaurant: {customer.favorite_restaurant().name}")

# Add a new review for a restaurant
new_restaurant = session.query(Restaurant).filter_by(name='Restaurant A').first()
customer.add_review(new_restaurant, 5)

# Print the updated reviews after adding a new one
print(f"Customer Updated Reviews: {customer.reviews()}")

# Delete all reviews for a specific restaurant
customer.delete_reviews(new_restaurant)

# Print the reviews after deleting all reviews for the restaurant
print(f"Customer Reviews after Deletion: {customer.reviews()}")

# Retrieve the first review from the database
review = session.query(Review).first()

# Print the customer for the review
print(f"Review Customer: {review.customer.full_name()}")

# Print the restaurant for the review
print(f"Review Restaurant: {review.restaurant.name}")

# Print the full review string
print(f"Review Full String: {review.full_review()}")

# Retrieve the first restaurant from the database
restaurant = session.query(Restaurant).first()

# Print the reviews for the restaurant
print(f"Restaurant Reviews: {restaurant.reviews()}")

# Print the customers who reviewed the restaurant
print(f"Restaurant Reviewers: {restaurant.customers()}")

# Print the fanciest restaurant
print(f"Fanciest Restaurant: {Restaurant.fanciest().name}")

# Print all reviews for the restaurant
print(f"All Reviews for Restaurant: {restaurant.all_reviews()}")

# Close the session
session.close()
