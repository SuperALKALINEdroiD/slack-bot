from sqlalchemy import create_engine

class Connection:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_engine(self):
        engine = create_engine(f'sqlite:///{self.db_path}')
        return engine
