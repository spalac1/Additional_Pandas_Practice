import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import csv
import datetime as dt

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ],
    columns=["State", "RegionName"]  )

    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''

    tobegin = pd.read_csv('university_towns.txt', sep='\n', header=None, names='t')
    lst = []
    st = ''
    reg = ''
    for i in list(range(0, len(tobegin['t']))):
        if '[ed' in tobegin['t'][i]:
            st = tobegin['t'][i].split('[ed')
            st = st[0]
        else:
            reg = tobegin['t'][i].split(' (')
            reg = reg[0]
            lst.append([st, reg])

    UniTowns = pd.DataFrame(lst, columns=['State', 'RegionName'])

    return UniTowns


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a
    string value in a format such as 2005q3'''

    GDP = pd.read_excel('gdplev.xls', skiprows=219, usecols=(4, 6))
    GDP = GDP.rename(columns={"1999q4": "Quarter", 12323.3: "GDP in Chained Dollars"})

    i = 0
    recbeg = ''
    while i <= len(GDP['GDP in Chained Dollars']) and i < len(GDP['GDP in Chained Dollars']) - 4:
        if GDP['GDP in Chained Dollars'][i] > GDP['GDP in Chained Dollars'][i + 1] and GDP['GDP in Chained Dollars'][
            i + 1] > GDP['GDP in Chained Dollars'][i + 2]:
            if GDP['GDP in Chained Dollars'][i + 2] < GDP['GDP in Chained Dollars'][i + 3] and \
                    GDP['GDP in Chained Dollars'][i + 3] < GDP['GDP in Chained Dollars'][i + 4]:
                recbeg = GDP['Quarter'][i - 1]
        i += 1

    return recbeg

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a
    string value in a format such as 2005q3'''
    GDP = pd.read_excel('gdplev.xls', skiprows = 219, usecols = (4,6))
    GDP = GDP.rename(columns = {"1999q4":"Quarter", 12323.3:"GDP in Chained Dollars"})

    i=0
    recend=''
    while i <= len(GDP['GDP in Chained Dollars']) and i < len(GDP['GDP in Chained Dollars'])-4:
        if GDP['GDP in Chained Dollars'][i]>GDP['GDP in Chained Dollars'][i+1] and GDP['GDP in Chained Dollars'][i+1]>GDP['GDP in Chained Dollars'][i+2]:
            if GDP['GDP in Chained Dollars'][i+2]<GDP['GDP in Chained Dollars'][i+3] and GDP['GDP in Chained Dollars'][i+3]<GDP['GDP in Chained Dollars'][i+4]:
                recend=GDP['Quarter'][i+4]
        i+=1
    return recend


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a
    string value in a format such as 2005q3'''

    GDP = pd.read_excel('gdplev.xls', skiprows=219, usecols=(4, 6))
    GDP = GDP.rename(columns={"1999q4": "Quarter", 12323.3: "GDP in Chained Dollars"})

    i = 0
    recbot = ''
    while i <= len(GDP['GDP in Chained Dollars']) and i < len(GDP['GDP in Chained Dollars']) - 4:
        if GDP['GDP in Chained Dollars'][i] > GDP['GDP in Chained Dollars'][i + 1] and GDP['GDP in Chained Dollars'][
            i + 1] > GDP['GDP in Chained Dollars'][i + 2]:
            if GDP['GDP in Chained Dollars'][i + 2] < GDP['GDP in Chained Dollars'][i + 3] and \
                    GDP['GDP in Chained Dollars'][i + 3] < GDP['GDP in Chained Dollars'][i + 4]:
                recbot = GDP['Quarter'][i + 2]
        i += 1
    return recbot


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.

    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''

    useful_cols = list([1, 2]) + list(np.arange(51, 251))

    df = pd.read_csv('City_Zhvi_AllHomes.csv', skiprows=0, header=0, usecols=(useful_cols))

    df['State'] = df['State'].replace(states)

    df = brah.set_index(['State', 'RegionName'])

    df.columns = pd.to_datetime(df.columns)

    df = df.resample('Q', axis=1).mean()
    df = df.rename(columns=lambda x: str(x.to_period('Q')).lower())

    return df


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''

    UniTowns = get_list_of_university_towns()
    recbeg = get_recession_start()
    recbot = get_recession_bottom()
    housingdata = convert_housing_data_to_quarters()

    housingdata['ratio'] = housingdata[recbeg] / housingdata[recbot]

    UniTowns_list = UniTowns.to_records(index=False).tolist()

    group1 = housingdata.loc[UniTowns_list]
    group2 = housingdata.loc[-housingdata.index.isin(UniTowns_list)]
    ans = ttest_ind(group1['ratio'], group2['ratio'], equal_var=True, nan_policy='omit')

    if ans[1] < .01:
        if ans[0] < 0:
            this = (True, ans[1], "university town")
        else:
            this = (True, ans[1], "non-university town")
    else:
        if ans[0] < 0:
            this = (False, ans[1], "university town")
        else:
            this = (False, ans[1], "non-university town")
    return this