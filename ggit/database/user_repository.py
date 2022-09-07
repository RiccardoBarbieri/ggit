from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ggit.database import DataSource

from ggit.entities import User

class UserRepository:
    """
    This repository is used to store and retrieve users from the database.
    It uses the DataSource class to create a session with the database and execute queries.

    Attributes
    ----------
    data_source: :class:`ggit.database.DataSource`
        The DataSource object used to create a session with the database.
    """
    
    data_source: "DataSource"

    def __init__(self, data_source: "DataSource") -> None:
        self.data_source = data_source

    def add_user(self, user: User) -> bool:
        """
        This method adds a user to the database, creating a node with the name and email properties.

        Parameters
        ----------
        user: :class:`ggit.entities.User`
            The user to be added to the database.

        Returns
        -------
        bool
            True if the user was added successfully, False otherwise.
        """
        with self.data_source.new_session() as session:
            result = session.run(
                "MERGE (user:User {name: $name, email: $email}) RETURN user", name=user.name, email=user.email)
            return result.consume().counters.nodes_created == 1

    def get_user(self, name: str, email: str) -> User:
        """
        This method gets a user from the database, given its name and email.

        Parameters
        ----------
        name: str
            The name of the user to be retrieved.
        email: str
            The email of the user to be retrieved.

        Returns
        -------
        :class:`ggit.entities.User`
            The user retrieved from the database.
        """
        with self.data_source.new_session() as session:
            result = session.run(
                "MATCH (user:User {name: $name, email: $email}) RETURN user", name=name, email=email)
            if result.single() is None:
                return None
            return User(result.single()['user']['name'], result.single()['user']['email'])

    def get_all_users(self) -> List[User]:
        """
        This method gets all the users from the database.
        
        Returns
        -------
        List[:class:`ggit.entities.User`]
            The list of users retrieved from the database.
        """
        with self.data_source.new_session() as session:
            result = session.run("MATCH (user:User) RETURN user")
            return [User(record['user']['name'], record['user']['email']) for record in result]

    def delete_user(self, name: str, email: str) -> bool:
        """
        This method deletes a user from the database, given its name and email.

        Parameters
        ----------
        name: str
            The name of the user to be deleted.
        email: str
            The email of the user to be deleted.

        Returns
        -------
        bool
            True if the user was deleted successfully, False otherwise.
        """
        with self.data_source.new_session() as session:
            result = session.run(
                "MATCH (user:User {name: $name, email: $email}) DETACH DELETE user", name=name, email=email)
            return result.consume().counters.nodes_deleted == 1