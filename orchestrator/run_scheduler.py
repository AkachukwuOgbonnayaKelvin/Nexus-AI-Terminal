#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the Central Scheduler"""

import sys
import os
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.scheduler.core import CentralScheduler
from orchestrator.registry.engine_registry import register_all_engines


def main():
    """Main entry point"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Central Scheduler...")
    
    # Create scheduler
    scheduler = CentralScheduler()
    
    # Register all engines
    register_all_engines(scheduler)
    
    # Run once
    logger.info("Running scheduler cycle...")
    results = scheduler.run_once()
    
    logger.info("Scheduler cycle complete:")
    for run in results["runs"]:
        logger.info(f"  {run['dataset_id']}: {run['status']}")
    
    return results


if __name__ == "__main__":
    main()
