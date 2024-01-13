# models.py


from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, Session, relationship

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    reviews = relationship("Review", back_populates="restaurant")   
    customers = relationship(
        "Customer", secondary="reviews", back_populates="preferred_restaurants"
    )

    @classmethod
    def fanciest(cls, session):
        return session.query(cls).order_by(cls.price.desc()).first()

    def get_reviews(self):
        return [
            f"Review for {self.name} by {review.customer.full_name()}: {review.star_rating} stars."
            for review in self.reviews
        ]

    def get_customers(self):
        return [review.customer for review in self.reviews]

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    reviews = relationship("Review", back_populates="customer")
    preferred_restaurants = relationship(
        "Restaurant", secondary="reviews", back_populates="customers"
    )

    def get_reviews(self):
        return [
            f"Review for {review.restaurant.name} by {self.full_name()}: {review.star_rating} stars."
            for review in self.reviews
        ]

    def get_restaurants(self):
        return [review.restaurant for review in self.reviews]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        return max(self.reviews, key=lambda review: review.star_rating).restaurant

    def add_review(self, restaurant, rating):
        new_review = Review(restaurant=restaurant, customer=self, star_rating=rating)
        self.reviews.append(new_review)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        reviews_to_delete = [
            review for review in self.reviews if review.restaurant == restaurant
        ]
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    restaurant = relationship("Restaurant", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")

    @property
    def reviewer(self):
        return self.customer

    @property
    def reviewed_restaurant(self):
        return self.restaurant

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."
