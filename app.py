from util.db_connection import get_db_connection
from abc import ABC, abstractmethod
from datetime import datetime

# Admin class
class Admin:
    def __init__(self, conn):
        self.conn = conn

    def create_event(self, event_name, event_date, event_time, venue_id, total_seats, event_type):
        try:
            with self.conn.cursor() as cursor:
                # Insert into Event table
                cursor.execute("""
                    INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (event_name, event_date, event_time, venue_id, total_seats, total_seats, event_type))
                
                event_id = cursor.lastrowid

                # Prompt for additional info based on event type
                if event_type.lower() == 'movie':
                    genre = input("🎬 Enter Genre: ")
                    actor_name = input("🎭 Enter Actor Name: ")
                    actress_name = input("🎭 Enter Actress Name: ")
                    cursor.execute("""
                        INSERT INTO Movie (event_id, genre, actor_name, actress_name)
                        VALUES (%s, %s, %s, %s)
                    """, (event_id, genre, actor_name, actress_name))

                elif event_type.lower() == 'concert':
                    artist = input("🎤 Enter Artist Name: ")
                    concert_type = input("🎵 Enter Concert Type (e.g., Solo, Band, Festival): ")
                    cursor.execute("""
                        INSERT INTO Concert (event_id, artist, concert_type)
                        VALUES (%s, %s, %s)
                    """, (event_id, artist, concert_type))

                elif event_type.lower() == 'sports':
                    sport_name = input("🏅 Enter Sport Name: ")
                    teams_name = input("🏆 Enter Teams (e.g., Team A vs Team B): ")
                    cursor.execute("""
                        INSERT INTO Sports (event_id, sport_name, teams_name)
                        VALUES (%s, %s, %s)
                    """, (event_id, sport_name, teams_name))

            self.conn.commit()
            print(f"\n✅ Event '{event_name}' created successfully with ID {event_id}!")

        except Exception as e:
            self.conn.rollback()
            print(f"❌ Failed to create event: {e}")

    def update_event(self, event_id, event_name, event_date, event_time, venue_id, total_seats, available_seats):
        """Updates event details in Event table and synchronizes changes with Movie, Concert, or Sports tables"""
        with self.conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Event
                SET event_name = %s, event_date = %s, event_time = %s, 
                    venue_id = %s, total_seats = %s, available_seats = %s
                WHERE event_id = %s
            """, (event_name, event_date, event_time, venue_id, total_seats, available_seats, event_id))

            cursor.execute("SELECT event_type FROM Event WHERE event_id = %s", (event_id,))
            result = cursor.fetchone()

            if result:
                event_type = result[0].lower()

                if event_type == "movie":
                    genre = input("Enter genre: ")
                    actor_name = input("Enter actor name: ")
                    actress_name = input("Enter actress name: ")

                    cursor.execute("""
                        UPDATE Movie 
                        SET genre = %s, actor_name = %s, actress_name = %s 
                        WHERE event_id = %s
                    """, (genre, actor_name, actress_name, event_id))

                elif event_type == "concert":
                    artist = input("Enter artist name: ")
                    concert_type = input("Enter concert type: ")

                    cursor.execute("""
                        UPDATE Concert 
                        SET artist = %s, concert_type = %s 
                        WHERE event_id = %s
                    """, (artist, concert_type, event_id))

                elif event_type == "sports":
                    sport_name = input("Enter sport name: ")
                    teams_name = input("Enter new teams: ")

                    cursor.execute("""
                        UPDATE Sports 
                        SET sport_name = %s, teams_name = %s 
                        WHERE event_id = %s
                    """, (sport_name, teams_name, event_id))

        self.conn.commit()
        print(f"✅ Event ID {event_id} updated successfully!")

    def calculate_total_revenue(self, event_id):
        """Calculates total revenue based on ticket sales"""
        price_mapping = {"Silver": 200, "Gold": 500, "Diamond": 1000}
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT ticket_category, SUM(num_tickets)
                FROM Booking
                WHERE event_id = %s
                GROUP BY ticket_category
            """, (event_id,))
            total_revenue = sum(price_mapping[category] * num_tickets for category, num_tickets in cursor.fetchall())
        return total_revenue  

    def get_event_statistics(self, event_id):
        """Returns total booked tickets, remaining tickets, and total revenue"""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT SUM(num_tickets) FROM Booking WHERE event_id = %s", (event_id,))
            booked_tickets = cursor.fetchone()[0] or 0  

            cursor.execute("SELECT available_seats FROM Event WHERE event_id = %s", (event_id,))
            remaining_tickets = cursor.fetchone()[0] or 0  

            total_revenue = self.calculate_total_revenue(event_id)
        return booked_tickets, remaining_tickets, total_revenue

# Venue Class
class Venue:
    def __init__(self, venue_name=None, address=None):
        self.venue_name = venue_name
        self.address = address

    def display_venue_details(self):
        print(f"Venue Name: {self.venue_name}")
        print(f"Address: {self.address}")

    def get_venue_name(self):
        return self.venue_name

    def set_venue_name(self, venue_name):
        self.venue_name = venue_name

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

# Customer Class
class Customer:
    def __init__(self, customer_name=None, email=None, phone_number=None):
        self.customer_name = customer_name
        self.email = email
        self.phone_number = phone_number

    def display_customer_details(self):
        print(f"Customer Name: {self.customer_name}")
        print(f"Email: {self.email}")
        print(f"Phone Number: {self.phone_number}")

    def get_customer_name(self):
        return self.customer_name

    def set_customer_name(self, customer_name):
        self.customer_name = customer_name

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_phone_number(self):
        return self.phone_number

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

# Booking Class
class Booking:
    booking_counter = 1

    def __init__(self, customer=None, event=None, num_tickets=0, ticket_category=None):
        self.booking_id = Booking.booking_counter
        Booking.booking_counter += 1
        self.customer = customer
        self.event = event
        self.num_tickets = num_tickets
        self.ticket_category = ticket_category
        self.total_cost = self.calculate_total_cost()
        self.booking_date = datetime.now()

    def calculate_total_cost(self):
        price_mapping = {"Silver": 200, "Gold": 500, "Diamond": 1000}
        return price_mapping.get(self.ticket_category, 0) * self.num_tickets

    def display_booking_details(self):
        print(f"Booking ID: {self.booking_id}")
        print(f"Customer Name: {self.customer.customer_name}")
        print(f"Event Name: {self.event.event_name}")
        print(f"Number of Tickets: {self.num_tickets}")
        print(f"Ticket Category: {self.ticket_category}")
        print(f"Total Cost: {self.total_cost}")
        print(f"Booking Date: {self.booking_date}")

    def get_booking_id(self):
        return self.booking_id

    def get_customer(self):
        return self.customer

    def set_customer(self, customer):
        self.customer = customer

    def get_event(self):
        return self.event

    def set_event(self, event):
        self.event = event

    def get_num_tickets(self):
        return self.num_tickets

    def set_num_tickets(self, num_tickets):
        self.num_tickets = num_tickets

    def get_total_cost(self):
        return self.total_cost

    def set_total_cost(self, total_cost):
        self.total_cost = total_cost

    def get_booking_date(self):
        return self.booking_date

    def set_booking_date(self, booking_date):
        self.booking_date = booking_date

# Abstract Event Class
class Event(ABC):
    def __init__(self, event_id, conn):
        self.event_id = event_id
        self.conn = conn
        self.event_name = None
        self.event_date = None
        self.event_time = None
        self.venue = None
        self.total_seats = 0
        self.available_seats = 0
        self.event_type = None
        self.load_event_details()

    def load_event_details(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT event_name, event_date, event_time, venue_id, total_seats, available_seats, event_type 
                FROM Event WHERE event_id = %s
            """, (self.event_id,))
            result = cursor.fetchone()
            if result:
                (self.event_name, self.event_date, self.event_time, 
                 venue_id, self.total_seats, self.available_seats, self.event_type) = result
                self.venue = self.load_venue(venue_id)

    def load_venue(self, venue_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT venue_name, address FROM Venue WHERE venue_id = %s", (venue_id,))
            result = cursor.fetchone()
            if result:
                venue_name, address = result
                return type("Venue", (), {"venue_name": venue_name, "location": address})()
        return None

    @abstractmethod
    def get_event_type(self):
        pass

    def calculate_total_revenue(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT SUM(tc.price * b.no_of_tickets)
                FROM Booking b
                JOIN TicketCategory tc ON b.ticket_category_id = tc.ticket_category_id
                WHERE b.event_id = %s
            """, (self.event_id,))
            result = cursor.fetchone()
            return result[0] if result and result[0] else 0

    def getBookedNoOfTickets(self):
        return self.total_seats - self.available_seats

    def book_tickets(self, customer_id, num_tickets, ticket_category):
        if num_tickets <= self.available_seats:
            self.available_seats -= num_tickets
            total_cost = self.calculate_total_cost(ticket_category, num_tickets)
           
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Booking (customer_id, event_id, num_tickets, ticket_category, total_cost, booking_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (customer_id, self.event_id, num_tickets, ticket_category, total_cost, datetime.now()))
                cursor.execute("""
                    UPDATE Event
                    SET available_seats = %s
                    WHERE event_id = %s
                """, (self.available_seats, self.event_id))
                self.conn.commit()
                booking_id = cursor.lastrowid
                if booking_id == 0:
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    booking_id = cursor.fetchone()[0]
                print(f"✅ Booking successful for {self.event_name}! Booking ID: {booking_id}")
                return booking_id
            
        else:
            print("❌ Not enough available seats!")
        return None

    def calculate_total_cost(self, ticket_category, num_tickets):
        price_mapping = {"Silver": 200, "Gold": 500, "Diamond": 1000}
        return price_mapping.get(ticket_category, 0) * num_tickets

    def cancel_booking(self, booking_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT num_tickets FROM Booking WHERE booking_id = %s", (booking_id,))
            result = cursor.fetchone()
            if result:
                num_tickets = result[0]
                self.available_seats += num_tickets
                cursor.execute("DELETE FROM Booking WHERE booking_id = %s", (booking_id,))
                cursor.execute("""
                    UPDATE Event
                    SET available_seats = %s
                    WHERE event_id = %s
                """, (self.available_seats, self.event_id))
                self.conn.commit()
                print(f"✅ Booking ID {booking_id} cancelled successfully!")
            else:
                print(f"❌ Booking ID {booking_id} not found!")

    def display_event_details(self):
        print(f"Event Name: {self.event_name}")
        print(f"Event Date: {self.event_date}")
        print(f"Event Time: {self.event_time}")
        if self.venue:
            print(f"Venue: {self.venue.venue_name}")
        print(f"Total Seats: {self.total_seats}")
        print(f"Available Seats: {self.available_seats}")
        print(f"Event Type: {self.event_type}")
        
class Movie(Event):
    def __init__(self, event_id, conn):
        super().__init__(event_id, conn)
        self.genre = None
        self.actor_name = None
        self.actress_name = None
        self.load_movie_details()

    def load_movie_details(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT genre, actor_name, actress_name FROM Movie WHERE event_id = %s", (self.event_id,))
            result = cursor.fetchone()
            if result:
                self.genre, self.actor_name, self.actress_name = result

    def display_event_details(self):
        super().display_event_details()
        print(f"🎬 Genre: {self.genre}")
        print(f"🎭 Actors: {self.actor_name} & {self.actress_name}\n")

    def get_event_type(self):
        return "Movie"

class Concert(Event):
    def __init__(self, event_id, conn):
        super().__init__(event_id, conn)
        self.artist = None
        self.concert_type = None
        self.load_concert_details()

    def load_concert_details(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT artist, concert_type FROM Concert WHERE event_id = %s", (self.event_id,))
            result = cursor.fetchone()
            if result:
                self.artist, self.concert_type = result

    def display_event_details(self):
        super().display_event_details()
        print(f"🎤 Artist: {self.artist}")
        print(f"🎵 Concert Type: {self.concert_type}\n")

    def get_event_type(self):
        return "Concert"

class Sports(Event):
    def __init__(self, event_id, conn):
        super().__init__(event_id, conn)
        self.sport_name = None
        self.teams_name = None
        self.load_sports_details()

    def load_sports_details(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT sport_name, teams_name FROM Sports WHERE event_id = %s", (self.event_id,))
            result = cursor.fetchone()
            if result:
                self.sport_name, self.teams_name = result

    def display_event_details(self):
        super().display_event_details()
        print(f"⚽ Sport: {self.sport_name}")
        print(f"🏆 Teams: {self.teams_name}\n")

    def get_event_type(self):
        return "Sports"

# Abstract BookingSystem Class
class BookingSystem(ABC):

    @abstractmethod
    def create_event(self, event_id):
        pass

    @abstractmethod
    def display_event_details(self, event):
        pass

    @abstractmethod
    def book_tickets(self, event_id, customer_id, num_tickets, ticket_category):
        pass

    @abstractmethod
    def cancel_booking(self, event_id, booking_id):
        pass

    @abstractmethod
    def get_available_seats(self, event_id):
        pass

# Concrete TicketBookingSystem Class
class TicketBookingSystem(BookingSystem):
    def __init__(self, conn):
        self.conn = conn
        self.events = []

    def create_event(self, event_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT event_name, event_date, venue_id, total_seats, event_type FROM Event WHERE event_id = %s", (event_id,))
            result = cursor.fetchone()

        if result:
            event_name, event_date, venue_id, total_seats, event_type = result
            if event_type.lower() == "movie":
                event = Movie(event_id, self.conn)
            elif event_type.lower() == "concert":
                event = Concert(event_id, self.conn)
            elif event_type.lower() == "sports":
                event = Sports(event_id, self.conn)
            else:
                event = None

            if event:
                self.events.append(event)
                return event
        return None

    def display_event_details(self, event):
        event.display_event_details()

    def book_tickets(self, event_id, customer_id, num_tickets, ticket_category):
        event = next((e for e in self.events if e.event_id == event_id), None)
        if not event:
            event = self.create_event(event_id)
        if event:
            return event.book_tickets(customer_id, num_tickets, ticket_category)
        else:
            print("Event not found!")
            return None

    def cancel_booking(self, event_id, booking_id):
        event = next((e for e in self.events if e.event_id == event_id), None)
        if not event:
            event = self.create_event(event_id)
        if event:
            return event.cancel_booking(booking_id)
        else:
            print("Event not found!")
            return None

    def get_available_seats(self, event_id):
        event = next((e for e in self.events if e.event_id == event_id), None)
        if not event:
            event = self.create_event(event_id)
        if event:
            return event.available_seats
        else:
            print("Event not found!")
            return None


# Main Function for Ticket Booking
def book_tickets():
    conn = get_db_connection()
    if not conn:
        print("❌ Database connection failed!")
        return

    system = TicketBookingSystem(conn)

    try:
        print("\n🔹 Welcome to the Ticket Booking System 🔹")
        role = input("Are you an Admin or a Customer? (Admin/Customer/Exit): ").strip().lower()

        if role == "customer":
            # Customer registration/login
            with conn.cursor() as cursor:
                email = input("Enter your email: ").strip()
                cursor.execute("SELECT customer_id FROM Customer WHERE email = %s", (email,))
                result = cursor.fetchone()

                if result:
                    customer_id = result[0]
                    print(f"✅ Welcome back!")
                else:
                    print("❌ No user exists!")
                    print("📝 Please register to continue.")
                    customer_name = input("Enter your name: ").strip()
                    phone_number = input("Enter your phone number: ").strip()
                    cursor.execute("""
                        INSERT INTO Customer (customer_name, email, phone_number)
                        VALUES (%s, %s, %s)
                    """, (customer_name, email, phone_number))
                    conn.commit()
                    customer_id = cursor.lastrowid
                    print("✅ Registration successful!")

            event_type = input("Which event do you want to book? (Movie/Concert/Sports): ").strip().capitalize()

            if event_type not in ["Movie", "Concert", "Sports"]:
                print("❌ Invalid event type! Please enter 'Movie', 'Concert', or 'Sports'.")
                return

            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT event_id, event_name, event_date, event_time 
                    FROM Event 
                    WHERE event_type = %s
                """, (event_type,))
                events = cursor.fetchall()

            if not events:
                print(f"❌ No {event_type} events available for booking!")
                return

            print(f"\n🎟 Available {event_type} Events:")
            for event in events:
                print(f"🔹 {event[0]}. {event[1]} on {event[2]} at {event[3]}")

            event_id = int(input("\nEnter Event ID to proceed with booking: "))
            event = system.create_event(event_id)

            if event is None or event.event_name is None:
                print("❌ Invalid Event ID! Please select from the available events.")
                return

            system.display_event_details(event)

            while True:
                action = input("Type 'Book' to book tickets, 'Cancel' to cancel a booking, or 'Exit' to quit: ").strip().lower()
                if action == "exit":
                    print("✅ Exiting the booking system. Thank you!")
                    break

                elif action == "book":
                    num_tickets = int(input("Enter the number of tickets to book: "))
                    print("💰 Ticket Prices:")
                    print("   🥈 Silver  - ₹200")
                    print("   🥇 Gold    - ₹500")
                    print("   💎 Diamond - ₹1000")
                    print("ℹ️  Final price depends on the selected category.")
                    ticket_category = input("Enter the ticket category (Silver/Gold/Diamond): ").strip().capitalize()
                    booking_id = system.book_tickets(event_id, customer_id, num_tickets, ticket_category)
                    
                    if booking_id:
                        print(f"✅ Tickets booked successfully for {event.event_name}!")
                        print(f"📄 Your Booking ID: {booking_id}")
                    else:
                        print("❌ Booking failed! Please try again.")

                elif action == "cancel":
                    booking_id = int(input("Enter Booking ID to cancel: "))
                    system.cancel_booking(event_id, booking_id)

        elif role == "admin":
            admin = Admin(conn)
            while True:
                print("\n🔹 Admin Panel 🔹")
                print("1. View Event Statistics")
                print("2. Create Event")
                print("3. Update Event")
                print("4. Exit")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    event_id = int(input("Enter Event ID: "))
                    booked_tickets, remaining_tickets, revenue = admin.get_event_statistics(event_id)

                    print(f"\n📊 Event Statistics for Event ID {event_id}:")
                    print(f"🎫 Total Booked Tickets: {booked_tickets}")
                    print(f"🎟️ Remaining Tickets: {remaining_tickets}")
                    print(f"💰 Total Revenue: {revenue}")

                elif choice == "2":
                    print("\n🆕 Create New Event:")
                    event_name = input("Enter Event Name: ")
                    event_date = input("Enter Event Date (YYYY-MM-DD): ")
                    event_time = input("Enter Event Time (HH:MM:SS): ")

                    # Display available venues before asking for venue_id
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT venue_id, venue_name, address FROM Venue")
                        venues = cursor.fetchall()
                        if venues:
                            print("\n📍 Available Venues:")
                            for v_id, v_name, v_address in venues:
                                print(f"🔹 ID: {v_id} - {v_name}, {v_address}")
                        else:
                            print("❌ No venues available. Please add venues before creating an event.")
                            continue  # Return to Admin menu if no venues

                    venue_id = int(input("Enter Venue ID: "))
                    total_seats = int(input("Enter Total Seats: "))
                    event_type = input("Enter Event Type (Movie/Concert/Sports): ").capitalize()

                    admin.create_event(event_name, event_date, event_time, venue_id, total_seats, event_type)

                elif choice == "3":
                    print("\n🆕 Update Event:")
                    event_id = int(input("Enter Event ID: "))
                    event_name = input("Enter Event Name: ")
                    event_date = input("Enter Event Date (YYYY-MM-DD): ")
                    event_time = input("Enter Event Time (HH:MM:SS): ")
                    venue_id = int(input("Enter Venue ID: "))
                    total_seats = int(input("Enter Total Seats: "))
                    available_seats = int(input("Enter Available Seats: "))

                    admin.update_event(event_id, event_name, event_date, event_time, venue_id, total_seats, available_seats)

                elif choice == "4":
                    print("✅ Exiting Admin Panel.")
                    break
                else:
                    print("❌ Invalid choice! Please select a valid option.")

        else:
            print("❌ Invalid input! Enter 'Admin', 'Customer', or 'Exit'.")

    finally:
        conn.close()


if __name__ == "__main__":
    book_tickets()