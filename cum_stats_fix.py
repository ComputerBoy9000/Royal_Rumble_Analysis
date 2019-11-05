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

for wrestler in RUMBLE_DATA['name'].unique():
    year_count = 0
    elim_count = 0
    time_count = 0
    app_count = 0
    for year in RUMBLE_DATA.loc[RUMBLE_DATA['name'] == wrestler, 'year']:
        RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'prev_app'] = year_count
        if year_count == 0:
            RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'cum_elim'] = 0
            RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'avg_cum_elim'] = 0
            RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'cum_time'] = 0
            RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'avg_cum_time'] = 0
        else:
            
            RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'cum_elim'] = elim_count
            RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'avg_cum_elim'] = elim_count/year_count
            RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'cum_time'] = time_count
            RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                (RUMBLE_DATA['year']== year), 'avg_cum_time'] = time_count/year_count
        year_count += 1

        elim_count += int(RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                        (RUMBLE_DATA['year']== year), 'total_elim'])
        time_count += int(RUMBLE_DATA.loc[(RUMBLE_DATA['name'] == wrestler) &
                                        (RUMBLE_DATA['year']== year), 'total_time'])


RUMBLE_DATA = RUMBLE_DATA.loc[RUMBLE_DATA['year'] != 1988]
RUMBLE_DATA = RUMBLE_DATA.loc[RUMBLE_DATA['year'] != 2018.5]
RUMBLE_DATA = RUMBLE_DATA.loc[RUMBLE_DATA['year'] != 2011]
RUMBLE_DATA.to_csv('/home/christian/Desktop/Royal_Rumble_Analysis/fixed_cum_data.csv')
