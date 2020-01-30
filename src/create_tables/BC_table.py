import numpy as np
import pandas as pd


def fix_a_row(row):
    # lst = row.split()
    # words = [x for x in lst if (x.strip('.').isalpha() or any(i in x for i in ['#','-',"'",'(']))]
    # stats = [x for x in lst if not (x.strip('.').isalpha() or any(i in x for i in ['#','-',"'",'(']))]

    lst = row

    lst_difficulties = ["Adv.", "Advanced", "Exp", "Low", "Hike"]
    
    if lst[-2] in lst_difficulties:
        level = [' '.join(lst[-2:])]
        trail_name = [' '.join(lst[1:-10])]
        stats = lst[-10:-2]
    else:
        level = [lst[-1]]
        trail_name = [' '.join(lst[1:-9])]
        stats = lst[-9:-1]
    
    if lst[1] == 'Beginner' and lst[2] == 'Terrain':
        trail_name = [lst[1] + ' ' + lst[2]]
        level = [lst[-1]]
        stats = ['0', '0'] + lst[3:-1]
        ### FIGURE THIS OUT!!!
    new_row = trail_name + stats + level
    
    return new_row


def make_dataframe(filename):
    with open(filename) as f:
        stuff = f.read()
    
    lst_stuff_split = stuff.split('\n')
    
    lst_level_endings = ['Advanced',
                         'Beginner',
                         'Bowl',
                         'Expert',
                         'Glade',
                         'Intermediate',
                         'Novice',
                         'To']

    trail_rows = []

    for row in lst_stuff_split:
        if len(row.split()) > 1 and (row.split()[-1] in lst_level_endings):
            trail_rows.append(row.split())

    # TODO: Which resorts does this apply to?
    # for row in trail_rows:
    #     if (len(row) >= 1) and (row[-1] == "%"):            
    #         trail_rows.append(row + ' Advanced Intermediate') # change THIS or something like it to deal with Vail line splits (in name and ability level)
            

    list_of_lists = []


    for row in trail_rows:
        list_of_lists.append(fix_a_row(row))
        
    colnames = ['trail_name', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'slope_length_(ft)', 'avg_width_(ft)', 'slope_area_(acres)', 'avg_grade_(%)', 'max_grade_(%)', 'ability_level']

    df = pd.DataFrame(list_of_lists, columns=colnames)
    return df
    

def fix_dtype(filename,resort,location):
    '''
    Inputs:
    filename: .txt file (str)
    resort: resort name (str)
    location: city (str)
    '''
    df = make_dataframe(filename)
    
    df['bottom_elev_(ft)'][df['trail_name'] == 'Beginner Terrain'] = '8100'
    
    columns_to_change = ['top_elev_(ft)',
                         'bottom_elev_(ft)',
                         'vert_rise_(ft)',
                         'slope_length_(ft)',
                         'avg_width_(ft)',
                         'slope_area_(acres)']

    for column in columns_to_change:
        df[column] = df[column].apply(lambda x: x.replace(',','')).astype(float)
    
    df['slope_area_(acres)'] = df['slope_area_(acres)'].astype(float)
    
    for column in ['max_grade_(%)','avg_grade_(%)']:
        df[column] = df[column].apply(lambda x: x.replace('%','')).astype(float)
    
    df['resort'] = resort
    df['location'] = location
    df['top_elev_(ft)'][df['trail_name'] == 'Beginner Terrain'] = df['bottom_elev_(ft)'] + df['vert_rise_(ft)']
    
    return df



'''
figure out how to deal with multi lines for Vail
'''


'''
add columns for 
-grooming
-face
-ski area
'''
