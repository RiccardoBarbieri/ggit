from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ggit.database import DataSource

from ggit.entities import User

class UserRepository:
    
        data_source: "DataSource"
    
        def __init__(self, data_source: "DataSource") -> None:
            self.data_source = data_source
    
        def add_user(self, user: User) -> bool:
            with self.data_source.new_session() as session:
                result = session.run(
                    "MERGE (user:User {name: $name, email: $email}) RETURN user", name=user.name, email=user.email)
                return result.consume().counters.nodes_created == 1
    
        def get_user(self, name: str, email: str) -> User:
            with self.data_source.new_session() as session:
                result = session.run(
                    "MATCH (user:User {name: $name, email: $email}) RETURN user", name=name, email=email)
                if result.single() is None:
                    return None
                return User(result.single()['user']['name'], result.single()['user']['email'])
    
        def get_all_users(self) -> List[User]:
            with self.data_source.new_session() as session:
                result = session.run("MATCH (user:User) RETURN user")
                return [User(record['user']['name'], record['user']['email']) for record in result]
    
        def delete_user(self, name: str, email: str) -> bool:
            with self.data_source.new_session() as session:
                result = session.run(
                    "MATCH (user:User {name: $name, email: $email}) DETACH DELETE user", name=name, email=email)
                return result.consume().counters.nodes_deleted == 1