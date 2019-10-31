import numpy as np
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

RUMBLE_DATA['break_begin'] = RUMBLE_DATA['break_begin'].fillna(0)
break_starts = RUMBLE_DATA.loc[RUMBLE_DATA['break_begin'] != 0, 'break_begin'] 
break_starts = break_starts.astype(str).str.split(':').apply(time_cleaner)
RUMBLE_DATA.loc[RUMBLE_DATA['break_begin'] != 0, 'break_begin'] = break_starts

RUMBLE_DATA['break_end'] = RUMBLE_DATA['break_end'].fillna(0)
break_ends = RUMBLE_DATA.loc[RUMBLE_DATA['break_end'] != 0, 'break_end'] 
break_ends = break_ends.astype(str).str.split(':').apply(time_cleaner)
RUMBLE_DATA.loc[RUMBLE_DATA['break_end'] != 0, 'break_end'] = break_ends

RUMBLE_DATA['total_break'] = RUMBLE_DATA['break_end'] - RUMBLE_DATA['break_begin']

RUMBLE_DATA['break'] = RUMBLE_DATA['break'].fillna(0)
RUMBLE_DATA.loc[RUMBLE_DATA['total_break'] > 0, 'break'] = 1



for year in RUMBLE_DATA['year'].unique():
    RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'exit_time'] = (RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'exit_time'] -
                                                                RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'entry_time'].min())

    RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'entry_time'] = (RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'entry_time'] -
                                                                  RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'entry_time'].min())

    
RUMBLE_DATA['total_time'] = RUMBLE_DATA['exit_time'] - RUMBLE_DATA['entry_time'] - RUMBLE_DATA['total_break']
RUMBLE_DATA['total_elim'] = (RUMBLE_DATA['solo_elim'] + RUMBLE_DATA['group_elim'] + 
                             RUMBLE_DATA['illegal_elim'])

RUMBLE_DATA['tag_partner'] = RUMBLE_DATA['tag_partner'].fillna(0)

MATCH_DATA = pd.DataFrame()

state_dict = {}

for year in RUMBLE_DATA['year'].unique():
    year_state_dict = {}
    entry_times = RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'entry_time'].unique().tolist()
    exit_times = RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'exit_time'].unique().tolist()
    split_times = entry_times + exit_times
    split_times.sort()
    entry_times.sort()
    exit_times.sort()
    
    year_list = []
    for i in range(len(split_times)):
        year_list.append(year)
    year_series = pd.Series(year_list)
    split_series = pd.Series(split_times)
    entry_series = pd.Series(entry_times)
    exit_series = pd.Series(exit_times)
    year_split = pd.concat([year_series, split_series, entry_series, exit_series], axis=1)
    MATCH_DATA = pd.concat([MATCH_DATA, year_split], axis=0)

MATCH_DATA.columns = ['year', 'split', 'entry_split', 'exit_split']

for wrestler in RUMBLE_DATA['name'].unique():
    year_count = 0
    elim_count = 0
    time_count = 0
    app_count = 0
    for year in RUMBLE_DATA.loc[RUMBLE_DATA['name'] == wrestler, 'year']:
        RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'prev_app'] = year_count
        year_count += 1
        elim_count += int(RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                        (RUMBLE_DATA['year']== year), 'total_elim'])
        time_count += int(RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                        (RUMBLE_DATA['year']== year), 'total_time'])
        RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'cum_elim'] = elim_count
        RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'avg_cum_elim'] = elim_count/year_count
        RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'cum_time'] = time_count
        RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'avg_cum_time'] = time_count/year_count                       


world_title_dict = eval(open('/home/christian/Desktop/Royal_Rumble_Analysis/world_title_dict','r').read())
us_title_dict = eval(open('/home/christian/Desktop/Royal_Rumble_Analysis/US_title_dict','r').read())
ic_title_dict = eval(open('/home/christian/Desktop/Royal_Rumble_Analysis/IC_Title_dict').read())

RUMBLE_DATA['world_reigns'] = RUMBLE_DATA['world_reigns'].fillna(0)
RUMBLE_DATA['us_reigns'] = RUMBLE_DATA['us_reigns'].fillna(0)
RUMBLE_DATA['ic_reigns' ]= RUMBLE_DATA['ic_reigns'].fillna(0)

for year in world_title_dict.keys():
    for wrestler in list(world_title_dict[year].keys()):
        if wrestler in RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'name'].tolist():
            RUMBLE_DATA.loc[(RUMBLE_DATA['year'] == year) 
                                & (RUMBLE_DATA['name'] == wrestler), 'world_reigns'] = world_title_dict[year][wrestler]

    
for year in us_title_dict.keys():
    for wrestler in list(us_title_dict[year].keys()):
        if wrestler in RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'name'].tolist():
            RUMBLE_DATA.loc[(RUMBLE_DATA['year'] == year) 
                                & (RUMBLE_DATA['name'] == wrestler), 'us_reigns'] = us_title_dict[year][wrestler]

for year in ic_title_dict.keys():
    for wrestler in list(ic_title_dict[year].keys()):
        if wrestler in RUMBLE_DATA.loc[RUMBLE_DATA['year'] == year, 'name'].tolist():
            RUMBLE_DATA.loc[(RUMBLE_DATA['year'] == year) 
                                & (RUMBLE_DATA['name'] == wrestler), 'ic_reigns'] = ic_title_dict[year][wrestler] 


RUMBLE_DATA = RUMBLE_DATA.fillna(0)

RUMBLE_DATA.to_csv('/home/christian/Desktop/Royal_Rumble_Analysis/Rumble_Data_Cleaned.csv')
MATCH_DATA.to_csv('/home/christian/Desktop/Royal_Rumble_Analysis/Match_Data.csv')


