@echo off
cd /d %~dp0..
python main.py >> logs\etl_latest.log 2>&1
