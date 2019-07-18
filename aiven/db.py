import psycopg2
import logging

logger = logging.getLogger(__name__)

HOST = 'pg-2f300e69-alexandv-8e59.aivencloud.com'
PORT = 12105
DBNAME = 'defaultdb'
USER = 'avnadmin'
PASSWORD = 'tavirlyf9q8bejxsHide'


class EventDB:
    MAX_CONN_ATTEMPT = 5
    SLEEP_BETWEEN_RETRIES_SEC = 5

    def __init__(self, autocommit = True, host=HOST, port=PORT, dbname=DBNAME, user=USER, password=PASSWORD):
        self.conn = None
        self.cur = None

        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password

    def __enter__(self):
        self.connect()

        return self

    def __exit__(self, type, value, traceback):
        if type is None and not self.conn.autocommit:
            self.conn.commit()

        if type is not None and not self.conn.autocommit:
            self.conn.rollback()

        self.close_conn()

    def connect(self):
        for attempt_num in range(1,BettingDB.MAX_CONN_ATTEMPT + 1):
            try:
                if self.bettingdbpool is not None:
                    logger.info("Getting connection from pool.")
                    self.conn = self.bettingdbpool.pool.getconn()
                else:
                    logger.info("Connecting to DB {}:{}. Attempt number {}/{}".format(self.host, self.port, attempt_num,
                                                                                      EventDB.MAX_CONN_ATTEMPT))
                    self.conn = psycopg2.connect("dbname="+self.dbname+" user="+self.user+" password="+self.password+" host="+self.host+" port="+str(self.port),cursor_factory=NamedTupleCursor)
            except psycopg2.OperationalError as e:
                logger.error("Error while connecting to postgres {}".format(e))
                if attempt_num == BettingDB.MAX_CONN_ATTEMPT:
                    logger.error("Attempts exhausted. Exiting")
                    sys.exit(1)
                logger.info("Sleeping {} seconds".format(BettingDB.SLEEP_BETWEEN_RETRIES_SEC))
                time.sleep(BettingDB.SLEEP_BETWEEN_RETRIES_SEC)
            else:
                break

        self.cur = self.conn.cursor()


    def close_conn(self):
        self.cur.close()
        if self.bettingdbpool is not None:
            self.bettingdbpool.pool.putconn(self.conn)
            logger.info("DB connection released from pool")
        else:
            self.conn.close()
            logger.info("DB connection closed")


    def insert_event(self) -> List[BetfairMarket]:
        self.cur.execute(f"INSERT INTO event VALUES ;")
        markets = self.cur.fetchall()

        return [BetfairMarket(market.id,market.name,market.betfair_id,market.is_finite_runners) for market in markets]


