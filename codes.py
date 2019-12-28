
# make resource
sex_codes = {
    'Male': '1',
    'm': '1',
    'M': '1',
    'male': '1',
    'Female': '2',
    'female': '2',
    'F': '2',
    'f': '2',
    'Unspecified': '9',
    'unspecified': '9',
}

# just import internally as others won't need to query the data as we will translate it for them in the JSON
admin_codes = [
    ['901', '2070', 'North and North-East'],
    ['901', '2350', 'Former Canal Zone'],
    ['901', '3150', 'Jewish Population'],
    ['902', '2070', 'South, South-East and Central West']
]
# just import internally as others won't need to query the data as we will translate it for them in the JSON
subdiv_codes = {
    'A10': 'Survey',
    'A20': 'Reporting Areas',
    'A30': 'Part',
    'A35': 'Selected Urban and Rural Areas',
    'A41': 'Selected Rural Areas',
    'A51': 'Selected Urban Areas',
    'A70': 'Cities',
    'A80': 'Certified Deaths',
}

# just import internally as others won't need to query the data as we will translate it for them in the JSON
age_format_codes = {
    '00': ['0', '1', '2', '3', '4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90-94', '95+', 'Unknown'],
    '01': ['0', '1', '2', '3', '4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+', 'empty24', 'empty25', 'Unknown'],
    '02': ['0', '1-4', 'empty4', 'empty5', 'empty6', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+', 'empty24', 'empty25', 'Unknown'],
    '03': ['0', '1', '2', '3', '4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75+', 'empty22', 'empty23', 'empty24', 'empty25', 'Unknown'],
    '04': ['0', '1-4', 'empty4', 'empty5', 'empty6', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75+', 'empty22', 'empty23', 'empty24', 'empty25', 'Unknown'],
    '05': ['0', '1-4', 'empty4', 'empty5', 'empty6', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70+', 'empty21', 'empty22', 'empty23', 'empty24', 'empty25', 'Unknown'],
    '06': ['0', '1-4', 'empty4', 'empty5', 'empty6', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65+', 'empty20', 'empty21', 'empty22', 'empty23', 'empty24', 'empty25', 'Unknown'],
    '07': ['0', '1-4', 'empty4', 'empty5', 'empty6', '5-14', 'empty8', '15-24', 'empty10', '25-34', 'empty12', '35-44', 'empty14', '45-54', 'empty16', '55-64', 'empty18', '65-74', 'empty20', '75+', 'empty22', 'empty23', 'empty24', 'empty25', 'Unknown'],
    '08': ['0', '1-4', 'empty4', 'empty5', 'empty6', '5-14', 'empty8', '15-24', 'empty10', '25-34', 'empty12', '35-44', 'empty14', '45-54', 'empty16', '55-64', 'empty18', '65+', 'empty20', 'empty21', 'empty22', 'empty23', 'empty24', 'empty25', 'Unknown'],
    '09': ['empty2', 'empty3', 'empty4', 'empty5', 'empty6', 'empty7', 'empty8', 'empty9', 'empty10', 'empty11', 'empty12', 'empty13', 'empty14', 'empty15', 'empty16', 'empty17', 'empty18', 'empty19', 'empty20', 'empty21', 'empty22', 'empty23', 'empty24', 'empty25', 'empty26']
}

# just import internally as others won't need to query the data as we will translate it for them in the JSON
infant_age_format_codes = {
    '01': ['0_days', '1-6_days', '7-27_days', '28-365_days'],
    '02': ['0-6_days', 'empty2', '7-27_days', '28-365_days'],
    '08': ['0-365_days', 'empty2', 'empty3', 'empty4']
}


icd_lists = {'101': "Condensed ICD10 tabulation from WHO docs",
             '103': "3 Character ICD10 codes",
             '104': "4 Character ICD10 codes",
             '10M': "3 and 4 Character ICD10 codes",
             'UE1': "Special Codes for Portugal 2004-2005"}
