import sqlite3
from operator import itemgetter
import sys
"""
SINCE YOU'RE TESTING YOU NEVER COMMITTED ANY CHANGES; ADD ALL THOSE COMMITS
"""
class Database:
    """sqlite3 database class that holds tidder info"""
    try:
        DB_LOCATION = "./anything.db"
    except Exception as e:
        print("Database name needs to be in command line. Error: ", e)


    def __init__(self):
        """Initialize db class variables"""
        self.connection = sqlite3.connect(Database.DB_LOCATION)
        self.c = self.connection.cursor()
    #
    def close(self):
        """close sqlite3 connection"""
        self.connection.close()
    #
    # def execute(self, parameters, new_data):
    #     """execute a row of data to current cursor"""
    #     self.cur.execute(parameters, new_data)
    #
    # def executescript(self, many_new_data):
    #     """add many new data to database in one go"""
    #     self.cur.executescript(many_new_data)
    #
    def commit(self):
        """commit changes to database"""
        self.connection.commit()

    def print_table(self, data): #STOLEN CODE!!!
        lengths = [
            [len(str(x)) for x in row]
            for row in data
        ]

        max_lengths = [
            max(map(itemgetter(x), lengths))
            for x in range(0, len(data[0]))
        ]

        format_str = ''.join(map(lambda x: '%%-%ss | ' % x, max_lengths))

        print(format_str % data[0])
        print('-' * (sum(max_lengths) + len(max_lengths) * 3 - 1))

        for x in data[1:]:
            print(format_str % x)
    #
    # def fetchall(self):
    #     self.cur.fetchall()

    """Creates database, and populates database with sample data"""
    def fill_db(self):
        """
        fill_db looks for a third argument in terminal. If the third argument is present then
        the function opens a file with same name and then separate each of the queries and run
        them one by one.
        :return: None
        """
        if len(sys.argv) >= 3:
            file = open(sys.argv[2], 'r')
            sqlFile = file.read()
            file.close()

            # spliting all the commands
            sqlCommands = sqlFile.split(';')

            # Execute every command from the file
            for command in sqlCommands:
                try:
                    self.c.execute(command)
                except sqlite3.OperationalError as msg:
                    print("Command skipped: ", msg)

        self.commit()