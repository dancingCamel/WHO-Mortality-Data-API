# WHO Mortality Data API

An API to allow easier querying of the World Health Organization's Mortality Data.

Data drawn from the WHO ICD-10 (parts 1 and 2) raw data file (Downloaded from https://www.who.int/healthinfo/statistics/mortality_rawdata/en/, November 2019). 

This API returns in JSON format.

## Data available
The following datasets are available:
- WHO Country codes
- WHO Sex codes and their meanings
- WHO 'Admin' codes and their meanings
- WHO 'Subdiv' codes and their meanings
- WHO Age format codes and their meanings
- WHO Infant age format codes and their meanings
- Country populations (from 1950)
- ICD-10 codes *not implemented*
- Mortality (cause of death) statistics *not implemented*
- Mortality (cause of death) statistics adjusted for population


## Endpoints
The following endpoints are available (grouped by section):

### Countries and Country Codes

#### List all countries:
Return all country names and associated codes used in WHO Mortality database.<br>
``` GET /api/country-list```

#### Find Country Code of Specific Country:
Return the name and code of a country (case insensitive). <br>
``` GET /api/country/<country_name>```

e.g. 
``` GET /api/country/djibouti```

> {<br>
>     "id": 14,<br>
>     "code": "1120",<br>
>     "name": "Djibouti"<br>
> }<br>

#### Search for Countries:
Return all countries with names that contain a search term <br>
``` GET /api/country-search/<search_term>```

e.g.
``` GET /api/country-search/ka'```

>{<br>
>    "id": 145,<br>
>    "code": "3365",<br>
>    "name": "Sri Lanka"<br>
>},<br>
>{<br>
>    "id": 178,<br>
>   "code": "4182",<br>
>    "name": "Kazakhstan"<br>
>}<br>

### WHO Sex Codes
Endpoints related to the 'Sex' section of the Mortality Database

#### List All Sex Codes
Return all sex codes used in the Mortality Database<br>
```GET /api/sex-list```

#### Find Sex Code for Specific Sex
Return the code for a know sex<br>
```GET /api/sex/<sex_name>```

e.g.
```GET /api/sex/female```
>{<br>
>    "name": "female",<br>
>    "code": "2"<br>
>}<br>


### WHO 'Admin' Codes
Endpoints related to the 'Admin' section of the Mortality Database

#### List All Admin Codes
Return all admin codes and descriptions used in WHO Mortality database.<br>
``` GET /api/admin-list```

#### Find Description of Specific Admin Code for Specific Country
Return the description of a specific admin code for a specific country.<br>
```GET /api/admin/<admin_code>/<country_code>```

e.g.  
```GET /api/admin/901/3150```
>{<br>
>    "admin": "901",<br>
>    "country": {<br>
>        "code": "3150",<br>
>        "name": "Israel"<br>
>    },<br>
>    "description": "Jewish Population"<br>
>}<br>


### WHO 'Subdiv' Codes 
Endpoints related to the 'Subdiv' section of the Mortality Database

#### List All Subdiv Codes
Return all subdiv codes and descriptions used in WHO Mortality database.<br>
``` GET /api/subdiv-list```

#### Find Description of Specific Subdiv Code 
Return the description of a specific subdiv code.<br>
```GET /api/subdiv/<subdiv_code>```

e.g. 
```GET /api/subdiv/A35```
>{<br>
>    "code": "A35",<br>
>    "description": "Selected Urban and Rural Areas"<br>
>}<br>

### WHO Age Formats
Endpoints related to the 'Age format' section of the Mortality Database

#### List All Age Format Codes
Return all age format codes and their year cut-off boundaries used in WHO Mortality database.<br>
``` GET /api/age-format-list```

#### Find Age Cut-Off Boundaries for Specific Age Format Code 
Return the description of a specific age format code.<br>
```GET /api/age-format/<age_format_code>```

e.g. 
```GET /api/age-format/08```
{<br>
>    "age_format_code": "08",<br>
>    "pop2": "0",<br>
>    "pop3": "1-4",<br>
>    "pop4": "empty4",<br>
>    "pop5": "empty5",<br>
>    "pop6": "empty6",<br>
>    "pop7": "5-14",<br>
>    "pop8": "empty8",<br>
>    "pop9": "15-24",<br>
>    "pop10": "empty10",<br>
>    "pop11": "25-34",<br>
>    "pop12": "empty12",<br>
>    "pop13": "35-44",<br>
>    "pop14": "empty14",<br>
>    "pop15": "45-54",<br>
>    "pop16": "empty16",<br>
>    "pop17": "55-64",<br>
>    "pop18": "empty18",<br>
>    "pop19": "65+",<br>
>    "pop20": "empty20",<br>
>    "pop21": "empty21",<br>
>    "pop22": "empty22",<br>
>    "pop23": "empty23",<br>
>    "pop24": "empty24",<br>
>    "pop25": "empty25",<br>
>    "pop26": "Unknown"<br>
>}<br>

### WHO Infant Age Formats
Endpoints related to the 'Infant Mortality' section of the Mortality Database

#### List All Infant Mortality Format Codes
Return all infant age format codes and their day cut-off boundaries used in WHO Mortality database.<br>
``` GET /api/infant-age-format-list```

#### Find Age Cut-Off Boundaries for Specific Infant Age Format Code 
Return the description of a specific infant mortality age format code.<br>
```GET /api/-infant-age-format/<infant_age_format_code>```

e.g. 
```GET /api/infant-age-format/01```

>{<br>
>    "infant_age_format_code": "01",<br>
>    "infant_age1": "0 days",<br>
>    "infant_age2": "1-6 days",<br>
>    "infant_age3": "7-27 days",<br>
>    "infant_age4": "28-365 days"<br>
>}<br>

### Population
Note: Population and live births are both in units. Population figures are mid-year populations as stated by member countries. 

All terms used in the population API queries should be in terms of WHO codes which can be found using other endpoints in this API

#### All Population Data
Return a dictionary of all available population data<br>
``` GET /api/population-list```

#### Find Multiple Population Entries Using Custom Query:
Get raw population data for given country, year, sex, admin or subdiv (or any combination thereof). Response returned as a list and multiple entries are allowed. <br>

``` GET /population/query?country=<country>&year=<year>&sex=<sex>&admin=<admin>&subdiv=<subdiv>```

e.g. 
Return population data for males and females in the United Kingdom in 1989:<br>
``` GET /population?country=4308&year=1989```

#### Find Single Population Entry Using Custom Query:
Get raw population data for given country, year, sex, admin or subdiv (or any combination thereof).
Returns data if only one population entry matches the query<br>

``` GET /population/query?country=<country>&year=<year>&sex=<sex>&admin=<admin>&subdiv=<subdiv>```

e.g. 
Return population data for only males in the United Kingdom in 1989:<br>
``` GET /population?country=4308&year=1989&sex=1```



### ICD-10 Codes (including condensed form)

### Mortality Data


Disclaimer: Every attempt has been made to keep data true to the original raw data files but veracity cannot be guaranteed. If this is important, download the data directly or use one of the WHO's data querying services (https://www.who.int/healthinfo/mortality_data/en/)
All analyses, interpretations or conclusions drawn from this API or found on this website are credited to the authors, not the WHO (which is responsible only for the provision of the original information).
For more information visit the [WHO website](https://www.who.int/healthinfo/statistics/mortality_rawdata/en/)

### Mortality Data - adjusted for population