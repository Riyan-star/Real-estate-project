from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base, engine

class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(40))
    email = Column(String(120))
    license_number = Column(String(80))
    properties = relationship("Property", back_populates="agent", cascade="all, delete-orphan")
    clients = relationship("Client", back_populates="agent", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Agent id={self.id} name={self.name}>"

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True)
    address = Column(String(200), nullable=False)
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    price = Column(Numeric)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    status = Column(String(30), default="For Sale")  # e.g., 'For Sale','Pending','Sold'
    description = Column(Text, default="")
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)

    agent = relationship("Agent", back_populates="properties")
    showings = relationship("Showing", back_populates="property", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="property", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Property id={self.id} {self.address} {self.city}>"

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(40))
    email = Column(String(120), unique=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)

    agent = relationship("Agent", back_populates="clients")
    showings = relationship("Showing", back_populates="client", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="client", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Client id={self.id} name={self.name}>"

class Showing(Base):
    __tablename__ = "showings"
    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    agent_id = Column(Integer, ForeignKey("agents.id"))
    date_time = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, default="")

    property = relationship("Property", back_populates="showings")
    client = relationship("Client", back_populates="showings")

    def __repr__(self):
        return f"<Showing id={self.id} property_id={self.property_id} client_id={self.client_id}>"

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    property_id = Column(Integer, ForeignKey("properties.id"))
    transaction_type = Column(String(20))  # 'buy' or 'rent'
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="transactions")
    property = relationship("Property", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction id={self.id} type={self.transaction_type}>"

# Helper to create all tables when running models.py directly
if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    print("Tables created (SQLAlchemy Base.metadata.create_all)")
