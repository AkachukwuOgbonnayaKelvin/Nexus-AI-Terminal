--
-- PostgreSQL database dump
--

\restrict 0xcDMlVLWKBIyqKtlxVSE8obrzoMNKoEZgQrj0uWpHRiiagKJDosbe1tuDQsfvs

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
-- Name: central_bank_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.central_bank_events (
    event_id text NOT NULL,
    provider text,
    bank text,
    country text,
    currency text,
    event_type text,
    title text,
    summary text,
    statement text,
    release_time timestamp with time zone,
    meeting_date timestamp with time zone,
    effective_date timestamp with time zone,
    old_rate double precision,
    new_rate double precision,
    rate_change double precision,
    vote_split text,
    governor text,
    importance text,
    policy_bias text,
    hawkish_dovish_score double precision,
    communication_type text,
    source_url text,
    attachments text[],
    document_hash text,
    confidence double precision,
    metadata jsonb,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.central_bank_events OWNER TO postgres;

--
-- Name: cot_changes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cot_changes (
    report_id text NOT NULL,
    market_code text NOT NULL,
    participant_type text NOT NULL,
    long_change integer,
    short_change integer,
    spreading_change integer,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.cot_changes OWNER TO postgres;

--
-- Name: cot_import_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cot_import_log (
    log_id integer NOT NULL,
    run_date timestamp with time zone DEFAULT now(),
    report_date date,
    markets_processed integer,
    records_inserted integer,
    errors integer,
    status text
);


ALTER TABLE public.cot_import_log OWNER TO postgres;

--
-- Name: cot_import_log_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cot_import_log_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cot_import_log_log_id_seq OWNER TO postgres;

--
-- Name: cot_import_log_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cot_import_log_log_id_seq OWNED BY public.cot_import_log.log_id;


--
-- Name: cot_market_registry; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cot_market_registry (
    market_code text NOT NULL,
    market_name text,
    exchange text,
    asset_class text,
    currency text,
    contract_size integer,
    tick_size numeric,
    first_seen date,
    last_seen date,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.cot_market_registry OWNER TO postgres;

--
-- Name: cot_markets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cot_markets (
    market_code text NOT NULL,
    market_name text,
    asset_class text,
    currency text,
    exchange text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.cot_markets OWNER TO postgres;

--
-- Name: cot_positions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cot_positions (
    report_id text NOT NULL,
    market_code text NOT NULL,
    participant_type text NOT NULL,
    long_positions integer,
    short_positions integer,
    spreading_positions integer,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.cot_positions OWNER TO postgres;

--
-- Name: cot_provider_health; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cot_provider_health (
    provider text NOT NULL,
    status text,
    last_sync timestamp with time zone,
    records integer,
    latency_ms integer,
    error_message text,
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.cot_provider_health OWNER TO postgres;

--
-- Name: cot_reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cot_reports (
    report_id text NOT NULL,
    provider text,
    report_date timestamp with time zone,
    market_code text NOT NULL,
    open_interest integer,
    confidence double precision,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.cot_reports OWNER TO postgres;

--
-- Name: cot_statistics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cot_statistics (
    stat_id integer NOT NULL,
    market_code text,
    report_date date,
    total_reports integer,
    avg_open_interest integer,
    max_open_interest integer,
    min_open_interest integer,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.cot_statistics OWNER TO postgres;

--
-- Name: cot_statistics_stat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cot_statistics_stat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cot_statistics_stat_id_seq OWNER TO postgres;

--
-- Name: cot_statistics_stat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cot_statistics_stat_id_seq OWNED BY public.cot_statistics.stat_id;


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
-- Name: news_articles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.news_articles (
    article_id text NOT NULL,
    provider text,
    provider_article_id text,
    headline text,
    summary text,
    body text,
    url text,
    author text,
    country text,
    region text,
    language text,
    published_at timestamp with time zone,
    updated_at timestamp with time zone,
    category text,
    subcategory text,
    importance text,
    tags text[],
    confidence double precision,
    metadata jsonb,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.news_articles OWNER TO postgres;

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
-- Name: cot_import_log log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_import_log ALTER COLUMN log_id SET DEFAULT nextval('public.cot_import_log_log_id_seq'::regclass);


--
-- Name: cot_statistics stat_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_statistics ALTER COLUMN stat_id SET DEFAULT nextval('public.cot_statistics_stat_id_seq'::regclass);


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
-- Name: central_bank_events central_bank_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.central_bank_events
    ADD CONSTRAINT central_bank_events_pkey PRIMARY KEY (event_id);


--
-- Name: cot_changes cot_changes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_changes
    ADD CONSTRAINT cot_changes_pkey PRIMARY KEY (report_id, market_code, participant_type);


--
-- Name: cot_import_log cot_import_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_import_log
    ADD CONSTRAINT cot_import_log_pkey PRIMARY KEY (log_id);


--
-- Name: cot_market_registry cot_market_registry_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_market_registry
    ADD CONSTRAINT cot_market_registry_pkey PRIMARY KEY (market_code);


--
-- Name: cot_markets cot_markets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_markets
    ADD CONSTRAINT cot_markets_pkey PRIMARY KEY (market_code);


--
-- Name: cot_positions cot_positions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_positions
    ADD CONSTRAINT cot_positions_pkey PRIMARY KEY (report_id, market_code, participant_type);


--
-- Name: cot_provider_health cot_provider_health_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_provider_health
    ADD CONSTRAINT cot_provider_health_pkey PRIMARY KEY (provider);


--
-- Name: cot_reports cot_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_reports
    ADD CONSTRAINT cot_reports_pkey PRIMARY KEY (report_id, market_code);


--
-- Name: cot_statistics cot_statistics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_statistics
    ADD CONSTRAINT cot_statistics_pkey PRIMARY KEY (stat_id);


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
-- Name: news_articles news_articles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_articles
    ADD CONSTRAINT news_articles_pkey PRIMARY KEY (article_id);


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
-- Name: idx_cot_changes_market; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cot_changes_market ON public.cot_changes USING btree (market_code);


--
-- Name: idx_cot_market_registry_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cot_market_registry_active ON public.cot_market_registry USING btree (is_active);


--
-- Name: idx_cot_market_registry_class; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cot_market_registry_class ON public.cot_market_registry USING btree (asset_class);


--
-- Name: idx_cot_positions_market; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cot_positions_market ON public.cot_positions USING btree (market_code);


--
-- Name: idx_cot_positions_report; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cot_positions_report ON public.cot_positions USING btree (report_id);


--
-- Name: idx_cot_positions_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cot_positions_type ON public.cot_positions USING btree (participant_type);


--
-- Name: idx_cot_reports_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cot_reports_date ON public.cot_reports USING btree (report_date DESC);


--
-- Name: idx_cot_reports_market; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cot_reports_market ON public.cot_reports USING btree (market_code);


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
-- Name: idx_news_category; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_news_category ON public.news_articles USING btree (category);


--
-- Name: idx_news_importance; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_news_importance ON public.news_articles USING btree (importance);


--
-- Name: idx_news_published; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_news_published ON public.news_articles USING btree (published_at DESC);


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
-- Name: cot_changes cot_changes_market_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_changes
    ADD CONSTRAINT cot_changes_market_code_fkey FOREIGN KEY (market_code) REFERENCES public.cot_markets(market_code);


--
-- Name: cot_positions cot_positions_market_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_positions
    ADD CONSTRAINT cot_positions_market_code_fkey FOREIGN KEY (market_code) REFERENCES public.cot_markets(market_code);


--
-- Name: cot_reports cot_reports_market_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_reports
    ADD CONSTRAINT cot_reports_market_code_fkey FOREIGN KEY (market_code) REFERENCES public.cot_markets(market_code);


--
-- Name: cot_statistics cot_statistics_market_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_statistics
    ADD CONSTRAINT cot_statistics_market_code_fkey FOREIGN KEY (market_code) REFERENCES public.cot_market_registry(market_code);


--
-- PostgreSQL database dump complete
--

\unrestrict 0xcDMlVLWKBIyqKtlxVSE8obrzoMNKoEZgQrj0uWpHRiiagKJDosbe1tuDQsfvs

