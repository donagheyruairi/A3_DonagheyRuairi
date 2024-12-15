import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import numpy as np

import os
print(os.listdir())

import pandas as pd
df = pd.read_csv('states_all_extended.csv')
print(df.head())

west = [
    'ARIZONA', 'CALIFORNIA', 'COLORADO', 'IDAHO', 
    'MONTANA', 'NEVADA', 'NEW_MEXICO', 'OREGON', 
    'UTAH', 'WASHINGTON', 'WYOMING'
]

midwest = [
    'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 
    'MICHIGAN', 'MINNESOTA', 'MISSOURI', 'NEBRASKA', 
    'NORTH_DAKOTA', 'OHIO', 'SOUTH_DAKOTA', 'WISCONSIN'
]

south = [
    'ALABAMA', 'ARKANSAS', 'DELAWARE', 'FLORIDA', 
    'GEORGIA', 'KENTUCKY', 'LOUISIANA', 'MARYLAND', 
    'MISSISSIPPI', 'NORTH_CAROLINA', 'OKLAHOMA', 
    'SOUTH_CAROLINA', 'TENNESSEE', 'TEXAS', 'VIRGINIA', 'WEST_VIRGINIA'
]

northeast = [
    'CONNECTICUT', 'MAINE', 'MASSACHUSETTS', 'NEW_HAMPSHIRE', 
    'NEW_JERSEY', 'NEW_YORK', 'PENNSYLVANIA', 'RHODE_ISLAND', 'VERMONT'
]

alaska_hawaii = ['ALASKA', 'HAWAII']

west_abbr = ['AZ', 'CA', 'CO', 'ID', 'MT', 'NV', 'NM', 'OR', 'UT', 'WA', 'WY']
midwest_abbr = ['IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NE', 'ND', 'OH', 'SD', 'WI']
south_abbr = ['AL', 'AR', 'DE', 'FL', 'GA', 'KY', 'LA', 'MD', 'MS', 'NC', 'OK', 'SC', 'TN', 'TX', 'VA', 'WV']
northeast_abbr = ['CT', 'ME', 'MA', 'NH', 'NJ', 'NY', 'PA', 'RI', 'VT']
alaska_hawaii_abbr = ['AK', 'HI']

regions = [west, midwest, south, northeast, alaska_hawaii]

def get_abbr(state):
    if state in west:
        return west_abbr[west.index(state)]
    if state in midwest:
        return midwest_abbr[midwest.index(state)]
    if state in south:
        return south_abbr[south.index(state)]
    if state in northeast:
        return northeast_abbr[northeast.index(state)]
    if state in alaska_hawaii:
        return alaska_hawaii_abbr[alaska_hawaii.index(state)]

state_maths = df[['STATE', 'YEAR', 'G04_A_A_MATHEMATICS']]
state_maths = state_maths[(state_maths['YEAR'] > 2001) & (state_maths['YEAR'] < 2013) & (state_maths['YEAR']%2 == 1)]

# state_maths['SCALED_MATH'] = np.log10(state_maths['G04_A_A_MATHEMATICS'])
sm_drop = state_maths.dropna(subset=['G04_A_A_MATHEMATICS'])
sm_drop = sm_drop.reset_index(drop=True)

# Jitter the data
jitter_series = [None] * len(sm_drop)

region_averages = {}

for year in sm_drop.YEAR.unique():
    year_data = sm_drop[(sm_drop.YEAR == year) & (sm_drop.STATE != 'NATIONAL') & (sm_drop.STATE != 'DODEA') & (sm_drop.STATE != 'DISTRICT_OF_COLUMBIA')]
    region_averages[year] = {}
    for i, region in enumerate(regions):
        region_data = year_data[year_data.STATE.isin(region)]
        if not region_data.empty:
            region_averages[year][i] = region_data.G04_A_A_MATHEMATICS.mean()
    buckets = np.linspace(year_data.G04_A_A_MATHEMATICS.min() - 0.01, year_data.G04_A_A_MATHEMATICS.max() + 0.01, 40)
    for bucket in buckets:
        year_bucket_slice = year_data[(year_data.G04_A_A_MATHEMATICS > bucket) & (year_data.G04_A_A_MATHEMATICS < bucket + (buckets[1] - buckets[0]))]
        if not year_bucket_slice.empty:
            seperation = np.linspace(-0.8, 0.8, len(year_bucket_slice)) if len(year_bucket_slice) != 1 else np.random.uniform(-0.36, 0.36, 1)
            for matching_index, offset in zip(year_bucket_slice.index, seperation):
                jitter_series[matching_index] = offset

