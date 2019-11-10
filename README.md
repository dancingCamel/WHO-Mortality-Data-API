# WHO Mortality Data API

An API to allow easier querying of the World Health Organization's Mortality Data.

Data drawn from the WHO ICD-10 (parts 1 and 2) raw data file (Downloaded from https://www.who.int/healthinfo/statistics/mortality_rawdata/en/, November 2019). 

This API returns in JSON format.

## Data available
The following datasets are available for searching:
- Country list and country codes
- Country populations
- ICD-10 codes *not implemented*
- Mortality (cause of death) numbers *not implemented*

## Endpoints
The following endpoints are available (grouped by section):

### Country

#### List all countries:
Return all country names and associated codes used in WHO Mortality database.
``` GET /api/country-all```

#### Find Country Code of Specific Country:
Return the name and code of a country (case insensitive). 
``` GET /api/country/<country_name>```

e.g. 
``` GET /api/country/djibouti```

> {
>     "id": 14,
>     "code": "1120",
>     "name": "Djibouti"
> }

#### Search for Countries:
Return all countries with names that contain a search term <br>
``` GET /api/country-search/<search_term>```

e.g.
``` GET /api/country-search/ka'```

>{
>    "id": 145,
>    "code": "3365",
>    "name": "Sri Lanka"
>},
>{
>    "id": 178,
>   "code": "4182",
>    "name": "Kazakhstan"
>}

### ICD-10 Codes (including condensed form)






### Population
Note: Population and live births are both in units. Population figures are mid-year populations as stated by member countries. 

All terms used in the population API queries should be in terms of WHO codes which can be found using other endpoints in this API

### Get All Population Data
Get a dictionary of all available population data
``` GET /api/population-all```

#### Find Multiple Population Entries Using Custom Query:
Get raw population data for given country, year, sex, admin or subdiv (or any combination thereof).
Multiple responses allowed. 

``` GET /population/query?country=<country>&year=<year>&sex=<sex>&admin=<admin>&subdiv=<subdiv>```

e.g. 
Return population data for males and females in the United Kingdom in 1989:
``` GET /population?country=4308&year=1989```

#### Find Single Population Entry Using Custom Query:
Get raw population data for given country, year, sex, admin or subdiv (or any combination thereof).
Returns data if only one population entry matches the query

``` GET /population/query?country=<country>&year=<year>&sex=<sex>&admin=<admin>&subdiv=<subdiv>```

e.g. 
Return population data for only males in the United Kingdom in 1989:
``` GET /population?country=4308&year=1989&sex=1```

### Mortality Data


Disclaimer: Every attempt has been made to keep data true to the original raw data files but veracity cannot be guaranteed. If this is important, download the data directly or use one of the WHO's data querying services (https://www.who.int/healthinfo/mortality_data/en/)
All analyses, interpretations or conclusions drawn from this API or found on this website are credited to the authors, not the WHO (which is responsible only for the provision of the original information).
For more information visit https://www.who.int/healthinfo/statistics/mortality_rawdata/en/