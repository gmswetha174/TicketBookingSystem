from abc import ABC, abstractmethod
from datetime import datetime

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
            try:
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
            except Exception as e:
                print(f"❌ Booking failed due to: {e}")
                self.conn.rollback()
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