sm_drop.insert(loc=len(sm_drop.columns), column='math_offset', value=jitter_series)

region_names = ['West', 'Midwest', 'South', 'Northeast', 'Alaska & Hawaii']

fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')

from mpl_toolkits.axes_grid1.inset_locator import inset_axes

math4 = inset_axes(ax, '32%', '49%', 'lower right')

for region, name in zip(regions, region_names):
    sm_region = sm_drop[sm_drop.STATE.isin(region)]
    math4.scatter(sm_region.YEAR + sm_region.math_offset, sm_region.G04_A_A_MATHEMATICS, label=name, s=50, alpha=0.75)

for sm in sm_drop.itertuples():
        math4.text(sm.YEAR + sm.math_offset, sm.G04_A_A_MATHEMATICS, get_abbr(sm.STATE), fontsize=5, ha='center', va='center', color='black')	

for year in sm_drop.YEAR.unique():
    if year != 2013:
        math4.axvline(x=year+1, linestyle='-', color='black')
    for i, (region, colour) in enumerate(zip(region_averages[year],['blue', 'orange', 'green', 'red', 'purple'])):
        math4.axhline(y=region_averages[year][region], xmin= ((year - 2003)/10), xmax=((year - 2003 + 2)/10), linestyle='-', color=colour)

math8 = inset_axes(ax, '32%', '49%', 'upper right')
state_maths = df[['STATE', 'YEAR', 'G08_A_A_MATHEMATICS']]
state_maths = state_maths[(state_maths['YEAR'] > 2001) & (state_maths['YEAR'] < 2013) & (state_maths['YEAR']%2 == 1)]

# state_maths['SCALED_MATH'] = np.log10(state_maths['G04_A_A_MATHEMATICS'])
sm_drop = state_maths.dropna(subset=['G08_A_A_MATHEMATICS'])
sm_drop = sm_drop.reset_index(drop=True)

# Jitter the data
jitter_series = [None] * len(sm_drop)

region_averages = {}

for year in sm_drop.YEAR.unique():
    year_data = sm_drop[(sm_drop.YEAR == year) & (sm_drop.STATE != 'NATIONAL') & (sm_drop.STATE != 'DODEA') & (sm_drop.STATE != 'DISTRICT_OF_COLUMBIA')]
    region_averages[year] = {}
    for i, region in enumerate(regions):
        region_data = year_data[year_data.STATE.isin(region)]
        if not region_data.empty:
            region_averages[year][i] = region_data.G08_A_A_MATHEMATICS.mean()
    buckets = np.linspace(year_data.G08_A_A_MATHEMATICS.min() - 0.01, year_data.G08_A_A_MATHEMATICS.max() + 0.01, 40)
    for bucket in buckets:
        year_bucket_slice = year_data[(year_data.G08_A_A_MATHEMATICS > bucket) & (year_data.G08_A_A_MATHEMATICS < bucket + (buckets[1] - buckets[0]))]
        if not year_bucket_slice.empty:
            seperation = np.linspace(-0.8, 0.8, len(year_bucket_slice)) if len(year_bucket_slice) != 1 else np.random.uniform(-0.36, 0.36, 1)
            for matching_index, offset in zip(year_bucket_slice.index, seperation):
                jitter_series[matching_index] = offset

sm_drop.insert(loc=len(sm_drop.columns), column='math_offset', value=jitter_series)

