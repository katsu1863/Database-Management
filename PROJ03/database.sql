DROP TABLE IF EXISTS Ticket;
DROP TABLE IF EXISTS Concert;
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Customer;

-- Database Schema
CREATE TABLE Artist (
    artist_id INT PRIMARY KEY AUTO_INCREMENT,
    artist_name VARCHAR(20) NOT NULL,
    genre VARCHAR(20) NOT NULL
);

CREATE TABLE Concert (
    concert_id INT PRIMARY KEY AUTO_INCREMENT,
    venue_name VARCHAR(40) NOT NULL,
    city VARCHAR(30) NOT NULL,
    concert_date DATE NOT NULL,
    artist_id INT NOT NULL,

    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id)
        ON DELETE CASCADE
);

CREATE TABLE Customer (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(20) NOT NULL
);

CREATE TABLE Ticket (
    ticket_id INT PRIMARY KEY AUTO_INCREMENT,
    concert_id INT NOT NULL,
    customer_id INT NOT NULL,
    seat_number VARCHAR(5) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,

    FOREIGN KEY (concert_id) REFERENCES Concert(concert_id)
        ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
        ON DELETE RESTRICT
);

-- Initial Inserts
INSERT INTO Artist VALUES (1, 'Stray Kids', 'K-Pop');
INSERT INTO Artist VALUES (2, 'Shakira', 'Pop');

INSERT INTO Concert VALUES (1, 'Flushing Meadows Park', 'Queens', '2026-06-06', 1);
INSERT INTO Concert VALUES (2, 'Intuit Dome', 'Inglewood', '2026-06-13', 2);

INSERT INTO Customer VALUES (1, 'Shirley');
INSERT INTO Customer VALUES (2, 'Susan');

INSERT INTO Ticket VALUES (1, 2, 1, '14D', 103.43);
INSERT INTO Ticket VALUES (2, 1, 1, '2F', 123.39);