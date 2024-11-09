# memory/memory_setup.py
from neo4j import GraphDatabase

class MemoryDatabase:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_user_preference(self, user_id, preference_type, preference):
        with self.driver.session() as session:
            session.run("MERGE (u:User {id: $user_id}) "
                        "MERGE (p:Preference {type: $preference_type, preference: $preference}) "
                        "MERGE (u)-[:PREFERS]->(p)",
                        user_id=user_id, preference_type=preference_type, preference=preference)
    
if __name__ == "__main__":
    db = MemoryDatabase("neo4j+s://07643c5a.databases.neo4j.io", "neo4j", "4LP_yOD_vYnRtVPwAQRKialPMWV4QyNx72ueBSK4SOQ")
    db.add_user_preference("user123", "interest", "historical sites")
    db.close()

# to run
# python memory_setup.py
