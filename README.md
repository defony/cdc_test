Context
-------
customers_cdc.py script is a simple CDC pipeline listener to capture and process row-level changes
on a table into JSON files.

How to run
----------
1. Install and configure PostgreSQL with logical replication enabled in your configuration (postgresql.conf)::

	wal_level = logical
	max_replication_slots = 10
	max_wal_senders = 10

2. Next, create a publication in PostgreSQL:

	CREATE PUBLICATION mypub FOR TABLE customers;

3. Open terminal and run script:

	py customers_cdc.py script
	
4. Create changes on table:
	
	INSERT INTO customers(name, email) values('Budi','budi@gmail.com');
