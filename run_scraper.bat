@echo off
cd C:\Users\sw\Downloads\job_finder
echo Running scraper at %date% %time% >> scraper_log.txt
C:\Users\sw\miniconda3\python.exe scraper.py >> scraper_log.txt 2>&1
echo Finished at %date% %time% >> scraper_log.txt
pause