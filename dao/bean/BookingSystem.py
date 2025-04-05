from abc import ABC, abstractmethod

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
