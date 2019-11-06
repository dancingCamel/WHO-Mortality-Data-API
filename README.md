# WHO Mortality Data API

An API to allows easier querying of the World Health Organization's mortality data database. 

All data is returned in JSON format.

## Data available
The following datasets are available for searching:
- country codes *not implemented*
- ICD-10 codes *not implemented*
- country populations *not implemented*
- Mortality (cause of death) *not implemented*

## Endpoints
The following endpoints are available (grouped by section):

### Country

#### List all countries:
Return all country names and associated codes used in WHO Mortality database.
>'/countries' 

#### Find Country Code of Specific Country:
Return the name and code of a country (case insensitive). 
>'country/<string:country_name>'

e.g. 
> GET 'country/djibouti'
```
{
    "id": 14,
    "code": "1120",
    "name": "Djibouti"
}
```
#### Search for Countries:
Return all countries with names that contain a search term
> GET '/country-search/<string:search_term>'

e.g.
> GET '/country-search/anu'
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

### Mortality Data
