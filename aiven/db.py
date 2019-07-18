import psycopg2
import logging

import sys

import time

logger = logging.getLogger(__name__)

class EventDB:
    '''
        Class to handle connection to the databases which stores events
        It support the context manager protocol and can thus be used with the "with" keyword
    '''
    MAX_CONN_ATTEMPT = 5
    SLEEP_BETWEEN_RETRIES_SEC = 5

    def __init__(self, host, port, dbname, user, password, sslcert):
        self.conn = None
        self.cur = None

        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.sslcert = sslcert

    def __enter__(self):
        self.connect()

        return self

    def __exit__(self,exc_type, exc_value, tb):
        self.close_conn()

    def connect(self):
        for attempt_num in range(1,EventDB.MAX_CONN_ATTEMPT + 1):
            try:
                logger.info("Connecting to DB {}:{}. Attempt number {}/{}".format(self.host, self.port, attempt_num,
                                                                                      EventDB.MAX_CONN_ATTEMPT))
                self.conn = psycopg2.connect("dbname="+self.dbname+" user="+self.user+" password="+self.password+" host="+self.host+" port="+str(self.port) + " sslmode=verify-full sslrootcert="+self.sslcert)
            except psycopg2.OperationalError as e:
                logger.error("Error while connecting to postgres {}".format(e))
                if attempt_num == EventDB.MAX_CONN_ATTEMPT:
                    logger.error("Attempts exhausted. Exiting")
                    sys.exit(1)
                logger.info("Sleeping {} seconds".format(EventDB.SLEEP_BETWEEN_RETRIES_SEC))
                time.sleep(EventDB.SLEEP_BETWEEN_RETRIES_SEC)
            else:
                break

        self.conn.autocommit = True
        self.cur = self.conn.cursor()


    def close_conn(self):
        self.cur.close()

        self.conn.close()
        logger.info("DB connection closed")


    def _get_max_id(self, tablename):
        """
            Helper method to retrieve the maximum id in a tablename.
            This is useful for getting the id of a primary key
        """
        self.cur.execute('select coalesce(max (id),0) as maxid from ' + tablename)
        maxid = self.cur.fetchone()

        return maxid[0]


    def insert_event(self, description: str) -> None:
        maxid = self._get_max_id('event')

        sql_event = "insert into event (id,event_type_id,description) values (%s,%s,%s);"
        self.cur.execute(sql_event, (maxid + 1, 1, description))


def get_insert_event_to_db(host, port, dbname, user, password, sslcert):
    '''
    This will return a function that can be used as a callback to insert an event to the DB

    :param host: Hostname for the database
    :param port: Port to connect to
    :param dbname: Database name
    :param user: Username to connect to
    :param password: Password for the connection
    :param sslcert: The root ca certificate used to authenticate the server
    :return:  A function that can be used to insert a message into the event table
    '''

    def insert_event_to_db(message: str):
        '''
            This function is used to insert the event into the DB
            It will handle opening the connection and logging
        '''
        with EventDB(host, port, dbname, user, password, sslcert) as db:
            db.insert_event(message)
            logger.info("Inserted event into DB: {}".format(message))

    return insert_event_to_db