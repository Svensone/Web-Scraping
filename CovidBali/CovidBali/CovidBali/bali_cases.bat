
@REM --- Option1 -Not working if directly invoked ' missing http.request module'
@REM -------------------------------------------------------
@REM https://stackoverflow.com/questions/55007574/schedule-scrapy-spider-via-batch-with-win10-task-scheduler
@REM @Echo Off
@REM @REM activate Python venv
@REM CALL "C:\ProgramData\Anaconda3\Scripts\activate.bat"
@REM CD "C:\Users\ansve\Coding\Projects-WebScraping\CovidBali\CovidBali\CovidBali\spiders\"
@REM CALL "C:\ProgramData\Anaconda3\python.exe" "C:\ProgramData\Anaconda3\Lib\site-packages\scrapy\cmdline.py" runspider dailyNewBaliCases.py -o out3.csv
@REM pause
@REM deactivate


@REM --- Working if invoked directly / not in Task Scheduler
@REM -------------------------------------------------------
@REM How to run a Python script in a given conda environment from a batch file.

@REM @REM It doesn't require:
@REM @REM - conda to be in the PATH
@REM @REM - cmd.exe to be initialized with conda init

@REM Define here the path to your conda installation
set CONDAPATH=C:\ProgramData\Anaconda3
@REM rem Define here the name of the environment
set ENVNAME=scrapy

@REM rem The following command activates the base environment.
@REM rem call C:\ProgramData\Miniconda3\Scripts\activate.bat C:\ProgramData\Miniconda3
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)

@REM rem Activate the conda environment
@REM rem Using call is required here, see: https://stackoverflow.com/questions/24678144/conda-environments-and-bat-files
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%

@REM rem Run a python script in that environment
scrapy crawl bali

@REM rem Deactivate the environment
call conda deactivate
