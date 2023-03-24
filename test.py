import pandas as pd 


df = pd.read_csv('2010.csv')
df = df.fillna(0)
df = df.drop(['Team EOG Score'], axis = 1)

point_collector = {}

points = 0

month_tracker = None
day_tracker = None

for index, row in df.iterrows():
   if (month_tracker == None) and (day_tracker == None):
      month_tracker = row['Month']
      day_tracker = row['Day']


   if index == df.index[-1]:
      key = f'{month_tracker}:{day_tracker}'
      points += row['Points']
      print(points)
      point_collector[key] = points
      break
   #create dictionary from two columns
   if (row['Month'] != month_tracker) or (row['Day'] != day_tracker):
      key = f'{month_tracker}:{day_tracker}'
      point_collector[key] = points
      points = row['Points']
      month_tracker, day_tracker = row['Month'], row['Day']
   else:

      points += row['Points']






l = []

for index, row in df.iterrows():
    month = row['Month']
    day = row['Day']
    key = f'{month}:{day}'
    points = point_collector[key]
    l.append(points)
    row['Points'] = points

df = df.assign(Team_EOG_Score =l)
df = df.rename(columns={"Team_EOG_Score": "Team EOG Score"})
df = df.reindex(columns=['Starters', 'Minutes Played', 'Field Goals', 'FGA',
       'Field Goal Percentage', '3-Point Field Goals',
       '3-Point Field Goal Attempts', '3-Point Field Goal Percentage',
       'Free Throws', 'Free Throw Attempts', 'Free Throw Percentage',
       'Offensive Rebounds', 'Defensive Rebounds', 'Total Rebounds', 'Assists',
       'Steals', 'Blocks', 'Turnovers', 'Personal Fouls', 'Points', 'Month',
       'Day', 'Opposing Team', 'Team EOG Score', 'Op EOG Score', 'Away',
       'year'],)

df.to_csv('fixed.csv')
