@REM @Echo Off
@REM REM activate Python venv
@REM CALL "C:\ProgramData\Anaconda3\Scripts\activate"
@REM CD "C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\CovidBali\CovidBali\spiders\"
@REM CALL "C:\ProgramData\Anaconda3\python.exe" "C:\ProgramData\Anaconda3\Lib\site-packages\scrapy\cmdline.py" runspider dailyNewBaliCases.py -o dailyCases.json -t json
@REM pause

@REM https://stackoverflow.com/questions/34622514/run-a-python-script-in-virtual-environment-from-windows-task-scheduler
@REM C:\ProgramData\Anaconda3\envs\scrapy\python.exe C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\CovidBali\CovidBali\spiders\dailyNewBaliCases.py

@REM cmd "/c activate scrapy && python dailyNewBaliCases.py && deactivate"
@REM pause

C:\ProgramData\Anaconda3\envs\scrapy\python.exe && python C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\CovidBali\CovidBali\spiders\dailyNewBaliCases.py