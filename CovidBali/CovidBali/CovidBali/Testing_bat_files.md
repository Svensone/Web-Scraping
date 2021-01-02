@Echo Off
REM activate Python venv
CALL "C:\ProgramData\Anaconda3\Scripts\activate.bat"
CD "C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\CovidBali\CovidBali\spiders\"
CALL "C:\ProgramData\Anaconda3\python.exe" "C:\ProgramData\Anaconda3\Lib\site-packages\scrapy\cmdline.py" runspider dailyNewBaliCases.py -o dailyCases.json -t json
pause