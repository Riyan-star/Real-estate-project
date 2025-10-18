from db import engine, get_session
from models import Base, Agent, Property, Client, Showing, Transaction
from sqlalchemy import text

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

def seed_data():
    session = get_session()
    # Add agents
    a1 = Agent(name="Alice Realtor", phone="+254700000001", email="alice@example.com", license_number="AGT-001")
    a2 = Agent(name="Bob Realtor", phone="+254700000002", email="bob@example.com", license_number="AGT-002")
    session.add_all([a1, a2])
    session.commit()

    # Add clients
    c1 = Client(name="John Doe", phone="+254700000010", email="john@example.com", agent_id=a1.id)
    c2 = Client(name="Jane Roe", phone="+254700000011", email="jane@example.com", agent_id=a2.id)
    session.add_all([c1, c2])
    session.commit()

    # Add properties
    p1 = Property(address="123 Main St", city="Nairobi", state="Nairobi", zip_code="00100",
                  price=120000, bedrooms=2, bathrooms=1, status="For Rent", agent_id=a1.id,
                  description="Cozy 2BR apartment in the city center.")
    p2 = Property(address="45 Beach Rd", city="Mombasa", state="Coast", zip_code="80100",
                  price=7500000, bedrooms=4, bathrooms=3, status="For Sale", agent_id=a2.id,
                  description="Spacious villa near the sea.")
    session.add_all([p1, p2])
    session.commit()

    print("Seed data inserted.")
    session.close()

if __name__ == '__main__':
    create_tables()
    seed_data()
