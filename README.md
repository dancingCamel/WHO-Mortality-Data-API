# WHO Mortality Data API

An API to allow easier querying of the World Health Organization's Mortality Data.

Mortality Data drawn from the WHO ICD-10 (parts 1 and 2) [raw data file](https://www.who.int/healthinfo/statistics/mortality_rawdata/en/) (accessed November 2019). 

ICD-10 codes taken from the [Centers for Medicare & Medicaid Services website](https://www.cms.gov/Medicare/Coding/ICD10/2018-ICD-10-CM-and-GEMs.html) and the [WHO Mortality Database Documentation](https://www.who.int/healthinfo/statistics/mortality_rawdata/en/) (accessed November 2019). 

This API returns data in JSON format with all values as strings.

## Data available
The following datasets are available:
- WHO Country codes
- WHO Sex codes and their meanings
- WHO 'Admin' codes and their meanings
- WHO 'Subdiv' codes and their meanings
- WHO Age format codes and their meanings
- WHO Infant age format codes and their meanings
- Country populations (from 1950)
- ICD-10 codes and description
- Mortality (cause of death) statistics (from 2005)
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

e.g. <br>
``` GET /api/country/djibouti```

> {<br>
>     "id": 14,<br>
>     "code": "1120",<br>
>     "name": "Djibouti"<br>
> }<br>

#### Search for Countries:
Return all countries with names that contain a search term <br>
``` GET /api/country-search/<search_term>```

e.g. <br>
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
(Short version: 1 = Male, 2 = Female, 9 = Unspecified)

#### List All Sex Codes
Return all sex codes used in the Mortality Database<br>
```GET /api/sex-list```

#### Find Sex Code for Specific Sex
Return the code for a know sex<br>
```GET /api/sex-desc/<sex_name>```

e.g. <br>
```GET /api/sex-desc/female```
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

e.g.  <br>
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

e.g. <br>
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
```GET /api/age-format-code/<age_format_code>```

e.g. <br>
```GET /api/age-format-code/08```
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
```GET /api/-infant-age-format-code/<infant_age_format_code>```

e.g. <br>
```GET /api/infant-age-format-code/01```

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

``` GET /api/population-search?country=<country>&year=<year>&sex=<sex>&admin=<admin>&subdiv=<subdiv>```<br>

Variables (variable name) = format: country = country code, year, sex = sex code, admin = admin code, subdiv = subdiv code <br>
e.g. 
Return population data for males and females in the United Kingdom in 1989:<br>
``` GET /api/population-search?country=4308&year=1989```

#### Find Single Population Entry Using Custom Query:
Get raw population data for given country, year, sex, admin or subdiv (or any combination thereof).
Returns data if only one population entry matches the query<br>

``` GET /api/population-one?country=<country>&year=<year>&sex=<sex>&admin=<admin>&subdiv=<subdiv>```

e.g. 
Return population data for only males in the United Kingdom in 1989:<br>
``` GET /api/population-one?country=4308&year=1989&sex=1```



### ICD-10 Codes (including condensed form)
Endpoints related to the ICD-10 codes including search for descriptions and codes across multiple list versions used by WHO in mortality data.

#### All ICD-10 Code Lists used in Mortality Data
Find descriptions of all different code lists used in Mortality Data.<br>
``` GET /api/icd10-code-list-list```

#### ICD-10 Code List Description
Find the description of a specific code list.<br>
``` GET /api/icd10-code-list/<code>```

e.g. <br>
```GET /api/icd10-code-list/103```

>{<br>
>    "list": "103",<br>
>    "description": "3 Character ICD10 codes"<br>
>}<br>

### ICD-10 Code Description
Find the description of a certain code in a certain list. (If list is unknown use the ICD-10 Search endpoint.)<br>
NOTE 1: Y34 and Y349 respectively refer to the sum of all deaths from accidental deaths V00-Y89 for countries reporting with list 103 and 104 respectively<br>
NOTE 2: If a country reports with a 4 character code in the 10M list, the death will not be counted in the 3 character code total (all numbers are mutually exclusive).<br>
``` GET /api/icd10/<list>/<code>```

e.g.<br>
```GET /api/icd10/104/Y25```

>{<br>
>    "list": "104",<br>
>    "code": "Y25",<br>
>    "description": "Contact with explosive material (undetermined intent)"<br>
>}<br>

#### ICD-10 Search
Search the ICD-10 with a search term (searches both codes and description)<br>
``` GET /api/icd10-search/<search_term>```

e.g.<br>
```GET /api/icd10-search/boil```

>{<br>
>    "results": [<br>
>        {<br>
>            "list": "103",<br>
>            "code": "W35",<br>
>            "description": "Explosion and rupture of boiler"<br>
>        },<br>
>        {<br>
>            "list": "104",<br>
>            "code": "W35",<br>
>            "description": "Explosion and rupture of boiler"<br>
>        },<br>
>        {<br>
>            "list": "10M",<br>
>            "code": "W35",<br>
>            "description": "Explosion and rupture of boiler"<br>
>        }<br>
>    ]<br>
>}<br>

#### ICD-10 List
Return all ICD-10 codes and their descriptions in all lists used in Mortality Database<br>
``` GET /api/icd10-list```


### Mortality Data
Endpoints related to the WHO Mortality Database. Each mortality database entry details the number of deaths in a given country in any given year for any given sex from a certain cause. When searching with a cause of death icd10 code the code must be in the correct format for that countries mortality data. Mortality data starts in 2005. 

NOTE: Some cause of death ICD-10 codes listed in the mortality database do not appear in any official ICD-10 documentation, specifically related to the W.. and Y.. cause of death codes. I have contacted the WHO for clarification on this issue.

#### Find All Mortality Entries Matching Set of Single Search Variables:
Get raw mortality data for given country, year, sex, admin or subdiv and cause (or any combination thereof). Response returned as a list and multiple entries are allowed. <br>

``` GET /api/mortality-data-search?country=<country>&year=<year>&sex=<sex>&admin=<admin>&subdiv=<subdiv>&cause=<cause>```<br>

Variables (variable = format): country = country code, year, sex = sex code, admin = admin code, subdiv = subdiv code, cause = cause code. All codes can be found from the respective endpoints <br>
e.g. 
Return mortality data for males and females in the United Kingdom in 2006 caused by "Airgun discharge (undetermined intent)":<br>
``` GET /api/mortality-data-search?country=4308&year=2006&cause=Y240```

#### Find Single Mortality Data Entry:
Get raw mortality data for given country, year, sex, admin or subdiv and cause (or any combination thereof).
Returns data only if only one mortality entry matches the query<br>

``` GET /api/mortality-data-one?country=<country>&year=<year>&sex=<sex>&admin=<admin>&subdiv=<subdiv>&cause=<cause>```

e.g. 
Return mortality data for only males in the United Kingdom in 2016 caused by "Driver of special agricultural vehicle injured in traffic accident":<br>

``` GET /api/mortality-data-one?country=4308&year=2016&sex=1&cause=V840```<br>


#### Find All Mortality Entries Matching Lists of Search Variables:
Get raw mortality data for lists of given country, year, sex, admin or subdiv and cause (or any combination thereof). Response returned as a list and multiple entries are allowed. <br>

``` GET /api/mortality-search-multiple?country=<country>,<country>,...&year=<year>,<year>,...&sex=<sex>,<sex>,...&admin=<admin>,<admin>,...&subdiv=<subdiv>,<subdiv>,...&cause=<cause>,<cause>,...```<br>

Return mortality data for males and females in the United Kingdom and Croatia in 2005 and 2006 caused by "Airgun discharge (undetermined intent)":<br>
```GET /api/mortality-data-search?country=4308,4038&year=2005,2006&cause=Y240&sex=1,2```<br>

### Mortality Data - adjusted for population
Endpoints related to the WHO Mortality Database with all mortalities adjusted for population (per 100,000) - also known as ASDR per 100,000. All other factors are the same as for the mortality data detailed above.

NOTE: Some cause of death ICD-10 codes listed in the mortality database do not appear in any official ICD-10 documentation, specifically related to the W.. and Y.. cause of death codes. I have contacted the WHO for clarification on this issue.
NOTE: In some cases there is population data but no mortality data, or vice versa. In these situations the data point is removed so as to avoid confusion due to mixing of age-specific and absolute data.

#### Find All Population Adjusted Mortality Entries Matching Set of Single Search Variables:
Get adjusted mortality data for given country, year, sex, admin or subdiv and cause (or any combination thereof). Response returned as a list and multiple entries are allowed. <br>

``` GET /api/mortality-adj-search?country=<country>&year=<year>&sex=<sex>&admin=<admin>&subdiv=<subdiv>&cause=<cause>```<br>

Variables (variable = format): country = country code, year, sex = sex code, admin = admin code, subdiv = subdiv code, cause = cause code. All codes can be found from the respective endpoints <br>
e.g. 
Return population adjusted mortality data for males and females in the United Kingdom in 2006 caused by "Airgun discharge (undetermined intent)":<br>
``` GET /api/mortality-adj-search?country=4308&year=2006&cause=Y240```<br>

#### Find Single Population Adjusted Mortality Data Entry:
Get adjusted mortality data for given country, year, sex, admin or subdiv and cause (or any combination thereof).
Returns data only if only one mortality entry matches the query<br>

``` GET /api/mortality-adj-one?country=<country>&year=<year>&sex=<sex>&admin=<admin>&subdiv=<subdiv>&cause=<cause>```<br>

e.g. 
Return population adjusted mortality data for only males in the United Kingdom in 2016 caused by "Driver of special agricultural vehicle injured in traffic accident":<br>

``` GET /api/mortality-adj-one?country=4308&year=2016&sex=1&cause=V840```<br>

#### Find All Population Adjusted Mortality Entries Matching Lists of Search Variables:
Get population adjusted mortality data for lists of given country, year, sex, admin or subdiv and cause (or any combination thereof). Response returned as a list and multiple entries are allowed. <br>

``` GET /api/mortality-search-multiple?country=<country>,<country>,...&year=<year>,<year>,...&sex=<sex>,<sex>,...&admin=<admin>,<admin>,...&subdiv=<subdiv>,<subdiv>,...&cause=<cause>,<cause>,...```<br>

Return population adjusted mortality data for males and females in the United Kingdom and Croatia in 2005 and 2006 caused by "Airgun discharge (undetermined intent)":<br>
```GET /api/mortality-data-search?country=4308,4038&year=2005,2006&cause=Y240&sex=1,2```<br>

### Disclaimer
Every attempt has been made to keep data true to the original raw data files but veracity cannot be guaranteed. If this is important, download the data directly or use one of the [WHO's data querying services](https://www.who.int/healthinfo/mortality_data/en/)
All analyses, interpretations or conclusions drawn from this API or found on this website are credited to the authors, not the WHO (which is responsible only for the provision of the original information).
For more information visit the [WHO website](https://www.who.int/healthinfo/statistics/mortality_rawdata/en/)