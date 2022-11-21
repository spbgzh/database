import psycopg2

conn = psycopg2.connect(database="cinema", user="spbgzh",
                        password="010307", host="localhost", port="5432")
cur = conn.cursor()
list_table = ["order_record", "ticket", "remaining_seat_matrix", "session",
              "hall", "comments",  "movie", "role", "client", "cinema"]

# create tables
cur.execute("""
CREATE TABLE "cinema" (
  "cinema_id" SERIAL,
  "name" varchar(50) NOT NULL,
  "address" varchar(120) NOT NULL,
  PRIMARY KEY ("cinema_id")
);
""")
cur.execute("""
CREATE TABLE "client" (
  "client_id" SERIAL,
  "name" varchar(30) NOT NULL,
  "password" varchar(30) NOT NULL,
  "email" varchar(30) NOT NULL,
  "headImg" varchar(30) DEFAULT NULL,
  PRIMARY KEY ("client_id")
);
""")
cur.execute("""
CREATE TABLE "role" (
  "client_id" Integer REFERENCES "client"(client_id),
  "role" varchar(10) DEFAULT 'USER',
  PRIMARY KEY ("client_id")
);
""")
cur.execute("""
CREATE TABLE "movie" (
  "movie_id" SERIAL,
  "name" varchar(30) NOT NULL,
  "staring" varchar(30) DEFAULT NULL,
  "detail" varchar(350) NOT NULL,
  "duration" varchar(20) DEFAULT NULL,
  "type" varchar(20) NOT NULL,
  "score" varchar(20) DEFAULT NULL,
  "picture" varchar(35) NOT NULL,
  "boxOffice" varchar(20) DEFAULT NULL,
  "commentsCount" varchar(30) DEFAULT NULL,
  "releaseDate" date DEFAULT NULL,
  "boxOfficeUnit" Integer DEFAULT NULL,
  "releasePoint" varchar(30) DEFAULT NULL,
  "commentsUnit" Integer DEFAULT NULL,
  PRIMARY KEY ("movie_id")
);
""")
cur.execute("""
CREATE TABLE "comments" (
  "comments_id" SERIAL,
  "client_id" Integer REFERENCES "client"(client_id),
  "comments" varchar(300) NOT NULL,
  "movie_id" Integer REFERENCES "movie"(movie_id),
  PRIMARY KEY ("comments_id")
);
""")
cur.execute("""
CREATE TABLE "hall" (
  "hall_id" SERIAL,
  "name" varchar(20) NOT NULL,
  "cinema_id" Integer REFERENCES "cinema"(cinema_id),
  "capacity" Integer NOT NULL,
  PRIMARY KEY ("hall_id")
);
""")
cur.execute("""
CREATE TABLE "session" (
  "session_id" SERIAL,
  "hall_id" Integer REFERENCES "hall"(hall_id),
  "cinema_id" Integer REFERENCES "cinema"(cinema_id),
  "movie_id" Integer REFERENCES "movie"(movie_id),
  "date" date NOT NULL,
  "startTime" time DEFAULT NULL,
  "price" Integer NOT NULL,
  PRIMARY KEY ("session_id")
);
""")
cur.execute("""
CREATE TABLE "remaining_seat_matrix" (
  "session_id" Integer REFERENCES "session"(session_id),
  "row" Integer NOT NULL,
  "column" Integer NOT NULL,
  "value" varchar(100) NOT NULL,
  PRIMARY KEY ("session_id")
);
""")
cur.execute("""
CREATE TABLE "ticket" (
  "ticket_id" SERIAL,
  "client_id" Integer REFERENCES "client"(client_id),
  "session_id" Integer REFERENCES "session"(session_id),
  "hall_id" Integer REFERENCES "hall"(hall_id),
  "seat" varchar(50) NOT NULL,
  PRIMARY KEY ("ticket_id")
);
""")
cur.execute("""
CREATE TABLE "order_record" (
  "order_record_id" SERIAL,
  "ticket_id" Integer REFERENCES "ticket"(ticket_id),
  "cinema_id" Integer REFERENCES "cinema"(cinema_id),
  PRIMARY KEY ("order_record_id")
);
""")
conn.commit()


# drop tables
cur.execute("DROP TABLE IF EXISTS {table}".format(table=', '.join(list_table)))
conn.commit()

