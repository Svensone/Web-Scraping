
# Covid Data Project

## Goal:

- create web app with daily numbers and choropleth Bali
- scrape data with scrapy / BeautifulSoup
- use Dash
- help Jackie in Facebook Group 'Bali Covid 19 update'

## Notes Miscs:

2020-12-09:
- scrapy crawl 'name of spider' -o 'filename' -t json for appending

2020-11-27: Struggling with Git
- need Extensions for geojson, ipykernel not working from VS Code - update conda 4.9 no permission from integrated terminal - use conda command admin rights
- choropleth plotly geojson tricky

2020.11.16: Beginning


# Visualization:

1. Matplotlib and Geopandas
2. Plotly
3. Dash Web App

integrate Dash ?
- https://dash.plotly.com/

Choropleth plotly express not working in dash. test in colab ?
running px.Choropleth in VS Code as .ipynb super slow and runtime error / timeout
    - maybe colab ?


# Data Scources

https://pendataan.baliprov.go.id/map_covid19/search?_token=4oZ4S1KfWBPVipGwcwmoEZKkifzDHR2RuNYUOudC&level=kabupaten&kabupaten=&tanggal=2020-11-12

- good since able to choose dates (how to spider crawl all dates ?)

https://pendataan.baliprov.go.id/

- best with tables "https://infocorona.baliprov.go.id/",
