import pandas as pd

RUMBLE_DATA = pd.read_csv('/home/christian/Desktop/Royal_Rumble_Analysis/RumbleData.csv').copy()

def time_cleaner(time_string):
    """
    Convert video timestamps into seconds
    """
    return 3600*int(time_string[0]) + 60*int(time_string[1]) + int(time_string[2])

RUMBLE_DATA['entry_time'] = RUMBLE_DATA['entry_time'].astype(str)
RUMBLE_DATA['exit_time'] = RUMBLE_DATA['exit_time'].astype(str)
ENTRY_TIME_SPLIT = RUMBLE_DATA['entry_time'].str.split(':')
EXIT_TIME_SPLIT = RUMBLE_DATA['exit_time'].str.split(':')

RUMBLE_DATA['entry_time'] = ENTRY_TIME_SPLIT.apply(time_cleaner)
RUMBLE_DATA['exit_time'] = EXIT_TIME_SPLIT.apply(time_cleaner)

for year in RUMBLE_DATA['year'].unique():
    RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'entry_time'] = (RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'entry_time'] -
                                                                  RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'entry_time'].min())

    RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'exit_time'] = (RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'exit_time'] -
                                                                RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'entry_time'].min())

RUMBLE_DATA['total_time'] = RUMBLE_DATA['exit_time'] - RUMBLE_DATA['entry_time']
RUMBLE_DATA['total_elim'] = (RUMBLE_DATA['solo_elim'] + RUMBLE_DATA['group_elim'] + 
                             RUMBLE_DATA['illegal_elim'])

MATCH_DATA = pd.DataFrame()

for year in RUMBLE_DATA['year'].unique():
    entry_times = RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'entry_time'].unique().tolist()
    exit_times = RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'exit_time'].unique().tolist()
    split_times = entry_times + exit_times
    split_times.sort()
    year_list = []
    for i in range(len(split_times)):
        year_list.append(year)
    year_series = pd.Series(year_list)
    split_series = pd.Series(split_times)
    year_split = pd.concat([year_series, split_series], axis=1)
    MATCH_DATA = pd.concat([MATCH_DATA, year_split], axis=0)

MATCH_DATA.columns = ['year', 'split']

print(MATCH_DATA)
