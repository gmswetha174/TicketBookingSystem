from entity.model.event import Event

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