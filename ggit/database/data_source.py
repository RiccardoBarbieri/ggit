from ggit.managers import ConfigManager
from ggit.utils import SingletonMeta
from neo4j import Driver, GraphDatabase, Session


class DataSource(metaclass=SingletonMeta):

    """
    This class is a simple wrapper for the neo4j driver, which is used to
    create a session with the database.

    It is a singleton class, so it can be accessed from anywhere in the application and
    the instance will be the same.

    The credentials for the database are retrieved using the :class:`ggit.managers.ConfigManager` class.

    Attributes
    ----------
    driver: :class:`neo4j.Driver`
        The neo4j driver used to create a session with the database.

    Parameters
    ----------
    uri: str
        The uri of the database.
    """

    driver: Driver

    def __init__(self, uri = 'bolt://localhost:7687/'):
        user = ConfigManager()['database_username']
        password = ConfigManager()['database_password']
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def get_driver(self) -> Driver:
        """
        Method to obtain the instance of the neo4j driver.

        Returns
        -------
        :class:`neo4j.Driver`
            The neo4j driver.
        """
        return self.driver

    def new_session(self) -> Session:
        """
        Method used to create a new session with the database.
        It is used as a context manager, so it can be used with the ``with`` statement.

        Returns
        -------
        :class:`neo4j.Session`
            The neo4j session.
        """
        return self.driver.session()

    def close(self):
        """
        Method used to close the connection with the database.
        """
        self.driver.close()

