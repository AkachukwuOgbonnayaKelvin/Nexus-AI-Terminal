--
-- PostgreSQL database dump
--

\restrict VHBAsLWOV5s2hoiabCFksdoaG79m1Q2r7DZi3fgCZgDhvDkI9o27fsMozg8k4Sv

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: economic_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.economic_events (
    "time" timestamp with time zone NOT NULL,
    event text NOT NULL,
    country text,
    actual double precision,
    forecast double precision,
    previous double precision,
    source text,
    asset_class text,
    metadata jsonb
);


ALTER TABLE public.economic_events OWNER TO postgres;

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
-- Name: idx_economic_events_event; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_economic_events_event ON public.economic_events USING btree (event, "time" DESC);


--
-- Name: idx_institutional_positions_symbol; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_institutional_positions_symbol ON public.institutional_positions USING btree (symbol, "time" DESC);


--
-- Name: idx_market_prices_symbol; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_market_prices_symbol ON public.market_prices USING btree (symbol, "time" DESC);


--
-- PostgreSQL database dump complete
--

\unrestrict VHBAsLWOV5s2hoiabCFksdoaG79m1Q2r7DZi3fgCZgDhvDkI9o27fsMozg8k4Sv