# delect data from tables
cur.execute("TRUNCATE TABLE {table}".format(table=', '.join(list_table)))
conn.commit()

# create data for tables
# cinema
cur.execute("INSERT INTO cinema VALUES (%s,%s,%s)", ('1', 'Cinemart Cinemas',
            '106-03 Metropolitan Ave, Queens, NY 11375, United States'))
cur.execute("INSERT INTO cinema VALUES (%s,%s,%s)", ('2', 'Alamo Drafthouse Cinema',
            '445 Albee Square W 4th floor, Brooklyn, NY 11201, United States'))
cur.execute("INSERT INTO cinema VALUES (%s,%s,%s)", ('3',
            'College Point Multiplex Cinemas', '2855 Ulmer St, Queens, NY 11357, United States'))
cur.execute("INSERT INTO cinema VALUES (%s,%s,%s)", ('4',
            'Alpine Cinema', '6817 5th Ave, Brooklyn, NY 11220, United States'))
cur.execute("INSERT INTO cinema VALUES (%s,%s,%s)", ('5',
            'Concourse Plaza Multiplex Cinemas', '214 E 161 St, The Bronx, NY 10451, United States'))
# client
cur.execute("INSERT INTO client VALUES (%s,%s,%s,%s,%s)",
            ('1', 'admin', '123', '365166709@gmail.com', 'img/head/admin.jpg'))
cur.execute("INSERT INTO client VALUES (%s,%s,%s,%s,%s)",
            ('2', 'fyf', '123', '2569548856@hotmail.com', 'img/head/fyf.jpg'))
cur.execute("INSERT INTO client VALUES (%s,%s,%s,%s,%s)",
            ('3', 'test1', '123', 'zms@qq.com', 'img/head/zms.jpg'))
cur.execute("INSERT INTO client VALUES (%s,%s,%s,%s,%s)",
            ('4', 'gg', '123', 'liuyang@163.com', 'img/head/ly.jpg'))
cur.execute("INSERT INTO client VALUES (%s,%s,%s,%s,%s)",
            ('5', 'test2', '123', 'test@tt.com', 'img/head/tt.jpg'))
# movie
cur.execute("INSERT INTO movie VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", ('1', 'Venom', 'Ruben Fleischer', 'In the film, struggling journalist Brock gains superpowers after becoming the host of an alien symbiote, Venom, whose species plans to invade Earth.',
            '112', 'Action,Sci-fi', '9.3', 'img/movies/movie1.jpg', '14.86', '66.8', '2018-11-09', '100000000', 'America', '10000'))
cur.execute("INSERT INTO movie VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", ('2', 'Fantastic Beasts', 'David Yates',
            'Set in 1927, it follows Newt Scamander and Albus Dumbledore as they attempt to take down the dark wizard Gellert Grindelwald while facing new threats in a more divided wizarding world.', '134', 'Fantasy,Adventure', '7.7', 'img/movies/movie2.jpg', '2.92', '90291', '2018-11-16', '100000000', 'Britain', '1'))
cur.execute("INSERT INTO movie VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", ('3', 'Case Closed: Zero the Enforcer', 'Yuzuru Tachikawa',
            'Located in Tokyo Bay, the newly built integrated resort and convention center "Edge of Ocean" is going to host an upcoming Summit Meeting. ', '111', 'animation, action', '8.5', 'img/movies/movie4.jpg', '1.22', '95339', '2018-11-09', '100000000', 'Japan', '1'))
# comments
cur.execute("INSERT INTO comments VALUES (%s,%s,%s,%s)",
            ('1', '1', 'Such a good movie!', '1'))
cur.execute("INSERT INTO comments VALUES (%s,%s,%s,%s)",
            ('2', '2', 'I love this movie!', '2'))
cur.execute("INSERT INTO comments VALUES (%s,%s,%s,%s)",
            ('3', '3', 'No doubt great mobie!', '2'))
cur.execute("INSERT INTO comments VALUES (%s,%s,%s,%s)",
            ('4', '4', 'So bad!', '3'))
cur.execute("INSERT INTO comments VALUES (%s,%s,%s,%s)",
            ('5', '1', 'Looking forward next movie!', '3'))
# hall
cur.execute("INSERT INTO hall VALUES (%s,%s,%s,%s)",
            ('1', 'Hall number one', '1', '30'))
