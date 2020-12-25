@Echo Off
REM activate Python venv
CALL "C:\ProgramData\Anaconda3\envs\scrapy\Scripts\activate.bat"
CD "C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\CovidBali\CovidBali\spiders\"
CALL "C:\ProgramData\Anaconda3\python.exe" "C:\ProgramData\Anaconda3\Lib\site-packages\scrapy\cmdline.py" crawl dailyNewBaliCases.py -o dailyCases.json -t json
deactivate

