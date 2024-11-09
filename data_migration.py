from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime, timedelta
from faker import Faker
import random

# Database setup
DATABASE_URI = "mysql+pymysql://app_user:app_password@localhost:3307/fraud_detection_db"
engine = create_engine(DATABASE_URI)
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    country_of_residence = Column(String(100), nullable=False)
    occupation = Column(String(100), nullable=True)
    status = Column(String(20), nullable=True)
    income = Column(Float, nullable=True)
    phone_number = Column(String(30), nullable=False)
    account_creation_date = Column(DateTime, default=datetime.utcnow)

    # Establish relationship with TradingTransaction
    transactions = relationship("TradingTransaction", back_populates="user")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, name='{self.name}')>"

# Define the TradingTransaction model
class TradingTransaction(Base):
    __tablename__ = 'trading_transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String(100), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # Foreign key linking to User table
    transaction_type = Column(String(20), nullable=False)  # e.g., 'buy', 'sell'
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    transaction_time = Column(DateTime, default=datetime.utcnow)
    location = Column(String(100), nullable=True)
    device_id = Column(String(100), nullable=True)
    ip_address = Column(String(20), nullable=True)

    # Establish relationship with User
    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<TradingTransaction(transaction_id={self.transaction_id}, user_id={self.user_id}, amount={self.amount})>"

# Drop all tables
Base.metadata.drop_all(engine)

# Recreate tables with the updated schema
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

# Create instance of Faker for dummy data generation
fake = Faker()

# Function to generate dummy users and transactions with varied hours for today's date
def generate_dummy_data(num_users=10000, transactions_per_user=5):
    users = []
    generated_emails = set()  # Track generated emails to avoid duplicates

    for _ in range(num_users):
        # Ensure unique email
        email = fake.email()
        while email in generated_emails:
            email = fake.email()
        generated_emails.add(email)

        user = User(
            name=fake.name(),
            email=email,
            age=random.randint(18, 80),
            gender=random.choice(['Male', 'Female']),
            country_of_residence=fake.country(),
            occupation=fake.job(),
            status=random.choice(['Single', 'Married']),
            income=round(random.uniform(30000, 150000), 2),
            phone_number=fake.numerify("##########"),  # Limit to 10 digits
            account_creation_date=fake.date_time_this_decade()
        )
        session.add(user)
        session.flush()  # Flush to get the generated user_id

        # Create dummy transactions for each user
        for _ in range(transactions_per_user):
            time_offset = timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
            transaction = TradingTransaction(
                transaction_id=fake.uuid4(),
                user_id=user.user_id,
                transaction_type=random.choice(['buy', 'sell']),
                amount=round(random.uniform(100.0, 10000.0), 2),
                currency=random.choice(['USD', 'EUR', 'GBP', 'JPY']),
                transaction_time=datetime.utcnow() + time_offset,
                location=fake.city(),
                device_id=fake.uuid4(),
                ip_address=fake.ipv4()
            )
            session.add(transaction)

    session.commit()
    print("Dummy data inserted successfully.")

# Generate and insert dummy data
generate_dummy_data()