CREATE DATABASE TicketBookingSystem;
USE TicketBookingSystem;


-- Venue Table
CREATE TABLE Venue (
    venue_id INT PRIMARY KEY AUTO_INCREMENT,
    venue_name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL
);

-- Event Table
CREATE TABLE Event (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    event_name VARCHAR(255) NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    venue_id INT NOT NULL,
    total_seats INT NOT NULL,
    available_seats INT NOT NULL,
    ticket_price DECIMAL(10,2) NOT NULL,
    event_type ENUM('Movie', 'Sports', 'Concert') NOT NULL,
    FOREIGN KEY (venue_id) REFERENCES Venue(venue_id)
);


-- Customer Table
CREATE TABLE Customer (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL
);


-- Booking Table
CREATE TABLE Booking (
    booking_id INT(20) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    customer_id INT NOT NULL,
    event_id INT NOT NULL,
    num_tickets INT NOT NULL,
    total_cost DECIMAL(10,2) NOT NULL,
    booking_date DATE NOT NULL ,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE
);

-- task 2
-- 1. Insert at least 10 sample records into each table
INSERT INTO Venue (venue_name, address) VALUES
('Stadium A', '123 Main St'),
('Concert Hall B', '456 Elm St'),
('Theater C', '789 Oak St'),
('Arena D', '321 Maple St'),
('Sports Complex E', '654 Pine St'),
('Convention Center F', '987 Cedar St'),
('Music Hall G', '741 Birch St'),
('Open Air Theater H', '852 Walnut St'),
('Multipurpose Hall I', '963 Cherry St'),
('Event Dome J', '147 Willow St'),
('Exhibition Center K', '258 Palm St'),
('Sports Arena L', '369 Spruce St'),
('Grand Theater M', '147 Redwood St'),
('City Auditorium N', '753 Cypress St'),
('Sky Dome O', '951 Magnolia St'),
('Royal Opera House P', '852 Juniper St'),
('Conference Hall Q', '654 Ash St'),
('Central Pavilion R', '321 Sycamore St'),
('Outdoor Stage S', '159 Fir St'),
('Mega Event Hall T', '753 Aspen St');


INSERT INTO Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, ticket_price, event_type) VALUES
('World Cup Final', '2025-06-10', '18:00:00', 1, 20000, 15000, 1500.00, 'Sports'),
('Rock Concert Night', '2025-07-15', '20:30:00', 2, 10000, 5000, 1200.00, 'Concert'),
('Football Cup Semi Final', '2025-05-20', '17:00:00', 1, 25000, 20000, 1800.00, 'Sports'),
('Movie Premiere', '2025-08-01', '19:30:00', 3, 500, 100, 500.00, 'Movie'),
('Jazz Concert Evening', '2025-07-25', '21:00:00', 4, 7000, 2000, 1600.00, 'Concert'),
('Cricket World Cup', '2025-09-12', '15:00:00', 5, 30000, 28000, 2100.00, 'Sports'),
('Drama Play Night', '2025-10-05', '19:00:00', 6, 800, 300, 700.00, 'Movie'),
('Music Festival', '2025-11-10', '22:00:00', 7, 15000, 9000, 2500.00, 'Concert'),
('Film Screening', '2025-12-01', '16:00:00', 8, 400, 50, 450.00, 'Movie'),
('The Grand Finale Concert', '2026-01-15', '20:00:00', 9, 20000, 10000, 2300.00, 'Concert'),
('Basketball Finals', '2025-06-20', '19:00:00', 11, 15000, 12000, 1700.00, 'Sports'),
('Symphony Orchestra', '2025-07-30', '20:00:00', 12, 2000, 800, 1300.00, 'Concert'),
('Tennis Championship', '2025-08-12', '18:00:00', 13, 10000, 7500, 900.00, 'Sports'),
('Broadway Musical', '2025-09-05', '19:30:00', 14, 500, 100, 1100.00, 'Movie'),
('Hip-Hop Festival', '2025-10-10', '21:00:00', 15, 12000, 5000, 2000.00, 'Concert'),
('Marathon Closing Ceremony', '2025-11-15', '14:00:00', 16, 3000, 2500, 600.00, 'Sports'),
('Cultural Dance Show', '2025-12-25', '20:30:00', 17, 700, 300, 800.00, 'Movie'),
('Opera Night', '2026-01-05', '19:00:00', 18, 2500, 1500, 2500.00, 'Concert'),
('Comedy Stand-Up', '2026-02-14', '20:00:00', 19, 3000, 2000, 1000.00, 'Movie'),
('Indie Rock Night', '2026-03-22', '22:00:00', 20, 10000, 6000, 2200.00, 'Concert');


