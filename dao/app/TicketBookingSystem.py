from util.db_connection import DBConnUtil
from bean.TicketBookingSystem import TicketBookingSystem
from entity.model.venue import Venue
from entity.model.customer import Customer

def main():
    conn = DBConnUtil.get_db_connection()
    if not conn:
        print("❌ Database connection failed!")
        return

    system = TicketBookingSystem(conn)

    try:
        while True:
            command = input("\nEnter command (create_event, book_tickets, cancel_tickets, get_available_seats, get_event_details, exit): ").strip().lower()
            
            if command == "create_event":
                event_name = input("Event Name: ")
                event_date = input("Event Date (YYYY-MM-DD): ")
                event_time = input("Event Time (HH:MM:SS): ")
                total_seats = int(input("Total Seats: "))
                event_type = input("Event Type (Movie, Concert, Sports): ")
                venue_name = input("Venue Name: ")
                address = input("Venue Address: ")
                venue = Venue(venue_name, address)
                event = system.create_event(event_name, event_date, event_time, venue, total_seats, event_type)
                if event:
                    print("✅ Event created successfully!")
                else:
                    print("❌ Failed to create event!")

            elif command == "book_tickets":
                event_id = int(input("Event ID: "))
                num_tickets = int(input("Number of Tickets: "))
                customers = []
                for _ in range(num_tickets):
                    customer_name = input("Customer Name: ")
                    email = input("Customer Email: ")
                    phone_number = input("Customer Phone Number: ")
                    customer = Customer(customer_name, email, phone_number)
                    customers.append(customer)
                booking = system.book_tickets(event_id, num_tickets, customers)
                if booking:
                    print("✅ Tickets booked successfully!")
                else:
                    print("❌ Failed to book tickets!")

            elif command == "cancel_tickets":
                booking_id = int(input("Booking ID: "))
                booking = system.cancel_booking(booking_id)
                if booking:
                    print("✅ Booking cancelled successfully!")
                else:
                    print("❌ Failed to cancel booking!")

            elif command == "get_available_seats":
                event_id = int(input("Event ID: "))
                available_seats = system.get_available_seats(event_id)
                print(f"Available Seats: {available_seats}")

            elif command == "get_event_details":
                event_id = int(input("Event ID: "))
                event = system.create_event(event_id)
                if event:
                    system.display_event_details(event)
                else:
                    print("❌ Event not found!")

            elif command == "exit":
                break

            else:
                print("❌ Invalid command!")

    finally:
        conn.close()

if __name__ == "__main__":
    main()