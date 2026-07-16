--
-- PostgreSQL database dump
--

\restrict yKVoTZ61iJD6yMLeYF4guLHz8zWecLtroWdPxPQBJo5TME63UUEQ6G1PmhfJwvb

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
-- Name: metadata; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA metadata;


ALTER SCHEMA metadata OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

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

\unrestrict yKVoTZ61iJD6yMLeYF4guLHz8zWecLtroWdPxPQBJo5TME63UUEQ6G1PmhfJwvb
