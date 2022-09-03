from ggit.config import ConfigManager
from ggit.utils import SingletonMeta
from neo4j import GraphDatabase


class DataSource(metaclass=SingletonMeta):

    def __init__(self, uri = 'bolt://localhost:7687/'):
        user = ConfigManager()['database_username']
        password = ConfigManager()['database_password']
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def get_driver(self):
        return self.driver

    def new_session(self):
        return self.driver.session()

    def close(self):
        self.driver.close()

data_source = DataSource()
# driver = data_source.get_driver()

with data_source.new_session() as session:
    result = session.run("MATCH (n) RETURN n LIMIT 25")
    for record in result:
        print(record)
