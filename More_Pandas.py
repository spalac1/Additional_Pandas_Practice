import pandas as pd
import numpy as np


def answer_one():
    energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skipfooter=38, usecols=(2, 3, 4, 5))
    energy = (energy.rename(columns={'Unnamed: 2': 'Country', 'Petajoules': 'Energy Supply',
                                     'Gigajoules': 'Energy Supply per Capita', '%': '% Renewable'})
              .replace('...', np.nan))
    energy['Energy Supply'] = energy['Energy Supply'].apply(lambda x: x * 1000000)
    energy['Country'] = (energy['Country'].replace({"Republic of Korea": "South Korea",
                                                    "United States of America20": "United States",
                                                    "United Kingdom of Great Britain and Northern Ireland19": "United Kingdom",
                                                    "China, Hong Kong Special Administrative Region3": "Hong Kong"})
                         .str.replace(r"\(.*\)", "")
                         .str.replace('\d+', ''))
    energy['Country'][98] = energy['Country'][98].rstrip()

    GDP = pd.read_csv('world_bank.csv', header=4, usecols=(0, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59))
    GDP['Country Name'] = GDP['Country Name'].replace({"Korea, Rep.": "South Korea",
                                                       "Iran, Islamic Rep.": "Iran",
                                                       "Hong Kong SAR, China": "Hong Kong"})
    GDP = GDP.rename(columns={'Country Name': 'Country'})

    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    ScimEn = (ScimEn.where(ScimEn['Rank'] <= 15.0)
              .dropna())

    energy = energy.set_index('Country')
    GDP = GDP.set_index('Country')
    ScimEn = ScimEn.set_index('Country')

    newish = pd.merge(ScimEn, energy, how='inner', left_index=True, right_index=True)
    newliester = pd.merge(newish, GDP, how='inner', left_index=True, right_index=True)
    return newliester.copy()

%%HTML
<svg width="800" height="300">
  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />
  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />
  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />
  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>
  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>
</svg>


def answer_two():
    energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skipfooter=38, usecols=(2, 3, 4, 5))
    energy = (energy.rename(columns={'Unnamed: 2': 'Country', 'Petajoules': 'Energy Supply',
                                     'Gigajoules': 'Energy Supply per Capita', '%': '% Renewable'})
              .replace('...', np.nan))
    energy['Energy Supply'] = energy['Energy Supply'].apply(lambda x: x * 100000)
    energy['Country'] = (energy['Country'].replace({"Republic of Korea": "South Korea",
                                                    "United States of America20": "United States",
                                                    "United Kingdom of Great Britain and Northern Ireland19": "United Kingdom",
                                                    "China, Hong Kong Special Administrative Region3": "Hong Kong"})
                         .str.replace(r"\(.*\)", "")
                         .str.replace('\d+', ''))
    energy['Country'][98] = energy['Country'][98].rstrip()

    GDP = pd.read_csv('world_bank.csv', header=4, usecols=(0, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59))
    GDP['Country Name'] = GDP['Country Name'].replace({"Korea, Rep.": "South Korea",
                                                       "Iran, Islamic Rep.": "Iran",
                                                       "Hong Kong SAR, China": "Hong Kong"})
    GDP = GDP.rename(columns={'Country Name': 'Country'})

    ScimEn = pd.read_excel('scimagojr-3.xlsx')

    energy = energy.set_index('Country')
    GDP = GDP.set_index('Country')
    ScimEn = ScimEn.set_index('Country')

    newish = pd.merge(ScimEn, energy, how='outer', left_index=True, right_index=True)
    newliester = pd.merge(newish, GDP, how='outer', left_index=True, right_index=True)

    not_filtered = len(newliester.index)

    ScimEn = (ScimEn.where(ScimEn['Rank'] <= 15.0)
              .dropna())

    newerly = pd.merge(ScimEn, energy, how='inner', left_index=True, right_index=True)
    newliestest = pd.merge(newish, GDP, how='inner', left_index=True, right_index=True)

    filtered = len(newliestest.index)

    ans = not_filtered - filtered
    return ans

