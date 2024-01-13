# seed_data.py

from models import Restaurant, Customer, Review

def seed_data(session):
    # Create restaurants
    restaurant1 = Restaurant(name='Restaurant A', price=3)
    restaurant2 = Restaurant(name='Restaurant B', price=4)

    # Create customers
    customer1 = Customer(first_name='John', last_name='Doe')
    customer2 = Customer(first_name='Jane', last_name='Smith')

    # Create reviews
    review1 = Review(star_rating=5, restaurant=restaurant1, customer=customer1)
    review2 = Review(star_rating=4, restaurant=restaurant2, customer=customer1)
    review3 = Review(star_rating=3, restaurant=restaurant1, customer=customer2)

    # Add instances to the session
    session.add_all([restaurant1, restaurant2, customer1, customer2, review1, review2, review3])

    # Commit the changes
    session.commit()

# If you want to test the seed_data function, you can add the following lines at the end:
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    from models import Base

    # Replace 'sqlite:///:memory:' with your actual database URL
    engine = create_engine('sqlite:///:memory:', echo=True)
    
    # Create the tables based on the models
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    session = Session(engine)

    # Seed the database with sample data
    seed_data(session)

    # Close the session
    session.close()
