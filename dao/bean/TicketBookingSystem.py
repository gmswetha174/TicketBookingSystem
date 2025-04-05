from dao.bean.BookingSystem import BookingSystem
from entity.model.movie import Movie
from entity.model.concert import Concert
from entity.model.sports import Sports
from entity.model.booking import Booking
from entity.model.customer import Customer
from util.db_connection import DBConnUtil
from exception.EventNotFoundException import EventNotFoundException
from exception.InvalidBookingIDException import InvalidBookingIDException
from exception.NullPointerException import NullPointerException

class TicketBookingSystem(BookingSystem):
    def __init__(self, conn=None):
        if conn is None:
            raise NullPointerException("Database connection is null")
        self.conn = conn
        self.events = []
        self.bookings = []

    def create_event(self, event_id):
        if self.conn is None:
            raise NullPointerException("Database connection is null")
        
        try:
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
            else:
                raise EventNotFoundException(f"Event with ID {event_id} not found.")
        except Exception as e:
            print(f"Error creating event: {e}")
        return None

    def display_event_details(self, event):
        event.display_event_details()

    def book_tickets(self, event_id, customer_id, num_tickets, ticket_category):
        try:
            event = next((e for e in self.events if e.event_id == event_id), None)
            if not event:
                event = self.create_event(event_id)
            if event and event.available_seats >= num_tickets:
                total_cost = self.calculate_booking_cost(num_tickets, ticket_category)
                customer = Customer(customer_id)
                booking = Booking(customer, event, num_tickets, ticket_category)
                self.bookings.append(booking)
                event.available_seats -= num_tickets

                # Update database
                with self.conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Booking (booking_id, customer_id, event_id, num_tickets, ticket_category, total_cost, booking_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (booking.booking_id, customer_id, event_id, num_tickets, ticket_category, total_cost, booking.booking_date))
                    cursor.execute("UPDATE Event SET available_seats = %s WHERE event_id = %s", (event.available_seats, event_id))
                    self.conn.commit()

                return booking.booking_id
            else:
                raise EventNotFoundException(f"Event with ID {event_id} not found or not enough available seats!")
        except Exception as e:
            print(f"Error booking tickets: {e}")
            self.conn.rollback()
            return None

    def cancel_booking(self, booking_id):
        try:
            booking = next((b for b in self.bookings if b.booking_id == booking_id), None)
            if booking:
                booking.event.available_seats += booking.num_tickets
                self.bookings.remove(booking)

                # Update database
                with self.conn.cursor() as cursor:
                    cursor.execute("DELETE FROM Booking WHERE booking_id = %s", (booking_id,))
                    cursor.execute("UPDATE Event SET available_seats = %s WHERE event_id = %s", (booking.event.available_seats, booking.event.event_id))
                    self.conn.commit()

                return booking.booking_id
            else:
                raise InvalidBookingIDException(f"Booking with ID {booking_id} not found!")
        except Exception as e:
            print(f"Error canceling booking: {e}")
            self.conn.rollback()
            return None

    def get_available_seats(self, event_id):
        try:
            event = next((e for e in self.events if e.event_id == event_id), None)
            if not event:
                event = self.create_event(event_id)
            if event:
                return event.available_seats
            else:
                raise EventNotFoundException(f"Event with ID {event_id} not found!")
        except Exception as e:
            print(f"Error getting available seats: {e}")
            return None

    def calculate_booking_cost(self, num_tickets, ticket_category):
        price_mapping = {"Silver": 200, "Gold": 500, "Diamond": 1000}
        return num_tickets * price_mapping.get(ticket_category, 0)

    def get_booking_details(self, booking_id):
        try:
            booking = next((b for b in self.bookings if b.booking_id == booking_id), None)
            if booking:
                return booking.display_booking_details()
            else:
                raise InvalidBookingIDException(f"Booking with ID {booking_id} not found!")
        except Exception as e:
            print(f"Error getting booking details: {e}")
            return None