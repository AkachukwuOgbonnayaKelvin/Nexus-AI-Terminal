# Nexus AI Terminal Architecture

## Overview

Nexus AI Terminal is built as a **bottom-up, layered architecture** where each layer depends only on the layers below it.

## Architecture Layers


## Documentation Sections

- [Development Roadmap](ROADMAP.md)
- [Universal Standards](../standards/)
- [API Reference](../api/)

## Key Principles

1. **One source of truth** for every piece of data
2. **NDIP is the only gateway** for external data
3. **Workspaces are self-contained** and independently testable
4. **All intelligence flows** through Hub → Publish Cache → Master Orchestrator
5. **The Dashboard visualizes intelligence**; it does not generate it
