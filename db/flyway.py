from py4j.java_gateway import JavaGateway, GatewayParameters
import os

class FlywayMigration:
    """Manages Flyway migrations via Java API"""

    def __init__(self, flyway_jar_path="lib/flyway/flyway-core-*.jar"):
        os.environ["CLASSPATH"] = flyway_jar_path
        self.gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True))
        self.Flyway = self.gateway.jvm.org.flywaydb.core.Flyway

        self.flyway = self.Flyway.configure() \
            .dataSource("jdbc:duckdb:pyperfect.db", "", "") \
            .locations("filesystem:db/migrations") \
            .baselineOnMigrate(True) \
            .load()

    def migrate(self):
        """Runs Flyway migrations"""
        self.flyway.migrate()

    def clean(self):
        """Drops all tables (only use in dev!)"""
        self.flyway.clean()

    def info(self):
        """Prints migration history"""
        print(self.flyway.info().all())
