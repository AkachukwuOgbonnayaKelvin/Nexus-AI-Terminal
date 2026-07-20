#!/bin/bash
# Backup large data files to local backup directory

BACKUP_DIR=~/backups/nexus_data_$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

echo "Backing up MKT-001 data..."
cp -r market_price_engine/data $BACKUP_DIR/market_price_data

echo "Backup complete: $BACKUP_DIR"
echo "Data size: $(du -sh $BACKUP_DIR)"