region_names = ['West', 'Midwest', 'South', 'Northeast', 'Alaska & Hawaii']
for region, name in zip(regions, region_names):
    sm_region = sm_drop[sm_drop.STATE.isin(region)]
    math8.scatter(sm_region.YEAR + sm_region.math_offset, sm_region.G08_A_A_MATHEMATICS, label=name, s=50, alpha=0.75)

for sm in sm_drop.itertuples():
    math8.text(sm.YEAR + sm.math_offset, sm.G08_A_A_MATHEMATICS, get_abbr(sm.STATE), fontsize=5, ha='center', va='center', color='black')	

for year in sm_drop.YEAR.unique():
    if year != 2013:
        math8.axvline(x=year+1, linestyle='-', color='black')
    for i, (region, colour) in enumerate(zip(region_averages[year],['blue', 'orange', 'green', 'red', 'purple'])):
        math8.axhline(y=region_averages[year][region], xmin= ((year - 2003)/10), xmax=((year - 2003 + 2)/10), linestyle='-', color=colour)

read8 = inset_axes(ax, '32%', '49%', 'upper center')

state_maths = df[['STATE', 'YEAR', 'G08_A_A_READING']]
state_maths = state_maths[(state_maths['YEAR'] > 2001) & (state_maths['YEAR'] < 2013) & (state_maths['YEAR']%2 == 1)]

# state_maths['SCALED_MATH'] = np.log10(state_maths['G04_A_A_MATHEMATICS'])
sm_drop = state_maths.dropna(subset=['G08_A_A_READING'])
sm_drop = sm_drop.reset_index(drop=True)

# Jitter the data
jitter_series = [None] * len(sm_drop)

region_averages = {}

for year in sm_drop.YEAR.unique():
    year_data = sm_drop[(sm_drop.YEAR == year)&(sm_drop.STATE != 'NATIONAL') & (sm_drop.STATE != 'DODEA')&(sm_drop.STATE != 'DISTRICT_OF_COLUMBIA')]
    region_averages[year] = {}
    for i, region in enumerate(regions):
        region_data = year_data[year_data.STATE.isin(region)]
        if not region_data.empty:
            region_averages[year][i] = region_data.G08_A_A_READING.mean()
    buckets = np.linspace(year_data.G08_A_A_READING.min() - 0.01, year_data.G08_A_A_READING.max() + 0.01, 40)
    for bucket in buckets:
        year_bucket_slice = year_data[(year_data.G08_A_A_READING > bucket) & (year_data.G08_A_A_READING < bucket + (buckets[1] - buckets[0]))]
        if not year_bucket_slice.empty:
            seperation = np.linspace(-0.8, 0.8, len(year_bucket_slice)) if len(year_bucket_slice) != 1 else np.random.uniform(-0.36, 0.36, 1)
            for matching_index, offset in zip(year_bucket_slice.index, seperation):
                jitter_series[matching_index] = offset

sm_drop.insert(loc=len(sm_drop.columns), column='math_offset', value=jitter_series)

region_names = ['West', 'Midwest', 'South', 'Northeast', 'Alaska & Hawaii']
for region, name in zip(regions, region_names):
    sm_region = sm_drop[sm_drop.STATE.isin(region)]
    read8.scatter(sm_region.YEAR + sm_region.math_offset, sm_region.G08_A_A_READING, label=name, s=50, alpha=0.75)

for sm in sm_drop.itertuples():
        read8.text(sm.YEAR + sm.math_offset, sm.G08_A_A_READING, get_abbr(sm.STATE), fontsize=5, ha='center', va='center', color='black')	

for year in sm_drop.YEAR.unique():
    if year != 2013:
        read8.axvline(x=year+1, linestyle='-', color='black')
    for i, (region, colour) in enumerate(zip(region_averages[year],['blue', 'orange', 'green', 'red', 'purple'])):
        read8.axhline(y=region_averages[year][region], xmin= ((year - 2003)/10), xmax=((year - 2003 + 2)/10), linestyle='-', color=colour)

