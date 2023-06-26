import sqlalchemy as db
import pandas as pd


class Connector:
    def __init__(self, host, user, secret, dbname):
        self.function_db = None
        self.connection = None
        self.engine = None
        self.clone_db = None
        self.meta = None
        self.host = host
        self.user = user
        self.secret = secret
        self.dbName = dbname

    def connect(self):
        self.engine = db.create_engine(
            f"postgresql://{self.user}:{self.secret}@{self.host}/{self.dbName}")
        self.meta = db.MetaData()
        self.connection = self.engine.connect()
        print(self.connection)

    def fetchTrueClones(self, limit=50000, offset=0, ty="1,2,3", extra=""):
        if not self.connection:
            print("Connection not established")
            return
        statement = db.text(f'''SELECT t1.function_id_one, t1.function_id_two ,t1.functionality_id, rt1.text as "cloneOne", rt2.text as "cloneTwo"
FROM clones t1
JOIN pretty_printed_functions rt1 ON t1.function_id_one = rt1.function_id
JOIN pretty_printed_functions rt2 ON t1.function_id_two = rt2.function_id
WHERE syntactic_type in ({ty})
and type = 'tagged-tagged'
limit {limit} offset {offset}
{extra};''')
        fetch = pd.read_sql_query(statement, self.connection)
        return fetch

        fetch = pd.read_sql_query(statement, self.connection)
        return fetch
    def select(self, custom=""):
        if not self.connection or not custom:
            print("Connection not established or empty query")
            return
        statement = db.text(f'''{custom}''')
        # statement = db.text(f'''
        #     SELECT text from pretty_printed_functions limit 40000;
        # ''')
        fetch = pd.read_sql_query(statement, self.connection)
        return fetch
    
    def fetchFalseClones(self, limit=50000, offset=0, bw=[0.1, 0.2], ty="1,2,3", extra=""):
        if not self.connection:
            print("Connection not established")
            return
        statement = db.text(f'''SELECT t1.function_id_one, t1.function_id_two ,t1.functionality_id, rt1.text as "cloneOne", rt2.text as "cloneTwo"
FROM false_positives t1
JOIN pretty_printed_functions rt1 ON t1.function_id_one = rt1.function_id
JOIN pretty_printed_functions rt2 ON t1.function_id_two = rt2.function_id
WHERE syntactic_type in ({ty})
limit {limit} offset {offset}
{extra};''')
        # statement = db.text(f'''
        #     SELECT text from pretty_printed_functions limit 40000;
        # ''')
        fetch = pd.read_sql_query(statement, self.connection)
        return fetch
    

    def add(self, values):
        if not self.connection:
            print("Connection not established")
            return
        res = self.connection.execute(db.insert(self.clone_db),
                                      values
                                      )
        self.connection.commit()
