
import psycopg2
import select
import json

# Connect to PostgreSQL DB
conn = psycopg2.connect(
    dbname="source_db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

# Create a replication slot
cur = conn.cursor()
cur.execute("SELECT * FROM pg_create_logical_replication_slot('cdc_slot', 'pgoutput');")
conn.commit()

# Begin changes replication
cur.execute("START_REPLICATION SLOT cdc_slot LOGICAL 0/0 (proto_version '1', publication_names 'mypub');")
conn.commit()

# Detect table changes every 5 seconds
while True:
    if select.select([conn], [], [], 5) == ([], [], []):
        print("Timeout")
    else:
        msg = conn.recv()
		json_data = json.loads(msg.decode('utf-8'))
		
		--write json data to a file
		timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
		file_name = f"customers_cdc_{timestamp}.json"
		
		with open(file_name, 'w') as file:
			json.dump(data, file, indent=4)
        print(msg.payload)
		
        cur.send_feedback(flush_lsn=msg.data_start)
		
		