exp = inset_axes(ax, '29%', '70%', 'lower left')

state_maths = df[['STATE', 'YEAR', 'ENROLL', 'TOTAL_EXPENDITURE']]
state_maths = state_maths[(state_maths['YEAR'] > 2002)&(state_maths['YEAR'] < 2013)&(state_maths['YEAR'] % 2 == 1)]
state_maths['EXP_PER_CAP'] = state_maths['TOTAL_EXPENDITURE'] / state_maths['ENROLL']

# state_maths['SCALED_EXP'] = np.log10(state_maths['TOTAL_EXPENDITURE'])
sm_drop = state_maths.dropna(subset=['EXP_PER_CAP'])
sm_drop = sm_drop.reset_index(drop=True)

# Jitter the data
jitter_series = [None] * len(sm_drop)

region_averages = {}

for year in sm_drop.YEAR.unique():
    year_data = sm_drop[(sm_drop.YEAR == year)&(sm_drop.STATE != 'NATIONAL')&(sm_drop.STATE != 'DODEA')&(sm_drop.STATE != 'DISTRICT_OF_COLUMBIA')]
    region_averages[year] = {}
    for i, region in enumerate(regions):
        region_data = year_data[year_data.STATE.isin(region)]
        if not region_data.empty:
            region_averages[year][i] = region_data.EXP_PER_CAP.mean()
    buckets = np.linspace(year_data.EXP_PER_CAP.min() - 0.001, year_data.EXP_PER_CAP.max() + 0.001, 28)
    for bucket in buckets:
        year_bucket_slice = year_data[(year_data.EXP_PER_CAP > bucket) & (year_data.EXP_PER_CAP < bucket + (buckets[1] - buckets[0]))]
        if not year_bucket_slice.empty:
            seperation = np.linspace(-0.8, 0.8, len(year_bucket_slice)) if len(year_bucket_slice) != 1 else np.random.uniform(-0.8, 0.8, 1)
            for matching_index, offset in zip(year_bucket_slice.index, seperation):
                jitter_series[matching_index] = offset

sm_drop.insert(loc=len(sm_drop.columns), column='math_offset', value=jitter_series)

region_names = ['West', 'Midwest', 'South', 'Northeast', 'Alaska & Hawaii']
for i, (region, name) in enumerate(zip(regions, region_names)):
    sm_region = sm_drop[sm_drop.STATE.isin(region)]
    exp.scatter(sm_region.YEAR - sm_region.math_offset , sm_region.EXP_PER_CAP, label=name, s=50, alpha=0.7)
    for sm in sm_region.itertuples():
        exp.text(sm.YEAR - sm.math_offset, sm.EXP_PER_CAP, get_abbr(sm.STATE), fontsize=5, ha='center', va='center', color='black')	

for year in sm_drop.YEAR.unique():
    if year != 2013:
        exp.axvline(x=year+1, linestyle='-', color='black')
    for i, (region, colour) in enumerate(zip(region_averages[year],['blue', 'orange', 'green', 'red', 'purple'])):
        exp.axhline(y=region_averages[year][region], xmin= ((year - 2003)/10), xmax=((year - 2003 + 2)/10), linestyle='-', color=colour)

read4 = inset_axes(ax, '32%', '49%', 'lower center')
state_maths = df[['STATE', 'YEAR', 'G04_A_A_READING']]
state_maths = state_maths[(state_maths['YEAR'] > 2001) & (state_maths['YEAR'] < 2013) & (state_maths['YEAR']%2 == 1)]

sm_drop = state_maths.dropna(subset=['G04_A_A_READING'])
sm_drop = sm_drop.reset_index(drop=True)

jitter_series = [None] * len(sm_drop)

region_averages = {}

