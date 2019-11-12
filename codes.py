
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
    'A10': 'Survery',
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
    '00': ['all_ages', '0', '1', '2', '3', '4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90-94', '95+', 'Unknown'],
    '01': ['all_ages', '0', '1', '2', '3', '4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+', None, None, 'Unknown'],
    '02': ['all_ages', '0', '1-4', None, None, None, '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+', None, None, 'Unknown'],
    '03': ['all_ages', '0', '1', '2', '3', '4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75+', None, None, None, None, 'Unknown'],
    '04': ['all_ages', '0', '1-4', None, None, None, '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75+', None, None, None, None, 'Unknown'],
    '05': ['all_ages', '0', '1-4', None, None, None, '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70+', None, None, None, None, None, 'Unknown'],
    '06': ['all_ages', '0', '1-4', None, None, None, '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65+', None, None, None, None, None, None, 'Unknown'],
    '07': ['all_ages', '0', '1-4', None, None, None, '5-14', None, '15-24', None, '25-34', None, '35-44', None, '45-54', None, '55-64', None, '65-74', None, '75+', None, None, None, None, 'Unknown'],
    '08': ['all_ages', '0', '1-4', None, None, None, '5-14', None, '15-24', None, '25-34', None, '35-44', None, '45-54', None, '55-64', None, '65+', None, None, None, None, None, None, 'Unknown'],
    '09': ['all_ages', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
}

# just import internally as others won't need to query the data as we will translate it for them in the JSON
infant_age_format_codes = {
    '01': ['0 day', '1-6 days', '7-27 days', '28-365 days'],
    '02': ['0-6 days', None, '7-27 days', '28-365 days'],
    '03': ['0-365 days', None, None, None]
}
