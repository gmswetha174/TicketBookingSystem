from datetime import datetime
from util.db_connection import DBConnUtil
from exception.NullPointerException import NullPointerException
class Booking:
    def __init__(self, customer=None, event=None, num_tickets=0, ticket_category=None):
        self.booking_id = self.generate_booking_id()
        self.customer = customer
        self.event = event
        self.num_tickets = num_tickets
        self.ticket_category = ticket_category
        self.total_cost = self.calculate_total_cost()
        self.booking_date = datetime.now()

    def generate_booking_id(self):
        conn = DBConnUtil.get_db_connection()
        if conn is None:
            raise NullPointerException("Database connection is null")
        with conn.cursor() as cursor:
            cursor.execute("SELECT MAX(booking_id) FROM Booking")
            result = cursor.fetchone()
            max_booking_id = result[0] if result[0] is not None else 0
            return max_booking_id + 1

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