for year in sm_drop.YEAR.unique():
    year_data = sm_drop[(sm_drop.YEAR == year)&(sm_drop.STATE != 'NATIONAL') & (sm_drop.STATE != 'DODEA')&(sm_drop.STATE != 'DISTRICT_OF_COLUMBIA')]
    region_averages[year] = {}
    for i, region in enumerate(regions):
        region_data = year_data[year_data.STATE.isin(region)]
        if not region_data.empty:
            region_averages[year][i] = region_data.G04_A_A_READING.mean()
    buckets = np.linspace(year_data.G04_A_A_READING.min() - 0.01, year_data.G04_A_A_READING.max() + 0.01, 40)
    for bucket in buckets:
        year_bucket_slice = year_data[(year_data.G04_A_A_READING > bucket) & (year_data.G04_A_A_READING < bucket + (buckets[1] - buckets[0]))]
        if not year_bucket_slice.empty:
            seperation = np.linspace(-0.8, 0.8, len(year_bucket_slice)) if len(year_bucket_slice) != 1 else np.random.uniform(-0.36, 0.36, 1)
            for matching_index, offset in zip(year_bucket_slice.index, seperation):
                jitter_series[matching_index] = offset

sm_drop.insert(loc=len(sm_drop.columns), column='math_offset', value=jitter_series)

region_names = ['West', 'Midwest', 'South', 'Northeast', 'Alaska & Hawaii']
for region, name in zip(regions, region_names):
    sm_region = sm_drop[sm_drop.STATE.isin(region)]
    read4.scatter(sm_region.YEAR + sm_region.math_offset, sm_region.G04_A_A_READING, label=name, s=50, alpha=0.75)

for sm in sm_drop.itertuples():
        read4.text(sm.YEAR + sm.math_offset, sm.G04_A_A_READING, get_abbr(sm.STATE), fontsize=5, ha='center', va='center', color='black')	

for year in sm_drop.YEAR.unique():
    if year != 2013:
        read4.axvline(x=year+1, linestyle='-', color='black')
    for i, (region, colour) in enumerate(zip(region_averages[year],['blue', 'orange', 'green', 'red', 'purple'])):
        read4.axhline(y=region_averages[year][region], xmin= ((year - 2003)/10), xmax=((year - 2003 + 2)/10), linestyle='-', color=colour)

#titles
math8.set_title('Maths Scores by State for 8th Grade', fontsize=10)
read4.set_title('Reading Scores by State for 4th Grade')
read8.set_title('Reading Scores by State for 8th Grade', fontsize=10)
exp.set_title('Education Expenditure per Capita', fontsize=10)

#axes params
math4.set_xlabel('YEAR')
read4.set_xlabel('YEAR')
exp.set_xlabel('YEAR')


math4.set_ylabel('STATE AVG MATHS SCORE 4th GRADE')
math8.set_ylabel('STATE AVG MATHS SCORE 8th GRADE')
read4.set_ylabel('ENROLL')
read8.set_ylabel('STATE AVG 8th GRADE')
exp.set_ylabel('DOLLARS/STUDENT')

math4.set_xlim(2002, 2012)
math8.set_xlim(2002, 2012)
read4.set_xlim(2002, 2012)
read8.set_xlim(2002, 2012)
exp.set_xlim(2002, 2012)

math4.set_ylim(222, 254)
math8.set_ylim(260, 300)
read4.set_ylim(202, 238)
read8.set_ylim(248.5, 276)
exp.set_ylim(5.57, 23.7)

math4.set_xticks(np.arange(2003, 2013, 2))
exp.set_xticks(np.arange(2003, 2013, 2))

math4.tick_params(labelsize=8)
math8.tick_params(labelsize=8, labelbottom=False)
read8.tick_params(labelsize=8, labelbottom=False)
exp.tick_params(labelsize=8)

plots = [math4, math8, read4, read8, exp]

frames = []
for ax in plots:
    ax.set_visible(True)
    frames_artists = [*ax.get_children()]
    frames.append(frames_artists)

ani = ArtistAnimation(fig, frames, interval=100, blit=True)
fig.canvas.toolbar_visible = False

plt.show()