INSERT INTO Customer (customer_name, email, phone_number) VALUES
('Alice Johnson', 'alice@email.com', '123450000'),
('Bob Smith', 'bob@email.com', '987650000'),
('Charlie Brown', 'charlie@email.com', '456780111'),
('David White', 'david@email.com', '321450222'),
('Eva Green', 'eva@email.com', '147850333'),
('Frank Black', 'frank@email.com', '258960444'),
('Grace Kelly', 'grace@email.com', '369070555'),
('Hank Moody', 'hank@email.com', '789650666'),
('Ivy Stone', 'ivy@email.com', '951260777'),
('Jack Daniels', 'jack@email.com', '159370888'),
('Karen Wilson', 'karen@email.com', '111222333'),
('Leo Adams', 'leo@email.com', '444555666'),
('Mia Thompson', 'mia@email.com', '777888999'),
('Noah Carter', 'noah@email.com', '000111222'),
('Olivia Wright', 'olivia@email.com', '333444555'),
('Paul Anderson', 'paul@email.com', '666777888'),
('Quinn Roberts', 'quinn@email.com', '999000111'),
('Rachel Scott', 'rachel@email.com', '222333444'),
('Steve Lopez', 'steve@email.com', '555666777'),
('Tina Martinez', 'tina@email.com', '888999000');


INSERT INTO Booking (customer_id, event_id, num_tickets, total_cost, booking_date) VALUES
(1, 1, 5, 7500.00, '2025-06-01'),
(2, 2, 2, 2400.00, '2025-07-10'),
(3, 3, 3, 5400.00, '2025-05-15'),
(4, 4, 1, 500.00, '2025-07-28'),
(5, 5, 4, 6400.00, '2025-07-20'),
(6, 6, 6, 12600.00, '2025-09-01'),
(7, 7, 2, 1400.00, '2025-10-02'),
(8, 8, 10, 25000.00, '2025-11-05'),
(9, 9, 1, 450.00, '2025-12-01'),
(10, 10, 8, 18400.00, '2026-01-05'),
(11, 11, 4, 6800.00, '2025-06-15'),
(12, 12, 2, 2600.00, '2025-07-28'),
(13, 13, 3, 2700.00, '2025-08-10'),
(14, 14, 1, 1100.00, '2025-09-02'),
(15, 15, 5, 10000.00, '2025-10-05'),
(16, 16, 6, 3600.00, '2025-11-10'),
(17, 17, 2, 1600.00, '2025-12-20'),
(18, 18, 8, 20000.00, '2026-01-01'),
(19, 19, 3, 3000.00, '2026-02-10'),
(20, 20, 7, 15400.00, '2026-03-15');

ALTER TABLE Booking DROP FOREIGN KEY Booking_ibfk_1;
ALTER TABLE Booking DROP FOREIGN KEY Booking_ibfk_2;
desc booking;

ALTER TABLE Event 
DROP COLUMN ticket_price;

desc event;

ALTER TABLE Booking 
ADD COLUMN ticket_category ENUM('Silver', 'Gold', 'Diamond') NOT NULL AFTER num_tickets;

desc booking;

ALTER TABLE Booking 
ADD CONSTRAINT fk_booking_customer FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
ADD CONSTRAINT fk_booking_event FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE;

SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE 
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS 
WHERE TABLE_NAME = 'Booking' AND TABLE_SCHEMA = DATABASE();

desc booking;

