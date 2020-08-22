import sqlite3
from sqlite3 import Error

######### DB NAME "appointment.db" ##########
database = "appointment.db"


class MyDbClass:
    __instance = None

    @staticmethod
    def getInstance(db_file):
        """ Static access method """
        if MyDbClass.__instance is None:
            MyDbClass(db_file)
        return MyDbClass.__instance

    def __init__(self, db_file):
        if MyDbClass.__instance is not None:
            raise Exception("Database connection already present.\n" +
                            "Database instance is Singleton")
        else:
            self.conn = self.create_connection(db_file)
            MyDbClass.__instance = self

    def create_connection(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn

    def runSQL(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()


    def runSQL_(self, sql,params):
        cur = self.conn.cursor()
        cur.execute(sql,params)
        self.conn.commit()
        return cur.rowcount

    def execute_create_table_query(self, sql):
        try:
            c = self.conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

    def execute_and_fetch_results(self, sql, params):
        cur = self.conn.cursor()
        cur.execute(sql,params)
        return cur.fetchall()

    def execute_and_fetch_results_(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

#Create users and availability tables
def create_tables():
    db_class = MyDbClass.getInstance(database)
    sql = """Create table if not exists users (
        userid integer NOT NULL,
        username text NOT NULL PRIMARY KEY,
        password text NOT NULL,
        firstname text NOT NULL,
        lastname text NOT NULL,
        age text NOT NULL,
        city text NOT NULL,
        gender text NOT NULL,
        address text NOT NULL
        );"""
    db_class.execute_create_table_query(sql)
    sql = """Create table if not exists availability (
        userid integer NOT NULL,
        username text NOT NULL,
        appointmentDate Date NOT NULL,
        appointmentTime text NOT NULL,
        doctorName text NOT NULL,
        PRIMARY KEY(userid,appointmentDate,appointmentTime,doctorName),
        CONSTRAINT fk FOREIGN KEY(userid) REFERENCES users(userid) ON DELETE CASCADE
        );"""
    db_class.execute_create_table_query(sql)

#Fetch result of sql query
def get_records(sql,params):
    db_class = MyDbClass.getInstance(database)
    return db_class.execute_and_fetch_results(sql,params)

#Fetch result of sql query with no params
def get_all_records(sql):
    db_class = MyDbClass.getInstance(database)
    return db_class.execute_and_fetch_results_(sql)

#Insert a new record using params
def insert_record(sql,params):
    db_class = MyDbClass.getInstance(database)
    return db_class.runSQL_(sql,params)

#Insert initial record
def insert_init_record(sql):
    db_class = MyDbClass.getInstance(database)
    return db_class.runSQL(sql)
