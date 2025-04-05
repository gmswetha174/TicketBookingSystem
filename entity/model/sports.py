from entity.model.event import Event

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