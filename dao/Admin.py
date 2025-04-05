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