CREATE TABLE Movie (
    movie_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT UNIQUE,
    genre VARCHAR(50) NOT NULL,
    actor_name VARCHAR(100) NOT NULL,
    actress_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE
);

DESC movie;
INSERT INTO Movie (event_id, genre, actor_name, actress_name) VALUES
((SELECT event_id FROM Event WHERE event_name = 'Movie Premiere'), 'Drama', 'Leonardo DiCaprio', 'Emma Watson'),
((SELECT event_id FROM Event WHERE event_name = 'Drama Play Night'), 'Theater', 'Hugh Jackman', 'Anne Hathaway'),
((SELECT event_id FROM Event WHERE event_name = 'Film Screening'), 'Thriller', 'Tom Hardy', 'Natalie Portman'),
((SELECT event_id FROM Event WHERE event_name = 'Broadway Musical'), 'Musical', 'Lin-Manuel Miranda', 'Idina Menzel'),
((SELECT event_id FROM Event WHERE event_name = 'Cultural Dance Show'), 'Dance', 'Shahid Kapoor', 'Madhuri Dixit'),
((SELECT event_id FROM Event WHERE event_name = 'Comedy Stand-Up'), 'Comedy', 'Kevin Hart', 'Tiffany Haddish');

SELECT*FROM movie;

CREATE TABLE Concert (
    concert_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT UNIQUE NOT NULL,
    artist VARCHAR(255) NOT NULL,
    concert_type VARCHAR(100) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE
);

DESC concert;

INSERT INTO Concert (event_id, artist, concert_type) VALUES
((SELECT event_id FROM Event WHERE event_name = 'Rock Concert Night'), 'Linkin Park', 'Rock'),
((SELECT event_id FROM Event WHERE event_name = 'Jazz Concert Evening'), 'Norah Jones', 'Jazz'),
((SELECT event_id FROM Event WHERE event_name = 'Music Festival'), 'Various Artists', 'Festival'),
((SELECT event_id FROM Event WHERE event_name = 'The Grand Finale Concert'), 'Ed Sheeran', 'Pop'),
((SELECT event_id FROM Event WHERE event_name = 'Symphony Orchestra'), 'London Philharmonic', 'Classical'),
((SELECT event_id FROM Event WHERE event_name = 'Hip-Hop Festival'), 'Kanye West', 'Hip-Hop'),
((SELECT event_id FROM Event WHERE event_name = 'Opera Night'), 'Andrea Bocelli', 'Opera'),
((SELECT event_id FROM Event WHERE event_name = 'Indie Rock Night'), 'The Strokes', 'Indie Rock');

SELECT * FROM concert;

CREATE TABLE Sports (
    sports_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT UNIQUE NOT NULL,
    sport_name VARCHAR(100) NOT NULL,
    teams_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE
);

DESC sports;

INSERT INTO Sports (event_id, sport_name, teams_name) VALUES
((SELECT event_id FROM Event WHERE event_name = 'World Cup Final'), 'Football', 'Brazil vs Argentina'),
((SELECT event_id FROM Event WHERE event_name = 'Football Cup Semi Final'), 'Football', 'Spain vs Germany'),
((SELECT event_id FROM Event WHERE event_name = 'Cricket World Cup'), 'Cricket', 'India vs Australia'),
((SELECT event_id FROM Event WHERE event_name = 'Basketball Finals'), 'Basketball', 'Lakers vs Warriors'),
((SELECT event_id FROM Event WHERE event_name = 'Tennis Championship'), 'Tennis', 'Novak Djokovic vs Rafael Nadal'),
((SELECT event_id FROM Event WHERE event_name = 'Marathon Closing Ceremony'), 'Athletics', 'Global Marathon Winners');


SELECT * FROM sports;

SELECT 'Event' AS TableName, COUNT(*) AS TotalEntries FROM Event
UNION ALL
SELECT 'Movie', COUNT(*) FROM Movie
UNION ALL
SELECT 'Concert', COUNT(*) FROM Concert
UNION ALL
SELECT 'Sports', COUNT(*) FROM Sports;
