--
-- PostgreSQL database dump
--

\restrict cYmORzXOjuJ8m8Zc8kElyh0dfa8nmufJI1uPTmULjj3w4fOQ6zL58QJKFEZ9eIn

-- Dumped from database version 16.13
-- Dumped by pg_dump version 16.13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: timescaledb; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS timescaledb WITH SCHEMA public;


--
-- Name: EXTENSION timescaledb; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION timescaledb IS 'Enables scalable inserts and complex queries for time-series data (Community Edition)';


--
-- Name: metadata; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA metadata;


ALTER SCHEMA metadata OWNER TO postgres;

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: economic_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.economic_events (
    event_id text NOT NULL,
    provider text,
    provider_event_id text,
    country text,
    region text,
    currency text,
    title text,
    short_title text,
    category text,
    subcategory text,
    forecast double precision,
    previous double precision,
    actual double precision,
    consensus double precision,
    revised_previous double precision,
    importance text,
    release_time_utc timestamp with time zone NOT NULL,
    release_time_local timestamp with time zone,
    timezone text,
    frequency text,
    status text,
    source_url text,
    tags text[],
    affected_assets text[],
    affected_markets text[],
    confidence double precision,
    quality_score double precision,
    metadata jsonb,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.economic_events OWNER TO postgres;

--
-- Name: _hyper_4_2_chunk; Type: TABLE; Schema: _timescaledb_internal; Owner: postgres
--

CREATE TABLE _timescaledb_internal._hyper_4_2_chunk (
    CONSTRAINT constraint_2 CHECK (((release_time_utc >= '2025-12-25 01:00:00+01'::timestamp with time zone) AND (release_time_utc < '2026-01-01 01:00:00+01'::timestamp with time zone)))
)
INHERITS (public.economic_events);


ALTER TABLE _timescaledb_internal._hyper_4_2_chunk OWNER TO postgres;

--
-- Name: _hyper_4_3_chunk; Type: TABLE; Schema: _timescaledb_internal; Owner: postgres
--

CREATE TABLE _timescaledb_internal._hyper_4_3_chunk (
    CONSTRAINT constraint_3 CHECK (((release_time_utc >= '2026-05-28 01:00:00+01'::timestamp with time zone) AND (release_time_utc < '2026-06-04 01:00:00+01'::timestamp with time zone)))
)
INHERITS (public.economic_events);


ALTER TABLE _timescaledb_internal._hyper_4_3_chunk OWNER TO postgres;

--
-- Name: _hyper_4_4_chunk; Type: TABLE; Schema: _timescaledb_internal; Owner: postgres
--

CREATE TABLE _timescaledb_internal._hyper_4_4_chunk (
    CONSTRAINT constraint_4 CHECK (((release_time_utc >= '2026-07-09 01:00:00+01'::timestamp with time zone) AND (release_time_utc < '2026-07-16 01:00:00+01'::timestamp with time zone)))
)
INHERITS (public.economic_events);


ALTER TABLE _timescaledb_internal._hyper_4_4_chunk OWNER TO postgres;

--
-- Name: _hyper_4_5_chunk; Type: TABLE; Schema: _timescaledb_internal; Owner: postgres
--

CREATE TABLE _timescaledb_internal._hyper_4_5_chunk (
    CONSTRAINT constraint_5 CHECK (((release_time_utc >= '2026-04-30 01:00:00+01'::timestamp with time zone) AND (release_time_utc < '2026-05-07 01:00:00+01'::timestamp with time zone)))
)
INHERITS (public.economic_events);


ALTER TABLE _timescaledb_internal._hyper_4_5_chunk OWNER TO postgres;

--
-- Name: macro_events_consensus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.macro_events_consensus (
    event_id text NOT NULL,
    country text,
    currency text,
    title text,
    category text,
    subcategory text,
    forecast double precision,
    previous double precision,
    actual double precision,
    consensus double precision,
    revised_previous double precision,
    importance text,
    impact_score integer,
    release_time_utc timestamp with time zone NOT NULL,
    status text,
    source_url text,
    tags text[],
    affected_assets text[],
    confidence double precision,
    quality_score double precision,
    metadata jsonb,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.macro_events_consensus OWNER TO postgres;

--
-- Name: _hyper_7_6_chunk; Type: TABLE; Schema: _timescaledb_internal; Owner: postgres
--

CREATE TABLE _timescaledb_internal._hyper_7_6_chunk (
    CONSTRAINT constraint_6 CHECK (((release_time_utc >= '2026-07-16 01:00:00+01'::timestamp with time zone) AND (release_time_utc < '2026-07-23 01:00:00+01'::timestamp with time zone)))
)
INHERITS (public.macro_events_consensus);


ALTER TABLE _timescaledb_internal._hyper_7_6_chunk OWNER TO postgres;

--
-- Name: asset_registry; Type: TABLE; Schema: metadata; Owner: postgres
--

CREATE TABLE metadata.asset_registry (
    asset_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    symbol text NOT NULL,
    display_symbol text,
    short_name text,
    long_name text,
    description text,
    isin text,
    cusip text,
    sedol text,
    ric text,
    bloomberg_ticker text,
    figi text,
    asset_class text,
    sub_asset_class text,
    instrument_type text,
    sector text,
    industry text,
    sub_industry text,
    theme text,
    strategy_group text,
    market_category text,
    exchange_code text,
    base_currency text,
    quote_currency text,
    settlement_currency text,
    profit_currency text,
    margin_currency text,
    tick_size numeric,
    tick_value numeric,
    point_size numeric,
    digits integer,
    lot_size numeric,
    min_volume numeric,
    max_volume numeric,
    volume_step numeric,
    contract_size numeric,
    market_open time without time zone,
    market_close time without time zone,
    trading_days text,
    holiday_calendar text,
    session_type text,
    timezone text,
    dst_rules text,
    expiration date,
    first_notice date,
    settlement_date date,
    underlying uuid,
    multiplier numeric,
    option_type text,
    strike numeric,
    price_precision integer,
    price_format text,
    tick_format text,
    pip_size numeric,
    fraction_display text,
    margin_requirement numeric,
    leverage_group text,
    swap_long numeric,
    swap_short numeric,
    swap_mode text,
    commission_group text,
    avg_daily_volume numeric,
    avg_spread numeric,
    liquidity_score numeric,
    volatility_score numeric,
    market_cap numeric,
    outstanding_shares numeric,
    float_shares numeric,
    company_id uuid,
    version integer DEFAULT 1,
    quality_score numeric,
    verified boolean DEFAULT false,
    provider text,
    provider_rank integer,
    checksum text,
    last_updated timestamp with time zone DEFAULT now(),
    country_code text,
    sector_id uuid,
    industry_id uuid,
    asset_type_id uuid
);


ALTER TABLE metadata.asset_registry OWNER TO postgres;

--
-- Name: asset_type_registry; Type: TABLE; Schema: metadata; Owner: postgres
--

CREATE TABLE metadata.asset_type_registry (
    asset_type_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name text,
    asset_class text,
    description text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE metadata.asset_type_registry OWNER TO postgres;

--
-- Name: company_registry; Type: TABLE; Schema: metadata; Owner: postgres
--

CREATE TABLE metadata.company_registry (
    company_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name text,
    ceo text,
    headquarters text,
    website text,
    employees integer,
    fiscal_year_end text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE metadata.company_registry OWNER TO postgres;

--
-- Name: country_registry; Type: TABLE; Schema: metadata; Owner: postgres
--

CREATE TABLE metadata.country_registry (
    code text NOT NULL,
    name text,
    region text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE metadata.country_registry OWNER TO postgres;

--
-- Name: currency_registry; Type: TABLE; Schema: metadata; Owner: postgres
--

CREATE TABLE metadata.currency_registry (
    code text NOT NULL,
    name text,
    symbol text,
    decimals integer,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE metadata.currency_registry OWNER TO postgres;

--
-- Name: exchange_registry; Type: TABLE; Schema: metadata; Owner: postgres
--

CREATE TABLE metadata.exchange_registry (
    mic_code text NOT NULL,
    name text,
    country text,
    timezone text,
    market_hours jsonb,
    website text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE metadata.exchange_registry OWNER TO postgres;

--
-- Name: industry_registry; Type: TABLE; Schema: metadata; Owner: postgres
--

CREATE TABLE metadata.industry_registry (
    industry_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name text,
    sector_id uuid,
    description text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE metadata.industry_registry OWNER TO postgres;

--
-- Name: provider_registry; Type: TABLE; Schema: metadata; Owner: postgres
--

CREATE TABLE metadata.provider_registry (
    provider_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name text,
    description text,
    tier integer,
    priority integer,
    status text,
    last_check timestamp with time zone,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE metadata.provider_registry OWNER TO postgres;

--
-- Name: quality_registry; Type: TABLE; Schema: metadata; Owner: postgres
--

CREATE TABLE metadata.quality_registry (
    quality_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    asset_id uuid,
    provider_id uuid,
    quality_score numeric,
    completeness numeric,
    freshness numeric,
    confidence numeric,
    verification_status text,
    issues text[],
    checked_at timestamp with time zone DEFAULT now()
);


ALTER TABLE metadata.quality_registry OWNER TO postgres;

--
-- Name: relationship_registry; Type: TABLE; Schema: metadata; Owner: postgres
--

CREATE TABLE metadata.relationship_registry (
    relationship_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    source_asset_id uuid,
    target_asset_id uuid,
    relationship_type text,
    strength numeric,
    metadata jsonb,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE metadata.relationship_registry OWNER TO postgres;

--
-- Name: sector_registry; Type: TABLE; Schema: metadata; Owner: postgres
--

CREATE TABLE metadata.sector_registry (
    sector_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name text,
    description text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE metadata.sector_registry OWNER TO postgres;

--
-- Name: version_history; Type: TABLE; Schema: metadata; Owner: postgres
--

CREATE TABLE metadata.version_history (
    version_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    asset_id uuid,
    version integer,
    changed_fields jsonb,
    changed_by text,
    changed_at timestamp with time zone DEFAULT now()
);


ALTER TABLE metadata.version_history OWNER TO postgres;

--
-- Name: engine_runs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.engine_runs (
    "time" timestamp with time zone NOT NULL,
    engine_name text NOT NULL,
    status text,
    records_fetched integer,
    error_message text,
    duration_ms integer
);


ALTER TABLE public.engine_runs OWNER TO postgres;

--
-- Name: institutional_positions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.institutional_positions (
    "time" timestamp with time zone NOT NULL,
    symbol text NOT NULL,
    report_type text,
    long_positions bigint,
    short_positions bigint,
    net_positions bigint,
    source text,
    metadata jsonb
);


ALTER TABLE public.institutional_positions OWNER TO postgres;

--
-- Name: macro_events_raw; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.macro_events_raw (
    raw_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    provider text,
    provider_event_id text,
    country text,
    currency text,
    title text,
    category text,
    forecast double precision,
    previous double precision,
    actual double precision,
    importance text,
    release_time_utc timestamp with time zone,
    status text,
    raw_data jsonb,
    ingested_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.macro_events_raw OWNER TO postgres;

--
-- Name: market_prices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.market_prices (
    "time" timestamp with time zone NOT NULL,
    symbol text NOT NULL,
    price double precision,
    volume numeric,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    source text,
    asset_class text,
    confidence_score double precision,
    metadata jsonb
);


ALTER TABLE public.market_prices OWNER TO postgres;

--
-- Name: price_commodities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.price_commodities (
    "time" timestamp with time zone NOT NULL,
    symbol text NOT NULL,
    price double precision,
    volume numeric,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    source text,
    metadata jsonb
);


ALTER TABLE public.price_commodities OWNER TO postgres;

--
-- Name: price_crypto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.price_crypto (
    "time" timestamp with time zone NOT NULL,
    symbol text NOT NULL,
    price double precision,
    volume numeric,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    source text,
    metadata jsonb
);


ALTER TABLE public.price_crypto OWNER TO postgres;

--
-- Name: price_forex; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.price_forex (
    "time" timestamp with time zone NOT NULL,
    symbol text NOT NULL,
    price double precision,
    volume numeric,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    source text,
    metadata jsonb
);


ALTER TABLE public.price_forex OWNER TO postgres;

--
-- Name: price_indices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.price_indices (
    "time" timestamp with time zone NOT NULL,
    symbol text NOT NULL,
    price double precision,
    volume numeric,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    source text,
    metadata jsonb
);


ALTER TABLE public.price_indices OWNER TO postgres;

--
-- Name: price_stocks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.price_stocks (
    "time" timestamp with time zone NOT NULL,
    symbol text NOT NULL,
    price double precision,
    volume numeric,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    source text,
    metadata jsonb
);


ALTER TABLE public.price_stocks OWNER TO postgres;

--
-- Name: _hyper_4_2_chunk created_at; Type: DEFAULT; Schema: _timescaledb_internal; Owner: postgres
--

ALTER TABLE ONLY _timescaledb_internal._hyper_4_2_chunk ALTER COLUMN created_at SET DEFAULT now();


--
-- Name: _hyper_4_3_chunk created_at; Type: DEFAULT; Schema: _timescaledb_internal; Owner: postgres
--

ALTER TABLE ONLY _timescaledb_internal._hyper_4_3_chunk ALTER COLUMN created_at SET DEFAULT now();


--
-- Name: _hyper_4_4_chunk created_at; Type: DEFAULT; Schema: _timescaledb_internal; Owner: postgres
--

ALTER TABLE ONLY _timescaledb_internal._hyper_4_4_chunk ALTER COLUMN created_at SET DEFAULT now();


--
-- Name: _hyper_4_5_chunk created_at; Type: DEFAULT; Schema: _timescaledb_internal; Owner: postgres
--

ALTER TABLE ONLY _timescaledb_internal._hyper_4_5_chunk ALTER COLUMN created_at SET DEFAULT now();


--
-- Name: _hyper_7_6_chunk created_at; Type: DEFAULT; Schema: _timescaledb_internal; Owner: postgres
--

ALTER TABLE ONLY _timescaledb_internal._hyper_7_6_chunk ALTER COLUMN created_at SET DEFAULT now();


--
-- Name: _hyper_7_6_chunk updated_at; Type: DEFAULT; Schema: _timescaledb_internal; Owner: postgres
--

ALTER TABLE ONLY _timescaledb_internal._hyper_7_6_chunk ALTER COLUMN updated_at SET DEFAULT now();


--
-- Data for Name: hypertable; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.hypertable (id, schema_name, table_name, associated_schema_name, associated_table_prefix, num_dimensions, chunk_sizing_func_schema, chunk_sizing_func_name, chunk_target_size, compression_state, compressed_hypertable_id, status) FROM stdin;
4	public	economic_events	_timescaledb_internal	_hyper_4	1	_timescaledb_functions	calculate_chunk_interval	0	0	\N	0
7	public	macro_events_consensus	_timescaledb_internal	_hyper_7	1	_timescaledb_functions	calculate_chunk_interval	0	0	\N	0
\.


--
-- Data for Name: bgw_job; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.bgw_job (id, application_name, schedule_interval, max_runtime, max_retries, retry_period, proc_schema, proc_name, owner, scheduled, fixed_schedule, initial_start, hypertable_id, config, check_schema, check_name, timezone) FROM stdin;
\.


--
-- Data for Name: chunk; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.chunk (id, hypertable_id, schema_name, table_name, compressed_chunk_id, status, osm_chunk, creation_time) FROM stdin;
2	4	_timescaledb_internal	_hyper_4_2_chunk	\N	0	f	2026-07-16 10:54:49.722141+01
3	4	_timescaledb_internal	_hyper_4_3_chunk	\N	0	f	2026-07-16 11:10:41.21676+01
4	4	_timescaledb_internal	_hyper_4_4_chunk	\N	0	f	2026-07-16 11:10:46.386451+01
5	4	_timescaledb_internal	_hyper_4_5_chunk	\N	0	f	2026-07-16 11:10:48.893678+01
6	7	_timescaledb_internal	_hyper_7_6_chunk	\N	0	f	2026-07-16 12:02:25.126528+01
\.


--
-- Data for Name: chunk_column_stats; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.chunk_column_stats (id, hypertable_id, chunk_id, column_name, range_start, range_end, valid) FROM stdin;
\.


--
-- Data for Name: compression_chunk_size; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.compression_chunk_size (chunk_id, compressed_chunk_id, uncompressed_heap_size, uncompressed_toast_size, uncompressed_index_size, compressed_heap_size, compressed_toast_size, compressed_index_size, numrows_pre_compression, numrows_post_compression, numrows_frozen_immediately) FROM stdin;
\.


--
-- Data for Name: compression_settings; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.compression_settings (relid, compress_relid, segmentby, orderby, orderby_desc, orderby_nullsfirst, index) FROM stdin;
\.


--
-- Data for Name: continuous_agg; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_agg (mat_hypertable_id, raw_hypertable_id, parent_mat_hypertable_id, user_view_schema, user_view_name, partial_view_schema, partial_view_name, direct_view_schema, direct_view_name, materialized_only, schema_change_timestamp) FROM stdin;
\.


--
-- Data for Name: continuous_aggs_bucket_function; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_aggs_bucket_function (mat_hypertable_id, bucket_func, bucket_width, bucket_origin, bucket_offset, bucket_timezone, bucket_fixed_width) FROM stdin;
\.


--
-- Data for Name: continuous_aggs_hypertable_invalidation_log; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_aggs_hypertable_invalidation_log (hypertable_id, lowest_modified_value, greatest_modified_value) FROM stdin;
\.


--
-- Data for Name: continuous_aggs_invalidation_threshold; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_aggs_invalidation_threshold (hypertable_id, watermark) FROM stdin;
\.


--
-- Data for Name: continuous_aggs_jobs_refresh_ranges; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_aggs_jobs_refresh_ranges (materialization_id, start_range, end_range, pid, job_id, created_at) FROM stdin;
\.


--
-- Data for Name: continuous_aggs_materialization_invalidation_log; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_aggs_materialization_invalidation_log (materialization_id, lowest_modified_value, greatest_modified_value) FROM stdin;
\.


--
-- Data for Name: continuous_aggs_materialization_ranges; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_aggs_materialization_ranges (materialization_id, lowest_modified_value, greatest_modified_value) FROM stdin;
\.


--
-- Data for Name: continuous_aggs_watermark; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.continuous_aggs_watermark (mat_hypertable_id, watermark) FROM stdin;
\.


--
-- Data for Name: dimension; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.dimension (id, hypertable_id, column_name, column_type, aligned, num_slices, partitioning_func_schema, partitioning_func, interval_length, compress_interval_length, integer_now_func_schema, integer_now_func) FROM stdin;
4	4	release_time_utc	timestamp with time zone	t	\N	\N	\N	604800000000	\N	\N	\N
7	7	release_time_utc	timestamp with time zone	t	\N	\N	\N	604800000000	\N	\N	\N
\.


--
-- Data for Name: dimension_slice; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.dimension_slice (id, chunk_id, dimension_id, range_start, range_end) FROM stdin;
2	2	4	1766620800000000	1767225600000000
3	3	4	1779926400000000	1780531200000000
4	4	4	1783555200000000	1784160000000000
5	5	4	1777507200000000	1778112000000000
6	6	7	1784160000000000	1784764800000000
\.


--
-- Data for Name: metadata; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.metadata (key, value, include_in_telemetry) FROM stdin;
install_timestamp	2026-07-16 10:44:20.81045+01	t
timescaledb_version	2.28.1	f
exported_uuid	a43a0eb3-d912-4481-8e12-14fdf83bf355	t
\.


--
-- Data for Name: tablespace; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: postgres
--

COPY _timescaledb_catalog.tablespace (id, hypertable_id, tablespace_name) FROM stdin;
\.


--
-- Data for Name: _hyper_4_2_chunk; Type: TABLE DATA; Schema: _timescaledb_internal; Owner: postgres
--

COPY _timescaledb_internal._hyper_4_2_chunk (event_id, provider, provider_event_id, country, region, currency, title, short_title, category, subcategory, forecast, previous, actual, consensus, revised_previous, importance, release_time_utc, release_time_local, timezone, frequency, status, source_url, tags, affected_assets, affected_markets, confidence, quality_score, metadata, created_at) FROM stdin;
fred_GDP_2026-01-01T00:00:00	fred	GDP	US	North America	USD	Gross Domestic Product	GDP	GDP	\N	\N	\N	31865.721	\N	\N	High	2026-01-01 00:00:00+01	\N	America/New_York	Quarterly	Released	https://fred.stlouisfed.org/series/GDP	{GDP}	{USD,Treasuries,Stocks}	{FX,Rates,Equities}	0.95	0.95	{"series_id": "GDP"}	2026-07-16 11:15:20.367581+01
\.


--
-- Data for Name: _hyper_4_3_chunk; Type: TABLE DATA; Schema: _timescaledb_internal; Owner: postgres
--

COPY _timescaledb_internal._hyper_4_3_chunk (event_id, provider, provider_event_id, country, region, currency, title, short_title, category, subcategory, forecast, previous, actual, consensus, revised_previous, importance, release_time_utc, release_time_local, timezone, frequency, status, source_url, tags, affected_assets, affected_markets, confidence, quality_score, metadata, created_at) FROM stdin;
fred_CPIAUCSL_2026-06-01T00:00:00	fred	CPIAUCSL	US	North America	USD	Consumer Price Index	CPI	Inflation	\N	\N	\N	332.568	\N	\N	High	2026-06-01 00:00:00+01	\N	America/New_York	Monthly	Released	https://fred.stlouisfed.org/series/CPIAUCSL	{Inflation}	{USD,Treasuries,Stocks}	{FX,Rates,Equities}	0.95	0.95	{"series_id": "CPIAUCSL"}	2026-07-16 11:15:22.480304+01
fred_UNRATE_2026-06-01T00:00:00	fred	UNRATE	US	North America	USD	Unemployment Rate	Unemployment	Employment	\N	\N	\N	4.2	\N	\N	High	2026-06-01 00:00:00+01	\N	America/New_York	Monthly	Released	https://fred.stlouisfed.org/series/UNRATE	{Employment}	{USD,Treasuries,Stocks}	{FX,Rates,Equities}	0.95	0.95	{"series_id": "UNRATE"}	2026-07-16 11:15:25.144497+01
fred_FEDFUNDS_2026-06-01T00:00:00	fred	FEDFUNDS	US	North America	USD	Federal Funds Rate	Fed Funds	Interest Rate	\N	\N	\N	3.63	\N	\N	High	2026-06-01 00:00:00+01	\N	America/New_York	Daily	Released	https://fred.stlouisfed.org/series/FEDFUNDS	{"Interest Rate"}	{USD,Treasuries,Stocks}	{FX,Rates,Equities}	0.95	0.95	{"series_id": "FEDFUNDS"}	2026-07-16 11:15:26.984166+01
fred_PAYEMS_2026-06-01T00:00:00	fred	PAYEMS	US	North America	USD	Nonfarm Payrolls	NFP	Employment	\N	\N	\N	158984	\N	\N	High	2026-06-01 00:00:00+01	\N	America/New_York	Monthly	Released	https://fred.stlouisfed.org/series/PAYEMS	{Employment}	{USD,Treasuries,Stocks}	{FX,Rates,Equities}	0.95	0.95	{"series_id": "PAYEMS"}	2026-07-16 11:15:29.744845+01
fred_PPIACO_2026-06-01T00:00:00	fred	PPIACO	US	North America	USD	Producer Price Index	PPI	Inflation	\N	\N	\N	286.827	\N	\N	High	2026-06-01 00:00:00+01	\N	America/New_York	Monthly	Released	https://fred.stlouisfed.org/series/PPIACO	{Inflation}	{USD,Treasuries,Stocks}	{FX,Rates,Equities}	0.95	0.95	{"series_id": "PPIACO"}	2026-07-16 11:15:35.205085+01
\.


--
-- Data for Name: _hyper_4_4_chunk; Type: TABLE DATA; Schema: _timescaledb_internal; Owner: postgres
--

COPY _timescaledb_internal._hyper_4_4_chunk (event_id, provider, provider_event_id, country, region, currency, title, short_title, category, subcategory, forecast, previous, actual, consensus, revised_previous, importance, release_time_utc, release_time_local, timezone, frequency, status, source_url, tags, affected_assets, affected_markets, confidence, quality_score, metadata, created_at) FROM stdin;
fred_DGS10_2026-07-14T00:00:00	fred	DGS10	US	North America	USD	10-Year Treasury Yield	10Y Treasury	Interest Rate	\N	\N	\N	4.58	\N	\N	High	2026-07-14 00:00:00+01	\N	America/New_York	Daily	Released	https://fred.stlouisfed.org/series/DGS10	{"Interest Rate"}	{USD,Treasuries,Stocks}	{FX,Rates,Equities}	0.95	0.95	{"series_id": "DGS10"}	2026-07-16 11:15:32.936137+01
\.


--
-- Data for Name: _hyper_4_5_chunk; Type: TABLE DATA; Schema: _timescaledb_internal; Owner: postgres
--

COPY _timescaledb_internal._hyper_4_5_chunk (event_id, provider, provider_event_id, country, region, currency, title, short_title, category, subcategory, forecast, previous, actual, consensus, revised_previous, importance, release_time_utc, release_time_local, timezone, frequency, status, source_url, tags, affected_assets, affected_markets, confidence, quality_score, metadata, created_at) FROM stdin;
fred_PCEPI_2026-05-01T00:00:00	fred	PCEPI	US	North America	USD	Personal Consumption Expenditures Price Index	PCE	Inflation	\N	\N	\N	131.527	\N	\N	High	2026-05-01 00:00:00+01	\N	America/New_York	Monthly	Released	https://fred.stlouisfed.org/series/PCEPI	{Inflation}	{USD,Treasuries,Stocks}	{FX,Rates,Equities}	0.95	0.95	{"series_id": "PCEPI"}	2026-07-16 11:15:37.228823+01
fred_M2SL_2026-05-01T00:00:00	fred	M2SL	US	North America	USD	M2 Money Supply	M2	Money Supply	\N	\N	\N	23052.3	\N	\N	Medium	2026-05-01 00:00:00+01	\N	America/New_York	Monthly	Released	https://fred.stlouisfed.org/series/M2SL	{"Money Supply"}	{}	{}	0.95	0.95	{"series_id": "M2SL"}	2026-07-16 11:15:39.102323+01
fred_RSXFS_2026-05-01T00:00:00	fred	RSXFS	US	North America	USD	Retail Sales	Retail Sales	Retail	\N	\N	\N	662752	\N	\N	High	2026-05-01 00:00:00+01	\N	America/New_York	Monthly	Released	https://fred.stlouisfed.org/series/RSXFS	{Retail}	{USD,Treasuries,Stocks}	{FX,Rates,Equities}	0.95	0.95	{"series_id": "RSXFS"}	2026-07-16 11:15:41.096142+01
\.


--
-- Data for Name: _hyper_7_6_chunk; Type: TABLE DATA; Schema: _timescaledb_internal; Owner: postgres
--

COPY _timescaledb_internal._hyper_7_6_chunk (event_id, country, currency, title, category, subcategory, forecast, previous, actual, consensus, revised_previous, importance, impact_score, release_time_utc, status, source_url, tags, affected_assets, confidence, quality_score, metadata, created_at, updated_at) FROM stdin;
ff_us_cpi_2026-07-16	US	USD	Consumer Price Index	Inflation	\N	2.8	2.6	\N	\N	\N	High	100	2026-07-16 08:30:00+01	Scheduled	\N	{}	{USD,US500,Bonds,Treasuries,US10Y,EURUSD,USDJPY,Gold}	0.7	0.7	{"title": "Consumer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "ff_us_cpi_2026-07-16", "forecast": 2.8, "previous": 2.6, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:02:25.052104+01	2026-07-16 12:32:21.283288+01
ff_ecb_rate_2026-07-16	EU	EUR	ECB Interest Rate Decision	Central Bank	\N	3	3.25	\N	\N	\N	High	100	2026-07-16 12:45:00+01	Scheduled	\N	{}	{EUR,Bund,GER40,EURUSD,EURGBP}	0.7	0.7	{"title": "ECB Interest Rate Decision", "actual": null, "status": "Scheduled", "country": "EU", "category": "Central Bank", "currency": "EUR", "event_id": "ff_ecb_rate_2026-07-16", "forecast": 3.0, "previous": 3.25, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T12:45:00"}	2026-07-16 12:02:25.728221+01	2026-07-16 12:32:21.287368+01
ff_us_jobless_2026-07-16	US	USD	Initial Jobless Claims	Labour	\N	220	215	\N	\N	\N	Medium	60	2026-07-16 13:30:00+01	Scheduled	\N	{}	{USD,US500,Bonds,Treasuries,US10Y,EURUSD,USDJPY,Gold}	0.7	0.7	{"title": "Initial Jobless Claims", "actual": null, "status": "Scheduled", "country": "US", "category": "Labour", "currency": "USD", "event_id": "ff_us_jobless_2026-07-16", "forecast": 220, "previous": 215, "provider": "forexfactory", "importance": "Medium", "release_time_utc": "2026-07-16T13:30:00"}	2026-07-16 12:02:25.74286+01	2026-07-16 12:32:21.290144+01
inv_us_ppi_2026-07-16	US	USD	Producer Price Index	Inflation	\N	0.3	0.2	\N	\N	\N	Medium	70	2026-07-16 08:30:00+01	Scheduled	\N	{}	{USD,US500,Bonds,Treasuries,US10Y,EURUSD,USDJPY,Gold}	0.65	0.65	{"title": "Producer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "inv_us_ppi_2026-07-16", "forecast": 0.3, "previous": 0.2, "provider": "investing", "importance": "Medium", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:02:25.765409+01	2026-07-16 12:32:21.293088+01
inv_gdp_q1_2026-07-16	US	USD	GDP Quarterly	Growth	GDP	2.5	2.3	\N	\N	\N	High	90	2026-07-16 12:30:00+01	Scheduled	\N	{}	{USD,US500,Bonds,Treasuries,US10Y,EURUSD,USDJPY,Gold}	0.65	0.65	{"title": "GDP Quarterly", "actual": null, "status": "Scheduled", "country": "US", "category": "Growth", "currency": "USD", "event_id": "inv_gdp_q1_2026-07-16", "forecast": 2.5, "previous": 2.3, "provider": "investing", "importance": "High", "release_time_utc": "2026-07-16T12:30:00"}	2026-07-16 12:02:25.771706+01	2026-07-16 12:32:21.295718+01
\.


--
-- Data for Name: asset_registry; Type: TABLE DATA; Schema: metadata; Owner: postgres
--

COPY metadata.asset_registry (asset_id, symbol, display_symbol, short_name, long_name, description, isin, cusip, sedol, ric, bloomberg_ticker, figi, asset_class, sub_asset_class, instrument_type, sector, industry, sub_industry, theme, strategy_group, market_category, exchange_code, base_currency, quote_currency, settlement_currency, profit_currency, margin_currency, tick_size, tick_value, point_size, digits, lot_size, min_volume, max_volume, volume_step, contract_size, market_open, market_close, trading_days, holiday_calendar, session_type, timezone, dst_rules, expiration, first_notice, settlement_date, underlying, multiplier, option_type, strike, price_precision, price_format, tick_format, pip_size, fraction_display, margin_requirement, leverage_group, swap_long, swap_short, swap_mode, commission_group, avg_daily_volume, avg_spread, liquidity_score, volatility_score, market_cap, outstanding_shares, float_shares, company_id, version, quality_score, verified, provider, provider_rank, checksum, last_updated, country_code, sector_id, industry_id, asset_type_id) FROM stdin;
40d67cd8-a03d-4401-a244-71b8f87d44a8	EURUSD	EURUSD=X	EUR/USD	EUR/USD		\N	\N	\N	\N	\N	\N	forex	\N	\N	\N	\N	\N	\N	\N	\N	CCY	USD	\N	\N	\N	\N	4	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N		\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	0	\N	\N	\N	\N	\N	\N	\N	5	0.90000000000000002220446049250313080847263336181640625	f	yahoo_metadata	5	\N	2026-07-16 09:24:03.234181+01	\N	\N	\N	\N
baa31c07-8546-4e83-a055-75faddcbc0c6	AAPL	AAPL	Apple Inc.	Apple Inc.	Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple Vision Pro, Apple TV, Apple Watch, Beats products, and HomePod, as well as Apple branded and third-party accessories. It also provides AppleCare support and cloud services; and operates various platforms, including the App Store that allows customers to discover and download applications and digital content, such as books, music, video, games, and podcasts, as well as advertising services include third-party licensing arrangements and its own advertising platforms. In addition, the company offers various subscription-based services, such as Apple Arcade, a game subscription service; Apple Fitness+, a personalized fitness service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV, which offers original content and live sports; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It distributes third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers and resellers. The company was formerly known as Apple Computer, Inc. and changed its name to Apple Inc. in January 2007. Apple Inc. was founded in 1976 and is headquartered in Cupertino, California.	\N	\N	\N	\N	\N	\N	equity	\N	\N	\N	\N	\N	\N	\N	\N	NMS	USD	\N	\N	\N	\N	2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N		\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	54481611	\N	\N	\N	4810109091840	\N	\N	\N	1	0.90000000000000002220446049250313080847263336181640625	f	yahoo_metadata	5	\N	2026-07-16 09:24:04.098921+01	United States	a6e6997e-9545-4019-a225-9b423d9493b6	198fe232-86e3-437d-b387-b257c4b1878c	\N
1f6270d2-ca6a-4178-918b-34f569cb8c67	BTC-USD	BTC-USD	Bitcoin USD	Bitcoin USD		\N	\N	\N	\N	\N	\N	unknown	\N	\N	\N	\N	\N	\N	\N	\N	CCC	USD	\N	\N	\N	\N	2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N		\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	31909275580	\N	\N	\N	1282041053184	\N	\N	\N	5	0.90000000000000002220446049250313080847263336181640625	f	yahoo_metadata	5	\N	2026-07-16 09:24:05.043335+01	\N	\N	\N	\N
74f9830d-22b5-44ed-82b9-2c8a67b48f1f	GC=F	GC=F	Gold Aug 26			\N	\N	\N	\N	\N	\N	futures	\N	\N	\N	\N	\N	\N	\N	\N	CMX	USD	\N	\N	\N	\N	2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N		\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2283	\N	\N	\N	\N	\N	\N	\N	5	0.90000000000000002220446049250313080847263336181640625	f	yahoo_metadata	5	\N	2026-07-16 09:24:05.888354+01	\N	\N	\N	\N
\.


--
-- Data for Name: asset_type_registry; Type: TABLE DATA; Schema: metadata; Owner: postgres
--

COPY metadata.asset_type_registry (asset_type_id, name, asset_class, description, created_at) FROM stdin;
74001d53-a93b-4eda-9563-51b54154a04a	Forex Spot	forex	Spot foreign exchange	2026-07-16 06:52:06.202322+01
87f25426-5733-46ac-ad8f-3c81ccbc6952	Stock	equity	Common stock	2026-07-16 06:52:06.202322+01
ee5fb79e-d60d-4ec0-b3e4-03ccaf189632	ETF	equity	Exchange Traded Fund	2026-07-16 06:52:06.202322+01
72cd284b-e349-4250-b2b1-6f9d90bcf6a3	Future	futures	Futures contract	2026-07-16 06:52:06.202322+01
7df6d020-e44b-425a-bc79-a911553efd05	Option	options	Options contract	2026-07-16 06:52:06.202322+01
738b261f-e0c6-4777-93d2-ba2becc5a4c0	Crypto	crypto	Cryptocurrency	2026-07-16 06:52:06.202322+01
e15e232f-f84d-4a96-8660-15f6b12ed5d0	CFD	cfd	Contract for Difference	2026-07-16 06:52:06.202322+01
635eec84-d439-4894-81af-c133fab766a2	Index	index	Market index	2026-07-16 06:52:06.202322+01
f38885f8-2645-4964-8c37-dcc17d54a662	Bond	bond	Government or corporate bond	2026-07-16 06:52:06.202322+01
\.


--
-- Data for Name: company_registry; Type: TABLE DATA; Schema: metadata; Owner: postgres
--

COPY metadata.company_registry (company_id, name, ceo, headquarters, website, employees, fiscal_year_end, created_at) FROM stdin;
\.


--
-- Data for Name: country_registry; Type: TABLE DATA; Schema: metadata; Owner: postgres
--

COPY metadata.country_registry (code, name, region, created_at) FROM stdin;
US	United States	North America	2026-07-16 06:52:05.960786+01
GB	United Kingdom	Europe	2026-07-16 06:52:05.960786+01
DE	Germany	Europe	2026-07-16 06:52:05.960786+01
FR	France	Europe	2026-07-16 06:52:05.960786+01
JP	Japan	Asia	2026-07-16 06:52:05.960786+01
AU	Australia	Oceania	2026-07-16 06:52:05.960786+01
CA	Canada	North America	2026-07-16 06:52:05.960786+01
CH	Switzerland	Europe	2026-07-16 06:52:05.960786+01
CN	China	Asia	2026-07-16 06:52:05.960786+01
HK	Hong Kong	Asia	2026-07-16 06:52:05.960786+01
United States	United States	\N	2026-07-16 09:24:03.919817+01
\.


--
-- Data for Name: currency_registry; Type: TABLE DATA; Schema: metadata; Owner: postgres
--

COPY metadata.currency_registry (code, name, symbol, decimals, created_at) FROM stdin;
USD	USD	\N	\N	2026-07-16 09:07:04.934169+01
\.


--
-- Data for Name: exchange_registry; Type: TABLE DATA; Schema: metadata; Owner: postgres
--

COPY metadata.exchange_registry (mic_code, name, country, timezone, market_hours, website, created_at) FROM stdin;
CCY	CCY		\N	\N	\N	2026-07-16 09:07:04.346038+01
NMS	NMS	United States	\N	\N	\N	2026-07-16 09:07:08.667318+01
CCC	CCC		\N	\N	\N	2026-07-16 09:07:10.447096+01
CMX	CMX		\N	\N	\N	2026-07-16 09:07:11.41298+01
\.


--
-- Data for Name: industry_registry; Type: TABLE DATA; Schema: metadata; Owner: postgres
--

COPY metadata.industry_registry (industry_id, name, sector_id, description, created_at) FROM stdin;
198fe232-86e3-437d-b387-b257c4b1878c	Consumer Electronics	\N	\N	2026-07-16 09:24:04.09157+01
\.


--
-- Data for Name: provider_registry; Type: TABLE DATA; Schema: metadata; Owner: postgres
--

COPY metadata.provider_registry (provider_id, name, description, tier, priority, status, last_check, created_at) FROM stdin;
b909fd3d-bbe9-452c-a865-9590e3a26c31	yahoo_metadata	Yahoo Finance metadata provider	2	5	active	\N	2026-07-16 06:15:42.500649+01
\.


--
-- Data for Name: quality_registry; Type: TABLE DATA; Schema: metadata; Owner: postgres
--

COPY metadata.quality_registry (quality_id, asset_id, provider_id, quality_score, completeness, freshness, confidence, verification_status, issues, checked_at) FROM stdin;
\.


--
-- Data for Name: relationship_registry; Type: TABLE DATA; Schema: metadata; Owner: postgres
--

COPY metadata.relationship_registry (relationship_id, source_asset_id, target_asset_id, relationship_type, strength, metadata, created_at) FROM stdin;
\.


--
-- Data for Name: sector_registry; Type: TABLE DATA; Schema: metadata; Owner: postgres
--

COPY metadata.sector_registry (sector_id, name, description, created_at) FROM stdin;
a6e6997e-9545-4019-a225-9b423d9493b6	Technology	Companies involved in technology development and services	2026-07-16 06:52:06.048267+01
66c30f24-25e5-4324-871a-30f09704ee37	Financials	Banks, insurance, and financial services	2026-07-16 06:52:06.048267+01
9f084673-111e-4006-996f-104bef419d2a	Healthcare	Healthcare providers, pharmaceuticals, and biotechnology	2026-07-16 06:52:06.048267+01
1c797ba9-8fa0-4dfe-b49b-9244a07302e4	Consumer Cyclical	Companies that are sensitive to economic cycles	2026-07-16 06:52:06.048267+01
d6184add-df0c-4afb-9348-c029f92f5360	Consumer Defensive	Companies that are less sensitive to economic cycles	2026-07-16 06:52:06.048267+01
71d8cb27-4637-4c41-b832-ab7366407146	Energy	Oil, gas, and energy services	2026-07-16 06:52:06.048267+01
f0311494-60b0-4e87-9c1b-b151b550fc75	Industrials	Industrial and manufacturing companies	2026-07-16 06:52:06.048267+01
5f9b86e3-8965-4018-96de-ea7b47cc2643	Materials	Materials and commodities	2026-07-16 06:52:06.048267+01
fd0ee7b8-012e-4bc2-be29-f96c0865bc36	Real Estate	Real estate investment trusts and services	2026-07-16 06:52:06.048267+01
b523e0d8-09ec-40ae-981e-58b7b9a7273c	Utilities	Utility companies	2026-07-16 06:52:06.048267+01
\.


--
-- Data for Name: version_history; Type: TABLE DATA; Schema: metadata; Owner: postgres
--

COPY metadata.version_history (version_id, asset_id, version, changed_fields, changed_by, changed_at) FROM stdin;
68fce81b-bed0-440c-b8ef-9ecb35383992	40d67cd8-a03d-4401-a244-71b8f87d44a8	1	{"symbol": "EURUSD", "website": "", "provider": "yahoo_metadata", "timezone": "", "long_name": "EUR/USD", "tick_size": 4, "market_cap": null, "short_name": "EUR/USD", "asset_class": "forex", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CCY", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "EURUSD=X", "avg_daily_volume": 0}	metadata_engine	2026-07-16 09:07:05.54416+01
0940b631-46f5-406b-b537-2476553ee2a4	1f6270d2-ca6a-4178-918b-34f569cb8c67	1	{"symbol": "BTC-USD", "website": "https://bitcoin.org/", "provider": "yahoo_metadata", "timezone": "", "long_name": "Bitcoin USD", "tick_size": 2, "market_cap": 1286340214784, "short_name": "Bitcoin USD", "asset_class": "unknown", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CCC", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "BTC-USD", "avg_daily_volume": 31909275580}	metadata_engine	2026-07-16 09:07:10.552712+01
5cf73f3a-cf6a-445a-9614-33a03e268e2f	74f9830d-22b5-44ed-82b9-2c8a67b48f1f	1	{"symbol": "GC=F", "website": "", "provider": "yahoo_metadata", "timezone": "", "long_name": "", "tick_size": 2, "market_cap": null, "short_name": "Gold Aug 26", "asset_class": "futures", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CMX", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "GC=F", "avg_daily_volume": 2283}	metadata_engine	2026-07-16 09:07:11.550632+01
e49011a8-8e7a-458e-96a9-ee9be0943c2f	40d67cd8-a03d-4401-a244-71b8f87d44a8	2	{"symbol": "EURUSD", "website": "", "provider": "yahoo_metadata", "timezone": "", "long_name": "EUR/USD", "tick_size": 4, "market_cap": null, "short_name": "EUR/USD", "asset_class": "forex", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CCY", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "EURUSD=X", "avg_daily_volume": 0}	metadata_engine	2026-07-16 09:18:43.133813+01
e52ae5dd-7dfc-4efa-aa21-400ff60408b7	1f6270d2-ca6a-4178-918b-34f569cb8c67	2	{"symbol": "BTC-USD", "website": "https://bitcoin.org/", "provider": "yahoo_metadata", "timezone": "", "long_name": "Bitcoin USD", "tick_size": 2, "market_cap": 1280947912704, "short_name": "Bitcoin USD", "asset_class": "unknown", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CCC", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "BTC-USD", "avg_daily_volume": 31909275580}	metadata_engine	2026-07-16 09:18:45.003582+01
bbf07bb8-c661-4ab5-b8e2-d92bcf26c643	74f9830d-22b5-44ed-82b9-2c8a67b48f1f	2	{"symbol": "GC=F", "website": "", "provider": "yahoo_metadata", "timezone": "", "long_name": "", "tick_size": 2, "market_cap": null, "short_name": "Gold Aug 26", "asset_class": "futures", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CMX", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "GC=F", "avg_daily_volume": 2283}	metadata_engine	2026-07-16 09:18:45.780809+01
86b76682-1b28-4107-b7b2-c7616a694723	40d67cd8-a03d-4401-a244-71b8f87d44a8	3	{"symbol": "EURUSD", "website": "", "provider": "yahoo_metadata", "timezone": "", "long_name": "EUR/USD", "tick_size": 4, "market_cap": null, "short_name": "EUR/USD", "asset_class": "forex", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CCY", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "EURUSD=X", "avg_daily_volume": 0}	metadata_engine	2026-07-16 09:21:38.34308+01
45131ef1-12f9-4ff2-9bde-729f5ab50f00	1f6270d2-ca6a-4178-918b-34f569cb8c67	3	{"symbol": "BTC-USD", "website": "https://bitcoin.org/", "provider": "yahoo_metadata", "timezone": "", "long_name": "Bitcoin USD", "tick_size": 2, "market_cap": 1282508324864, "short_name": "Bitcoin USD", "asset_class": "unknown", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CCC", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "BTC-USD", "avg_daily_volume": 31909275580}	metadata_engine	2026-07-16 09:21:39.755874+01
94cc746b-007f-4452-b7c4-9c3d789f7c39	74f9830d-22b5-44ed-82b9-2c8a67b48f1f	3	{"symbol": "GC=F", "website": "", "provider": "yahoo_metadata", "timezone": "", "long_name": "", "tick_size": 2, "market_cap": null, "short_name": "Gold Aug 26", "asset_class": "futures", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CMX", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "GC=F", "avg_daily_volume": 2283}	metadata_engine	2026-07-16 09:21:40.649037+01
cf139c72-0ad2-4e0c-a284-2efa3abdc09c	40d67cd8-a03d-4401-a244-71b8f87d44a8	4	{"symbol": "EURUSD", "website": "", "provider": "yahoo_metadata", "timezone": "", "long_name": "EUR/USD", "tick_size": 4, "market_cap": null, "short_name": "EUR/USD", "asset_class": "forex", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CCY", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "EURUSD=X", "avg_daily_volume": 0}	metadata_engine	2026-07-16 09:22:40.125156+01
753ffeb5-9c29-490e-a4da-6dfbfba3392d	1f6270d2-ca6a-4178-918b-34f569cb8c67	4	{"symbol": "BTC-USD", "website": "https://bitcoin.org/", "provider": "yahoo_metadata", "timezone": "", "long_name": "Bitcoin USD", "tick_size": 2, "market_cap": 1282041053184, "short_name": "Bitcoin USD", "asset_class": "unknown", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CCC", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "BTC-USD", "avg_daily_volume": 31909275580}	metadata_engine	2026-07-16 09:22:41.527876+01
940a2142-b39b-4462-a6a5-e3aecd83e1ea	74f9830d-22b5-44ed-82b9-2c8a67b48f1f	4	{"symbol": "GC=F", "website": "", "provider": "yahoo_metadata", "timezone": "", "long_name": "", "tick_size": 2, "market_cap": null, "short_name": "Gold Aug 26", "asset_class": "futures", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CMX", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "GC=F", "avg_daily_volume": 2283}	metadata_engine	2026-07-16 09:22:42.317642+01
66dfbf74-e9bd-4382-ac13-06426065a8bf	40d67cd8-a03d-4401-a244-71b8f87d44a8	5	{"symbol": "EURUSD", "website": "", "provider": "yahoo_metadata", "timezone": "", "long_name": "EUR/USD", "tick_size": 4, "market_cap": null, "short_name": "EUR/USD", "asset_class": "forex", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CCY", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "EURUSD=X", "avg_daily_volume": 0}	metadata_engine	2026-07-16 09:24:03.236302+01
faa91333-9985-43fd-931d-bd587fcf1eaf	1f6270d2-ca6a-4178-918b-34f569cb8c67	5	{"symbol": "BTC-USD", "website": "https://bitcoin.org/", "provider": "yahoo_metadata", "timezone": "", "long_name": "Bitcoin USD", "tick_size": 2, "market_cap": 1282041053184, "short_name": "Bitcoin USD", "asset_class": "unknown", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CCC", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "BTC-USD", "avg_daily_volume": 31909275580}	metadata_engine	2026-07-16 09:24:05.045024+01
a9adc8ff-6ef7-4045-b33b-2ca37d83c6e9	74f9830d-22b5-44ed-82b9-2c8a67b48f1f	5	{"symbol": "GC=F", "website": "", "provider": "yahoo_metadata", "timezone": "", "long_name": "", "tick_size": 2, "market_cap": null, "short_name": "Gold Aug 26", "asset_class": "futures", "description": "", "market_open": null, "market_close": null, "base_currency": "USD", "exchange_code": "CMX", "provider_rank": 5, "quality_score": 0.9, "display_symbol": "GC=F", "avg_daily_volume": 2283}	metadata_engine	2026-07-16 09:24:05.894883+01
\.


--
-- Data for Name: economic_events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.economic_events (event_id, provider, provider_event_id, country, region, currency, title, short_title, category, subcategory, forecast, previous, actual, consensus, revised_previous, importance, release_time_utc, release_time_local, timezone, frequency, status, source_url, tags, affected_assets, affected_markets, confidence, quality_score, metadata, created_at) FROM stdin;
\.


--
-- Data for Name: engine_runs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.engine_runs ("time", engine_name, status, records_fetched, error_message, duration_ms) FROM stdin;
\.


--
-- Data for Name: institutional_positions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.institutional_positions ("time", symbol, report_type, long_positions, short_positions, net_positions, source, metadata) FROM stdin;
\.


--
-- Data for Name: macro_events_consensus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.macro_events_consensus (event_id, country, currency, title, category, subcategory, forecast, previous, actual, consensus, revised_previous, importance, impact_score, release_time_utc, status, source_url, tags, affected_assets, confidence, quality_score, metadata, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: macro_events_raw; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.macro_events_raw (raw_id, provider, provider_event_id, country, currency, title, category, forecast, previous, actual, importance, release_time_utc, status, raw_data, ingested_at) FROM stdin;
d467df3a-d790-47ba-b041-0138da227d41	forexfactory	ff_us_cpi_2026-07-16	US	USD	Consumer Price Index	Inflation	2.8	2.6	\N	High	2026-07-16 08:30:00+01	Scheduled	{"title": "Consumer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "ff_us_cpi_2026-07-16", "forecast": 2.8, "previous": 2.6, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:01:10.68796+01
045765ea-34eb-4960-b5ec-4e6f9c6a8b58	forexfactory	ff_ecb_rate_2026-07-16	EU	EUR	ECB Interest Rate Decision	Central Bank	3	3.25	\N	High	2026-07-16 12:45:00+01	Scheduled	{"title": "ECB Interest Rate Decision", "actual": null, "status": "Scheduled", "country": "EU", "category": "Central Bank", "currency": "EUR", "event_id": "ff_ecb_rate_2026-07-16", "forecast": 3.0, "previous": 3.25, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T12:45:00"}	2026-07-16 12:01:11.946429+01
a222a1d0-b54e-45e8-bc36-930aefaf878e	forexfactory	ff_us_jobless_2026-07-16	US	USD	Initial Jobless Claims	Labour	220	215	\N	Medium	2026-07-16 13:30:00+01	Scheduled	{"title": "Initial Jobless Claims", "actual": null, "status": "Scheduled", "country": "US", "category": "Labour", "currency": "USD", "event_id": "ff_us_jobless_2026-07-16", "forecast": 220, "previous": 215, "provider": "forexfactory", "importance": "Medium", "release_time_utc": "2026-07-16T13:30:00"}	2026-07-16 12:01:12.002792+01
b971dc53-4a66-40bc-a7e4-01a11fcc5ef6	investing	inv_us_ppi_2026-07-16	US	USD	Producer Price Index	Inflation	0.3	0.2	\N	Medium	2026-07-16 08:30:00+01	Scheduled	{"title": "Producer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "inv_us_ppi_2026-07-16", "forecast": 0.3, "previous": 0.2, "provider": "investing", "importance": "Medium", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:01:12.009339+01
9e01654b-b3b4-4b53-9f1e-e016073f5166	investing	inv_gdp_q1_2026-07-16	US	USD	GDP Quarterly	Growth	2.5	2.3	\N	High	2026-07-16 12:30:00+01	Scheduled	{"title": "GDP Quarterly", "actual": null, "status": "Scheduled", "country": "US", "category": "Growth", "currency": "USD", "event_id": "inv_gdp_q1_2026-07-16", "forecast": 2.5, "previous": 2.3, "provider": "investing", "importance": "High", "release_time_utc": "2026-07-16T12:30:00"}	2026-07-16 12:01:12.012434+01
bdcfb603-448c-4f8c-a327-e748d95b936a	forexfactory	ff_us_cpi_2026-07-16	US	USD	Consumer Price Index	Inflation	2.8	2.6	\N	High	2026-07-16 08:30:00+01	Scheduled	{"title": "Consumer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "ff_us_cpi_2026-07-16", "forecast": 2.8, "previous": 2.6, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:02:25.042159+01
a2b03113-5dc8-49bc-abb8-efa8634d737e	forexfactory	ff_ecb_rate_2026-07-16	EU	EUR	ECB Interest Rate Decision	Central Bank	3	3.25	\N	High	2026-07-16 12:45:00+01	Scheduled	{"title": "ECB Interest Rate Decision", "actual": null, "status": "Scheduled", "country": "EU", "category": "Central Bank", "currency": "EUR", "event_id": "ff_ecb_rate_2026-07-16", "forecast": 3.0, "previous": 3.25, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T12:45:00"}	2026-07-16 12:02:25.72077+01
b017a931-765e-4b3b-a07a-cbb7c50ca042	forexfactory	ff_us_jobless_2026-07-16	US	USD	Initial Jobless Claims	Labour	220	215	\N	Medium	2026-07-16 13:30:00+01	Scheduled	{"title": "Initial Jobless Claims", "actual": null, "status": "Scheduled", "country": "US", "category": "Labour", "currency": "USD", "event_id": "ff_us_jobless_2026-07-16", "forecast": 220, "previous": 215, "provider": "forexfactory", "importance": "Medium", "release_time_utc": "2026-07-16T13:30:00"}	2026-07-16 12:02:25.735805+01
dff00f23-653d-4f27-b9e4-4abb332e0b3b	investing	inv_us_ppi_2026-07-16	US	USD	Producer Price Index	Inflation	0.3	0.2	\N	Medium	2026-07-16 08:30:00+01	Scheduled	{"title": "Producer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "inv_us_ppi_2026-07-16", "forecast": 0.3, "previous": 0.2, "provider": "investing", "importance": "Medium", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:02:25.747575+01
4d302ec8-058a-4fc9-8630-c606adc1c082	investing	inv_gdp_q1_2026-07-16	US	USD	GDP Quarterly	Growth	2.5	2.3	\N	High	2026-07-16 12:30:00+01	Scheduled	{"title": "GDP Quarterly", "actual": null, "status": "Scheduled", "country": "US", "category": "Growth", "currency": "USD", "event_id": "inv_gdp_q1_2026-07-16", "forecast": 2.5, "previous": 2.3, "provider": "investing", "importance": "High", "release_time_utc": "2026-07-16T12:30:00"}	2026-07-16 12:02:25.767615+01
d09a5fb3-5d6e-43f5-9032-c8fafcb558e7	forexfactory	ff_us_cpi_2026-07-16	US	USD	Consumer Price Index	Inflation	2.8	2.6	\N	High	2026-07-16 08:30:00+01	Scheduled	{"title": "Consumer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "ff_us_cpi_2026-07-16", "forecast": 2.8, "previous": 2.6, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:19:59.335433+01
102b4762-80cf-4fa6-9d83-39db305ef08f	forexfactory	ff_ecb_rate_2026-07-16	EU	EUR	ECB Interest Rate Decision	Central Bank	3	3.25	\N	High	2026-07-16 12:45:00+01	Scheduled	{"title": "ECB Interest Rate Decision", "actual": null, "status": "Scheduled", "country": "EU", "category": "Central Bank", "currency": "EUR", "event_id": "ff_ecb_rate_2026-07-16", "forecast": 3.0, "previous": 3.25, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T12:45:00"}	2026-07-16 12:19:59.466426+01
3b127f84-539c-4866-976c-c0fee4ab366d	forexfactory	ff_us_jobless_2026-07-16	US	USD	Initial Jobless Claims	Labour	220	215	\N	Medium	2026-07-16 13:30:00+01	Scheduled	{"title": "Initial Jobless Claims", "actual": null, "status": "Scheduled", "country": "US", "category": "Labour", "currency": "USD", "event_id": "ff_us_jobless_2026-07-16", "forecast": 220, "previous": 215, "provider": "forexfactory", "importance": "Medium", "release_time_utc": "2026-07-16T13:30:00"}	2026-07-16 12:19:59.470795+01
ed142e45-d4eb-4d07-8110-d093549e45e2	investing	inv_us_ppi_2026-07-16	US	USD	Producer Price Index	Inflation	0.3	0.2	\N	Medium	2026-07-16 08:30:00+01	Scheduled	{"title": "Producer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "inv_us_ppi_2026-07-16", "forecast": 0.3, "previous": 0.2, "provider": "investing", "importance": "Medium", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:19:59.474764+01
cd53a9d8-e73a-4c42-87df-f8c4a9f55daf	investing	inv_gdp_q1_2026-07-16	US	USD	GDP Quarterly	Growth	2.5	2.3	\N	High	2026-07-16 12:30:00+01	Scheduled	{"title": "GDP Quarterly", "actual": null, "status": "Scheduled", "country": "US", "category": "Growth", "currency": "USD", "event_id": "inv_gdp_q1_2026-07-16", "forecast": 2.5, "previous": 2.3, "provider": "investing", "importance": "High", "release_time_utc": "2026-07-16T12:30:00"}	2026-07-16 12:19:59.478482+01
3d376852-7a6c-48a2-a95f-f2fe89eb19d1	forexfactory	ff_us_cpi_2026-07-16	US	USD	Consumer Price Index	Inflation	2.8	2.6	\N	High	2026-07-16 08:30:00+01	Scheduled	{"title": "Consumer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "ff_us_cpi_2026-07-16", "forecast": 2.8, "previous": 2.6, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:20:45.56003+01
ffb4aee1-33cf-44ae-a4ba-a4fd673dce12	forexfactory	ff_ecb_rate_2026-07-16	EU	EUR	ECB Interest Rate Decision	Central Bank	3	3.25	\N	High	2026-07-16 12:45:00+01	Scheduled	{"title": "ECB Interest Rate Decision", "actual": null, "status": "Scheduled", "country": "EU", "category": "Central Bank", "currency": "EUR", "event_id": "ff_ecb_rate_2026-07-16", "forecast": 3.0, "previous": 3.25, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T12:45:00"}	2026-07-16 12:20:45.683924+01
c8a29a52-33a8-4ebe-a96c-fa96142b0920	forexfactory	ff_us_jobless_2026-07-16	US	USD	Initial Jobless Claims	Labour	220	215	\N	Medium	2026-07-16 13:30:00+01	Scheduled	{"title": "Initial Jobless Claims", "actual": null, "status": "Scheduled", "country": "US", "category": "Labour", "currency": "USD", "event_id": "ff_us_jobless_2026-07-16", "forecast": 220, "previous": 215, "provider": "forexfactory", "importance": "Medium", "release_time_utc": "2026-07-16T13:30:00"}	2026-07-16 12:20:45.697684+01
4cd51e0a-5cb6-453b-9676-a74b880acd54	investing	inv_us_ppi_2026-07-16	US	USD	Producer Price Index	Inflation	0.3	0.2	\N	Medium	2026-07-16 08:30:00+01	Scheduled	{"title": "Producer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "inv_us_ppi_2026-07-16", "forecast": 0.3, "previous": 0.2, "provider": "investing", "importance": "Medium", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:20:45.708101+01
fcb54b8d-ab59-42b5-bee9-d5e4f6ad0973	investing	inv_gdp_q1_2026-07-16	US	USD	GDP Quarterly	Growth	2.5	2.3	\N	High	2026-07-16 12:30:00+01	Scheduled	{"title": "GDP Quarterly", "actual": null, "status": "Scheduled", "country": "US", "category": "Growth", "currency": "USD", "event_id": "inv_gdp_q1_2026-07-16", "forecast": 2.5, "previous": 2.3, "provider": "investing", "importance": "High", "release_time_utc": "2026-07-16T12:30:00"}	2026-07-16 12:20:45.718359+01
d96f268c-0672-4560-97c7-4c501a639515	forexfactory	ff_us_cpi_2026-07-16	US	USD	Consumer Price Index	Inflation	2.8	2.6	\N	High	2026-07-16 08:30:00+01	Scheduled	{"title": "Consumer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "ff_us_cpi_2026-07-16", "forecast": 2.8, "previous": 2.6, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:31:55.998054+01
f9392413-960c-44a1-b89a-0fac69fb1e2e	forexfactory	ff_ecb_rate_2026-07-16	EU	EUR	ECB Interest Rate Decision	Central Bank	3	3.25	\N	High	2026-07-16 12:45:00+01	Scheduled	{"title": "ECB Interest Rate Decision", "actual": null, "status": "Scheduled", "country": "EU", "category": "Central Bank", "currency": "EUR", "event_id": "ff_ecb_rate_2026-07-16", "forecast": 3.0, "previous": 3.25, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T12:45:00"}	2026-07-16 12:31:56.121415+01
83c5fb29-89c6-49a4-a4da-217d12b9404e	forexfactory	ff_us_jobless_2026-07-16	US	USD	Initial Jobless Claims	Labour	220	215	\N	Medium	2026-07-16 13:30:00+01	Scheduled	{"title": "Initial Jobless Claims", "actual": null, "status": "Scheduled", "country": "US", "category": "Labour", "currency": "USD", "event_id": "ff_us_jobless_2026-07-16", "forecast": 220, "previous": 215, "provider": "forexfactory", "importance": "Medium", "release_time_utc": "2026-07-16T13:30:00"}	2026-07-16 12:31:56.146264+01
d234be10-4321-4ec8-8be5-01f1ebbaf3d5	investing	inv_us_ppi_2026-07-16	US	USD	Producer Price Index	Inflation	0.3	0.2	\N	Medium	2026-07-16 08:30:00+01	Scheduled	{"title": "Producer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "inv_us_ppi_2026-07-16", "forecast": 0.3, "previous": 0.2, "provider": "investing", "importance": "Medium", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:31:56.150866+01
7522fabf-3cec-40d4-a55e-e69992aca8cd	investing	inv_gdp_q1_2026-07-16	US	USD	GDP Quarterly	Growth	2.5	2.3	\N	High	2026-07-16 12:30:00+01	Scheduled	{"title": "GDP Quarterly", "actual": null, "status": "Scheduled", "country": "US", "category": "Growth", "currency": "USD", "event_id": "inv_gdp_q1_2026-07-16", "forecast": 2.5, "previous": 2.3, "provider": "investing", "importance": "High", "release_time_utc": "2026-07-16T12:30:00"}	2026-07-16 12:31:56.156234+01
08b0d751-8c91-4860-996e-a1f03da245b8	forexfactory	ff_us_cpi_2026-07-16	US	USD	Consumer Price Index	Inflation	2.8	2.6	\N	High	2026-07-16 08:30:00+01	Scheduled	{"title": "Consumer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "ff_us_cpi_2026-07-16", "forecast": 2.8, "previous": 2.6, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:32:21.273718+01
18c2b3c7-f63a-4c5a-96b6-45456771f6c4	forexfactory	ff_ecb_rate_2026-07-16	EU	EUR	ECB Interest Rate Decision	Central Bank	3	3.25	\N	High	2026-07-16 12:45:00+01	Scheduled	{"title": "ECB Interest Rate Decision", "actual": null, "status": "Scheduled", "country": "EU", "category": "Central Bank", "currency": "EUR", "event_id": "ff_ecb_rate_2026-07-16", "forecast": 3.0, "previous": 3.25, "provider": "forexfactory", "importance": "High", "release_time_utc": "2026-07-16T12:45:00"}	2026-07-16 12:32:21.285597+01
b40c2f44-9d0b-44fc-9cc3-f9623a8907da	forexfactory	ff_us_jobless_2026-07-16	US	USD	Initial Jobless Claims	Labour	220	215	\N	Medium	2026-07-16 13:30:00+01	Scheduled	{"title": "Initial Jobless Claims", "actual": null, "status": "Scheduled", "country": "US", "category": "Labour", "currency": "USD", "event_id": "ff_us_jobless_2026-07-16", "forecast": 220, "previous": 215, "provider": "forexfactory", "importance": "Medium", "release_time_utc": "2026-07-16T13:30:00"}	2026-07-16 12:32:21.288274+01
93e3ae23-9e54-4f32-814c-73221331dd89	investing	inv_us_ppi_2026-07-16	US	USD	Producer Price Index	Inflation	0.3	0.2	\N	Medium	2026-07-16 08:30:00+01	Scheduled	{"title": "Producer Price Index", "actual": null, "status": "Scheduled", "country": "US", "category": "Inflation", "currency": "USD", "event_id": "inv_us_ppi_2026-07-16", "forecast": 0.3, "previous": 0.2, "provider": "investing", "importance": "Medium", "release_time_utc": "2026-07-16T08:30:00"}	2026-07-16 12:32:21.291305+01
691ab18f-0d7d-4cc9-8006-f76ebff50d1e	investing	inv_gdp_q1_2026-07-16	US	USD	GDP Quarterly	Growth	2.5	2.3	\N	High	2026-07-16 12:30:00+01	Scheduled	{"title": "GDP Quarterly", "actual": null, "status": "Scheduled", "country": "US", "category": "Growth", "currency": "USD", "event_id": "inv_gdp_q1_2026-07-16", "forecast": 2.5, "previous": 2.3, "provider": "investing", "importance": "High", "release_time_utc": "2026-07-16T12:30:00"}	2026-07-16 12:32:21.294112+01
\.


--
-- Data for Name: market_prices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.market_prices ("time", symbol, price, volume, open, high, low, close, source, asset_class, confidence_score, metadata) FROM stdin;
\.


--
-- Data for Name: price_commodities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.price_commodities ("time", symbol, price, volume, open, high, low, close, source, metadata) FROM stdin;
\.


--
-- Data for Name: price_crypto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.price_crypto ("time", symbol, price, volume, open, high, low, close, source, metadata) FROM stdin;
2026-07-16 04:27:51.643054+01	BTC-USD	64603.12109375	27195033600	64720.35546875	64793.71484375	64389.390625	64603.12109375	yahoo	{}
2026-07-16 04:53:11.719382+01	BTC-USD	64523.26171875	27106297856	64720.35546875	64793.71484375	64389.390625	64523.26171875	yahoo	{}
2026-07-16 04:53:12.32848+01	ETH-USD	1916.780029296875	12669704192	1917.0543212890625	1926.4071044921875	1907.8677978515625	1916.780029296875	yahoo	{}
2026-07-16 04:53:12.886871+01	SOL-USD	76.7699966430664	2075698432	77.26387023925781	77.37681579589844	76.75849914550781	76.7699966430664	yahoo	{}
2026-07-16 04:53:13.603133+01	XRP-USD	1.1124999523162842	1189801856	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1124999523162842	yahoo	{}
2026-07-16 04:53:14.271183+01	ADA-USD	0.1647000014781952	300570080	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.1647000014781952	yahoo	{}
2026-07-16 04:53:14.804892+01	DOT-USD	0.8479999899864197	88679800	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8479999899864197	yahoo	{}
2026-07-16 04:53:15.490621+01	LINK-USD	8.510000228881836	293143136	8.535067558288574	8.542733192443848	8.464689254760742	8.510000228881836	yahoo	{}
2026-07-16 04:53:15.971709+01	DOGE-USD	0.07391999661922455	629164288	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07391999661922455	yahoo	{}
2026-07-16 04:53:16.578525+01	SHIB-USD	4.2100000428035855e-06	55496016	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.2100000428035855e-06	yahoo	{}
2026-07-16 04:53:17.115+01	AVAX-USD	6.699999809265137	208608880	6.696125507354736	6.715437889099121	6.670616149902344	6.699999809265137	yahoo	{}
2026-07-16 04:53:20.621275+01	ATOM-USD	1.5479999780654907	25807044	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5479999780654907	yahoo	{}
2026-07-16 04:54:56.395095+01	BTC-USD	64556.01953125	27018129408	64720.35546875	64793.71484375	64389.390625	64556.01953125	yahoo	{}
2026-07-16 04:54:56.722335+01	ETH-USD	1917.199951171875	12565070848	1917.0543212890625	1926.4071044921875	1907.8677978515625	1917.199951171875	yahoo	{}
2026-07-16 04:54:57.047593+01	SOL-USD	76.86000061035156	2076043264	77.26387023925781	77.37681579589844	76.75849914550781	76.86000061035156	yahoo	{}
2026-07-16 04:54:57.375902+01	XRP-USD	1.1124999523162842	1189322112	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1124999523162842	yahoo	{}
2026-07-16 04:54:57.725254+01	ADA-USD	0.1648000031709671	300058496	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.1648000031709671	yahoo	{}
2026-07-16 04:54:58.033244+01	DOT-USD	0.8479999899864197	88764112	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8479999899864197	yahoo	{}
2026-07-16 04:54:58.312727+01	LINK-USD	8.519000053405762	293156256	8.535067558288574	8.542733192443848	8.464689254760742	8.519000053405762	yahoo	{}
2026-07-16 04:54:58.65967+01	DOGE-USD	0.07395000010728836	628147584	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07395000010728836	yahoo	{}
2026-07-16 04:54:58.959095+01	SHIB-USD	4.219999937049579e-06	55514656	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.219999937049579e-06	yahoo	{}
2026-07-16 04:54:59.283667+01	AVAX-USD	6.710000038146973	208463312	6.696125507354736	6.715437889099121	6.670616149902344	6.710000038146973	yahoo	{}
2026-07-16 04:55:01.942536+01	ATOM-USD	1.5470000505447388	25798186	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5470000505447388	yahoo	{}
2026-07-16 04:56:37.616375+01	BTC-USD	64553.75	27009742848	64720.35546875	64793.71484375	64389.390625	64553.75	yahoo	{}
2026-07-16 04:56:37.963171+01	ETH-USD	1917.219970703125	12571315200	1917.0543212890625	1926.4071044921875	1907.8677978515625	1917.219970703125	yahoo	{}
2026-07-16 04:56:38.288956+01	SOL-USD	76.87999725341797	2075740928	77.26387023925781	77.37681579589844	76.75849914550781	76.87999725341797	yahoo	{}
2026-07-16 04:56:38.619519+01	XRP-USD	1.111899971961975	1189358080	1.1127955913543701	1.1164233684539795	1.107488751411438	1.111899971961975	yahoo	{}
2026-07-16 04:56:38.927699+01	ADA-USD	0.1648000031709671	299755552	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.1648000031709671	yahoo	{}
2026-07-16 04:56:39.225915+01	DOT-USD	0.8479999899864197	88764112	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8479999899864197	yahoo	{}
2026-07-16 04:56:39.537883+01	LINK-USD	8.517999649047852	289270496	8.535067558288574	8.542733192443848	8.464689254760742	8.517999649047852	yahoo	{}
2026-07-16 04:56:39.840054+01	DOGE-USD	0.07393000274896622	627638976	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07393000274896622	yahoo	{}
2026-07-16 04:56:40.159841+01	SHIB-USD	4.219999937049579e-06	55514656	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.219999937049579e-06	yahoo	{}
2026-07-16 04:56:40.490527+01	AVAX-USD	6.710000038146973	208423312	6.696125507354736	6.715437889099121	6.670616149902344	6.710000038146973	yahoo	{}
2026-07-16 04:56:43.252326+01	ATOM-USD	1.5490000247955322	25781892	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5490000247955322	yahoo	{}
2026-07-16 04:58:19.77872+01	BTC-USD	64548.94140625	27004723200	64720.35546875	64793.71484375	64389.390625	64548.94140625	yahoo	{}
2026-07-16 04:58:20.099334+01	ETH-USD	1917.1099853515625	12562417664	1917.0543212890625	1926.4071044921875	1907.8677978515625	1917.1099853515625	yahoo	{}
2026-07-16 04:58:20.440655+01	SOL-USD	76.88999938964844	2075703296	77.26387023925781	77.37681579589844	76.75849914550781	76.88999938964844	yahoo	{}
2026-07-16 04:58:20.835747+01	XRP-USD	1.1121000051498413	1188960256	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1121000051498413	yahoo	{}
2026-07-16 04:58:21.192267+01	ADA-USD	0.164900004863739	299755552	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.164900004863739	yahoo	{}
2026-07-16 04:58:21.523739+01	DOT-USD	0.8479999899864197	88795136	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8479999899864197	yahoo	{}
2026-07-16 04:58:21.853527+01	LINK-USD	8.517999649047852	289246240	8.535067558288574	8.542733192443848	8.464689254760742	8.517999649047852	yahoo	{}
2026-07-16 04:58:22.204362+01	DOGE-USD	0.07389000058174133	627638976	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07389000058174133	yahoo	{}
2026-07-16 04:58:22.510539+01	SHIB-USD	4.219999937049579e-06	55529208	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.219999937049579e-06	yahoo	{}
2026-07-16 04:58:22.857864+01	AVAX-USD	6.710000038146973	208563600	6.696125507354736	6.715437889099121	6.670616149902344	6.710000038146973	yahoo	{}
2026-07-16 04:58:25.632761+01	ATOM-USD	1.5490000247955322	25782304	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5490000247955322	yahoo	{}
2026-07-16 05:00:03.039512+01	BTC-USD	64562.140625	26961573888	64720.35546875	64793.71484375	64389.390625	64562.140625	yahoo	{}
2026-07-16 05:00:03.451702+01	ETH-USD	1917.469970703125	12567491584	1917.0543212890625	1926.4071044921875	1907.8677978515625	1917.469970703125	yahoo	{}
2026-07-16 05:00:03.752707+01	SOL-USD	76.88999938964844	2076439552	77.26387023925781	77.37681579589844	76.75849914550781	76.88999938964844	yahoo	{}
2026-07-16 05:00:04.152308+01	XRP-USD	1.1122000217437744	1189085312	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1122000217437744	yahoo	{}
2026-07-16 05:00:04.455103+01	ADA-USD	0.164900004863739	299600800	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.164900004863739	yahoo	{}
2026-07-16 05:00:04.783929+01	DOT-USD	0.8500000238418579	88811032	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8500000238418579	yahoo	{}
2026-07-16 05:00:05.126888+01	LINK-USD	8.522000312805176	289169056	8.535067558288574	8.542733192443848	8.464689254760742	8.522000312805176	yahoo	{}
2026-07-16 05:00:05.421182+01	DOGE-USD	0.07394000142812729	627487424	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07394000142812729	yahoo	{}
2026-07-16 05:00:05.774394+01	SHIB-USD	4.219999937049579e-06	55529608	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.219999937049579e-06	yahoo	{}
2026-07-16 05:00:06.073797+01	AVAX-USD	6.710000038146973	208561456	6.696125507354736	6.715437889099121	6.670616149902344	6.710000038146973	yahoo	{}
2026-07-16 05:00:08.805345+01	ATOM-USD	1.5499999523162842	25780706	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5499999523162842	yahoo	{}
2026-07-16 05:01:44.850779+01	BTC-USD	64580.23046875	26975170560	64720.35546875	64793.71484375	64389.390625	64580.23046875	yahoo	{}
2026-07-16 05:01:45.198287+01	ETH-USD	1917.199951171875	12558777344	1917.0543212890625	1926.4071044921875	1907.8677978515625	1917.199951171875	yahoo	{}
2026-07-16 05:01:45.563686+01	SOL-USD	76.91000366210938	2076424448	77.26387023925781	77.37681579589844	76.75849914550781	76.91000366210938	yahoo	{}
2026-07-16 05:01:45.873585+01	XRP-USD	1.1125999689102173	1189330816	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1125999689102173	yahoo	{}
2026-07-16 05:01:46.189961+01	ADA-USD	0.1648000031709671	299552256	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.1648000031709671	yahoo	{}
2026-07-16 05:01:46.521798+01	DOT-USD	0.8500000238418579	88795864	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8500000238418579	yahoo	{}
2026-07-16 05:01:46.833947+01	LINK-USD	8.52299976348877	289094560	8.535067558288574	8.542733192443848	8.464689254760742	8.52299976348877	yahoo	{}
2026-07-16 05:01:47.137483+01	DOGE-USD	0.07395000010728836	627397248	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07395000010728836	yahoo	{}
2026-07-16 05:01:47.425112+01	SHIB-USD	4.219999937049579e-06	55573312	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.219999937049579e-06	yahoo	{}
2026-07-16 05:01:47.760722+01	AVAX-USD	6.710000038146973	208586400	6.696125507354736	6.715437889099121	6.670616149902344	6.710000038146973	yahoo	{}
2026-07-16 05:01:50.436935+01	ATOM-USD	1.5490000247955322	25781978	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5490000247955322	yahoo	{}
2026-07-16 05:03:28.659925+01	BTC-USD	64581.33984375	27042265088	64720.35546875	64793.71484375	64389.390625	64581.33984375	yahoo	{}
2026-07-16 05:03:28.980969+01	ETH-USD	1917.5400390625	12635824128	1917.0543212890625	1926.4071044921875	1907.8677978515625	1917.5400390625	yahoo	{}
2026-07-16 05:03:29.296992+01	SOL-USD	76.93000030517578	2071793024	77.26387023925781	77.37681579589844	76.75849914550781	76.93000030517578	yahoo	{}
2026-07-16 05:03:29.651879+01	XRP-USD	1.1123000383377075	1186118528	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1123000383377075	yahoo	{}
2026-07-16 05:03:29.999936+01	ADA-USD	0.164900004863739	298540128	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.164900004863739	yahoo	{}
2026-07-16 05:03:30.302991+01	DOT-USD	0.8500000238418579	88806224	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8500000238418579	yahoo	{}
2026-07-16 05:03:30.615849+01	LINK-USD	8.527999877929688	288637408	8.535067558288574	8.542733192443848	8.464689254760742	8.527999877929688	yahoo	{}
2026-07-16 05:03:30.97243+01	DOGE-USD	0.07395999878644943	627397248	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07395999878644943	yahoo	{}
2026-07-16 05:05:28.314608+01	BTC-USD	64566.5	27026847744	64720.35546875	64793.71484375	64389.390625	64566.5	yahoo	{}
2026-07-16 05:05:28.640081+01	ETH-USD	1917.18994140625	12632541184	1917.0543212890625	1926.4071044921875	1907.8677978515625	1917.18994140625	yahoo	{}
2026-07-16 05:05:28.993485+01	SOL-USD	76.8499984741211	2070177664	77.26387023925781	77.37681579589844	76.75849914550781	76.8499984741211	yahoo	{}
2026-07-16 05:05:29.349351+01	XRP-USD	1.1119999885559082	1186422400	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1119999885559082	yahoo	{}
2026-07-16 05:05:29.698151+01	ADA-USD	0.1647000014781952	298342592	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.1647000014781952	yahoo	{}
2026-07-16 05:05:30.058192+01	DOT-USD	0.843999981880188	88804880	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.843999981880188	yahoo	{}
2026-07-16 05:05:30.389459+01	LINK-USD	8.531999588012695	292074080	8.535067558288574	8.542733192443848	8.464689254760742	8.531999588012695	yahoo	{}
2026-07-16 05:05:30.73676+01	DOGE-USD	0.07388000190258026	626786944	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07388000190258026	yahoo	{}
2026-07-16 05:05:31.092207+01	SHIB-USD	4.219999937049579e-06	55580084	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.219999937049579e-06	yahoo	{}
2026-07-16 05:05:31.401807+01	AVAX-USD	6.710000038146973	208331344	6.696125507354736	6.715437889099121	6.670616149902344	6.710000038146973	yahoo	{}
2026-07-16 05:05:34.091266+01	ATOM-USD	1.5470000505447388	25705508	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5470000505447388	yahoo	{}
2026-07-16 05:07:10.001597+01	BTC-USD	64569.8203125	27026847744	64720.35546875	64793.71484375	64389.390625	64569.8203125	yahoo	{}
2026-07-16 05:07:10.310515+01	ETH-USD	1917.2099609375	12632541184	1917.0543212890625	1926.4071044921875	1907.8677978515625	1917.2099609375	yahoo	{}
2026-07-16 05:07:10.628721+01	SOL-USD	76.87000274658203	2070215680	77.26387023925781	77.37681579589844	76.75849914550781	76.87000274658203	yahoo	{}
2026-07-16 05:07:10.910615+01	XRP-USD	1.1117000579833984	1186422400	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1117000579833984	yahoo	{}
2026-07-16 05:07:11.237172+01	ADA-USD	0.1648000031709671	298342592	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.1648000031709671	yahoo	{}
2026-07-16 05:07:11.574419+01	DOT-USD	0.843999981880188	88804880	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.843999981880188	yahoo	{}
2026-07-16 05:07:11.890435+01	LINK-USD	8.527999877929688	292074080	8.535067558288574	8.542733192443848	8.464689254760742	8.527999877929688	yahoo	{}
2026-07-16 05:07:12.244283+01	DOGE-USD	0.07388000190258026	626786944	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07388000190258026	yahoo	{}
2026-07-16 05:07:12.579123+01	SHIB-USD	4.219999937049579e-06	55586664	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.219999937049579e-06	yahoo	{}
2026-07-16 05:07:12.928411+01	AVAX-USD	6.710000038146973	208331344	6.696125507354736	6.715437889099121	6.670616149902344	6.710000038146973	yahoo	{}
2026-07-16 05:07:15.630321+01	ATOM-USD	1.5470000505447388	25705508	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5470000505447388	yahoo	{}
2026-07-16 05:08:51.706443+01	BTC-USD	64563.51953125	27030042624	64720.35546875	64793.71484375	64389.390625	64563.51953125	yahoo	{}
2026-07-16 05:08:52.05491+01	ETH-USD	1916.6099853515625	12631064576	1917.0543212890625	1926.4071044921875	1907.8677978515625	1916.6099853515625	yahoo	{}
2026-07-16 05:08:52.691863+01	SOL-USD	76.80999755859375	2070215680	77.26387023925781	77.37681579589844	76.75849914550781	76.80999755859375	yahoo	{}
2026-07-16 05:08:53.024146+01	XRP-USD	1.1110999584197998	1185313024	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1110999584197998	yahoo	{}
2026-07-16 05:08:53.335062+01	ADA-USD	0.1647000014781952	298377952	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.1647000014781952	yahoo	{}
2026-07-16 05:08:53.621994+01	DOT-USD	0.8450000286102295	89008216	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8450000286102295	yahoo	{}
2026-07-16 05:08:53.90104+01	LINK-USD	8.527000427246094	292041504	8.535067558288574	8.542733192443848	8.464689254760742	8.527000427246094	yahoo	{}
2026-07-16 05:08:54.219466+01	DOGE-USD	0.07385999709367752	626796992	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07385999709367752	yahoo	{}
2026-07-16 05:08:54.53889+01	SHIB-USD	4.219999937049579e-06	55549680	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.219999937049579e-06	yahoo	{}
2026-07-16 05:08:54.880561+01	AVAX-USD	6.710000038146973	208477344	6.696125507354736	6.715437889099121	6.670616149902344	6.710000038146973	yahoo	{}
2026-07-16 05:08:57.496257+01	ATOM-USD	1.5470000505447388	25701714	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5470000505447388	yahoo	{}
2026-07-16 05:10:34.359501+01	BTC-USD	64558	27026386944	64720.35546875	64793.71484375	64389.390625	64558	yahoo	{}
2026-07-16 05:10:34.682494+01	ETH-USD	1916.300048828125	12636737536	1917.0543212890625	1926.4071044921875	1907.8677978515625	1916.300048828125	yahoo	{}
2026-07-16 05:10:35.067785+01	SOL-USD	76.77999877929688	2069731584	77.26387023925781	77.37681579589844	76.75849914550781	76.77999877929688	yahoo	{}
2026-07-16 05:10:35.372298+01	XRP-USD	1.1109000444412231	1185656960	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1109000444412231	yahoo	{}
2026-07-16 05:10:35.699783+01	ADA-USD	0.1647000014781952	298516608	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.1647000014781952	yahoo	{}
2026-07-16 05:10:36.014774+01	DOT-USD	0.8450000286102295	89673440	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8450000286102295	yahoo	{}
2026-07-16 05:10:36.327214+01	LINK-USD	8.529999732971191	291938272	8.535067558288574	8.542733192443848	8.464689254760742	8.529999732971191	yahoo	{}
2026-07-16 05:10:36.612883+01	DOGE-USD	0.07387000322341919	626711488	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07387000322341919	yahoo	{}
2026-07-16 05:10:36.928175+01	SHIB-USD	4.2100000428035855e-06	55558596	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.2100000428035855e-06	yahoo	{}
2026-07-16 05:10:37.27853+01	AVAX-USD	6.699999809265137	208409024	6.696125507354736	6.715437889099121	6.670616149902344	6.699999809265137	yahoo	{}
2026-07-16 05:10:39.946601+01	ATOM-USD	1.5460000038146973	25694912	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5460000038146973	yahoo	{}
2026-07-16 05:12:16.156601+01	BTC-USD	64608.01171875	27026296832	64720.35546875	64793.71484375	64389.390625	64608.01171875	yahoo	{}
2026-07-16 05:12:16.464509+01	ETH-USD	1919.300048828125	12634974208	1917.0543212890625	1926.4071044921875	1907.8677978515625	1919.300048828125	yahoo	{}
2026-07-16 05:12:16.754878+01	SOL-USD	76.91000366210938	2068943872	77.26387023925781	77.37681579589844	76.75849914550781	76.91000366210938	yahoo	{}
2026-07-16 05:12:17.055268+01	XRP-USD	1.1122000217437744	1186213248	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1122000217437744	yahoo	{}
2026-07-16 05:12:17.377199+01	ADA-USD	0.16500000655651093	298753280	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.16500000655651093	yahoo	{}
2026-07-16 05:12:17.723705+01	DOT-USD	0.8429999947547913	89916152	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8429999947547913	yahoo	{}
2026-07-16 05:12:18.060819+01	LINK-USD	8.541999816894531	291520544	8.535067558288574	8.542733192443848	8.464689254760742	8.541999816894531	yahoo	{}
2026-07-16 05:12:18.40123+01	DOGE-USD	0.07400999963283539	627221248	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07400999963283539	yahoo	{}
2026-07-16 05:12:18.722306+01	SHIB-USD	4.2100000428035855e-06	55562044	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.2100000428035855e-06	yahoo	{}
2026-07-16 05:12:19.054167+01	AVAX-USD	6.699999809265137	208424976	6.696125507354736	6.715437889099121	6.670616149902344	6.699999809265137	yahoo	{}
2026-07-16 05:12:21.722944+01	ATOM-USD	1.5479999780654907	25691852	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5479999780654907	yahoo	{}
2026-07-16 05:13:59.304664+01	BTC-USD	64595.859375	27025004544	64720.35546875	64793.71484375	64389.390625	64595.859375	yahoo	{}
2026-07-16 05:13:59.886783+01	ETH-USD	1919.3900146484375	12640037888	1917.0543212890625	1926.4071044921875	1907.8677978515625	1919.3900146484375	yahoo	{}
2026-07-16 05:14:00.253439+01	SOL-USD	76.91999816894531	2068836992	77.26387023925781	77.37681579589844	76.75849914550781	76.91999816894531	yahoo	{}
2026-07-16 05:14:00.593709+01	XRP-USD	1.1123000383377075	1186265088	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1123000383377075	yahoo	{}
2026-07-16 05:14:01.028585+01	ADA-USD	0.16500000655651093	298747648	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.16500000655651093	yahoo	{}
2026-07-16 05:14:01.426963+01	DOT-USD	0.843999981880188	89904104	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.843999981880188	yahoo	{}
2026-07-16 05:14:01.851249+01	LINK-USD	8.54699993133545	291492384	8.535067558288574	8.542733192443848	8.464689254760742	8.54699993133545	yahoo	{}
2026-07-16 05:14:02.24126+01	DOGE-USD	0.07401999831199646	627230656	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07401999831199646	yahoo	{}
2026-07-16 05:14:02.602362+01	SHIB-USD	4.2100000428035855e-06	55583764	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.2100000428035855e-06	yahoo	{}
2026-07-16 05:14:02.90573+01	AVAX-USD	6.710000038146973	208540224	6.696125507354736	6.715437889099121	6.670616149902344	6.710000038146973	yahoo	{}
2026-07-16 05:14:05.543546+01	ATOM-USD	1.5490000247955322	25683438	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5490000247955322	yahoo	{}
2026-07-16 05:15:45.170615+01	BTC-USD	64577.69921875	27014995968	64720.35546875	64793.71484375	64389.390625	64577.69921875	yahoo	{}
2026-07-16 05:15:45.523042+01	ETH-USD	1917.31005859375	12630880256	1917.0543212890625	1926.4071044921875	1907.8677978515625	1917.31005859375	yahoo	{}
2026-07-16 05:15:45.832271+01	SOL-USD	76.87000274658203	2068978176	77.26387023925781	77.37681579589844	76.75849914550781	76.87000274658203	yahoo	{}
2026-07-16 05:15:46.146709+01	XRP-USD	1.111899971961975	1185745408	1.1127955913543701	1.1164233684539795	1.107488751411438	1.111899971961975	yahoo	{}
2026-07-16 05:15:46.491069+01	ADA-USD	0.16500000655651093	298771072	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.16500000655651093	yahoo	{}
2026-07-16 05:15:46.782878+01	DOT-USD	0.8429999947547913	89910336	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8429999947547913	yahoo	{}
2026-07-16 05:15:47.259092+01	LINK-USD	8.541999816894531	291569888	8.535067558288574	8.542733192443848	8.464689254760742	8.541999816894531	yahoo	{}
2026-07-16 05:15:47.585529+01	DOGE-USD	0.07400000095367432	627230656	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07400000095367432	yahoo	{}
2026-07-16 05:15:47.896541+01	SHIB-USD	4.2100000428035855e-06	55602308	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.2100000428035855e-06	yahoo	{}
2026-07-16 05:15:48.264847+01	AVAX-USD	6.710000038146973	208528608	6.696125507354736	6.715437889099121	6.670616149902344	6.710000038146973	yahoo	{}
2026-07-16 05:15:50.94906+01	ATOM-USD	1.5479999780654907	25694778	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5479999780654907	yahoo	{}
2026-07-16 05:17:27.623222+01	BTC-USD	64566.80078125	27008366592	64720.35546875	64793.71484375	64389.390625	64566.80078125	yahoo	{}
2026-07-16 05:17:27.929742+01	ETH-USD	1916.6300048828125	12630585344	1917.0543212890625	1926.4071044921875	1907.8677978515625	1916.6300048828125	yahoo	{}
2026-07-16 05:17:28.26509+01	SOL-USD	76.83999633789062	2069068416	77.26387023925781	77.37681579589844	76.75849914550781	76.83999633789062	yahoo	{}
2026-07-16 05:17:28.572869+01	XRP-USD	1.111299991607666	1185524480	1.1127955913543701	1.1164233684539795	1.107488751411438	1.111299991607666	yahoo	{}
2026-07-16 05:17:28.863347+01	ADA-USD	0.16500000655651093	298766272	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.16500000655651093	yahoo	{}
2026-07-16 05:17:29.155059+01	DOT-USD	0.8429999947547913	90013288	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8429999947547913	yahoo	{}
2026-07-16 05:17:29.441713+01	LINK-USD	8.53499984741211	291751232	8.535067558288574	8.542733192443848	8.464689254760742	8.53499984741211	yahoo	{}
2026-07-16 05:17:29.783099+01	DOGE-USD	0.07394000142812729	626983424	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07394000142812729	yahoo	{}
2026-07-16 05:17:30.184151+01	SHIB-USD	4.2100000428035855e-06	55659112	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.2100000428035855e-06	yahoo	{}
2026-07-16 05:17:30.519172+01	AVAX-USD	6.699999809265137	208744176	6.696125507354736	6.715437889099121	6.670616149902344	6.699999809265137	yahoo	{}
2026-07-16 05:17:33.188063+01	ATOM-USD	1.5479999780654907	25688892	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5479999780654907	yahoo	{}
2026-07-16 05:19:15.230032+01	BTC-USD	64541.3984375	26865246208	64720.35546875	64793.71484375	64389.390625	64541.3984375	yahoo	{}
2026-07-16 05:19:15.702522+01	ETH-USD	1915.52001953125	12518701056	1917.0543212890625	1926.4071044921875	1907.8677978515625	1915.52001953125	yahoo	{}
2026-07-16 05:19:16.069689+01	SOL-USD	76.81999969482422	2069566336	77.26387023925781	77.37681579589844	76.75849914550781	76.81999969482422	yahoo	{}
2026-07-16 05:19:16.37528+01	XRP-USD	1.11080002784729	1184825088	1.1127955913543701	1.1164233684539795	1.107488751411438	1.11080002784729	yahoo	{}
2026-07-16 05:19:16.660148+01	ADA-USD	0.164900004863739	298847328	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.164900004863739	yahoo	{}
2026-07-16 05:19:16.961757+01	DOT-USD	0.8429999947547913	90049432	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8429999947547913	yahoo	{}
2026-07-16 05:19:17.29391+01	LINK-USD	8.527000427246094	291822752	8.535067558288574	8.542733192443848	8.464689254760742	8.527000427246094	yahoo	{}
2026-07-16 05:19:17.576545+01	DOGE-USD	0.0738999992609024	626949568	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.0738999992609024	yahoo	{}
2026-07-16 05:19:17.896107+01	SHIB-USD	4.2100000428035855e-06	55702408	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.2100000428035855e-06	yahoo	{}
2026-07-16 05:19:18.58587+01	AVAX-USD	6.699999809265137	208876608	6.696125507354736	6.715437889099121	6.670616149902344	6.699999809265137	yahoo	{}
2026-07-16 05:19:21.279859+01	ATOM-USD	1.5470000505447388	25684890	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5470000505447388	yahoo	{}
2026-07-16 05:20:57.250754+01	BTC-USD	64519.62109375	26982631424	64720.35546875	64793.71484375	64389.390625	64519.62109375	yahoo	{}
2026-07-16 05:20:57.586843+01	ETH-USD	1914.760009765625	12522885120	1917.0543212890625	1926.4071044921875	1907.8677978515625	1914.760009765625	yahoo	{}
2026-07-16 05:20:57.912126+01	SOL-USD	76.79000091552734	2070482432	77.26387023925781	77.37681579589844	76.75849914550781	76.79000091552734	yahoo	{}
2026-07-16 05:20:58.262958+01	XRP-USD	1.1110999584197998	1184666624	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1110999584197998	yahoo	{}
2026-07-16 05:20:58.626137+01	ADA-USD	0.1648000031709671	298372192	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.1648000031709671	yahoo	{}
2026-07-16 05:20:58.966842+01	DOT-USD	0.8420000076293945	89978464	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8420000076293945	yahoo	{}
2026-07-16 05:20:59.302815+01	LINK-USD	8.526000022888184	291842304	8.535067558288574	8.542733192443848	8.464689254760742	8.526000022888184	yahoo	{}
2026-07-16 05:20:59.613105+01	DOGE-USD	0.07388000190258026	626718848	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07388000190258026	yahoo	{}
2026-07-16 05:20:59.901813+01	SHIB-USD	4.2100000428035855e-06	55686736	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.2100000428035855e-06	yahoo	{}
2026-07-16 05:21:00.230468+01	AVAX-USD	6.690000057220459	208809920	6.696125507354736	6.715437889099121	6.670616149902344	6.690000057220459	yahoo	{}
2026-07-16 05:21:02.925074+01	ATOM-USD	1.5470000505447388	25685990	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5470000505447388	yahoo	{}
2026-07-16 05:35:13.197223+01	BTC-USD	64561.9609375	27000475648	64720.35546875	64793.71484375	64389.390625	64561.9609375	yahoo	{}
2026-07-16 05:35:13.616021+01	ETH-USD	1917.199951171875	12360718336	1917.0543212890625	1926.4071044921875	1907.8677978515625	1917.199951171875	yahoo	{}
2026-07-16 05:35:13.925995+01	SOL-USD	76.80000305175781	2078147072	77.26387023925781	77.37681579589844	76.73925018310547	76.80000305175781	yahoo	{}
2026-07-16 05:35:14.249905+01	XRP-USD	1.1121000051498413	1183279872	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1121000051498413	yahoo	{}
2026-07-16 05:35:14.598103+01	ADA-USD	0.1647000014781952	295600000	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.1647000014781952	yahoo	{}
2026-07-16 05:35:14.920146+01	DOT-USD	0.8429999947547913	90058536	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8429999947547913	yahoo	{}
2026-07-16 05:35:15.250271+01	LINK-USD	8.53499984741211	292751456	8.535067558288574	8.542733192443848	8.464689254760742	8.53499984741211	yahoo	{}
2026-07-16 05:35:15.661245+01	DOGE-USD	0.0738999992609024	627223616	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.0738999992609024	yahoo	{}
2026-07-16 05:35:16.009928+01	SHIB-USD	4.229999831295572e-06	55745164	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.229999831295572e-06	yahoo	{}
2026-07-16 05:35:16.333328+01	AVAX-USD	6.699999809265137	209255136	6.696125507354736	6.715437889099121	6.670616149902344	6.699999809265137	yahoo	{}
2026-07-16 05:35:21.193359+01	ATOM-USD	1.5479999780654907	25625550	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5479999780654907	yahoo	{}
2026-07-16 05:36:35.337691+01	BTC-USD	64561.9609375	27000475648	64720.35546875	64793.71484375	64389.390625	64561.9609375	yahoo	{}
2026-07-16 05:36:35.798994+01	ETH-USD	1917.199951171875	12360718336	1917.0543212890625	1926.4071044921875	1907.8677978515625	1917.199951171875	yahoo	{}
2026-07-16 05:36:36.225631+01	SOL-USD	76.80000305175781	2078147072	77.26387023925781	77.37681579589844	76.73925018310547	76.80000305175781	yahoo	{}
2026-07-16 05:36:36.570148+01	XRP-USD	1.1121000051498413	1183279872	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1121000051498413	yahoo	{}
2026-07-16 05:36:36.914314+01	ADA-USD	0.1647000014781952	295600000	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.1647000014781952	yahoo	{}
2026-07-16 05:36:37.277552+01	DOT-USD	0.8429999947547913	90058536	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8429999947547913	yahoo	{}
2026-07-16 05:36:37.565951+01	LINK-USD	8.53499984741211	292751456	8.535067558288574	8.542733192443848	8.464689254760742	8.53499984741211	yahoo	{}
2026-07-16 05:36:37.860649+01	DOGE-USD	0.0738999992609024	627223616	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.0738999992609024	yahoo	{}
2026-07-16 05:36:38.192115+01	SHIB-USD	4.229999831295572e-06	55745164	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.229999831295572e-06	yahoo	{}
2026-07-16 05:36:38.501347+01	AVAX-USD	6.699999809265137	209255136	6.696125507354736	6.715437889099121	6.670616149902344	6.699999809265137	yahoo	{}
2026-07-16 05:36:43.269198+01	ATOM-USD	1.5479999780654907	25625550	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5479999780654907	yahoo	{}
2026-07-16 05:37:56.681968+01	BTC-USD	64557.33984375	27095975936	64720.35546875	64793.71484375	64389.390625	64557.33984375	yahoo	{}
2026-07-16 05:37:57.047217+01	ETH-USD	1917.1700439453125	12450116608	1917.0543212890625	1926.4071044921875	1907.8677978515625	1917.1700439453125	yahoo	{}
2026-07-16 05:37:57.37257+01	SOL-USD	76.80999755859375	2077816320	77.26387023925781	77.37681579589844	76.73925018310547	76.80999755859375	yahoo	{}
2026-07-16 05:37:57.667325+01	XRP-USD	1.1125999689102173	1183763200	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1125999689102173	yahoo	{}
2026-07-16 05:37:58.066433+01	ADA-USD	0.1647000014781952	295471232	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.1647000014781952	yahoo	{}
2026-07-16 05:37:58.379056+01	DOT-USD	0.8429999947547913	90009544	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8429999947547913	yahoo	{}
2026-07-16 05:37:58.682855+01	LINK-USD	8.538000106811523	292736192	8.535067558288574	8.542733192443848	8.464689254760742	8.538000106811523	yahoo	{}
2026-07-16 05:37:59.0164+01	DOGE-USD	0.0738999992609024	627116544	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.0738999992609024	yahoo	{}
2026-07-16 05:37:59.318514+01	SHIB-USD	4.219999937049579e-06	55684436	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.219999937049579e-06	yahoo	{}
2026-07-16 05:37:59.637265+01	AVAX-USD	6.699999809265137	209267392	6.696125507354736	6.715437889099121	6.670616149902344	6.699999809265137	yahoo	{}
2026-07-16 05:38:04.339589+01	ATOM-USD	1.5520000457763672	25625848	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5520000457763672	yahoo	{}
2026-07-16 05:39:17.778599+01	BTC-USD	64552.28125	27061293056	64720.35546875	64793.71484375	64389.390625	64552.28125	yahoo	{}
2026-07-16 05:39:18.110187+01	ETH-USD	1917.4100341796875	12636280832	1917.0543212890625	1926.4071044921875	1907.8677978515625	1917.4100341796875	yahoo	{}
2026-07-16 05:39:18.414042+01	SOL-USD	76.81999969482422	2077228800	77.26387023925781	77.37681579589844	76.73925018310547	76.81999969482422	yahoo	{}
2026-07-16 05:39:18.765831+01	XRP-USD	1.1126999855041504	1183629312	1.1127955913543701	1.1164233684539795	1.107488751411438	1.1126999855041504	yahoo	{}
2026-07-16 05:39:19.092391+01	ADA-USD	0.1647000014781952	295471232	0.1650838702917099	0.16619683802127838	0.16412928700447083	0.1647000014781952	yahoo	{}
2026-07-16 05:39:19.766217+01	DOT-USD	0.8410000205039978	90009544	0.8464276194572449	0.8496637344360352	0.8399677276611328	0.8410000205039978	yahoo	{}
2026-07-16 05:39:20.067378+01	LINK-USD	8.538999557495117	292736192	8.535067558288574	8.542733192443848	8.464689254760742	8.538999557495117	yahoo	{}
2026-07-16 05:39:20.390636+01	DOGE-USD	0.07388000190258026	627116544	0.0740443542599678	0.07430679351091385	0.07370540499687195	0.07388000190258026	yahoo	{}
2026-07-16 05:39:20.700326+01	SHIB-USD	4.219999937049579e-06	55662396	4.232715582475066e-06	4.234066182107199e-06	4.207840447634226e-06	4.219999937049579e-06	yahoo	{}
2026-07-16 05:39:21.012907+01	AVAX-USD	6.699999809265137	209267392	6.696125507354736	6.715437889099121	6.670616149902344	6.699999809265137	yahoo	{}
2026-07-16 05:39:25.592513+01	ATOM-USD	1.5520000457763672	25625848	1.5548127889633179	1.5565645694732666	1.5417639017105103	1.5520000457763672	yahoo	{}
\.


--
-- Data for Name: price_forex; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.price_forex ("time", symbol, price, volume, open, high, low, close, source, metadata) FROM stdin;
2026-07-16 04:27:50.269649+01	EURUSD	1.1471836566925049	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1471836566925049	yahoo	{}
2026-07-16 04:52:12.431829+01	EURUSD	1.1469204425811768	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1469204425811768	yahoo	{}
2026-07-16 04:52:15.453544+01	GBPUSD	1.3532898426055908	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.3532898426055908	yahoo	{}
2026-07-16 04:52:15.786341+01	USDJPY	162.0970001220703	0	162.10400390625	162.16900634765625	162.0229949951172	162.0970001220703	yahoo	{}
2026-07-16 04:52:16.095273+01	AUDUSD	0.7000349760055542	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7000349760055542	yahoo	{}
2026-07-16 04:52:16.400432+01	USDCAD	1.404770016670227	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.404770016670227	yahoo	{}
2026-07-16 04:52:16.699253+01	NZDUSD	0.5852402448654175	0	0.5849663615226746	0.5853772759437561	0.5836348533630371	0.5852402448654175	yahoo	{}
2026-07-16 04:52:16.986337+01	USDCHF	0.8058500289916992	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8058500289916992	yahoo	{}
2026-07-16 04:52:17.290916+01	EURGBP	0.8472800254821777	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8472800254821777	yahoo	{}
2026-07-16 04:52:17.589345+01	EURJPY	185.86199951171875	0	185.87600708007812	185.9949951171875	185.78199768066406	185.86199951171875	yahoo	{}
2026-07-16 04:52:17.917968+01	GBPJPY	219.35299682617188	0	219.36500549316406	219.5489959716797	219.1929931640625	219.35299682617188	yahoo	{}
2026-07-16 04:52:18.218691+01	AUDJPY	113.4260025024414	0	113.52799987792969	113.63800048828125	113.26799774169922	113.4260025024414	yahoo	{}
2026-07-16 04:52:18.554184+01	EURCHF	0.9239799976348877	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9239799976348877	yahoo	{}
2026-07-16 04:52:18.850804+01	USDCNH	6.766590118408203	0	6.765820026397705	6.772039890289307	6.764150142669678	6.766590118408203	yahoo	{}
2026-07-16 04:54:20.945278+01	EURUSD	1.1469204425811768	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1469204425811768	yahoo	{}
2026-07-16 04:54:21.275177+01	GBPUSD	1.3532166481018066	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.3532166481018066	yahoo	{}
2026-07-16 04:54:21.592688+01	USDJPY	162.09500122070312	0	162.10400390625	162.16900634765625	162.0229949951172	162.09500122070312	yahoo	{}
2026-07-16 04:54:21.92205+01	AUDUSD	0.7000839710235596	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7000839710235596	yahoo	{}
2026-07-16 04:54:22.269805+01	USDCAD	1.4047499895095825	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4047499895095825	yahoo	{}
2026-07-16 04:54:22.616806+01	NZDUSD	0.5852402448654175	0	0.5849663615226746	0.5853772759437561	0.5836348533630371	0.5852402448654175	yahoo	{}
2026-07-16 04:54:22.909827+01	USDCHF	0.8058500289916992	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8058500289916992	yahoo	{}
2026-07-16 04:54:23.273198+01	EURGBP	0.8472700119018555	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8472700119018555	yahoo	{}
2026-07-16 04:54:23.600676+01	EURJPY	185.85800170898438	0	185.87600708007812	185.9949951171875	185.78199768066406	185.85800170898438	yahoo	{}
2026-07-16 04:54:23.889291+01	GBPJPY	219.34800720214844	0	219.36500549316406	219.5489959716797	219.1929931640625	219.34800720214844	yahoo	{}
2026-07-16 04:54:24.184736+01	AUDJPY	113.43599700927734	0	113.52799987792969	113.63800048828125	113.26799774169922	113.43599700927734	yahoo	{}
2026-07-16 04:54:24.499883+01	EURCHF	0.9239599704742432	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9239599704742432	yahoo	{}
2026-07-16 04:54:24.825876+01	USDCNH	6.766089916229248	0	6.765820026397705	6.772039890289307	6.764150142669678	6.766089916229248	yahoo	{}
2026-07-16 04:56:02.294534+01	EURUSD	1.1469204425811768	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1469204425811768	yahoo	{}
2026-07-16 04:56:02.60324+01	GBPUSD	1.353234887123108	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.353234887123108	yahoo	{}
2026-07-16 04:56:02.911869+01	USDJPY	162.10400390625	0	162.10400390625	162.16900634765625	162.0229949951172	162.10400390625	yahoo	{}
2026-07-16 04:56:03.21992+01	AUDUSD	0.7000839710235596	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7000839710235596	yahoo	{}
2026-07-16 04:56:03.548595+01	USDCAD	1.4047199487686157	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4047199487686157	yahoo	{}
2026-07-16 04:56:03.851568+01	NZDUSD	0.5852060317993164	0	0.5849663615226746	0.5853772759437561	0.5836348533630371	0.5852060317993164	yahoo	{}
2026-07-16 04:56:04.158411+01	USDCHF	0.805899977684021	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.805899977684021	yahoo	{}
2026-07-16 04:56:04.47839+01	EURGBP	0.8472800254821777	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8472800254821777	yahoo	{}
2026-07-16 04:56:04.802235+01	EURJPY	185.86399841308594	0	185.87600708007812	185.9949951171875	185.78199768066406	185.86399841308594	yahoo	{}
2026-07-16 04:56:05.104037+01	GBPJPY	219.33599853515625	0	219.36500549316406	219.5489959716797	219.1929931640625	219.33599853515625	yahoo	{}
2026-07-16 04:56:05.431597+01	AUDJPY	113.43800354003906	0	113.52799987792969	113.63800048828125	113.26799774169922	113.43800354003906	yahoo	{}
2026-07-16 04:56:05.751576+01	EURCHF	0.9239799976348877	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9239799976348877	yahoo	{}
2026-07-16 04:56:06.063802+01	USDCNH	6.766200065612793	0	6.765820026397705	6.772039890289307	6.764150142669678	6.766200065612793	yahoo	{}
2026-07-16 04:57:43.639376+01	EURUSD	1.1469204425811768	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1469204425811768	yahoo	{}
2026-07-16 04:57:44.021348+01	GBPUSD	1.3533082008361816	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.3533082008361816	yahoo	{}
2026-07-16 04:57:44.347765+01	USDJPY	162.1009979248047	0	162.10400390625	162.16900634765625	162.0229949951172	162.1009979248047	yahoo	{}
2026-07-16 04:57:44.703778+01	AUDUSD	0.7001820206642151	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7001820206642151	yahoo	{}
2026-07-16 04:57:45.070753+01	USDCAD	1.4046900272369385	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4046900272369385	yahoo	{}
2026-07-16 04:57:45.404282+01	NZDUSD	0.5852744579315186	0	0.5849663615226746	0.5853772759437561	0.5836348533630371	0.5852744579315186	yahoo	{}
2026-07-16 04:57:45.718192+01	USDCHF	0.8058500289916992	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8058500289916992	yahoo	{}
2026-07-16 04:57:46.063412+01	EURGBP	0.8473100066184998	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8473100066184998	yahoo	{}
2026-07-16 04:57:46.407608+01	EURJPY	185.87100219726562	0	185.87600708007812	185.9949951171875	185.78199768066406	185.87100219726562	yahoo	{}
2026-07-16 04:57:46.725334+01	GBPJPY	219.343994140625	0	219.36500549316406	219.5489959716797	219.1929931640625	219.343994140625	yahoo	{}
2026-07-16 04:57:47.032443+01	AUDJPY	113.45700073242188	0	113.52799987792969	113.63800048828125	113.26799774169922	113.45700073242188	yahoo	{}
2026-07-16 04:57:47.36584+01	EURCHF	0.9240099787712097	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9240099787712097	yahoo	{}
2026-07-16 04:57:47.683009+01	USDCNH	6.766550064086914	0	6.765820026397705	6.772039890289307	6.764150142669678	6.766550064086914	yahoo	{}
2026-07-16 04:59:25.970033+01	EURUSD	1.1469204425811768	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1469204425811768	yahoo	{}
2026-07-16 04:59:26.267697+01	GBPUSD	1.3532166481018066	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.3532166481018066	yahoo	{}
2026-07-16 04:59:26.578556+01	USDJPY	162.0959930419922	0	162.10400390625	162.16900634765625	162.0229949951172	162.0959930419922	yahoo	{}
2026-07-16 04:59:26.934215+01	AUDUSD	0.7002310752868652	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7002310752868652	yahoo	{}
2026-07-16 04:59:27.235284+01	USDCAD	1.4047800302505493	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4047800302505493	yahoo	{}
2026-07-16 04:59:27.547573+01	NZDUSD	0.5852744579315186	0	0.5849663615226746	0.5853772759437561	0.5836348533630371	0.5852744579315186	yahoo	{}
2026-07-16 04:59:28.235086+01	USDCHF	0.8058599829673767	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8058599829673767	yahoo	{}
2026-07-16 04:59:28.544534+01	EURGBP	0.8472800254821777	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8472800254821777	yahoo	{}
2026-07-16 04:59:28.871512+01	EURJPY	185.86000061035156	0	185.87600708007812	185.9949951171875	185.78199768066406	185.86000061035156	yahoo	{}
2026-07-16 04:59:29.183771+01	GBPJPY	219.3459930419922	0	219.36500549316406	219.5489959716797	219.1929931640625	219.3459930419922	yahoo	{}
2026-07-16 04:59:29.532616+01	AUDJPY	113.46600341796875	0	113.52799987792969	113.63800048828125	113.26799774169922	113.46600341796875	yahoo	{}
2026-07-16 04:59:29.862209+01	EURCHF	0.9239299893379211	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9239299893379211	yahoo	{}
2026-07-16 04:59:30.207848+01	USDCNH	6.766600131988525	0	6.765820026397705	6.772039890289307	6.764150142669678	6.766600131988525	yahoo	{}
2026-07-16 05:01:09.15376+01	EURUSD	1.1469204425811768	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1469204425811768	yahoo	{}
2026-07-16 05:01:09.489182+01	GBPUSD	1.353363037109375	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.353363037109375	yahoo	{}
2026-07-16 05:01:09.794684+01	USDJPY	162.09300231933594	0	162.10400390625	162.16900634765625	162.0229949951172	162.09300231933594	yahoo	{}
2026-07-16 05:01:10.101848+01	AUDUSD	0.7002801299095154	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7002801299095154	yahoo	{}
2026-07-16 05:01:10.449153+01	USDCAD	1.4047499895095825	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4047499895095825	yahoo	{}
2026-07-16 05:01:10.773542+01	NZDUSD	0.5853430032730103	0	0.5849663615226746	0.5853772759437561	0.5836348533630371	0.5853430032730103	yahoo	{}
2026-07-16 05:01:11.141301+01	USDCHF	0.8058000206947327	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8058000206947327	yahoo	{}
2026-07-16 05:01:11.469753+01	EURGBP	0.8472399711608887	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8472399711608887	yahoo	{}
2026-07-16 05:01:11.831329+01	EURJPY	185.86599731445312	0	185.87600708007812	185.9949951171875	185.78199768066406	185.86599731445312	yahoo	{}
2026-07-16 05:01:12.176618+01	GBPJPY	219.36500549316406	0	219.36500549316406	219.5489959716797	219.1929931640625	219.36500549316406	yahoo	{}
2026-07-16 05:01:12.506719+01	AUDJPY	113.46399688720703	0	113.52799987792969	113.63800048828125	113.26799774169922	113.46399688720703	yahoo	{}
2026-07-16 05:01:12.841451+01	EURCHF	0.9239699840545654	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9239699840545654	yahoo	{}
2026-07-16 05:01:13.177044+01	USDCNH	6.765820026397705	0	6.765820026397705	6.772039890289307	6.764150142669678	6.765820026397705	yahoo	{}
2026-07-16 05:02:50.835354+01	EURUSD	1.1469204425811768	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1469204425811768	yahoo	{}
2026-07-16 05:02:51.160382+01	GBPUSD	1.353363037109375	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.353363037109375	yahoo	{}
2026-07-16 05:02:51.488963+01	USDJPY	162.07899475097656	0	162.10400390625	162.16900634765625	162.0229949951172	162.07899475097656	yahoo	{}
2026-07-16 05:02:51.853552+01	AUDUSD	0.7002801299095154	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7002801299095154	yahoo	{}
2026-07-16 05:02:52.156827+01	USDCAD	1.4046499729156494	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4046499729156494	yahoo	{}
2026-07-16 05:02:52.476801+01	NZDUSD	0.5853430032730103	0	0.5849663615226746	0.5853772759437561	0.5836348533630371	0.5853430032730103	yahoo	{}
2026-07-16 05:02:52.793558+01	USDCHF	0.8058900237083435	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8058900237083435	yahoo	{}
2026-07-16 05:02:53.114663+01	EURGBP	0.8472300171852112	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8472300171852112	yahoo	{}
2026-07-16 05:02:53.428139+01	EURJPY	185.84500122070312	0	185.87600708007812	185.9949951171875	185.78199768066406	185.84500122070312	yahoo	{}
2026-07-16 05:02:53.779073+01	GBPJPY	219.33599853515625	0	219.36500549316406	219.5489959716797	219.1929931640625	219.33599853515625	yahoo	{}
2026-07-16 05:02:54.072771+01	AUDJPY	113.45099639892578	0	113.52799987792969	113.63800048828125	113.26799774169922	113.45099639892578	yahoo	{}
2026-07-16 05:02:54.412819+01	EURCHF	0.924019992351532	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.924019992351532	yahoo	{}
2026-07-16 05:02:54.761833+01	USDCNH	6.766409873962402	0	6.765820026397705	6.772039890289307	6.764150142669678	6.766409873962402	yahoo	{}
2026-07-16 05:04:52.779008+01	EURUSD	1.1469204425811768	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1469204425811768	yahoo	{}
2026-07-16 05:04:53.113119+01	GBPUSD	1.3533447980880737	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.3533447980880737	yahoo	{}
2026-07-16 05:04:53.421708+01	USDJPY	162.09100341796875	0	162.10400390625	162.16900634765625	162.0229949951172	162.09100341796875	yahoo	{}
2026-07-16 05:04:53.71914+01	AUDUSD	0.7002310752868652	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7002310752868652	yahoo	{}
2026-07-16 05:04:54.013217+01	USDCAD	1.4046399593353271	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4046399593353271	yahoo	{}
2026-07-16 05:04:54.309035+01	NZDUSD	0.5853430032730103	0	0.5849663615226746	0.5853772759437561	0.5836348533630371	0.5853430032730103	yahoo	{}
2026-07-16 05:04:54.59487+01	USDCHF	0.8059300184249878	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8059300184249878	yahoo	{}
2026-07-16 05:04:54.909675+01	EURGBP	0.8471800088882446	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8471800088882446	yahoo	{}
2026-07-16 05:04:55.206467+01	EURJPY	185.8459930419922	0	185.87600708007812	185.9949951171875	185.78199768066406	185.8459930419922	yahoo	{}
2026-07-16 05:04:55.504861+01	GBPJPY	219.34800720214844	0	219.36500549316406	219.5489959716797	219.1929931640625	219.34800720214844	yahoo	{}
2026-07-16 05:04:55.823581+01	AUDJPY	113.45999908447266	0	113.52799987792969	113.63800048828125	113.26799774169922	113.45999908447266	yahoo	{}
2026-07-16 05:04:56.117583+01	EURCHF	0.9240000247955322	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9240000247955322	yahoo	{}
2026-07-16 05:04:56.435876+01	USDCNH	6.766499996185303	0	6.765820026397705	6.772039890289307	6.764150142669678	6.766499996185303	yahoo	{}
2026-07-16 05:06:34.405016+01	EURUSD	1.1467890739440918	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1467890739440918	yahoo	{}
2026-07-16 05:06:34.759068+01	GBPUSD	1.353271484375	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.353271484375	yahoo	{}
2026-07-16 05:06:35.081957+01	USDJPY	162.08799743652344	0	162.10400390625	162.16900634765625	162.0229949951172	162.08799743652344	yahoo	{}
2026-07-16 05:06:35.414323+01	AUDUSD	0.7002801299095154	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7002801299095154	yahoo	{}
2026-07-16 05:06:35.718135+01	USDCAD	1.4046499729156494	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4046499729156494	yahoo	{}
2026-07-16 05:06:36.026972+01	NZDUSD	0.5853087306022644	0	0.5849663615226746	0.5853772759437561	0.5836348533630371	0.5853087306022644	yahoo	{}
2026-07-16 05:06:36.354873+01	USDCHF	0.8059300184249878	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8059300184249878	yahoo	{}
2026-07-16 05:06:36.69328+01	EURGBP	0.8471699953079224	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8471699953079224	yahoo	{}
2026-07-16 05:06:37.046641+01	EURJPY	185.83599853515625	0	185.87600708007812	185.9949951171875	185.78199768066406	185.83599853515625	yahoo	{}
2026-07-16 05:06:37.393241+01	GBPJPY	219.3459930419922	0	219.36500549316406	219.5489959716797	219.1929931640625	219.3459930419922	yahoo	{}
2026-07-16 05:06:37.745151+01	AUDJPY	113.46299743652344	0	113.52799987792969	113.63800048828125	113.26799774169922	113.46299743652344	yahoo	{}
2026-07-16 05:06:38.102826+01	EURCHF	0.924019992351532	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.924019992351532	yahoo	{}
2026-07-16 05:06:38.484455+01	USDCNH	6.76584005355835	0	6.765820026397705	6.772039890289307	6.764150142669678	6.76584005355835	yahoo	{}
2026-07-16 05:08:15.991833+01	EURUSD	1.1467890739440918	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1467890739440918	yahoo	{}
2026-07-16 05:08:16.304698+01	GBPUSD	1.3533447980880737	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.3533447980880737	yahoo	{}
2026-07-16 05:08:16.597793+01	USDJPY	162.0919952392578	0	162.10400390625	162.16900634765625	162.0229949951172	162.0919952392578	yahoo	{}
2026-07-16 05:08:16.912446+01	AUDUSD	0.7002801299095154	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7002801299095154	yahoo	{}
2026-07-16 05:08:17.273804+01	USDCAD	1.4046499729156494	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4046499729156494	yahoo	{}
2026-07-16 05:08:17.599408+01	NZDUSD	0.5853087306022644	0	0.5849663615226746	0.5853772759437561	0.5836348533630371	0.5853087306022644	yahoo	{}
2026-07-16 05:08:17.905335+01	USDCHF	0.8059899806976318	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8059899806976318	yahoo	{}
2026-07-16 05:08:18.218612+01	EURGBP	0.8472099900245667	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8472099900245667	yahoo	{}
2026-07-16 05:08:18.548938+01	EURJPY	185.8509979248047	0	185.87600708007812	185.9949951171875	185.78199768066406	185.8509979248047	yahoo	{}
2026-07-16 05:08:18.891661+01	GBPJPY	219.3419952392578	0	219.36500549316406	219.5489959716797	219.1929931640625	219.3419952392578	yahoo	{}
2026-07-16 05:08:19.18399+01	AUDJPY	113.46199798583984	0	113.52799987792969	113.63800048828125	113.26799774169922	113.46199798583984	yahoo	{}
2026-07-16 05:08:19.513142+01	EURCHF	0.9240800142288208	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9240800142288208	yahoo	{}
2026-07-16 05:08:19.836658+01	USDCNH	6.765979766845703	0	6.765820026397705	6.772039890289307	6.764150142669678	6.765979766845703	yahoo	{}
2026-07-16 05:09:57.79314+01	EURUSD	1.1467890739440918	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1467890739440918	yahoo	{}
2026-07-16 05:09:58.159802+01	GBPUSD	1.3533082008361816	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.3533082008361816	yahoo	{}
2026-07-16 05:09:58.537566+01	USDJPY	162.10499572753906	0	162.10400390625	162.16900634765625	162.0229949951172	162.10499572753906	yahoo	{}
2026-07-16 05:09:58.828034+01	AUDUSD	0.7002801299095154	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7002801299095154	yahoo	{}
2026-07-16 05:09:59.129134+01	USDCAD	1.404770016670227	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.404770016670227	yahoo	{}
2026-07-16 05:09:59.427165+01	NZDUSD	0.5853087306022644	0	0.5849663615226746	0.5853772759437561	0.5836348533630371	0.5853087306022644	yahoo	{}
2026-07-16 05:09:59.737879+01	USDCHF	0.8061299920082092	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8061299920082092	yahoo	{}
2026-07-16 05:10:00.023059+01	EURGBP	0.8471599817276001	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8471599817276001	yahoo	{}
2026-07-16 05:10:00.325538+01	EURJPY	185.83999633789062	0	185.87600708007812	185.9949951171875	185.78199768066406	185.83999633789062	yahoo	{}
2026-07-16 05:10:00.62089+01	GBPJPY	219.35800170898438	0	219.36500549316406	219.5489959716797	219.1929931640625	219.35800170898438	yahoo	{}
2026-07-16 05:10:01.199955+01	AUDJPY	113.45800018310547	0	113.52799987792969	113.63800048828125	113.26799774169922	113.45800018310547	yahoo	{}
2026-07-16 05:10:01.565083+01	EURCHF	0.9241200089454651	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9241200089454651	yahoo	{}
2026-07-16 05:10:01.986034+01	USDCNH	6.766829967498779	0	6.765820026397705	6.772039890289307	6.764150142669678	6.766829967498779	yahoo	{}
2026-07-16 05:11:40.286802+01	EURUSD	1.1467890739440918	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1467890739440918	yahoo	{}
2026-07-16 05:11:40.630072+01	GBPUSD	1.3532531261444092	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.3532531261444092	yahoo	{}
2026-07-16 05:11:40.97014+01	USDJPY	162.11000061035156	0	162.10400390625	162.16900634765625	162.0229949951172	162.11000061035156	yahoo	{}
2026-07-16 05:11:41.327286+01	AUDUSD	0.7002310752868652	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7002310752868652	yahoo	{}
2026-07-16 05:11:41.672233+01	USDCAD	1.4043999910354614	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4043999910354614	yahoo	{}
2026-07-16 05:11:41.96988+01	NZDUSD	0.5852402448654175	0	0.5849663615226746	0.5853772759437561	0.5836348533630371	0.5852402448654175	yahoo	{}
2026-07-16 05:11:42.283968+01	USDCHF	0.8059099912643433	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8059099912643433	yahoo	{}
2026-07-16 05:11:42.616846+01	EURGBP	0.8471400141716003	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8471400141716003	yahoo	{}
2026-07-16 05:11:42.972378+01	EURJPY	185.85299682617188	0	185.87600708007812	185.9949951171875	185.78199768066406	185.85299682617188	yahoo	{}
2026-07-16 05:11:43.310886+01	GBPJPY	219.3769989013672	0	219.36500549316406	219.5489959716797	219.1929931640625	219.3769989013672	yahoo	{}
2026-07-16 05:11:43.620765+01	AUDJPY	113.48200225830078	0	113.52799987792969	113.63800048828125	113.26799774169922	113.48200225830078	yahoo	{}
2026-07-16 05:11:43.930105+01	EURCHF	0.9239599704742432	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9239599704742432	yahoo	{}
2026-07-16 05:11:44.319365+01	USDCNH	6.765779972076416	0	6.765820026397705	6.772039890289307	6.764150142669678	6.765779972076416	yahoo	{}
2026-07-16 05:13:22.040901+01	EURUSD	1.1467890739440918	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1467890739440918	yahoo	{}
2026-07-16 05:13:22.368378+01	GBPUSD	1.3533813953399658	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.3533813953399658	yahoo	{}
2026-07-16 05:13:22.709129+01	USDJPY	162.09800720214844	0	162.10400390625	162.16900634765625	162.0229949951172	162.09800720214844	yahoo	{}
2026-07-16 05:13:23.025999+01	AUDUSD	0.700427234172821	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.700427234172821	yahoo	{}
2026-07-16 05:13:23.362184+01	USDCAD	1.4045599699020386	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4045599699020386	yahoo	{}
2026-07-16 05:13:23.680768+01	NZDUSD	0.5853087306022644	0	0.5849663615226746	0.5853772759437561	0.5836348533630371	0.5853087306022644	yahoo	{}
2026-07-16 05:13:24.24229+01	USDCHF	0.8059099912643433	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8059099912643433	yahoo	{}
2026-07-16 05:13:24.545151+01	EURGBP	0.8471099734306335	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8471099734306335	yahoo	{}
2026-07-16 05:13:24.867354+01	EURJPY	185.85499572753906	0	185.87600708007812	185.9949951171875	185.78199768066406	185.85499572753906	yahoo	{}
2026-07-16 05:13:25.178453+01	GBPJPY	219.3769989013672	0	219.36500549316406	219.5489959716797	219.1929931640625	219.3769989013672	yahoo	{}
2026-07-16 05:13:25.526701+01	AUDJPY	113.49500274658203	0	113.52799987792969	113.63800048828125	113.26799774169922	113.49500274658203	yahoo	{}
2026-07-16 05:13:25.84097+01	EURCHF	0.9239599704742432	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9239599704742432	yahoo	{}
2026-07-16 05:13:26.217834+01	USDCNH	6.765659809112549	0	6.765820026397705	6.772039890289307	6.764150142669678	6.765659809112549	yahoo	{}
2026-07-16 05:15:05.983711+01	EURUSD	1.1467890739440918	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1467890739440918	yahoo	{}
2026-07-16 05:15:06.352893+01	GBPUSD	1.3534730672836304	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.3534730672836304	yahoo	{}
2026-07-16 05:15:06.955149+01	USDJPY	162.11599731445312	0	162.10400390625	162.16900634765625	162.0229949951172	162.11599731445312	yahoo	{}
2026-07-16 05:15:07.454184+01	AUDUSD	0.7005254030227661	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7005254030227661	yahoo	{}
2026-07-16 05:15:07.754611+01	USDCAD	1.4041999578475952	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4041999578475952	yahoo	{}
2026-07-16 05:15:08.062285+01	NZDUSD	0.5854800939559937	0	0.5849663615226746	0.5854800939559937	0.5836348533630371	0.5854800939559937	yahoo	{}
2026-07-16 05:15:08.392119+01	USDCHF	0.8059399724006653	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8059399724006653	yahoo	{}
2026-07-16 05:15:10.049003+01	EURGBP	0.8470799922943115	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8470799922943115	yahoo	{}
2026-07-16 05:15:10.538198+01	EURJPY	185.8719940185547	0	185.87600708007812	185.9949951171875	185.78199768066406	185.8719940185547	yahoo	{}
2026-07-16 05:15:10.932163+01	GBPJPY	219.41000366210938	0	219.36500549316406	219.5489959716797	219.1929931640625	219.41000366210938	yahoo	{}
2026-07-16 05:15:11.411252+01	AUDJPY	113.5250015258789	0	113.52799987792969	113.63800048828125	113.26799774169922	113.5250015258789	yahoo	{}
2026-07-16 05:15:11.741491+01	EURCHF	0.9240000247955322	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9240000247955322	yahoo	{}
2026-07-16 05:15:12.248217+01	USDCNH	6.7657599449157715	0	6.765820026397705	6.772039890289307	6.764150142669678	6.7657599449157715	yahoo	{}
2026-07-16 05:16:51.274701+01	EURUSD	1.1467890739440918	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1467890739440918	yahoo	{}
2026-07-16 05:16:51.638485+01	GBPUSD	1.3534730672836304	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.3534730672836304	yahoo	{}
2026-07-16 05:16:51.951001+01	USDJPY	162.1179962158203	0	162.10400390625	162.16900634765625	162.0229949951172	162.1179962158203	yahoo	{}
2026-07-16 05:16:52.289899+01	AUDUSD	0.7005254030227661	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7005254030227661	yahoo	{}
2026-07-16 05:16:52.626692+01	USDCAD	1.4043999910354614	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4043999910354614	yahoo	{}
2026-07-16 05:16:52.930681+01	NZDUSD	0.5854800939559937	0	0.5849663615226746	0.5854800939559937	0.5836348533630371	0.5854800939559937	yahoo	{}
2026-07-16 05:16:53.253782+01	USDCHF	0.8059899806976318	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8059899806976318	yahoo	{}
2026-07-16 05:16:53.551187+01	EURGBP	0.847029983997345	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.847029983997345	yahoo	{}
2026-07-16 05:16:53.919318+01	EURJPY	185.86399841308594	0	185.87600708007812	185.9949951171875	185.78199768066406	185.86399841308594	yahoo	{}
2026-07-16 05:16:54.236648+01	GBPJPY	219.406005859375	0	219.36500549316406	219.5489959716797	219.1929931640625	219.406005859375	yahoo	{}
2026-07-16 05:16:54.540163+01	AUDJPY	113.51699829101562	0	113.52799987792969	113.63800048828125	113.26799774169922	113.51699829101562	yahoo	{}
2026-07-16 05:16:54.8935+01	EURCHF	0.9240000247955322	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9240000247955322	yahoo	{}
2026-07-16 05:16:55.267788+01	USDCNH	6.766160011291504	0	6.765820026397705	6.772039890289307	6.764150142669678	6.766160011291504	yahoo	{}
2026-07-16 05:18:33.519666+01	EURUSD	1.1467890739440918	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1467890739440918	yahoo	{}
2026-07-16 05:18:34.79398+01	GBPUSD	1.3533997535705566	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.3533997535705566	yahoo	{}
2026-07-16 05:18:35.155722+01	USDJPY	162.1179962158203	0	162.10400390625	162.16900634765625	162.0229949951172	162.1179962158203	yahoo	{}
2026-07-16 05:18:35.54423+01	AUDUSD	0.7004762887954712	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.7004762887954712	yahoo	{}
2026-07-16 05:18:35.827919+01	USDCAD	1.4046299457550049	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4046299457550049	yahoo	{}
2026-07-16 05:18:36.139171+01	NZDUSD	0.5853087306022644	0	0.5849663615226746	0.5854800939559937	0.5836348533630371	0.5853087306022644	yahoo	{}
2026-07-16 05:18:36.453092+01	USDCHF	0.8060500025749207	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8060500025749207	yahoo	{}
2026-07-16 05:18:36.746896+01	EURGBP	0.8470600247383118	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8470600247383118	yahoo	{}
2026-07-16 05:18:37.07549+01	EURJPY	185.85899353027344	0	185.87600708007812	185.9949951171875	185.78199768066406	185.85899353027344	yahoo	{}
2026-07-16 05:18:37.422177+01	GBPJPY	219.39599609375	0	219.36500549316406	219.5489959716797	219.1929931640625	219.39599609375	yahoo	{}
2026-07-16 05:18:37.822961+01	AUDJPY	113.51799774169922	0	113.52799987792969	113.63800048828125	113.26799774169922	113.51799774169922	yahoo	{}
2026-07-16 05:18:38.228718+01	EURCHF	0.9241099953651428	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9241099953651428	yahoo	{}
2026-07-16 05:18:38.519745+01	USDCNH	6.766849994659424	0	6.765820026397705	6.772039890289307	6.764150142669678	6.766849994659424	yahoo	{}
2026-07-16 05:20:21.637591+01	EURUSD	1.1466574668884277	0	1.1469204425811768	1.1477103233337402	1.1463946104049683	1.1466574668884277	yahoo	{}
2026-07-16 05:20:21.978219+01	GBPUSD	1.3532898426055908	0	1.3535646200180054	1.3544446229934692	1.3520456552505493	1.3532898426055908	yahoo	{}
2026-07-16 05:20:22.312396+01	USDJPY	162.12600708007812	0	162.10400390625	162.16900634765625	162.0229949951172	162.12600708007812	yahoo	{}
2026-07-16 05:20:22.639417+01	AUDUSD	0.700427234172821	0	0.7007708549499512	0.701311469078064	0.6989585757255554	0.700427234172821	yahoo	{}
2026-07-16 05:20:22.976302+01	USDCAD	1.4043999910354614	0	1.4039000272750854	1.4053699970245361	1.4026999473571777	1.4043999910354614	yahoo	{}
2026-07-16 05:20:23.28615+01	NZDUSD	0.5851717591285706	0	0.5849663615226746	0.5854800939559937	0.5836348533630371	0.5851717591285706	yahoo	{}
2026-07-16 05:20:23.619222+01	USDCHF	0.8061299920082092	0	0.8045099973678589	0.806439995765686	0.8035200238227844	0.8061299920082092	yahoo	{}
2026-07-16 05:20:23.922959+01	EURGBP	0.8470900058746338	0	0.8468400239944458	0.8479499816894531	0.8460599780082703	0.8470900058746338	yahoo	{}
2026-07-16 05:20:24.258305+01	EURJPY	185.85800170898438	0	185.87600708007812	185.9949951171875	185.78199768066406	185.85800170898438	yahoo	{}
2026-07-16 05:20:24.573489+01	GBPJPY	219.3939971923828	0	219.36500549316406	219.5489959716797	219.1929931640625	219.3939971923828	yahoo	{}
2026-07-16 05:20:24.887077+01	AUDJPY	113.50499725341797	0	113.52799987792969	113.63800048828125	113.26799774169922	113.50499725341797	yahoo	{}
2026-07-16 05:20:25.190269+01	EURCHF	0.9241300225257874	0	0.9224200248718262	0.9243999719619751	0.9223099946975708	0.9241300225257874	yahoo	{}
2026-07-16 05:20:25.521608+01	USDCNH	6.766980171203613	0	6.765820026397705	6.772039890289307	6.764150142669678	6.766980171203613	yahoo	{}
2026-07-16 08:34:57+01	EURUSD	1.14645	0	\N	\N	\N	\N	mt5	{"ask": 1.14645, "bid": 1.14635, "spread": 10}
2026-07-16 08:34:57+01	GBPUSD	1.3532	0	\N	\N	\N	\N	mt5	{"ask": 1.3532, "bid": 1.35309, "spread": 11}
2026-07-16 08:34:55+01	USDJPY	162.145	0	\N	\N	\N	\N	mt5	{"ask": 162.145, "bid": 162.133, "spread": 12}
2026-07-16 08:34:50+01	AUDUSD	0.70016	0	\N	\N	\N	\N	mt5	{"ask": 0.70016, "bid": 0.70006, "spread": 10}
2026-07-16 08:34:57+01	USDCAD	1.40488	0	\N	\N	\N	\N	mt5	{"ask": 1.40488, "bid": 1.40475, "spread": 13}
2026-07-16 08:34:56+01	NZDUSD	0.5849	0	\N	\N	\N	\N	mt5	{"ask": 0.5849, "bid": 0.58478, "spread": 12}
2026-07-16 08:34:58+01	USDCHF	0.80626	0	\N	\N	\N	\N	mt5	{"ask": 0.80626, "bid": 0.80614, "spread": 12}
2026-07-16 08:34:56+01	EURGBP	0.84726	0	\N	\N	\N	\N	mt5	{"ask": 0.84726, "bid": 0.84715, "spread": 11}
2026-07-16 08:34:58+01	EURJPY	185.894	0	\N	\N	\N	\N	mt5	{"ask": 185.894, "bid": 185.874, "spread": 20}
2026-07-16 08:34:56+01	GBPJPY	219.41	0	\N	\N	\N	\N	mt5	{"ask": 219.41, "bid": 219.391, "spread": 19}
2026-07-16 08:34:57+01	AUDJPY	113.525	0	\N	\N	\N	\N	mt5	{"ask": 113.525, "bid": 113.505, "spread": 20}
2026-07-16 08:34:57+01	EURCHF	0.92431	0	\N	\N	\N	\N	mt5	{"ask": 0.92431, "bid": 0.92416, "spread": 15}
2026-07-16 08:34:55+01	USDCNH	6.7674199999999995	0	\N	\N	\N	\N	mt5	{"ask": 6.7674199999999995, "bid": 6.7668, "spread": 62}
2026-07-16 08:34:58+01	XAUUSD	4032.96	0	\N	\N	\N	\N	mt5	{"ask": 4032.96, "bid": 4032.74, "spread": 22}
2026-07-16 08:34:57+01	XAGUSD	57.082	0	\N	\N	\N	\N	mt5	{"ask": 57.082, "bid": 57.047, "spread": 35}
2026-07-16 08:36:11+01	EURUSD	1.14648	0	\N	\N	\N	\N	mt5	{"ask": 1.14648, "bid": 1.14638, "spread": 10}
2026-07-16 08:36:22+01	GBPUSD	1.3532899999999999	0	\N	\N	\N	\N	mt5	{"ask": 1.3532899999999999, "bid": 1.35317, "spread": 12}
2026-07-16 08:36:21+01	USDJPY	162.144	0	\N	\N	\N	\N	mt5	{"ask": 162.144, "bid": 162.131, "spread": 13}
2026-07-16 08:36:22+01	AUDUSD	0.70019	0	\N	\N	\N	\N	mt5	{"ask": 0.70019, "bid": 0.70009, "spread": 10}
2026-07-16 08:36:18+01	USDCAD	1.40487	0	\N	\N	\N	\N	mt5	{"ask": 1.40487, "bid": 1.40473, "spread": 14}
2026-07-16 08:36:21+01	NZDUSD	0.58491	0	\N	\N	\N	\N	mt5	{"ask": 0.58491, "bid": 0.58479, "spread": 12}
2026-07-16 08:36:15+01	USDCHF	0.80624	0	\N	\N	\N	\N	mt5	{"ask": 0.80624, "bid": 0.80613, "spread": 11}
2026-07-16 08:36:19+01	EURGBP	0.84725	0	\N	\N	\N	\N	mt5	{"ask": 0.84725, "bid": 0.84714, "spread": 11}
2026-07-16 08:36:22+01	EURJPY	185.896	0	\N	\N	\N	\N	mt5	{"ask": 185.896, "bid": 185.878, "spread": 18}
2026-07-16 08:36:22+01	GBPJPY	219.413	0	\N	\N	\N	\N	mt5	{"ask": 219.413, "bid": 219.397, "spread": 16}
2026-07-16 08:36:22+01	AUDJPY	113.527	0	\N	\N	\N	\N	mt5	{"ask": 113.527, "bid": 113.51, "spread": 17}
2026-07-16 08:36:22+01	EURCHF	0.92431	0	\N	\N	\N	\N	mt5	{"ask": 0.92431, "bid": 0.92416, "spread": 15}
2026-07-16 08:36:22+01	USDCNH	6.76745	0	\N	\N	\N	\N	mt5	{"ask": 6.76745, "bid": 6.76682, "spread": 63}
2026-07-16 08:36:22+01	XAUUSD	4032.76	0	\N	\N	\N	\N	mt5	{"ask": 4032.76, "bid": 4032.53, "spread": 23}
2026-07-16 08:36:21+01	XAGUSD	57.097	0	\N	\N	\N	\N	mt5	{"ask": 57.097, "bid": 57.066, "spread": 31}
2026-07-16 08:37:37+01	EURUSD	1.14658	0	\N	\N	\N	\N	mt5	{"ask": 1.14658, "bid": 1.14648, "spread": 10}
2026-07-16 08:37:44+01	GBPUSD	1.3534	0	\N	\N	\N	\N	mt5	{"ask": 1.3534, "bid": 1.35327, "spread": 13}
2026-07-16 08:37:44+01	USDJPY	162.134	0	\N	\N	\N	\N	mt5	{"ask": 162.134, "bid": 162.121, "spread": 13}
2026-07-16 08:37:41+01	AUDUSD	0.70023	0	\N	\N	\N	\N	mt5	{"ask": 0.70023, "bid": 0.70013, "spread": 10}
2026-07-16 08:37:42+01	USDCAD	1.40478	0	\N	\N	\N	\N	mt5	{"ask": 1.40478, "bid": 1.40464, "spread": 14}
2026-07-16 08:37:44+01	NZDUSD	0.58491	0	\N	\N	\N	\N	mt5	{"ask": 0.58491, "bid": 0.58479, "spread": 12}
2026-07-16 08:37:43+01	USDCHF	0.80618	0	\N	\N	\N	\N	mt5	{"ask": 0.80618, "bid": 0.80606, "spread": 12}
2026-07-16 08:37:22+01	EURGBP	0.84725	0	\N	\N	\N	\N	mt5	{"ask": 0.84725, "bid": 0.84714, "spread": 11}
2026-07-16 08:37:44+01	EURJPY	185.898	0	\N	\N	\N	\N	mt5	{"ask": 185.898, "bid": 185.882, "spread": 16}
2026-07-16 08:37:44+01	GBPJPY	219.417	0	\N	\N	\N	\N	mt5	{"ask": 219.417, "bid": 219.399, "spread": 18}
2026-07-16 08:37:44+01	AUDJPY	113.526	0	\N	\N	\N	\N	mt5	{"ask": 113.526, "bid": 113.511, "spread": 15}
2026-07-16 08:37:43+01	EURCHF	0.92431	0	\N	\N	\N	\N	mt5	{"ask": 0.92431, "bid": 0.92416, "spread": 15}
2026-07-16 08:37:43+01	USDCNH	6.76734	0	\N	\N	\N	\N	mt5	{"ask": 6.76734, "bid": 6.76672, "spread": 62}
2026-07-16 08:37:44+01	XAUUSD	4033.63	0	\N	\N	\N	\N	mt5	{"ask": 4033.63, "bid": 4033.41, "spread": 22}
2026-07-16 08:37:44+01	XAGUSD	57.122	0	\N	\N	\N	\N	mt5	{"ask": 57.122, "bid": 57.087, "spread": 35}
2026-07-16 08:39:00+01	EURUSD	1.14661	0	\N	\N	\N	\N	mt5	{"ask": 1.14661, "bid": 1.14651, "spread": 10}
2026-07-16 08:39:04+01	GBPUSD	1.35341	0	\N	\N	\N	\N	mt5	{"ask": 1.35341, "bid": 1.3532899999999999, "spread": 12}
2026-07-16 08:39:04+01	USDJPY	162.131	0	\N	\N	\N	\N	mt5	{"ask": 162.131, "bid": 162.119, "spread": 12}
2026-07-16 08:39:04+01	AUDUSD	0.70022	0	\N	\N	\N	\N	mt5	{"ask": 0.70022, "bid": 0.70012, "spread": 10}
2026-07-16 08:39:03+01	USDCAD	1.40478	0	\N	\N	\N	\N	mt5	{"ask": 1.40478, "bid": 1.40464, "spread": 14}
2026-07-16 08:39:00+01	NZDUSD	0.58495	0	\N	\N	\N	\N	mt5	{"ask": 0.58495, "bid": 0.58483, "spread": 12}
2026-07-16 08:39:02+01	USDCHF	0.80617	0	\N	\N	\N	\N	mt5	{"ask": 0.80617, "bid": 0.80604, "spread": 13}
2026-07-16 08:38:59+01	EURGBP	0.84724	0	\N	\N	\N	\N	mt5	{"ask": 0.84724, "bid": 0.84713, "spread": 11}
2026-07-16 08:39:03+01	EURJPY	185.907	0	\N	\N	\N	\N	mt5	{"ask": 185.907, "bid": 185.887, "spread": 20}
2026-07-16 08:39:05+01	GBPJPY	219.426	0	\N	\N	\N	\N	mt5	{"ask": 219.426, "bid": 219.407, "spread": 19}
2026-07-16 08:39:04+01	AUDJPY	113.526	0	\N	\N	\N	\N	mt5	{"ask": 113.526, "bid": 113.507, "spread": 19}
2026-07-16 08:39:00+01	EURCHF	0.92432	0	\N	\N	\N	\N	mt5	{"ask": 0.92432, "bid": 0.92417, "spread": 15}
2026-07-16 08:39:05+01	USDCNH	6.7675	0	\N	\N	\N	\N	mt5	{"ask": 6.7675, "bid": 6.76684, "spread": 66}
2026-07-16 08:39:04+01	XAUUSD	4033.58	0	\N	\N	\N	\N	mt5	{"ask": 4033.58, "bid": 4033.4, "spread": 18}
2026-07-16 08:39:05+01	XAGUSD	57.103	0	\N	\N	\N	\N	mt5	{"ask": 57.103, "bid": 57.068, "spread": 35}
\.


--
-- Data for Name: price_indices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.price_indices ("time", symbol, price, volume, open, high, low, close, source, metadata) FROM stdin;
\.


--
-- Data for Name: price_stocks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.price_stocks ("time", symbol, price, volume, open, high, low, close, source, metadata) FROM stdin;
2026-07-16 04:27:51.316039+01	AAPL	327.5	60780931	317.625	328.7200012207031	317.32000732421875	327.5	yahoo	{}
2026-07-16 04:52:27.747949+01	WTI	3.4100000858306885	3409980	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 04:52:30.451796+01	NG	5.699999809265137	4032263	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 04:52:56.070701+01	AAPL	327.5	60780931	317.625	328.7200012207031	317.32000732421875	327.5	yahoo	{}
2026-07-16 04:52:57.493915+01	MSFT	395.6300048828125	32663427	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 04:52:58.61506+01	GOOGL	370.9200134277344	28115784	358.1499938964844	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 04:52:59.21728+01	AMZN	254.9600067138672	42296511	249.97000122070312	256.4800109863281	249.9199981689453	254.9600067138672	yahoo	{}
2026-07-16 04:52:59.88832+01	NVDA	212.5	118979465	212.00999450683594	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 04:53:00.43135+01	META	681.3099975585938	17731107	663.5999755859375	686.0800170898438	656.6600952148438	681.3099975585938	yahoo	{}
2026-07-16 04:53:00.943788+01	TSLA	394.4599914550781	31393664	399.3949890136719	406.5895080566406	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 04:53:01.587405+01	JPM	346.9100036621094	10741102	345.8450012207031	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 04:53:02.484422+01	V	355.1400146484375	8846866	354	360.42999267578125	349.1600036621094	355.1400146484375	yahoo	{}
2026-07-16 04:53:03.629932+01	WMT	112.52999877929688	15525020	113.18000030517578	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 04:53:04.341267+01	JNJ	247.02000427246094	10005307	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 04:53:05.063427+01	PG	148.0500030517578	6129328	145.27999877929688	148.58999633789062	144.72999572753906	148.0500030517578	yahoo	{}
2026-07-16 04:53:05.655605+01	UNH	418.5199890136719	6745442	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 04:53:06.322503+01	HD	341.44000244140625	3942239	338.989990234375	346.25	337.25909423828125	341.44000244140625	yahoo	{}
2026-07-16 04:53:07.079269+01	BAC	61.59000015258789	35350776	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 04:53:08.048745+01	XOM	144.50999450683594	9901276	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 04:53:08.925405+01	CVX	181.60000610351562	5341301	182.1699981689453	182.40089416503906	178.5749969482422	181.60000610351562	yahoo	{}
2026-07-16 04:53:09.829875+01	KO	82.44999694824219	11400870	82.93000030517578	83.23500061035156	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 04:53:10.693019+01	PEP	135.39999389648438	7428048	135.0500030517578	136.99000549316406	134.65460205078125	135.39999389648438	yahoo	{}
2026-07-16 04:53:11.402898+01	MCD	264.95001220703125	6033786	268	270.25	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 04:54:28.432243+01	WTI	3.4100000858306885	3409980	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 04:54:30.293646+01	NG	5.699999809265137	4032263	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 04:54:49.199668+01	AAPL	327.5	60780931	317.625	328.7200012207031	317.32000732421875	327.5	yahoo	{}
2026-07-16 04:54:49.53251+01	MSFT	395.6300048828125	32663427	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 04:54:49.845279+01	GOOGL	370.9200134277344	28115784	358.1499938964844	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 04:54:50.154324+01	AMZN	254.9600067138672	42296511	249.97000122070312	256.4800109863281	249.9199981689453	254.9600067138672	yahoo	{}
2026-07-16 04:54:50.461762+01	NVDA	212.5	118979465	212.00999450683594	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 04:54:50.769916+01	META	681.3099975585938	17731107	663.5999755859375	686.0800170898438	656.6600952148438	681.3099975585938	yahoo	{}
2026-07-16 04:54:51.085053+01	TSLA	394.4599914550781	31393664	399.3949890136719	406.5895080566406	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 04:54:51.430417+01	JPM	346.9100036621094	10741102	345.8450012207031	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 04:54:51.815715+01	V	355.1400146484375	8846866	354	360.42999267578125	349.1600036621094	355.1400146484375	yahoo	{}
2026-07-16 04:54:52.198704+01	WMT	112.52999877929688	15525020	113.18000030517578	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 04:54:52.571717+01	JNJ	247.02000427246094	10005307	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 04:54:52.963586+01	PG	148.0500030517578	6129328	145.27999877929688	148.58999633789062	144.72999572753906	148.0500030517578	yahoo	{}
2026-07-16 04:54:53.328591+01	UNH	418.5199890136719	6745442	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 04:54:53.68256+01	HD	341.44000244140625	3942239	338.989990234375	346.25	337.25909423828125	341.44000244140625	yahoo	{}
2026-07-16 04:54:54.058884+01	BAC	61.59000015258789	35350776	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 04:54:54.494042+01	XOM	144.50999450683594	9901276	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 04:54:54.872446+01	CVX	181.60000610351562	5341301	182.1699981689453	182.40089416503906	178.5749969482422	181.60000610351562	yahoo	{}
2026-07-16 04:54:55.277537+01	KO	82.44999694824219	11400870	82.93000030517578	83.23500061035156	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 04:54:55.692661+01	PEP	135.39999389648438	7428048	135.0500030517578	136.99000549316406	134.65460205078125	135.39999389648438	yahoo	{}
2026-07-16 04:54:56.082152+01	MCD	264.95001220703125	6033786	268	270.25	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 04:56:09.499494+01	WTI	3.4100000858306885	3409980	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 04:56:11.359618+01	NG	5.699999809265137	4032263	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 04:56:30.322429+01	AAPL	327.5	60780931	317.625	328.7200012207031	317.32000732421875	327.5	yahoo	{}
2026-07-16 04:56:30.695579+01	MSFT	395.6300048828125	32663427	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 04:56:31.063411+01	GOOGL	370.9200134277344	28115784	358.1499938964844	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 04:56:31.376468+01	AMZN	254.9600067138672	42296511	249.97000122070312	256.4800109863281	249.9199981689453	254.9600067138672	yahoo	{}
2026-07-16 04:56:31.726833+01	NVDA	212.5	118979465	212.00999450683594	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 04:56:32.091691+01	META	681.3099975585938	17731107	663.5999755859375	686.0800170898438	656.6600952148438	681.3099975585938	yahoo	{}
2026-07-16 04:56:32.42175+01	TSLA	394.4599914550781	31393664	399.3949890136719	406.5895080566406	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 04:56:32.767997+01	JPM	346.9100036621094	10741102	345.8450012207031	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 04:56:33.096168+01	V	355.1400146484375	8846866	354	360.42999267578125	349.1600036621094	355.1400146484375	yahoo	{}
2026-07-16 04:56:33.490486+01	WMT	112.52999877929688	15525020	113.18000030517578	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 04:56:33.919134+01	JNJ	247.02000427246094	10005307	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 04:56:34.297425+01	PG	148.0500030517578	6129328	145.27999877929688	148.58999633789062	144.72999572753906	148.0500030517578	yahoo	{}
2026-07-16 04:56:34.666405+01	UNH	418.5199890136719	6745442	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 04:56:35.018234+01	HD	341.44000244140625	3942239	338.989990234375	346.25	337.25909423828125	341.44000244140625	yahoo	{}
2026-07-16 04:56:35.384696+01	BAC	61.59000015258789	35350776	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 04:56:35.735964+01	XOM	144.50999450683594	9901276	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 04:56:36.129978+01	CVX	181.60000610351562	5341301	182.1699981689453	182.40089416503906	178.5749969482422	181.60000610351562	yahoo	{}
2026-07-16 04:56:36.554697+01	KO	82.44999694824219	11400870	82.93000030517578	83.23500061035156	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 04:56:36.896529+01	PEP	135.39999389648438	7428048	135.0500030517578	136.99000549316406	134.65460205078125	135.39999389648438	yahoo	{}
2026-07-16 04:56:37.267051+01	MCD	264.95001220703125	6033786	268	270.25	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 04:57:51.11778+01	WTI	3.4100000858306885	3409980	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 04:57:53.042656+01	NG	5.699999809265137	4032263	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 04:58:12.190043+01	AAPL	327.5	60780931	317.625	328.7200012207031	317.32000732421875	327.5	yahoo	{}
2026-07-16 04:58:12.564299+01	MSFT	395.6300048828125	32663427	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 04:58:12.916668+01	GOOGL	370.9200134277344	28115784	358.1499938964844	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 04:58:13.257328+01	AMZN	254.9600067138672	42296511	249.97000122070312	256.4800109863281	249.9199981689453	254.9600067138672	yahoo	{}
2026-07-16 04:58:13.621022+01	NVDA	212.5	118979465	212.00999450683594	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 04:58:13.950581+01	META	681.3099975585938	17731107	663.5999755859375	686.0800170898438	656.6600952148438	681.3099975585938	yahoo	{}
2026-07-16 04:58:14.262281+01	TSLA	394.4599914550781	31393664	399.3949890136719	406.5895080566406	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 04:58:14.645984+01	JPM	346.9100036621094	10741102	345.8450012207031	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 04:58:15.004451+01	V	355.1400146484375	8846866	354	360.42999267578125	349.1600036621094	355.1400146484375	yahoo	{}
2026-07-16 04:58:15.401021+01	WMT	112.52999877929688	15525020	113.18000030517578	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 04:58:15.779599+01	JNJ	247.02000427246094	10005307	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 04:58:16.240708+01	PG	148.0500030517578	6129328	145.27999877929688	148.58999633789062	144.72999572753906	148.0500030517578	yahoo	{}
2026-07-16 04:58:16.614015+01	UNH	418.5199890136719	6745442	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 04:58:17.00606+01	HD	341.44000244140625	3942239	338.989990234375	346.25	337.25909423828125	341.44000244140625	yahoo	{}
2026-07-16 04:58:17.410625+01	BAC	61.59000015258789	35350776	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 04:58:17.809268+01	XOM	144.50999450683594	9901276	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 04:58:18.218782+01	CVX	181.60000610351562	5341301	182.1699981689453	182.40089416503906	178.5749969482422	181.60000610351562	yahoo	{}
2026-07-16 04:58:18.591314+01	KO	82.44999694824219	11400870	82.93000030517578	83.23500061035156	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 04:58:19.014916+01	PEP	135.39999389648438	7428048	135.0500030517578	136.99000549316406	134.65460205078125	135.39999389648438	yahoo	{}
2026-07-16 04:58:19.457909+01	MCD	264.95001220703125	6033786	268	270.25	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 04:59:33.62748+01	WTI	3.4100000858306885	3409980	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 04:59:35.455761+01	NG	5.699999809265137	4032263	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 04:59:54.678255+01	AAPL	327.5	60780931	317.625	328.7200012207031	317.32000732421875	327.5	yahoo	{}
2026-07-16 04:59:55.308206+01	MSFT	395.6300048828125	32663427	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 04:59:55.68757+01	GOOGL	370.9200134277344	28115784	358.1499938964844	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 04:59:55.995328+01	AMZN	254.9600067138672	42296511	249.97000122070312	256.4800109863281	249.9199981689453	254.9600067138672	yahoo	{}
2026-07-16 04:59:56.35528+01	NVDA	212.5	118979465	212.00999450683594	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 04:59:56.740444+01	META	681.3099975585938	17731107	663.5999755859375	686.0800170898438	656.6600952148438	681.3099975585938	yahoo	{}
2026-07-16 04:59:57.11567+01	TSLA	394.4599914550781	31393664	399.3949890136719	406.5895080566406	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 04:59:57.477047+01	JPM	346.9100036621094	10741102	345.8450012207031	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 04:59:57.781109+01	V	355.1400146484375	8846866	354	360.42999267578125	349.1600036621094	355.1400146484375	yahoo	{}
2026-07-16 04:59:58.451649+01	WMT	112.52999877929688	15525020	113.18000030517578	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 04:59:58.932093+01	JNJ	247.02000427246094	10005307	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 04:59:59.56403+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 04:59:59.9375+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:00:00.387673+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:00:00.78607+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:00:01.170798+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:00:01.542478+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:00:01.950465+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:00:02.346401+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:00:02.698752+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:01:16.610187+01	WTI	3.4100000858306885	3421000	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 05:01:18.492508+01	NG	5.699999809265137	4169200	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 05:01:37.419836+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:01:37.78645+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:01:38.138893+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:01:38.477546+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:01:38.785742+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:01:39.082244+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:01:39.409589+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:01:39.777695+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:01:40.125112+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:01:40.488589+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:01:40.92428+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:01:41.36045+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:01:41.741337+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:01:42.119159+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:01:42.460187+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:01:42.895701+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:01:43.310088+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:01:43.721228+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:01:44.12065+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:01:44.513146+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:02:58.220807+01	WTI	3.4100000858306885	3421000	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 05:03:00.235584+01	NG	5.699999809265137	4169200	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 05:03:19.17514+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:03:19.559753+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:03:20.179333+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:03:20.521495+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:03:20.838442+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:03:21.138552+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:03:21.42654+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:03:21.784893+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:03:22.124049+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:03:22.491912+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:03:22.857559+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:03:24.937703+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:03:25.317168+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:03:26.099784+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:03:26.44834+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:03:26.84674+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:03:27.224964+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:03:27.609698+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:03:27.971246+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:03:28.354189+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:04:59.859152+01	WTI	3.4100000858306885	3421000	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 05:05:01.714575+01	NG	5.699999809265137	4169200	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 05:05:20.702717+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:05:21.071874+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:05:21.438224+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:05:21.76798+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:05:22.104458+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:05:22.406503+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:05:22.745472+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:05:23.193518+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:05:23.560545+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:05:23.948235+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:05:24.349091+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:05:24.772963+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:05:25.154846+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:05:25.539337+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:05:25.880723+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:05:26.291455+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:05:26.745777+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:05:27.141666+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:05:27.550052+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:05:27.977935+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:06:41.971893+01	WTI	3.4100000858306885	3421000	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 05:06:43.830063+01	NG	5.699999809265137	4169200	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 05:07:02.563448+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:07:02.900291+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:07:03.227313+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:07:03.550588+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:07:03.858358+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:07:04.172275+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:07:04.503551+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:07:04.924332+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:07:05.241844+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:07:05.659372+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:07:06.065217+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:07:06.488358+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:07:06.856915+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:07:07.248056+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:07:07.645946+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:07:08.074861+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:07:08.474466+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:07:08.872013+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:07:09.278691+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:07:09.650666+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:08:23.311397+01	WTI	3.4100000858306885	3421000	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 05:08:25.278056+01	NG	5.699999809265137	4169200	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 05:08:44.365144+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:08:44.71865+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:08:45.058046+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:08:45.365329+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:08:45.706977+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:08:46.022344+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:08:46.309876+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:08:46.715976+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:08:47.046429+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:08:47.409139+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:08:47.852921+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:08:48.284065+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:08:48.652399+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:08:49.138681+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:08:49.498485+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:08:49.8796+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:08:50.231218+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:08:50.63971+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:08:51.016303+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:08:51.39289+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:10:05.424398+01	WTI	3.4100000858306885	3421000	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 05:10:07.187924+01	NG	5.699999809265137	4169200	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 05:10:26.938516+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:10:27.3169+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:10:27.635225+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:10:27.952859+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:10:28.255637+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:10:28.571168+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:10:28.923913+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:10:29.307182+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:10:29.616336+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:10:29.966887+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:10:30.361943+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:10:30.706388+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:10:31.267948+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:10:31.636769+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:10:31.996134+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:10:32.418877+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:10:32.843106+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:10:33.249982+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:10:33.652942+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:10:34.045142+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:11:48.127768+01	WTI	3.4100000858306885	3421000	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 05:11:50.027425+01	NG	5.699999809265137	4169200	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 05:12:09.064205+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:12:09.380573+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:12:09.708179+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:12:10.008868+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:12:10.334547+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:12:10.637383+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:12:10.94944+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:12:11.322838+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:12:11.628082+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:12:11.965886+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:12:12.37217+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:12:12.806606+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:12:13.149824+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:12:13.488667+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:12:13.874123+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:12:14.253652+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:12:14.641868+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:12:15.059777+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:12:15.474911+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:12:15.84397+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:13:29.675306+01	WTI	3.4100000858306885	3421000	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 05:13:31.582311+01	NG	5.699999809265137	4169200	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 05:13:50.267743+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:13:50.671738+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:13:51.014223+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:13:51.339767+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:13:51.949316+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:13:52.341333+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:13:52.675201+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:13:53.162068+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:13:53.628505+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:13:54.063216+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:13:54.543563+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:13:55.316048+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:13:55.806416+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:13:56.244845+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:13:56.684933+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:13:57.112366+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:13:57.547769+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:13:58.017121+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:13:58.546081+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:13:58.944678+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:15:16.072143+01	WTI	3.4100000858306885	3421000	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 05:15:18.562576+01	NG	5.699999809265137	4169200	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 05:15:37.689311+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:15:38.178739+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:15:38.552171+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:15:39.116352+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:15:39.432586+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:15:39.726252+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:15:40.022479+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:15:40.366566+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:15:40.702375+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:15:41.084835+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:15:41.49638+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:15:41.942991+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:15:42.269758+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:15:42.609684+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:15:42.949378+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:15:43.365408+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:15:43.724426+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:15:44.130434+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:15:44.518269+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:15:44.847161+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:16:58.730614+01	WTI	3.4100000858306885	3421000	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 05:17:00.645086+01	NG	5.699999809265137	4169200	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 05:17:20.188113+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:17:20.55721+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:17:20.903542+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:17:21.242338+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:17:21.623786+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:17:21.953435+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:17:22.254515+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:17:22.630857+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:17:22.99364+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:17:23.340253+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:17:23.775714+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:17:24.193111+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:17:24.555135+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:17:24.930611+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:17:25.346914+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:17:25.73392+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:17:26.147705+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:17:26.568971+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:17:26.95107+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:17:27.306035+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:18:42.164084+01	WTI	3.4100000858306885	3421000	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 05:18:44.329657+01	NG	5.699999809265137	4169200	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 05:19:03.410075+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:19:03.849131+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:19:04.201085+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:19:04.571918+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:19:04.871601+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:19:05.185857+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:19:05.503609+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:19:05.893921+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:19:06.263257+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:19:06.648232+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:19:10.687472+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:19:11.404338+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:19:12.102581+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:19:12.515125+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:19:12.899698+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:19:13.331135+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:19:13.769788+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:19:14.166588+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:19:14.548609+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:19:14.952961+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:20:28.967018+01	WTI	3.4100000858306885	3421000	3.5899999141693115	3.619999885559082	3.319999933242798	3.4100000858306885	yahoo	{}
2026-07-16 05:20:30.834277+01	NG	5.699999809265137	4169200	5.909999847412109	6.010000228881836	5.650000095367432	5.699999809265137	yahoo	{}
2026-07-16 05:20:49.988286+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:20:50.356102+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:20:50.718271+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:20:51.066087+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:20:51.406926+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:20:51.742001+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:20:52.081554+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:20:52.426205+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:20:52.732605+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:20:53.111234+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:20:53.492627+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:20:53.878892+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:20:54.268626+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:20:54.596302+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:20:54.935123+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:20:55.298739+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:20:55.653254+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:20:56.063988+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:20:56.465299+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:20:56.912329+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:34:58.613391+01	WTI	79.52999877929688	11199	80	80.58999633789062	79.2699966430664	79.52999877929688	yahoo	{}
2026-07-16 05:34:58.960392+01	BRENT	84.7699966430664	2214	85.22000122070312	85.75	84.41000366210938	84.7699966430664	yahoo	{}
2026-07-16 05:34:59.370954+01	NG	2.9079999923706055	2509	2.9210000038146973	2.9240000247955322	2.885999917984009	2.9079999923706055	yahoo	{}
2026-07-16 05:35:03.769392+01	PLATINUM	1677.800048828125	2139	1682.0999755859375	1698	1667	1677.800048828125	yahoo	{}
2026-07-16 05:35:04.115176+01	PALLADIUM	1315.5	335	1322	1323	1306.5	1315.5	yahoo	{}
2026-07-16 05:35:04.449223+01	US100	26269.23046875	7379560000	26261.1796875	26316.810546875	26041.130859375	26269.23046875	yahoo	{}
2026-07-16 05:35:04.783535+01	JP225	67072.4375	0	67900.4296875	68069.8203125	66499.4921875	67072.4375	yahoo	{}
2026-07-16 05:35:05.177509+01	AU200	8824.2998046875	0	8841.099609375	8856.2001953125	8808.099609375	8824.2998046875	yahoo	{}
2026-07-16 05:35:05.503927+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:35:05.888622+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:35:06.194973+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:35:06.525988+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:35:06.891689+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:35:07.212342+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:35:07.658904+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:35:08.01391+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:35:08.343611+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:35:08.763301+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:35:09.258067+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:35:09.672864+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:35:10.011283+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:35:10.417801+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:35:10.82347+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:35:11.283439+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:35:11.680268+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:35:12.047628+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:35:12.433394+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:35:12.84744+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:36:21.642879+01	WTI	79.55999755859375	11203	80	80.58999633789062	79.2699966430664	79.55999755859375	yahoo	{}
2026-07-16 05:36:21.960687+01	BRENT	84.79000091552734	2217	85.22000122070312	85.75	84.41000366210938	84.79000091552734	yahoo	{}
2026-07-16 05:36:22.273379+01	NG	2.9079999923706055	2513	2.9210000038146973	2.9240000247955322	2.885999917984009	2.9079999923706055	yahoo	{}
2026-07-16 05:36:25.902701+01	PLATINUM	1677.800048828125	2139	1682.0999755859375	1698	1667	1677.800048828125	yahoo	{}
2026-07-16 05:36:26.229274+01	PALLADIUM	1315.5	335	1322	1323	1306.5	1315.5	yahoo	{}
2026-07-16 05:36:26.557469+01	US100	26269.23046875	7379560000	26261.1796875	26316.810546875	26041.130859375	26269.23046875	yahoo	{}
2026-07-16 05:36:26.893503+01	JP225	67025.9609375	0	67900.4296875	68069.8203125	66499.4921875	67025.9609375	yahoo	{}
2026-07-16 05:36:27.248148+01	AU200	8823.2998046875	0	8841.099609375	8856.2001953125	8808.099609375	8823.2998046875	yahoo	{}
2026-07-16 05:36:27.618508+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:36:27.952621+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:36:28.312718+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:36:28.634918+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:36:29.128012+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:36:29.467548+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:36:29.8299+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:36:30.201606+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:36:30.642988+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:36:31.006211+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:36:31.415199+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:36:31.83629+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:36:32.219872+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:36:32.612329+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:36:33.037467+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:36:33.436877+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:36:33.819301+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:36:34.220279+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:36:34.600418+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:36:34.991663+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:37:43.680387+01	WTI	79.55999755859375	11213	80	80.58999633789062	79.2699966430664	79.55999755859375	yahoo	{}
2026-07-16 05:37:44.020505+01	BRENT	84.79000091552734	2217	85.22000122070312	85.75	84.41000366210938	84.79000091552734	yahoo	{}
2026-07-16 05:37:44.348396+01	NG	2.9100000858306885	2521	2.9210000038146973	2.9240000247955322	2.885999917984009	2.9100000858306885	yahoo	{}
2026-07-16 05:37:47.410765+01	PLATINUM	1677.800048828125	2139	1682.0999755859375	1698	1667	1677.800048828125	yahoo	{}
2026-07-16 05:37:47.760519+01	PALLADIUM	1315.5	335	1322	1323	1306.5	1315.5	yahoo	{}
2026-07-16 05:37:48.100653+01	US100	26269.23046875	7379560000	26261.1796875	26316.810546875	26041.130859375	26269.23046875	yahoo	{}
2026-07-16 05:37:48.426901+01	JP225	66980.78125	0	67900.4296875	68069.8203125	66499.4921875	66980.78125	yahoo	{}
2026-07-16 05:37:48.72341+01	AU200	8822.5	0	8841.099609375	8856.2001953125	8808.099609375	8822.5	yahoo	{}
2026-07-16 05:37:49.096221+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:37:49.468863+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:37:49.839637+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:37:50.171934+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:37:50.498074+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:37:50.832297+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:37:51.188742+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:37:51.546801+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:37:51.94719+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:37:52.377044+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:37:52.756579+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:37:53.217276+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:37:53.583565+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:37:53.966117+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:37:54.356293+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:37:54.724066+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:37:55.123813+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:37:55.512995+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:37:55.914066+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:37:56.33435+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
2026-07-16 05:39:04.893659+01	WTI	79.52999877929688	11224	80	80.58999633789062	79.2699966430664	79.52999877929688	yahoo	{}
2026-07-16 05:39:05.279178+01	BRENT	84.79000091552734	2217	85.22000122070312	85.75	84.41000366210938	84.79000091552734	yahoo	{}
2026-07-16 05:39:05.613883+01	NG	2.9119999408721924	2535	2.9210000038146973	2.9240000247955322	2.885999917984009	2.9119999408721924	yahoo	{}
2026-07-16 05:39:08.555501+01	PLATINUM	1676	2141	1682.0999755859375	1698	1667	1676	yahoo	{}
2026-07-16 05:39:08.854976+01	PALLADIUM	1315.5	335	1322	1323	1306.5	1315.5	yahoo	{}
2026-07-16 05:39:09.169075+01	US100	26269.23046875	7379560000	26261.1796875	26316.810546875	26041.130859375	26269.23046875	yahoo	{}
2026-07-16 05:39:09.576608+01	JP225	66960.5	0	67900.4296875	68069.8203125	66499.4921875	66960.5	yahoo	{}
2026-07-16 05:39:09.914212+01	AU200	8821.7001953125	0	8841.099609375	8856.2001953125	8808.099609375	8821.7001953125	yahoo	{}
2026-07-16 05:39:10.29045+01	AAPL	327.5	60884500	317.6199951171875	328.7300109863281	317.32000732421875	327.5	yahoo	{}
2026-07-16 05:39:10.631262+01	MSFT	395.6300048828125	36199900	387.79998779296875	398.9599914550781	386.3999938964844	395.6300048828125	yahoo	{}
2026-07-16 05:39:10.953697+01	GOOGL	370.9200134277344	28274200	357.9700012207031	373.6499938964844	357.760009765625	370.9200134277344	yahoo	{}
2026-07-16 05:39:11.289523+01	AMZN	254.9600067138672	45166300	249.75	256.4800109863281	249.75	254.9600067138672	yahoo	{}
2026-07-16 05:39:11.6543+01	NVDA	212.5	124482600	211.9600067138672	213.80999755859375	206.0399932861328	212.5	yahoo	{}
2026-07-16 05:39:11.964439+01	META	681.3099975585938	18983100	663.5999755859375	686.0800170898438	656.6599731445312	681.3099975585938	yahoo	{}
2026-07-16 05:39:12.309375+01	TSLA	394.4599914550781	31471800	399.3999938964844	406.5899963378906	390.6600036621094	394.4599914550781	yahoo	{}
2026-07-16 05:39:12.690284+01	JPM	346.9100036621094	10747000	345.8500061035156	351.239990234375	344.04998779296875	346.9100036621094	yahoo	{}
2026-07-16 05:39:13.058821+01	V	355.1400146484375	8849400	354	360.42999267578125	349.1199951171875	355.1400146484375	yahoo	{}
2026-07-16 05:39:13.481997+01	WMT	112.52999877929688	16457200	113.25	114.7300033569336	112.06999969482422	112.52999877929688	yahoo	{}
2026-07-16 05:39:13.901839+01	JNJ	247.02000427246094	10544300	250.08999633789062	256.8299865722656	246.0500030517578	247.02000427246094	yahoo	{}
2026-07-16 05:39:14.305113+01	PG	148.0500030517578	6179000	145.27999877929688	148.58999633789062	144.66000366210938	148.0500030517578	yahoo	{}
2026-07-16 05:39:14.689398+01	UNH	418.5199890136719	6757300	419.489990234375	424.1099853515625	414.3699951171875	418.5199890136719	yahoo	{}
2026-07-16 05:39:15.065796+01	HD	341.44000244140625	3952400	338.989990234375	346.25	337.260009765625	341.44000244140625	yahoo	{}
2026-07-16 05:39:15.478833+01	BAC	61.59000015258789	43357500	61.31999969482422	62.029998779296875	61.11000061035156	61.59000015258789	yahoo	{}
2026-07-16 05:39:15.86436+01	XOM	144.50999450683594	13439400	145.08999633789062	145.08999633789062	142.02999877929688	144.50999450683594	yahoo	{}
2026-07-16 05:39:16.278031+01	CVX	181.60000610351562	6663500	182.1699981689453	182.39999389648438	178.5800018310547	181.60000610351562	yahoo	{}
2026-07-16 05:39:16.670064+01	KO	82.44999694824219	18377500	82.93000030517578	83.23999786376953	82.2300033569336	82.44999694824219	yahoo	{}
2026-07-16 05:39:17.057566+01	PEP	135.39999389648438	8075400	135.08999633789062	136.99000549316406	134.64999389648438	135.39999389648438	yahoo	{}
2026-07-16 05:39:17.452079+01	MCD	264.95001220703125	6046400	268	270.2799987792969	264.0899963378906	264.95001220703125	yahoo	{}
\.


--
-- Name: bgw_job_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_catalog.bgw_job_id_seq', 1000, false);


--
-- Name: chunk_column_stats_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_column_stats_id_seq', 1, false);


--
-- Name: chunk_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_id_seq', 6, true);


--
-- Name: dimension_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_catalog.dimension_id_seq', 7, true);


--
-- Name: dimension_slice_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_catalog.dimension_slice_id_seq', 6, true);


--
-- Name: hypertable_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: postgres
--

SELECT pg_catalog.setval('_timescaledb_catalog.hypertable_id_seq', 7, true);


--
-- Name: _hyper_4_2_chunk 2_economic_events_pkey; Type: CONSTRAINT; Schema: _timescaledb_internal; Owner: postgres
--

ALTER TABLE ONLY _timescaledb_internal._hyper_4_2_chunk
    ADD CONSTRAINT "2_economic_events_pkey" PRIMARY KEY (event_id, release_time_utc);


--
-- Name: _hyper_4_3_chunk 3_economic_events_pkey; Type: CONSTRAINT; Schema: _timescaledb_internal; Owner: postgres
--

ALTER TABLE ONLY _timescaledb_internal._hyper_4_3_chunk
    ADD CONSTRAINT "3_economic_events_pkey" PRIMARY KEY (event_id, release_time_utc);


--
-- Name: _hyper_4_4_chunk 4_economic_events_pkey; Type: CONSTRAINT; Schema: _timescaledb_internal; Owner: postgres
--

ALTER TABLE ONLY _timescaledb_internal._hyper_4_4_chunk
    ADD CONSTRAINT "4_economic_events_pkey" PRIMARY KEY (event_id, release_time_utc);


--
-- Name: _hyper_4_5_chunk 5_economic_events_pkey; Type: CONSTRAINT; Schema: _timescaledb_internal; Owner: postgres
--

ALTER TABLE ONLY _timescaledb_internal._hyper_4_5_chunk
    ADD CONSTRAINT "5_economic_events_pkey" PRIMARY KEY (event_id, release_time_utc);


--
-- Name: _hyper_7_6_chunk 6_macro_events_consensus_pkey; Type: CONSTRAINT; Schema: _timescaledb_internal; Owner: postgres
--

ALTER TABLE ONLY _timescaledb_internal._hyper_7_6_chunk
    ADD CONSTRAINT "6_macro_events_consensus_pkey" PRIMARY KEY (event_id, release_time_utc);


--
-- Name: asset_registry asset_registry_pkey; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_pkey PRIMARY KEY (asset_id);


--
-- Name: asset_registry asset_registry_symbol_key; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_symbol_key UNIQUE (symbol);


--
-- Name: asset_type_registry asset_type_registry_name_key; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_type_registry
    ADD CONSTRAINT asset_type_registry_name_key UNIQUE (name);


--
-- Name: asset_type_registry asset_type_registry_pkey; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_type_registry
    ADD CONSTRAINT asset_type_registry_pkey PRIMARY KEY (asset_type_id);


--
-- Name: company_registry company_registry_pkey; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.company_registry
    ADD CONSTRAINT company_registry_pkey PRIMARY KEY (company_id);


--
-- Name: country_registry country_registry_pkey; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.country_registry
    ADD CONSTRAINT country_registry_pkey PRIMARY KEY (code);


--
-- Name: currency_registry currency_registry_pkey; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.currency_registry
    ADD CONSTRAINT currency_registry_pkey PRIMARY KEY (code);


--
-- Name: exchange_registry exchange_registry_pkey; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.exchange_registry
    ADD CONSTRAINT exchange_registry_pkey PRIMARY KEY (mic_code);


--
-- Name: industry_registry industry_registry_name_key; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.industry_registry
    ADD CONSTRAINT industry_registry_name_key UNIQUE (name);


--
-- Name: industry_registry industry_registry_pkey; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.industry_registry
    ADD CONSTRAINT industry_registry_pkey PRIMARY KEY (industry_id);


--
-- Name: provider_registry provider_registry_name_key; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.provider_registry
    ADD CONSTRAINT provider_registry_name_key UNIQUE (name);


--
-- Name: provider_registry provider_registry_pkey; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.provider_registry
    ADD CONSTRAINT provider_registry_pkey PRIMARY KEY (provider_id);


--
-- Name: quality_registry quality_registry_pkey; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.quality_registry
    ADD CONSTRAINT quality_registry_pkey PRIMARY KEY (quality_id);


--
-- Name: relationship_registry relationship_registry_pkey; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.relationship_registry
    ADD CONSTRAINT relationship_registry_pkey PRIMARY KEY (relationship_id);


--
-- Name: sector_registry sector_registry_name_key; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.sector_registry
    ADD CONSTRAINT sector_registry_name_key UNIQUE (name);


--
-- Name: sector_registry sector_registry_pkey; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.sector_registry
    ADD CONSTRAINT sector_registry_pkey PRIMARY KEY (sector_id);


--
-- Name: version_history version_history_pkey; Type: CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.version_history
    ADD CONSTRAINT version_history_pkey PRIMARY KEY (version_id);


--
-- Name: economic_events economic_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.economic_events
    ADD CONSTRAINT economic_events_pkey PRIMARY KEY (event_id, release_time_utc);


--
-- Name: macro_events_consensus macro_events_consensus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.macro_events_consensus
    ADD CONSTRAINT macro_events_consensus_pkey PRIMARY KEY (event_id, release_time_utc);


--
-- Name: macro_events_raw macro_events_raw_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.macro_events_raw
    ADD CONSTRAINT macro_events_raw_pkey PRIMARY KEY (raw_id);


--
-- Name: _hyper_4_2_chunk_economic_events_release_time_utc_idx; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_2_chunk_economic_events_release_time_utc_idx ON _timescaledb_internal._hyper_4_2_chunk USING btree (release_time_utc DESC);


--
-- Name: _hyper_4_2_chunk_idx_economic_events_category; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_2_chunk_idx_economic_events_category ON _timescaledb_internal._hyper_4_2_chunk USING btree (category);


--
-- Name: _hyper_4_2_chunk_idx_economic_events_country; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_2_chunk_idx_economic_events_country ON _timescaledb_internal._hyper_4_2_chunk USING btree (country);


--
-- Name: _hyper_4_2_chunk_idx_economic_events_importance; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_2_chunk_idx_economic_events_importance ON _timescaledb_internal._hyper_4_2_chunk USING btree (importance);


--
-- Name: _hyper_4_3_chunk_economic_events_release_time_utc_idx; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_3_chunk_economic_events_release_time_utc_idx ON _timescaledb_internal._hyper_4_3_chunk USING btree (release_time_utc DESC);


--
-- Name: _hyper_4_3_chunk_idx_economic_events_category; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_3_chunk_idx_economic_events_category ON _timescaledb_internal._hyper_4_3_chunk USING btree (category);


--
-- Name: _hyper_4_3_chunk_idx_economic_events_country; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_3_chunk_idx_economic_events_country ON _timescaledb_internal._hyper_4_3_chunk USING btree (country);


--
-- Name: _hyper_4_3_chunk_idx_economic_events_importance; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_3_chunk_idx_economic_events_importance ON _timescaledb_internal._hyper_4_3_chunk USING btree (importance);


--
-- Name: _hyper_4_4_chunk_economic_events_release_time_utc_idx; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_4_chunk_economic_events_release_time_utc_idx ON _timescaledb_internal._hyper_4_4_chunk USING btree (release_time_utc DESC);


--
-- Name: _hyper_4_4_chunk_idx_economic_events_category; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_4_chunk_idx_economic_events_category ON _timescaledb_internal._hyper_4_4_chunk USING btree (category);


--
-- Name: _hyper_4_4_chunk_idx_economic_events_country; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_4_chunk_idx_economic_events_country ON _timescaledb_internal._hyper_4_4_chunk USING btree (country);


--
-- Name: _hyper_4_4_chunk_idx_economic_events_importance; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_4_chunk_idx_economic_events_importance ON _timescaledb_internal._hyper_4_4_chunk USING btree (importance);


--
-- Name: _hyper_4_5_chunk_economic_events_release_time_utc_idx; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_5_chunk_economic_events_release_time_utc_idx ON _timescaledb_internal._hyper_4_5_chunk USING btree (release_time_utc DESC);


--
-- Name: _hyper_4_5_chunk_idx_economic_events_category; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_5_chunk_idx_economic_events_category ON _timescaledb_internal._hyper_4_5_chunk USING btree (category);


--
-- Name: _hyper_4_5_chunk_idx_economic_events_country; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_5_chunk_idx_economic_events_country ON _timescaledb_internal._hyper_4_5_chunk USING btree (country);


--
-- Name: _hyper_4_5_chunk_idx_economic_events_importance; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_4_5_chunk_idx_economic_events_importance ON _timescaledb_internal._hyper_4_5_chunk USING btree (importance);


--
-- Name: _hyper_7_6_chunk_idx_macro_consensus_category; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_7_6_chunk_idx_macro_consensus_category ON _timescaledb_internal._hyper_7_6_chunk USING btree (category);


--
-- Name: _hyper_7_6_chunk_idx_macro_consensus_country; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_7_6_chunk_idx_macro_consensus_country ON _timescaledb_internal._hyper_7_6_chunk USING btree (country);


--
-- Name: _hyper_7_6_chunk_macro_events_consensus_release_time_utc_idx; Type: INDEX; Schema: _timescaledb_internal; Owner: postgres
--

CREATE INDEX _hyper_7_6_chunk_macro_events_consensus_release_time_utc_idx ON _timescaledb_internal._hyper_7_6_chunk USING btree (release_time_utc DESC);


--
-- Name: idx_asset_class; Type: INDEX; Schema: metadata; Owner: postgres
--

CREATE INDEX idx_asset_class ON metadata.asset_registry USING btree (asset_class);


--
-- Name: idx_asset_currency; Type: INDEX; Schema: metadata; Owner: postgres
--

CREATE INDEX idx_asset_currency ON metadata.asset_registry USING btree (base_currency);


--
-- Name: idx_asset_exchange; Type: INDEX; Schema: metadata; Owner: postgres
--

CREATE INDEX idx_asset_exchange ON metadata.asset_registry USING btree (exchange_code);


--
-- Name: idx_asset_symbol; Type: INDEX; Schema: metadata; Owner: postgres
--

CREATE INDEX idx_asset_symbol ON metadata.asset_registry USING btree (symbol);


--
-- Name: idx_quality_asset; Type: INDEX; Schema: metadata; Owner: postgres
--

CREATE INDEX idx_quality_asset ON metadata.quality_registry USING btree (asset_id);


--
-- Name: idx_relationship_source; Type: INDEX; Schema: metadata; Owner: postgres
--

CREATE INDEX idx_relationship_source ON metadata.relationship_registry USING btree (source_asset_id);


--
-- Name: idx_relationship_target; Type: INDEX; Schema: metadata; Owner: postgres
--

CREATE INDEX idx_relationship_target ON metadata.relationship_registry USING btree (target_asset_id);


--
-- Name: idx_version_asset; Type: INDEX; Schema: metadata; Owner: postgres
--

CREATE INDEX idx_version_asset ON metadata.version_history USING btree (asset_id);


--
-- Name: economic_events_release_time_utc_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX economic_events_release_time_utc_idx ON public.economic_events USING btree (release_time_utc DESC);


--
-- Name: idx_economic_events_category; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_economic_events_category ON public.economic_events USING btree (category);


--
-- Name: idx_economic_events_country; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_economic_events_country ON public.economic_events USING btree (country);


--
-- Name: idx_economic_events_importance; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_economic_events_importance ON public.economic_events USING btree (importance);


--
-- Name: idx_economic_events_release_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_economic_events_release_time ON public.economic_events USING btree (release_time_utc DESC);


--
-- Name: idx_institutional_positions_symbol; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_institutional_positions_symbol ON public.institutional_positions USING btree (symbol, "time" DESC);


--
-- Name: idx_macro_consensus_category; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_macro_consensus_category ON public.macro_events_consensus USING btree (category);


--
-- Name: idx_macro_consensus_country; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_macro_consensus_country ON public.macro_events_consensus USING btree (country);


--
-- Name: idx_macro_consensus_release; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_macro_consensus_release ON public.macro_events_consensus USING btree (release_time_utc DESC);


--
-- Name: idx_market_prices_symbol; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_market_prices_symbol ON public.market_prices USING btree (symbol, "time" DESC);


--
-- Name: idx_price_commodities_symbol_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_price_commodities_symbol_time ON public.price_commodities USING btree (symbol, "time" DESC);


--
-- Name: idx_price_crypto_symbol_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_price_crypto_symbol_time ON public.price_crypto USING btree (symbol, "time" DESC);


--
-- Name: idx_price_forex_symbol_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_price_forex_symbol_time ON public.price_forex USING btree (symbol, "time" DESC);


--
-- Name: idx_price_indices_symbol_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_price_indices_symbol_time ON public.price_indices USING btree (symbol, "time" DESC);


--
-- Name: idx_price_stocks_symbol_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_price_stocks_symbol_time ON public.price_stocks USING btree (symbol, "time" DESC);


--
-- Name: macro_events_consensus_release_time_utc_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX macro_events_consensus_release_time_utc_idx ON public.macro_events_consensus USING btree (release_time_utc DESC);


--
-- Name: asset_registry asset_registry_asset_type_id_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_asset_type_id_fkey FOREIGN KEY (asset_type_id) REFERENCES metadata.asset_type_registry(asset_type_id);


--
-- Name: asset_registry asset_registry_base_currency_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_base_currency_fkey FOREIGN KEY (base_currency) REFERENCES metadata.currency_registry(code);


--
-- Name: asset_registry asset_registry_company_id_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_company_id_fkey FOREIGN KEY (company_id) REFERENCES metadata.company_registry(company_id);


--
-- Name: asset_registry asset_registry_country_code_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_country_code_fkey FOREIGN KEY (country_code) REFERENCES metadata.country_registry(code);


--
-- Name: asset_registry asset_registry_exchange_code_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_exchange_code_fkey FOREIGN KEY (exchange_code) REFERENCES metadata.exchange_registry(mic_code);


--
-- Name: asset_registry asset_registry_industry_id_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_industry_id_fkey FOREIGN KEY (industry_id) REFERENCES metadata.industry_registry(industry_id);


--
-- Name: asset_registry asset_registry_margin_currency_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_margin_currency_fkey FOREIGN KEY (margin_currency) REFERENCES metadata.currency_registry(code);


--
-- Name: asset_registry asset_registry_profit_currency_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_profit_currency_fkey FOREIGN KEY (profit_currency) REFERENCES metadata.currency_registry(code);


--
-- Name: asset_registry asset_registry_quote_currency_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_quote_currency_fkey FOREIGN KEY (quote_currency) REFERENCES metadata.currency_registry(code);


--
-- Name: asset_registry asset_registry_sector_id_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_sector_id_fkey FOREIGN KEY (sector_id) REFERENCES metadata.sector_registry(sector_id);


--
-- Name: asset_registry asset_registry_settlement_currency_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_settlement_currency_fkey FOREIGN KEY (settlement_currency) REFERENCES metadata.currency_registry(code);


--
-- Name: asset_registry asset_registry_underlying_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.asset_registry
    ADD CONSTRAINT asset_registry_underlying_fkey FOREIGN KEY (underlying) REFERENCES metadata.asset_registry(asset_id);


--
-- Name: industry_registry industry_registry_sector_id_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.industry_registry
    ADD CONSTRAINT industry_registry_sector_id_fkey FOREIGN KEY (sector_id) REFERENCES metadata.sector_registry(sector_id);


--
-- Name: quality_registry quality_registry_asset_id_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.quality_registry
    ADD CONSTRAINT quality_registry_asset_id_fkey FOREIGN KEY (asset_id) REFERENCES metadata.asset_registry(asset_id);


--
-- Name: quality_registry quality_registry_provider_id_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.quality_registry
    ADD CONSTRAINT quality_registry_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES metadata.provider_registry(provider_id);


--
-- Name: relationship_registry relationship_registry_source_asset_id_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.relationship_registry
    ADD CONSTRAINT relationship_registry_source_asset_id_fkey FOREIGN KEY (source_asset_id) REFERENCES metadata.asset_registry(asset_id);


--
-- Name: relationship_registry relationship_registry_target_asset_id_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.relationship_registry
    ADD CONSTRAINT relationship_registry_target_asset_id_fkey FOREIGN KEY (target_asset_id) REFERENCES metadata.asset_registry(asset_id);


--
-- Name: version_history version_history_asset_id_fkey; Type: FK CONSTRAINT; Schema: metadata; Owner: postgres
--

ALTER TABLE ONLY metadata.version_history
    ADD CONSTRAINT version_history_asset_id_fkey FOREIGN KEY (asset_id) REFERENCES metadata.asset_registry(asset_id);


--
-- PostgreSQL database dump complete
--

\unrestrict cYmORzXOjuJ8m8Zc8kElyh0dfa8nmufJI1uPTmULjj3w4fOQ6zL58QJKFEZ9eIn
