import psycopg2 as psycopg2

from loadConfig import load_config
from teamsProvider import TeamsProvider

# Load config file
app_config = load_config()

db_name = app_config["db_name"]
db_schema = app_config["db_schema"]
db_username = app_config["db_username"]
db_password = app_config["db_password"]
db_server = app_config["db_server"]
db_port = app_config["db_port"]
db_flavor = app_config["db_flavor"]
db_conn = f'dbname={db_name} user={db_username} password={db_password} host={db_server} port={db_port}'
teams_webhook_error = app_config["teams_webhook_error"]
teams_webhook_error_test = app_config["teams_webhook_error_test"]

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
