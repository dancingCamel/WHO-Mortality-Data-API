# WHO Mortality Data API

An API to allow easier querying of the World Health Organization's Mortality. 

All data is returned in JSON format.

## Data available
The following datasets are available for searching:
- Country list and country codes
- country populations 
- ICD-10 codes *not implemented*
- Mortality (cause of death) numbers *not implemented*

## Endpoints
The following endpoints are available (grouped by section):

### Country

#### List all countries:
Return all country names and associated codes used in WHO Mortality database.
>'/api/country-all' 

#### Find Country Code of Specific Country:
Return the name and code of a country (case insensitive). 
>'/api/country/<country_name>'

e.g. 
> GET '/api/country/djibouti'
```
{
    "id": 14,
    "code": "1120",
    "name": "Djibouti"
}
```
#### Search for Countries:
Return all countries with names that contain a search term
> GET '/api/country-search/<search_term>'

e.g.
> GET '/api/country-search/ka'
```
{
    "id": 145,
    "code": "3365",
    "name": "Sri Lanka"
},
{
    "id": 178,
    "code": "4182",
    "name": "Kazakhstan"
}
```
### ICD-10

### Population
Note: Population and live births are both in units. Population figures are mid-year populations as stated by member countries. 

All terms used in the population API queries should be in terms of WHO codes which can be found using other endpoints in this API

### Get All Population Data
Get a dictionary of all available population data
>GET '/api/population-all'


#### Find Population Using Custom Query:
Get population data for given country, year or sex (or any combination thereof).

>GET '/population/query?country=<country>&year=<year>&sex=<sex>'

e.g. 
Return population data for Males in the United Kingdom in 1989:
>GET '/population/query?country=4308&year=1989&sex=1'

### Mortality Data
