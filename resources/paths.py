from flask_restful import Resource
from auth import requireApiKey


class Paths(Resource):
    @requireApiKey
    def get(self):
        # object containing swagger style info on all paths we want users to see
        return {
            # '/api/country-code/<string:country_code>'
            "/api/country-code/{country_code}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return code and description for country code",
                    "responses": {
                        "200": {
                            "description": "Country.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "code": "code of country",
                                            "description": "description of country"
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Country not found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "Error message"
                                        }
                                    }

                                }
                            }
                        }
                    }
                }
            },
            # '/api/country-name/<string:country_name>'
            "/api/country-name/{country_name}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return code and description for country name",
                    "responses": {
                        "200": {
                            "description": "Country.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "code": "code of country",
                                            "description": "description of country"
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Country not found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "Error message"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/country-desc/<string:search_term>'
            "/api/country-desc/{search_term}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all countries matching search term",
                    "responses": {
                        "200": {
                            "description": "A list of country objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema":
                                            {
                                                "code": "code of country",
                                                "description": "description of country"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No countries match search term",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "Error message"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/country-list'
            "/api/country-list": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all countries in database",
                    "responses": {
                        "200": {
                            "description": "A list of country objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema":
                                            {
                                                "code": "code of country",
                                                "description": "description of country"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/country-search/<string:search_term>'
            "/api/country-search/{search_term}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all countries matching search term",
                    "responses": {
                        "200": {
                            "description": "A list of country objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema":
                                            {
                                                "code": "code of country",
                                                "description": "description of country"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No countries match search term",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "Error message"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/sex-code/<string:sex_code>'
            "/api/sex-code/{sex_code}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return sex object for given sex code",
                    "responses": {
                        "200": {
                            "description": "A sex object.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                                "code": "code of sex",
                                                "description": "description of sex"
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Sex code not in database",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "Sex not found"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/sex-desc/<string:sex>'
            "/api/sex-desc/{sex}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return sex object for given sex description",
                    "responses": {
                        "200": {
                            "description": "A sex object.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                                "code": "code of sex",
                                                "description": "description of sex"
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Sex description not in database",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "Sex not found"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/sex-list/'
            "/api/sex-list": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all sexes in database",
                    "responses": {
                        "200": {
                            "description": "A list of sex objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema":
                                            {
                                                "code": "sex code",
                                                "description": "description of sex"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/admin/<string:admin_code>/<string:country_code>'
            "/api/admin/{admin_code}/{country_code}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return description given admin and country code",
                    "responses": {
                        "200": {
                            "description": "An admin object.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                                "code": "admin code",
                                                "country": {
                                                    "schema": {
                                                        "type": "object",
                                                        "items": {
                                                            "code": "Country code",
                                                            "description": "Name of country"
                                                        }
                                                    }
                                                },
                                            "description": "description for admin code"
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Given admin and country combination not in database",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No admin entry found for code and country"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/admin-list'
            "/api/admin-list": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all admin / country combinations in database",
                    "responses": {
                        "200": {
                            "description": "A list of admin objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema":
                                            {
                                                "code": "admin code",
                                                "country": {
                                                    "schema": {
                                                        "type": "object",
                                                        "items": {
                                                            "code": "Country code",
                                                            "description": "Name of country"
                                                        }
                                                    }
                                                },
                                                "description": "description of admin"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/admin-code/<string:admin_code>'
            "/api/admin-code/{admin_code}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all admin / country combinations that match a given admin code",
                    "responses": {
                        "200": {
                            "description": "A list of admin objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema":
                                            {
                                                "code": "admin code",
                                                "country": {
                                                    "schema": {
                                                        "type": "object",
                                                        "items": {
                                                            "code": "Country code",
                                                            "description": "Name of country"
                                                        }
                                                    }
                                                },
                                                "description": "description of admin"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Given admin code not in database",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No admins match that code"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/admin-desc/<string:search_term>'
            "/api/admin-desc/{search_term}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all admins matching search term",
                    "responses": {
                        "200": {
                            "description": "A list of admin objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema":
                                            {
                                                "code": "admin code",
                                                "country": {
                                                    "schema": {
                                                        "type": "object",
                                                        "items": {
                                                            "code": "Country code",
                                                            "description": "Name of country"
                                                        }
                                                    }
                                                },
                                                "description": "description of admin"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No admins match search term",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No Admins match that search term"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/admin-search/<string:search_term>'
            "/api/admin-search/{search_term}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all admins matching search term",
                    "responses": {
                        "200": {
                            "description": "A list of admin objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema":
                                            {
                                                "code": "admin code",
                                                "country": {
                                                    "schema": {
                                                        "type": "object",
                                                        "items": {
                                                            "code": "Country code",
                                                            "description": "Name of country"
                                                        }
                                                    }
                                                },
                                                "description": "description of admin"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No admins match search term",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No Admins match that search term"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # # Subdiv endpoints
            # '/api/subdiv-code/<string:subdiv_code>'
            "/api/subdiv-code/{subdiv_code}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return subdiv object for given subdiv code",
                    "responses": {
                        "200": {
                            "description": "A subdiv object.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                                "code": "code for subdiv",
                                                "description": "description of subdiv"
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Subdiv not in database",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "Subdiv not found"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/subdiv-desc/<string:search_term>'
            "/api/subdiv-desc/{search_term}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all subdivs matching search term",
                    "responses": {
                        "200": {
                            "description": "A list of subdiv objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema":
                                            {
                                                "code": "code for subdiv",
                                                "description": "description of subdiv"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No subdivs match search term",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No subdivs match that search term"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/subdiv-search/<string:search_term>'
            "/api/subdiv-search/{search_term}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all subdivs matching search term",
                    "responses": {
                        "200": {
                            "description": "A list of subdiv objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema":
                                            {
                                                "code": "code for subdiv",
                                                "description": "description of subdiv"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No subdivs match search term",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No subdivs match that search term"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/subdiv-list'
            "/api/subdiv-list": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all subdivs in database",
                    "responses": {
                        "200": {
                            "description": "A list of subdiv objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema":
                                            {
                                                "code": "code for subdiv",
                                                "description": "description of subdiv"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # Age format endpoints
            # '/api/age-format-code/<string:age_format_code>'
            "/api/age-format-code/{age_format_code}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return age format object for given age format code",
                    "responses": {
                        "200": {
                            "description": "An age format object.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items":
                                        {
                                            'age_format_code': "age format code",
                                            'pop2': "pop 2 from official data",
                                            'pop3': "pop 3 from official data",
                                            'pop4': "pop 4 from official data",
                                            'pop5': "pop 5 from official data",
                                            'pop6': "pop 6 from official data",
                                            'pop7': "pop 7 from official data",
                                            'pop8': "pop 8 from official data",
                                            'pop9': "pop 9 from official data",
                                            'pop10': "pop 10 from official data",
                                            'pop11': "pop 11 from official data",
                                            'pop12': "pop 12 from official data",
                                            'pop13': "pop 13 from official data",
                                            'pop14': "pop 14 from official data",
                                            'pop15': "pop 15 from official data",
                                            'pop16': "pop 16 from official data",
                                            'pop17': "pop 17 from official data",
                                            'pop18': "pop 18 from official data",
                                            'pop19': "pop 19 from official data",
                                            'pop20': "pop 20 from official data",
                                            'pop21': "pop 21 from official data",
                                            'pop22': "pop 22 from official data",
                                            'pop23': "pop 23 from official data",
                                            'pop24': "pop 24 from official data",
                                            'pop25': "pop 25 from official data",
                                            'pop26': "pop 26 from official data",
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Age format not in database",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "Age format not found"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/age-format-list'
            "/api/age-format-list": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all age formats in database",
                    "responses": {
                        "200": {
                            "description": "A list of age format objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items":
                                                {
                                                    'age_format_code': "age format code",
                                                    'pop2': "pop 2 from official data",
                                                    'pop3': "pop 3 from official data",
                                                    'pop4': "pop 4 from official data",
                                                    'pop5': "pop 5 from official data",
                                                    'pop6': "pop 6 from official data",
                                                    'pop7': "pop 7 from official data",
                                                    'pop8': "pop 8 from official data",
                                                    'pop9': "pop 9 from official data",
                                                    'pop10': "pop 10 from official data",
                                                    'pop11': "pop 11 from official data",
                                                    'pop12': "pop 12 from official data",
                                                    'pop13': "pop 13 from official data",
                                                    'pop14': "pop 14 from official data",
                                                    'pop15': "pop 15 from official data",
                                                    'pop16': "pop 16 from official data",
                                                    'pop17': "pop 17 from official data",
                                                    'pop18': "pop 18 from official data",
                                                    'pop19': "pop 19 from official data",
                                                    'pop20': "pop 20 from official data",
                                                    'pop21': "pop 21 from official data",
                                                    'pop22': "pop 22 from official data",
                                                    'pop23': "pop 23 from official data",
                                                    'pop24': "pop 24 from official data",
                                                    'pop25': "pop 25 from official data",
                                                    'pop26': "pop 26 from official data",
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/infant-age-format-code/<string:infant_age_format_code>'
            "/api/infant-age-format-code/{infant_age_format_code}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return infant age format object for given infant age format code",
                    "responses": {
                        "200": {
                            "description": "An infant age format object.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items":
                                        {
                                            'infant_age_format_code': "infant age format code",
                                            'infant_age1': "infantAge1 from WHO docs",
                                            'infant_age2': "infantAge2 from WHO docs",
                                            'infant_age3': "infantAge3 from WHO docs",
                                            'infant_age4': "infantAge4 from WHO docs"
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Infant age format not in database",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No infant age format found with code"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/infant-age-format-list'
            "/api/infant-age-format-list": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all infant age formats in database",
                    "responses": {
                        "200": {
                            "description": "A list of infant age format objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items":
                                                {
                                                    'infant_age_format_code': "infant age format code",
                                                    'infant_age1': "infantAge1 from WHO docs",
                                                    'infant_age2': "infantAge2 from WHO docs",
                                                    'infant_age3': "infantAge3 from WHO docs",
                                                    'infant_age4': "infantAge4 from WHO docs"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # Population endpoints
            # '/api/population-search'
            "/api/population-search?{search_term_arguments}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all populations matching search term arguments",
                    "arguments":
                    {
                        "country": "country code string",
                        "year": "year as string",
                        "sex": "sex code string",
                        "admin": "admin code string",
                        "subdiv": "subdiv code string"
                    },
                    "responses": {
                        "200": {
                            "description": "A list of population objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'id': "id of data in database",
                                                    'country': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of country",
                                                                "description": "description of country"
                                                            }
                                                        }
                                                    },
                                                    'admin': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "admin code",
                                                                "country":
                                                                {
                                                                    "schema": {
                                                                        "type": "object",
                                                                        "items": {
                                                                            "code": "Country code",
                                                                            "description": "Name of country"
                                                                        }
                                                                    }
                                                                },
                                                                "description": "description for admin code"
                                                            }
                                                        }
                                                    },
                                                    'subdiv': {
                                                        "type": "object",
                                                        "items": {
                                                            "schema":
                                                            {
                                                                "code": "code for subdiv",
                                                                "description": "description of subdiv"
                                                            }
                                                        }
                                                    },
                                                    'year': "year",
                                                    'sex': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of sex",
                                                                "description": "description of sex"
                                                            }
                                                        }
                                                    },
                                                    'age_format': "age format code",
                                                    'all_ages': "total population",
                                                    'age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "pops": "Populations for all age brackets dictated by age format code",
                                                            }
                                                        }
                                                    },
                                                    'live_births': "live births"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No matching populations",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No populations match your query arguments"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/population-one'
            "/api/population-one?{search_term_arguments}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return one population matching search term arguments, otherwise return error",
                    "arguments":
                    {
                        "country": "country code string",
                        "year": "year as string",
                        "sex": "sex code string",
                        "admin": "admin code string",
                        "subdiv": "subdiv code string"
                    },
                    "responses": {
                        "200": {
                            "description": "A list of population objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'id': "id of data in database",
                                                    'country': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of country",
                                                                "description": "description of country"
                                                            }
                                                        }
                                                    },
                                                    'admin': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "admin code",
                                                                "country":
                                                                {
                                                                    "schema": {
                                                                        "type": "object",
                                                                        "items": {
                                                                            "code": "Country code",
                                                                            "description": "Name of country"
                                                                        }
                                                                    }
                                                                },
                                                                "description": "description for admin code"
                                                            }
                                                        }
                                                    },
                                                    'subdiv': {
                                                        "type": "object",
                                                        "items": {
                                                            "schema":
                                                            {
                                                                "code": "code for subdiv",
                                                                "description": "description of subdiv"
                                                            }
                                                        }
                                                    },
                                                    'year': "year",
                                                    'sex': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of sex",
                                                                "description": "description of sex"
                                                            }
                                                        }
                                                    },
                                                    'age_format': "age format code",
                                                    'all_ages': "total population",
                                                    'age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "pops": "Populations for all age brackets dictated by age format code",
                                                            }
                                                        }
                                                    },
                                                    'live_births': "live births"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No matching populations",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No populations match your query arguments"
                                        }
                                    }
                                }
                            }
                        }
                    },
                        "404": {
                            "description": "No matching populations",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No populations match your query arguments"
                                        }
                                    }
                                }
                            }
                    },
                        "400": {
                            "description": "More than one population found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "More than one population entry was found with the given parameters"
                                        }
                                    }
                                }
                            }
                    }
                }

            },
            # '/api/population-list'
            "/api/population-list": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all populations in database",
                    "responses": {
                        "200": {
                            "description": "A list of population objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'id': "id of data in database",
                                                    'country': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of country",
                                                                "description": "description of country"
                                                            }
                                                        }
                                                    },
                                                    'admin': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "admin code",
                                                                "country":
                                                                {
                                                                    "schema": {
                                                                        "type": "object",
                                                                        "items": {
                                                                            "code": "Country code",
                                                                            "description": "Name of country"
                                                                        }
                                                                    }
                                                                },
                                                                "description": "description for admin code"
                                                            }
                                                        }
                                                    },
                                                    'subdiv': {
                                                        "type": "object",
                                                        "items": {
                                                            "schema":
                                                            {
                                                                "code": "code for subdiv",
                                                                "description": "description of subdiv"
                                                            }
                                                        }
                                                    },
                                                    'year': "year",
                                                    'sex': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of sex",
                                                                "description": "description of sex"
                                                            }
                                                        }
                                                    },
                                                    'age_format': "age format code",
                                                    'all_ages': "total population",
                                                    'age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "pops": "Populations for all age brackets dictated by age format code",
                                                            }
                                                        }
                                                    },
                                                    'live_births': "live births"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                    }
                }
            },
            # '/api/population-search-multiple'
            "/api/population-search-multiple?{search_term_arguments}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return one population matching search term arguments, otherwise return error",
                    "arguments":
                    {
                        "country": "comma separated list of country code strings",
                        "year": "comma separated list year as strings",
                        "sex": "comma separated list sex code strings",
                        "admin": "comma separated list admin code strings",
                        "subdiv": "comma separated list subdiv code strings"
                    },
                    "responses": {
                        "200": {
                            "description": "A list of population objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'id': "id of data in database",
                                                    'country': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of country",
                                                                "description": "description of country"
                                                            }
                                                        }
                                                    },
                                                    'admin': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "admin code",
                                                                "country":
                                                                {
                                                                    "schema": {
                                                                        "type": "object",
                                                                        "items": {
                                                                            "code": "Country code",
                                                                            "description": "Name of country"
                                                                        }
                                                                    }
                                                                },
                                                                "description": "description for admin code"
                                                            }
                                                        }
                                                    },
                                                    'subdiv': {
                                                        "type": "object",
                                                        "items": {
                                                            "schema":
                                                            {
                                                                "code": "code for subdiv",
                                                                "description": "description of subdiv"
                                                            }
                                                        }
                                                    },
                                                    'year': "year",
                                                    'sex': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of sex",
                                                                "description": "description of sex"
                                                            }
                                                        }
                                                    },
                                                    'age_format': "age format code",
                                                    'all_ages': "total population",
                                                    'age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "pops": "Populations for all age brackets dictated by age format code",
                                                            }
                                                        }
                                                    },
                                                    'live_births': "live births"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No matching populations",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No populations match your query arguments"
                                        }
                                    }
                                }
                            }
                        }
                    },
                        "404": {
                            "description": "No matching populations",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No populations match your query arguments"
                                        }
                                    }
                                }
                            }
                    }
                }
            },
            # ICD10 code endpoints
            # '/api/icd10/<string:code_list>/<string:code>'
            "/api/icd10/{code_list}/{code}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return description for given icd code in given code list",
                    "responses": {
                        "200": {
                            "description": "An icd code object.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            'list': "code list that contains the code",
                                            'code': "ICD code",
                                            'description': "description of code"
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Code not found in given list",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "Code was not found in list"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/icd10-list'
            "/api/icd10-list": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all ICD codes in database",
                    "responses": {
                        "200": {
                            "description": "A list of ICD code objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'list': "code list that contains the code",
                                                    'code': "ICD code",
                                                    'description': "description of code"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/icd10-search/<string:search_term>'
            "/api/icd10-search/{search_term}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all ICD codes matching search term",
                    "responses": {
                        "200": {
                            "description": "A list of ICD code objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'list': "code list that contains the code",
                                                    'code': "ICD code",
                                                    'description': "description of code"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No ICD codes match search term",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No results match the search term"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/icd10-desc/<string:search_term>'
            "/api/icd10-desc/{search_term}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all ICD codes matching search term (greater than 3 characters)",
                    "responses": {
                        "200": {
                            "description": "A list of ICD code objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'list': "code list that contains the code",
                                                    'code': "ICD code",
                                                    'description': "description of code"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No ICD codes match search term",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No results match the search term"
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Search term not specific enough",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "Please search for a term at least 3 characters long"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/icd10-code/<string:code>'
            "/api/icd10-code/{code}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return list of ICD code objects for given code (multiple code lists can have duplicate codes)",
                    "responses": {
                        "200": {
                            "description": "A list of ICD code objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'list': "code list that contains the code",
                                                    'code': "ICD code",
                                                    'description': "description of code"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "ICD code not in database",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No results match the code"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # ICD code list endpoints
            # '/api/icd10-code-list-code/<string:code>'
            "/api/icd10-code-list-code/{code}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return ICD code list object for given list code",
                    "responses": {
                        "200": {
                            "description": "An ICD code list object.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            'list': "code for ICD code list",
                                            'description': "description of ICD code list"
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Code list not in database",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "Code list not found"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/icd10-code-list-desc/<string:search_term>'
            "/api/icd10-code-list-desc/{search_term}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return list of all ICD code lists matching search term",
                    "responses": {
                        "200": {
                            "description": "A list of ICD code list objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'list': "code for ICD code list",
                                                    'description': "description of ICD code list"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No code lists match search term",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No lists match that search term"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/icd10-code-lists'
            "/api/icd10-code-list-list": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return all ICD code lists",
                    "responses": {
                        "200": {
                            "description": "A list of ICD code list objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'list': "code for ICD code list",
                                                    'description': "description of ICD code list"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # Mortality data endpoints
            # '/api/mortality-data-search'
            "/api/mortality-data-search?{search_arguments}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return list of all mortality data matching search arguments",
                    "arguments":
                    {
                        "country": "country code string",
                        "year": "year as string",
                        "sex": "sex code string",
                        "admin": "admin code string",
                        "subdiv": "subdiv code string",
                        "cause": "cause code string"
                    },
                    "responses": {
                        "200": {
                            "description": "A list of mortality data objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'country': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of country",
                                                                "description": "description of country"
                                                            }
                                                        }
                                                    },
                                                    'admin': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "admin code",
                                                                "country":
                                                                {
                                                                    "schema": {
                                                                        "type": "object",
                                                                        "items": {
                                                                            "code": "Country code",
                                                                            "description": "Name of country"
                                                                        }
                                                                    }
                                                                },
                                                                "description": "description for admin code"
                                                            }
                                                        }
                                                    },
                                                    'subdiv': {
                                                        "type": "object",
                                                        "items": {
                                                            "schema":
                                                            {
                                                                "code": "code for subdiv",
                                                                "description": "description of subdiv"
                                                            }
                                                        }
                                                    },
                                                    'year': "year",
                                                    'code_list': "ICD Code list",
                                                    'cause': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                'list': "code list that contains the code",
                                                                'code': "ICD code",
                                                                'description': "description of code"
                                                            }
                                                        }
                                                    },
                                                    'sex': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of sex",
                                                                "description": "description of sex"
                                                            }
                                                        }
                                                    },
                                                    'age_format': "age format code",
                                                    'infant_age_format': "infant age format code",
                                                    'all_ages': "total deaths due to given cause",
                                                    'age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "(age_range)": "Deaths for all age brackets dictated by age format code",
                                                            }
                                                        }
                                                    },
                                                    'infant_age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "(age_range)": "Deaths for all age brackets dictated by infant age format code",
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No matching mortality data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No mortality data matches your query arguments"
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid inputs",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "User input are invalid"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/mortality-data-one'
            "/api/mortality-data-one?{search_arguments}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return single mortality data entry matching search arguments",
                    "arguments":
                    {
                        "country": "country code string",
                        "year": "year as string",
                        "sex": "sex code string",
                        "admin": "admin code string",
                        "subdiv": "subdiv code string",
                        "cause": "cause code string"
                    },
                    "responses": {
                        "200": {
                            "description": "A mortality data object.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                                "items": {
                                                    'country': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of country",
                                                                "description": "description of country"
                                                            }
                                                        }
                                                    },
                                                    'admin': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "admin code",
                                                                "country":
                                                                {
                                                                    "schema": {
                                                                        "type": "object",
                                                                        "items": {
                                                                            "code": "Country code",
                                                                            "description": "Name of country"
                                                                        }
                                                                    }
                                                                },
                                                                "description": "description for admin code"
                                                            }
                                                        }
                                                    },
                                                    'subdiv': {
                                                        "type": "object",
                                                        "items": {
                                                            "schema":
                                                            {
                                                                "code": "code for subdiv",
                                                                "description": "description of subdiv"
                                                            }
                                                        }
                                                    },
                                                    'year': "year",
                                                    'code_list': "ICD Code list",
                                                    'cause': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                'list': "code list that contains the code",
                                                                'code': "ICD code",
                                                                'description': "description of code"
                                                            }
                                                        }
                                                    },
                                                    'sex': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of sex",
                                                                "description": "description of sex"
                                                            }
                                                        }
                                                    },
                                                    'age_format': "age format code",
                                                    'infant_age_format': "infant age format code",
                                                    'all_ages': "total deaths due to given cause",
                                                    'age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "(age_range)": "Deaths for all age brackets dictated by age format code",
                                                            }
                                                        }
                                                    },
                                                    'infant_age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "(age_range)": "Deaths for all age brackets dictated by infant age format code",
                                                            }
                                                        }
                                                    }
                                                }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No matching mortality data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No mortality data matches your query arguments"
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid inputs",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "User input are invalid"
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "More than one matching mortality data entry",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "More than one mortality entry was found matching your query, please be more specific.",
                                            "entries": {
                                                "schema": {
                                                    "type": "array",
                                                    "items": "A list of mortality data entries."
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/mortality-search-multiple'
            "/api/mortality-search-multiple?{search_arguments}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return list of all mortality data matching search arguments",
                    "arguments":
                    {
                        "country": "Comma separated list of country code strings",
                        "year": "Comma separated list of year as strings",
                        "sex": "Comma separated list of sex code strings",
                        "admin": "Comma separated list of admin code strings",
                        "subdiv": "Comma separated list of subdiv code strings",
                        "cause": "Comma separated list of cause code strings"
                    },
                    "responses": {
                        "200": {
                            "description": "A list of mortality data objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'country': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of country",
                                                                "description": "description of country"
                                                            }
                                                        }
                                                    },
                                                    'admin': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "admin code",
                                                                "country":
                                                                {
                                                                    "schema": {
                                                                        "type": "object",
                                                                        "items": {
                                                                            "code": "Country code",
                                                                            "description": "Name of country"
                                                                        }
                                                                    }
                                                                },
                                                                "description": "description for admin code"
                                                            }
                                                        }
                                                    },
                                                    'subdiv': {
                                                        "type": "object",
                                                        "items": {
                                                            "schema":
                                                            {
                                                                "code": "code for subdiv",
                                                                "description": "description of subdiv"
                                                            }
                                                        }
                                                    },
                                                    'year': "year",
                                                    'code_list': "ICD Code list",
                                                    'cause': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                'list': "code list that contains the code",
                                                                'code': "ICD code",
                                                                'description': "description of code"
                                                            }
                                                        }
                                                    },
                                                    'sex': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of sex",
                                                                "description": "description of sex"
                                                            }
                                                        }
                                                    },
                                                    'age_format': "age format code",
                                                    'infant_age_format': "infant age format code",
                                                    'all_ages': "total deaths due to given cause",
                                                    'age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "(age_range)": "Deaths for all age brackets dictated by age format code",
                                                            }
                                                        }
                                                    },
                                                    'infant_age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "(age_range)": "Deaths for all age brackets dictated by infant age format code",
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No matching mortality data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No mortality data matches your query arguments"
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid inputs",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "Please add at least a year, country, sex and cause variable"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/mortality-adj-search'
            "/api/mortality-adj-search?{search_arguments}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return list of all population adjusted mortality data matching search arguments",
                    "arguments":
                    {
                        "country": "country code string",
                        "year": "year as string",
                        "sex": "sex code string",
                        "admin": "admin code string",
                        "subdiv": "subdiv code string",
                        "cause": "cause code string"
                    },
                    "responses": {
                        "200": {
                            "description": "A list of mortality data objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'country': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of country",
                                                                "description": "description of country"
                                                            }
                                                        }
                                                    },
                                                    'admin': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "admin code",
                                                                "country":
                                                                {
                                                                    "schema": {
                                                                        "type": "object",
                                                                        "items": {
                                                                            "code": "Country code",
                                                                            "description": "Name of country"
                                                                        }
                                                                    }
                                                                },
                                                                "description": "description for admin code"
                                                            }
                                                        }
                                                    },
                                                    'subdiv': {
                                                        "type": "object",
                                                        "items": {
                                                            "schema":
                                                            {
                                                                "code": "code for subdiv",
                                                                "description": "description of subdiv"
                                                            }
                                                        }
                                                    },
                                                    'year': "year",
                                                    'code_list': "ICD Code list",
                                                    'cause': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                'list': "code list that contains the code",
                                                                'code': "ICD code",
                                                                'description': "description of code"
                                                            }
                                                        }
                                                    },
                                                    'sex': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of sex",
                                                                "description": "description of sex"
                                                            }
                                                        }
                                                    },
                                                    'age_format': "age format code",
                                                    'infant_age_format': "infant age format code",
                                                    'all_ages': "population adjusted total deaths due to given cause",
                                                    'age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "(age_range)": "Population adjusted deaths for all age brackets dictated by age format code",
                                                            }
                                                        }
                                                    },
                                                    'infant_age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "(age_range)": "Population adjusted deaths for all age brackets dictated by infant age format code",
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No matching mortality data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No mortality data matches your query arguments"
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No matching population data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No population data matches your query arguments"
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid inputs",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "User input are invalid"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/mortality-adj-one'
            "/api/mortality-adj-one?{search_arguments}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return single population adjusted mortality data matching search arguments",
                    "arguments":
                    {
                        "country": "country code string",
                        "year": "year as string",
                        "sex": "sex code string",
                        "admin": "admin code string",
                        "subdiv": "subdiv code string",
                        "cause": "cause code string"
                    },
                    "responses": {
                        "200": {
                            "description": "A population adjusted mortality data object.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            'country': {
                                                "schema": {
                                                    "type": "object",
                                                    "items": {
                                                        "code": "code of country",
                                                        "description": "description of country"
                                                    }
                                                }
                                            },
                                            'admin': {
                                                "schema": {
                                                    "type": "object",
                                                    "items": {
                                                        "code": "admin code",
                                                        "country":
                                                        {
                                                            "schema": {
                                                                "type": "object",
                                                                "items": {
                                                                    "code": "Country code",
                                                                    "description": "Name of country"
                                                                }
                                                            }
                                                        },
                                                        "description": "description for admin code"
                                                    }
                                                }
                                            },
                                            'subdiv': {
                                                "type": "object",
                                                "items": {
                                                    "schema":
                                                    {
                                                        "code": "code for subdiv",
                                                        "description": "description of subdiv"
                                                    }
                                                }
                                            },
                                            'year': "year",
                                            'code_list': "ICD Code list",
                                            'cause': {
                                                "schema": {
                                                    "type": "object",
                                                    "items": {
                                                        'list': "code list that contains the code",
                                                        'code': "ICD code",
                                                        'description': "description of code"
                                                    }
                                                }
                                            },
                                            'sex': {
                                                "schema": {
                                                    "type": "object",
                                                    "items": {
                                                        "code": "code of sex",
                                                        "description": "description of sex"
                                                    }
                                                }
                                            },
                                            'age_format': "age format code",
                                            'infant_age_format': "infant age format code",
                                            'all_ages': "population adjusted total deaths due to given cause",
                                            'age_breakdown': {
                                                "schema": {
                                                    "type": "object",
                                                    "items": {
                                                        "(age_range)": "Population adjusted deaths for all age brackets dictated by age format code",
                                                    }
                                                }
                                            },
                                            'infant_age_breakdown': {
                                                "schema": {
                                                    "type": "object",
                                                    "items": {
                                                        "(age_range)": "Population adjusted deaths for all age brackets dictated by infant age format code",
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No matching mortality data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No mortality data matches your query arguments"
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No matching population data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No population data matches your query arguments"
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid inputs",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "User input are invalid"
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "More than one matching mortality data set",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "More than one population entry was found matching your query"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # '/api/mortality-adj-search-multiple'
            "/api/mortality-adj-search-multiple?{search_arguments}": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return list of all population adjusted mortality data matching search arguments",
                    "arguments":
                    {
                        "country": "Comma separated list of country code strings",
                        "year": "Comma separated list of year as strings",
                        "sex": "Comma separated list of sex code strings",
                        "admin": "Comma separated list of admin code strings",
                        "subdiv": "Comma separated list of subdiv code strings",
                        "cause": "Comma separated list of cause code strings"
                    },
                    "responses": {
                        "200": {
                            "description": "A list of mortality data objects.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "schema": {
                                                "type": "object",
                                                "items": {
                                                    'country': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of country",
                                                                "description": "description of country"
                                                            }
                                                        }
                                                    },
                                                    'admin': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "admin code",
                                                                "country":
                                                                {
                                                                    "schema": {
                                                                        "type": "object",
                                                                        "items": {
                                                                            "code": "Country code",
                                                                            "description": "Name of country"
                                                                        }
                                                                    }
                                                                },
                                                                "description": "description for admin code"
                                                            }
                                                        }
                                                    },
                                                    'subdiv': {
                                                        "type": "object",
                                                        "items": {
                                                            "schema":
                                                            {
                                                                "code": "code for subdiv",
                                                                "description": "description of subdiv"
                                                            }
                                                        }
                                                    },
                                                    'year': "year",
                                                    'code_list': "ICD Code list",
                                                    'cause': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                'list': "code list that contains the code",
                                                                'code': "ICD code",
                                                                'description': "description of code"
                                                            }
                                                        }
                                                    },
                                                    'sex': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "code": "code of sex",
                                                                "description": "description of sex"
                                                            }
                                                        }
                                                    },
                                                    'age_format': "age format code",
                                                    'infant_age_format': "infant age format code",
                                                    'all_ages': "population adjusted total deaths due to given cause",
                                                    'age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "(age_range)": "Population adjusted deaths for all age brackets dictated by age format code",
                                                            }
                                                        }
                                                    },
                                                    'infant_age_breakdown': {
                                                        "schema": {
                                                            "type": "object",
                                                            "items": {
                                                                "(age_range)": "Population adjusted deaths for all age brackets dictated by infant age format code",
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No matching mortality data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No mortality data matches your query arguments"
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "No matching population data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "No population data matches your query arguments"
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid inputs",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "message": "User input are invalid"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },

            # Info, '/api/info'
            "/api/info": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return info about API",
                    "responses": {
                        "200": {
                            "description": "Info about the API.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "title": "API Title",
                                            "description": "Description of API.",
                                            "disclaimer": "WHO legal disclaimer",
                                            "contact": {
                                                "schema": {
                                                    "type": "object",
                                                    "items": {
                                                        "name": "App Support",
                                                        "url": "url for contact page",
                                                        "email": "contact email address"
                                                    }
                                                }
                                            },
                                            "license": {
                                                "schema": {
                                                    "type": "object",
                                                    "items": {
                                                        "name": "API license",
                                                        "url": "link to api license"
                                                    }
                                                }
                                            },
                                            "version": "API version number"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # ExternalDocs, '/api/externalDocs'
            "/api/externalDocs": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return link to external documentation for API",
                    "responses": {
                        "200": {
                            "description": "link to external documentation",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "description": "external docs description",
                                            "url": "link to external docs"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            # Paths, '/api/paths'
            "/api/paths": {
                "get": {
                    "security":
                    {
                        "type": "apiKey",
                                "name": "api_key",
                                "in": "header"
                    },
                    "description": "Return info about all API paths",
                    "responses": {
                        "200": {
                            "description": "All API paths.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "items": {
                                            "paths": "All paths..."
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
        }
