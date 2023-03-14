import os.path

import psycopg2 as psycopg2

from loadConfig import load_config
from registryLoader import RegistryLoader
from teamsProvider import TeamsProvider

# Load config file/registry
app_config = load_config()
registry = RegistryLoader(app_config["registry_path"])

db_name = registry.get_registry("db_name")
db_schema = registry.get_registry("db_schema")
db_username = registry.get_registry("db_username")
db_password = registry.get_registry("db_password")
db_server = registry.get_registry("db_server")
db_port = registry.get_registry("db_port")
db_flavor = registry.get_registry("db_flavor")
teams_webhook_error = registry.get_registry("teams_webhook_error")
teams_webhook_error_test = registry.get_registry("teams_webhook_error_test")

db_conn = f'dbname={db_name} user={db_username} password={db_password} host={db_server} port={db_port}'


conn = None

try:
    # Setup teams provider
    teamsProvider = TeamsProvider(teams_webhook_error)

    # connect to the PostgreSQL server
    conn = psycopg2.connect(db_conn)

    # create a cursor
    cur = conn.cursor()

    # execute stored procedure / function
    sql = '''select __reports_dw.__reports_dw_lot_list_snapshot()'''
    cur.execute(sql)

    conn.commit()
except (Exception, psycopg2.DatabaseError) as e:
    conn.rollback()
    teamsProvider.text("LOTLIST " + e.pgerror)
    teamsProvider.send()
finally:
    if conn:
        cur.close()
        conn.close()