def answer_three():
    Top15 = answer_one()
    Top15['avgGDP'] = Top15.mean(axis=1)
    avgGDP = pd.Series(Top15['avgGDP'])
    avgGDP = avgGDP.sort_values(ascending = False)
    return avgGDP

def answer_four():
    Top15 = answer_one()
    Top15['avgGDP'] = Top15.mean(axis=1)
    Top15['avgGDP'] = Top15['avgGDP'].astype('float')
    Top15 = Top15.sort_values('avgGDP', ascending = False)
    number6 = Top15.iloc[5]
    ans = number6['2015']-number6['2006']
    return ans

def answer_five():
    Top15 = answer_one()
    ans = Top15['Energy Supply per Capita'].mean()
    return ans

def answer_six():
    Top15 = answer_one()
    best = Top15['% Renewable'].max()
    best_count = (Top15.where(Top15['% Renewable']==best)
                      .dropna())
    best_count = best_count.index[0]
    ans = (best_count, best)
    return ans

def answer_seven():
    Top15 = answer_one()
    Top15['self_to_total_ratio'] = Top15['Self-citations']/Top15['Citations']
    best = Top15['self_to_total_ratio'].max()
    best_count = (Top15.where(Top15['self_to_total_ratio']==best)
                      .dropna())
    best_count = best_count.index[0]
    ans = (best_count, best)
    return ans

def answer_eight():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15 = Top15.sort(['Population'], ascending = False)
    ans = Top15.index[2]
    return ans

def answer_nine():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15['Citable Documents per Person'] = Top15['Citable documents']/Top15['Population']
    ans = Top15['Citable Documents per Person'].corr(Top15['Energy Supply per Capita'])
    return ans


def plot9():
    import matplotlib as plt
    #%matplotlib inline

    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])

plot9()

def answer_ten():
    Top15 = answer_one()
    med = Top15['% Renewable'].median()
    Top15['HighRenew'] = 0
    for i in list(range(0,14)):
        if Top15['% Renewable'][i]>=med:
            Top15['HighRenew'][i] = 1
        else:
            Top15['HighRenew'][i] = 0

    Top15 = Top15.sort(['Rank'])

    HighRenew = pd.Series(Top15['HighRenew'],index=Top15.index)
    return HighRenew

ContinentDict  = {'China':'Asia',
                  'United States':'North America',
                  'Japan':'Asia',
                  'United Kingdom':'Europe',
                  'Russian Federation':'Europe',
                  'Canada':'North America',
                  'Germany':'Europe',
                  'India':'Asia',
                  'France':'Europe',
                  'South Korea':'Asia',
                  'Italy':'Europe',
                  'Spain':'Europe',
                  'Iran':'Asia',
                  'Australia':'Australia',
                  'Brazil':'South America',
                  'Turkey' : 'Europe'}

def answer_eleven():
    Top15 = answer_one()
    Top15['Continent'] = pd.Series(ContinentDict)
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    #this = Top15.groupby('Continent').size()
    that = Top15.groupby('Continent').agg({'Population':['sum','mean','std']})

    #that['size'] = this
    return that

def answer_twelve():
    Top15 = answer_one()
    Top15['Continent'] = pd.Series(ContinentDict)

    ans = Top15.groupby(['Continent',pd.cut(Top15['% Renewable'],5)]).size()
    return ans

def answer_thirteen():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']

    Top15_copy = ["{:,}".format(Top15['Population'][i]) for i in list(range(0,len(Top15['Population'])))]

    ans = pd.Series(Top15_copy,index = Top15.index)
    return ans

def plot_optional():
    import matplotlib as plt
    #%matplotlib inline
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter',
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'],
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. \
This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' \
2014 GDP, and the color corresponds to the continent.")

plot_optional()