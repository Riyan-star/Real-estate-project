from db import get_session
from models import Agent, Property, Client, Showing, Transaction
from sqlalchemy import select

def input_int(prompt):
    try:
        return int(input(prompt))
    except (ValueError, TypeError):
        return None

def list_properties():
    session = get_session()
    try:
        props = session.execute(select(Property)).scalars().all()
        print("---- Properties ----")
        if not props:
            print("No properties found.")
            return
        for p in props:
            print(f"{p.id}: {p.address}, {p.city} - {p.price} ({p.status}) [Agent {p.agent_id}]")
    finally:
        session.close()

def add_agent():
    name = input("Agent name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    license_no = input("License number: ").strip()
    session = get_session()
    try:
        a = Agent(name=name, phone=phone, email=email, license_number=license_no)
        session.add(a)
        session.commit()
        print(f"Added Agent id={a.id}")
    finally:
        session.close()

def add_property():
    address = input("Address: ").strip()
    city = input("City: ").strip()
    state = input("State: ").strip()
    zip_code = input("Zip code: ").strip()
    price = input("Price: ").strip() or "0"
    bedrooms = input_int("Bedrooms: ")
    bathrooms = input_int("Bathrooms: ")
    status = input("Status (For Sale/For Rent): ").strip() or "For Sale"
    agent_id = input_int("Agent id (leave blank for none): ")
    session = get_session()
    try:
        p = Property(address=address, city=city, state=state, zip_code=zip_code,
                     price=price, bedrooms=bedrooms, bathrooms=bathrooms,
                     status=status, agent_id=agent_id)
        session.add(p)
        session.commit()
        print(f"Added Property id={p.id}")
    finally:
        session.close()

def list_agents():
    session = get_session()
    try:
        agents = session.execute(select(Agent)).scalars().all()
        print("---- Agents ----")
        if not agents:
            print("No agents found.")
            return
        for a in agents:
            # some models use 'phone' and 'license_number' fields
            phone = getattr(a, "phone", "")
            license_no = getattr(a, "license_number", "")
            email = getattr(a, "email", "")
            print(f"{a.id}: {a.name} - {email} ({phone}) License: {license_no}")
    finally:
        session.close()

def main_menu():
    menu = {
        "1": ("List properties", list_properties),
        "2": ("Add agent", add_agent),
        "3": ("Add property", add_property),
        "4": ("List agents", list_agents),
        "0": ("Exit", None),
    }
    while True:
        print("\n=== Real Estate CLI ===")
        for k, (label, _) in menu.items():
            print(f"{k}. {label}")
        choice = input("Choose: ").strip()
        if choice == "0":
            print("Bye")
            break
        action = menu.get(choice)
        if not action:
            print("Invalid choice")
            continue
        _, fn = action
        fn()

if __name__ == '__main__':
    main_menu()
