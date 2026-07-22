# Data Intelligence Layer

## Overview

The Data Intelligence Layer is the foundation of Nexus AI Terminal. It handles all data acquisition, normalization, storage, and distribution.

## Components

### 1. NDIP (Normalized Data Intelligence Protocol)

The NDIP is the communication layer between intelligence domains. It prevents engines from directly depending on each other's internal implementation.

**Location:** `./ndip/`

**Purpose:**
- Loose coupling between engines
- Clear communication boundaries
- Easier testing and replacement of engines
- Better observability
- Reduced circular dependencies

**Flow:**

### 2. Data Acquisition

Each engine has its own acquisition layer for fetching raw data.

**Location:** `*/acquisition/`

**Engines with Acquisition:**
- Central Bank Engine
- Corporate Earnings Engine
- Economic Events Engine
- Financial News Engine
- Institutional Positioning Engine
- Macroeconomic Events Engine
- Macroeconomic Statistics Engine
- Market Price Engine

### 3. Data Normalization

Raw data is normalized into a consistent format.

**Location:** `*/normalization/` or `*/normalizers/`

**Process:**
- Validation
- Cleaning
- Symbol mapping
- Time alignment
- Missing data handling

### 4. Data Warehouse

All raw and processed data is stored in the warehouse.

**Location:** `*/warehouse/`

**Storage:**
- TimescaleDB: Time-series data
- SQLite: Structured data
- Redis: In-memory cache

### 5. Data Providers

External data sources are accessed through providers.

**Location:** `*/providers/`

**Sources:**
- Yahoo Finance
- Alpha Vantage
- ExchangeRate.host
- COT Reports
- Macro APIs
- Central Banks
- News Feeds

## Data Flow


## Engine Acquisition/Normalization/Warehouse Structure

| Engine | Acquisition | Normalization | Warehouse |
|--------|-------------|---------------|-----------|
| Central Bank | ✅ | ✅ | ✅ |
| Corporate Earnings | ✅ | ✅ | ✅ |
| Economic Events | ✅ | ✅ | ✅ |
| Financial News | ✅ | ✅ | ✅ |
| Institutional Positioning | ✅ | ✅ | ✅ |
| Macroeconomic Events | ✅ | ✅ | ✅ |
| Macroeconomic Statistics | ✅ | ✅ | ✅ |
| Market Price | ✅ | ✅ | ✅ |

## Status


## Engine Acquisition/Normalization/Warehouse Structure

| Engine | Acquisition | Normalization | Warehouse |
|--------|-------------|---------------|-----------|
| Central Bank | ✅ | ✅ | ✅ |
| Corporate Earnings | ✅ | ✅ | ✅ |
| Economic Events | ✅ | ✅ | ✅ |
| Financial News | ✅ | ✅ | ✅ |
| Institutional Positioning | ✅ | ✅ | ✅ |
| Macroeconomic Events | ✅ | ✅ | ✅ |
| Macroeconomic Statistics | ✅ | ✅ | ✅ |
| Market Price | ✅ | ✅ | ✅ |

## Status
