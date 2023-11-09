import mysql.connector

class DB:
    def __init__(self):
        #connect to the database
        try:
            self.conn = mysql.connector.connect(
                host='flights.ctuoxf.us-east-1.rds.amazonaws.com',
                user='admin',
                password='',
                database='flights'
            )
            self.mycursor = self.conn.cursor()
            print('connection established')
        except:
            print('connection error')

    def fetch_city_names(self):
        city = []
        self.mycursor.execute("""SELECT distinct(destination) FROM airport
                                 union
                                 SELECT distinct(source) FROM airport""")

        data = self.mycursor.fetchall()
        for item in data:
            city.append(item[0])

        return city

    def fetch_all_flights(self,source,destination):

        self.mycursor.execute(""" select Airline,Route,Dep_Time,Duration,Price
                                           from airport where source = '{}' and destination = '{}' 
                                           """.format(source,destination))
        data = self.mycursor.fetchall()
        return data

    def fetch_airline_frequency(self):
        airline = []
        frequency = []
        self.mycursor.execute("""
        select airline,count(*) from airport
        group by airline;
        """)
        data = self.mycursor.fetchall()

        for item in data:
            airline.append(item[0])
            frequency.append(item[1])
        return airline,frequency

    def busy_airport(self):
        city = []
        frequency = []
        self.mycursor.execute("""
        select source,count(*) from (select source from airport
							union all
							select destination from airport) t
        group by source
        order by count(*) DESC
        """)
        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])
            frequency.append(item[1])
        return city,frequency

    def daily_frequency(self):
        date = []
        frequency = []
        self.mycursor.execute("""
                select date_of_journey,count(*) from airport
                group by date_of_journey
                """)
        data = self.mycursor.fetchall()
        print(data)

        for item in data:
            date.append(item[0])
            frequency.append(item[1])
        return date, frequency


obj1 = DB()
obj1.daily_frequency()
