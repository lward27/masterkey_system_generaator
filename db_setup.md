This is a test!

```bash
docker pull postgres
```

```bash
docker run --name postgres-mks -p 5432:5432 -e POSTGRES_PASSWORD={topsecretpassword} -d postgres
```

```bash
docker inspect postgres-mks
# find Networks.bridge.IPAddress
```
Primary: 172.17.0.3

```bash
psql -h 172.17.0.3 -p 5432 -U postgres
```

```sql
CREATE DATABASE masterkey_system_generator;
\c masterkey_system_generator
CREATE TABLE masterkey_system (
    id uuid,
    great_grand_master_key VARCHAR(10) NOT NULL,
    rotation VARCHAR(10) NOT NULL,
    key_bitting_array_1 VARCHAR(10) NOT NULL,
    key_bitting_array_2 VARCHAR(10) NOT NULL,
    key_bitting_array_3 VARCHAR(10) NOT NULL,
    key_bitting_array_4 VARCHAR(10) NOT NULL,
    key_bitting_array_5 VARCHAR(10) NULL,
    number_of_pins int NOT NULL,
    kBA_length int NOT NULL,
    page_master_count int NOT NULL,
    maximum_adjacent_cuts int NOT NULL,
    created_on TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE bitting (
    id uuid,
    blind_code VARCHAR(10) NOT NULL,
    bitting VARCHAR(10) NOT NULL,
    top_pin VARCHAR(10) NOT NULL,
    bottom_pin VARCHAR(10) NOT NULL,
    state VARCHAR(10),
    master_key_system uuid NOT NULL,
    great_grand_master uuid NULL,
    row_master uuid NULL,
    page_master uuid NULL,
    page_block_master uuid NULL,
    page_group_master uuid NULL,
    page_section_master uuid NULL,
    block_master uuid NULL,
    key_level VARCHAR(20) NOT NULL,
    PRIMARY KEY (id)
);
```

HERE DOWN IS NOT RELEVANT TO RUNNING THE MAIN APPLICATION AND IS JUST FOR FUN!

## To setup logical replication

On Both Containers run:
```bash
docker exec -it postgres-mks bash
apt-get update
apt-get install vim
apt-get install iputils-ping
```

```bash
cd /var/lib/postgresql/data
vim postgresql.conf

# edit
wal_level = logical
max_wal_senders = 10
```

```bash
apt-get install iputils-ping
ping 172.17.0.4
```

```bash
cd /var/lib/postgresql/data
vim pg_hba.conf
```

On Primary:
```sql
\c test_database
CREATE PUBLICATION testpub FOR TABLE foo;
```

On Secondary:
```sql
\c test_database
CREATE SUBSCRIPTION testsub CONNECTION 'dbname=test_database host=172.17.0.2 user=postgres password={topsecretpassword}' PUBLICATION testpub;
```

On Primary:
```sql
\c test_database
INSERT INTO foo (first_name, last_name, email, created_on) VALUES ('Lucas', 'Ward', 'lucasward@gmail.com', CURRENT_TIMESTAMP);

--> then retrieve the row to see the data
SELECT * FROM foo;
```

On Secondary:
```sql
\c test_database
SELECT * FROM foo;
```

# Graph Database setup

```bash
docker run -d -p 8080:8080 \
  -e HASURA_GRAPHQL_DATABASE_URL=postgres://postgres:{topsecretpassword}@127.0.0.1:5432/test_database \
  -e HASURA_GRAPHQL_ENABLE_CONSOLE=true \
  hasura/graphql-engine:latest
```