cur.execute("INSERT INTO hall VALUES (%s,%s,%s,%s)",
            ('2', 'Hall number two', '1', '30'))
cur.execute("INSERT INTO hall VALUES (%s,%s,%s,%s)",
            ('3', 'Hall number three', '1', '30'))
cur.execute("INSERT INTO hall VALUES (%s,%s,%s,%s)",
            ('4', 'Hall number one', '2', '30'))
cur.execute("INSERT INTO hall VALUES (%s,%s,%s,%s)",
            ('5', 'Hall number two', '2', '30'))
# session
cur.execute("INSERT INTO session VALUES (%s,%s,%s,%s,%s,%s,%s)",
            ('1', '1', '1', '1', '2022-11-28', '20:30:00', '43'))
cur.execute("INSERT INTO session VALUES (%s,%s,%s,%s,%s,%s,%s)",
            ('2', '2', '1', '2', '2022-11-30', '20:50:00', '43'))
cur.execute("INSERT INTO session VALUES (%s,%s,%s,%s,%s,%s,%s)",
            ('3', '1', '1', '3', '2022-11-30', '10:30:00', '38'))
cur.execute("INSERT INTO session VALUES (%s,%s,%s,%s,%s,%s,%s)",
            ('4', '1', '2', '2', '2022-11-30', '19:45:00', '39'))
cur.execute("INSERT INTO session VALUES (%s,%s,%s,%s,%s,%s,%s)",
            ('5', '2', '2', '3', '2022-11-30', '19:45:00', '39'))
# ticket
cur.execute("INSERT INTO ticket VALUES (%s,%s,%s,%s,%s)",
            ('1', '1', '2', '2', 'R1'))
cur.execute("INSERT INTO ticket VALUES (%s,%s,%s,%s,%s)",
            ('2', '1', '2', '2', 'P2'))
cur.execute("INSERT INTO ticket VALUES (%s,%s,%s,%s,%s)",
            ('3', '1', '2', '2', 'I1'))
cur.execute("INSERT INTO ticket VALUES (%s,%s,%s,%s,%s)",
            ('4', '1', '2', '2', 'R13'))
cur.execute("INSERT INTO ticket VALUES (%s,%s,%s,%s,%s)",
            ('5', '1', '2', '2', 'J10'))
# order_record
cur.execute("INSERT INTO ticket VALUES (%s,%s,%s)", ('1', '1', '1'))
cur.execute("INSERT INTO ticket VALUES (%s,%s,%s)", ('2', '2', '1'))
cur.execute("INSERT INTO ticket VALUES (%s,%s,%s)", ('3', '3', '2'))
cur.execute("INSERT INTO ticket VALUES (%s,%s,%s)", ('4', '4', '2'))
cur.execute("INSERT INTO ticket VALUES (%s,%s,%s)", ('5', '5', '2'))
# remaining_seat_matrix
cur.execute("INSERT INTO remaining_seat_matrix VALUES (%s,%s,%s,%s)",
            ('1', '5', '6', '000010101010100000100010000110'))
cur.execute("INSERT INTO remaining_seat_matrix VALUES (%s,%s,%s,%s)",
            ('2', '5', '6', '000010101010100000100010000110'))
cur.execute("INSERT INTO remaining_seat_matrix VALUES (%s,%s,%s,%s)",
            ('3', '5', '6', '000010101010100000100010000110'))
cur.execute("INSERT INTO remaining_seat_matrix VALUES (%s,%s,%s,%s)",
            ('4', '5', '6', '000010101010100000100010000110'))
cur.execute("INSERT INTO remaining_seat_matrix VALUES (%s,%s,%s,%s)",
            ('5', '5', '6', '000010101010100000100010000110'))
# role
cur.execute("INSERT INTO role VALUES (%s,%s)", ('1', 'ADMIN'))
cur.execute("INSERT INTO role VALUES (%s,%s)", ('2', 'USER'))
cur.execute("INSERT INTO role VALUES (%s,%s)", ('3', 'VIP'))
cur.execute("INSERT INTO role VALUES (%s,%s)", ('4', 'USER'))
cur.execute("INSERT INTO role VALUES (%s,%s)", ('5', 'VIP'))
conn.commit()


cur.close()
conn.close()
