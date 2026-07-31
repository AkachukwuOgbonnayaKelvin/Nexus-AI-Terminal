                                          Table "raw.calendar_events"
   Column   |           Type           | Collation | Nullable |                     Default                     
------------+--------------------------+-----------+----------+-------------------------------------------------
 id         | integer                  |           | not null | nextval('raw.calendar_events_id_seq'::regclass)
 event_name | text                     |           |          | 
 event_time | timestamp with time zone |           |          | 
 currency   | text                     |           |          | 
 importance | text                     |           |          | 
 actual     | numeric                  |           |          | 
 forecast   | numeric                  |           |          | 
 previous   | numeric                  |           |          | 
 created_at | timestamp with time zone |           |          | now()
Indexes:
    "calendar_events_pkey" PRIMARY KEY, btree (id)

                Sequence "raw.calendar_events_id_seq"
  Type   | Start | Minimum |  Maximum   | Increment | Cycles? | Cache 
---------+-------+---------+------------+-----------+---------+-------
 integer |     1 |       1 | 2147483647 |         1 | no      |     1
Owned by: raw.calendar_events.id

   Index "raw.calendar_events_pkey"
 Column |  Type   | Key? | Definition 
--------+---------+------+------------
 id     | integer | yes  | id
primary key, btree, for table "raw.calendar_events"

                          Table "raw.prices"
  Column   |           Type           | Collation | Nullable | Default 
-----------+--------------------------+-----------+----------+---------
 symbol    | text                     |           | not null | 
 timeframe | text                     |           | not null | 
 timestamp | timestamp with time zone |           | not null | 
 open      | numeric                  |           |          | 
 high      | numeric                  |           |          | 
 low       | numeric                  |           |          | 
 close     | numeric                  |           |          | 
 volume    | numeric                  |           |          | 
Indexes:
    "prices_pkey" PRIMARY KEY, btree (symbol, timeframe, "timestamp")

                  Index "raw.prices_pkey"
  Column   |           Type           | Key? | Definition  
-----------+--------------------------+------+-------------
 symbol    | text                     | yes  | symbol
 timeframe | text                     | yes  | timeframe
 timestamp | timestamp with time zone | yes  | "timestamp"
primary key, btree, for table "raw.prices"

                          Table "raw.symbols"
   Column   |           Type           | Collation | Nullable | Default 
------------+--------------------------+-----------+----------+---------
 symbol     | text                     |           | not null | 
 name       | text                     |           |          | 
 asset_type | text                     |           |          | 
 is_active  | boolean                  |           |          | true
 created_at | timestamp with time zone |           |          | now()
Indexes:
    "symbols_pkey" PRIMARY KEY, btree (symbol)

     Index "raw.symbols_pkey"
 Column | Type | Key? | Definition 
--------+------+------+------------
 symbol | text | yes  | symbol
primary key, btree, for table "raw.symbols"

                           Table "raw.sync_state"
     Column     |           Type           | Collation | Nullable | Default 
----------------+--------------------------+-----------+----------+---------
 stream_name    | text                     |           | not null | 
 last_timestamp | timestamp with time zone |           |          | 
 last_id        | bigint                   |           |          | 
 updated_at     | timestamp with time zone |           |          | now()
Indexes:
    "sync_state_pkey" PRIMARY KEY, btree (stream_name)

       Index "raw.sync_state_pkey"
   Column    | Type | Key? | Definition  
-------------+------+------+-------------
 stream_name | text | yes  | stream_name
primary key, btree, for table "raw.sync_state"

