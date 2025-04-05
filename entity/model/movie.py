from entity.model.event import Event

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