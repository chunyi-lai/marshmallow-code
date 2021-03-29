from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, insert

class Database():
    def __init__(self, db_user, db_port, db_name, db_host):
        '''
        Constructor
        '''
        self.db_user = db_user
        self.db_port = db_port
        self.db_name = db_name
        self.db_host = db_host
    
    def setup_db_connection(self):
        '''
        Setup the db connection
        '''

        # Create engine
        self.engine = create_engine(f"postgresql://{self.db_user}@{self.db_port}:{self.db_port}/{self.db_name}")
