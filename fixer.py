import pandas as pd 


class  PointFixer(object):
    def __init__(self, df, output):
        self.df = df
        self.point_collector = {}
        self.output = output


    def data_load(self):
        df  = self.df
        df = df.fillna(0)
        df = df.drop(['Team EOG Score'], axis = 1)
        return df

    def point_collection(self,df):
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
                self.point_collector[key] = points
                break
            #create dictionary from two columns
            if (row['Month'] != month_tracker) or (row['Day'] != day_tracker):
                key = f'{month_tracker}:{day_tracker}'
                self.point_collector[key] = points
                points = row['Points']
                month_tracker, day_tracker = row['Month'], row['Day']
            else:

                points += row['Points']

    def clean_data(self,df):
        #remove first columng: empty inded
        #df = df.iloc[: , 1:]
        df.astype({'Month': 'string'}).dtypes
        #remove comma from data so it can be a tring 
        df['Day'] = df['Day'].apply(lambda x: x.split(',')[0])
        #turn day and year, EOF Score  into floats 
        df['Day'] = df['Day'].astype(float)
        df['year'] = df['year'].astype(float)
        df['Op EOG Score'] = df['Op EOG Score'].astype(float)

        #replace words with 0
        df['Minutes Played'] = df['Minutes Played'].apply(lambda a: str(0) if a == 'Did Not Play' else a)
        df['Minutes Played'] = df['Minutes Played'].apply(lambda a: str(0) if a == 'Did Not Dress' else a)
        df['Minutes Played'] = df['Minutes Played'].apply(lambda a: str(0) if a == 'Not With Team' else a)


        df['Minutes Played'] = df['Minutes Played'].apply(lambda a: float(str(a).split(':')[0]))
        
        output = self.output
        df.to_csv(output, index = False)

    def point_column_creation(self,df):
        point_list = []

        for index, row in df.iterrows():
            month = row['Month']
            day = row['Day']
            key = f'{month}:{day}'
            points = self.point_collector[key]
            point_list.append(points)
            row['Points'] = points

        df = df.assign(Team_EOG_Score = point_list)
        df = df.rename(columns={"Team_EOG_Score": "Team EOG Score"})
        df = df.reindex(columns=['Starters', 'Minutes Played', 'Field Goals', 'FGA',
            'Field Goal Percentage', '3-Point Field Goals',
            '3-Point Field Goal Attempts', '3-Point Field Goal Percentage',
            'Free Throws', 'Free Throw Attempts', 'Free Throw Percentage',
            'Offensive Rebounds', 'Defensive Rebounds', 'Total Rebounds', 'Assists',
            'Steals', 'Blocks', 'Turnovers', 'Personal Fouls', 'Points', 'Month',
            'Day', 'Opposing Team', 'Team EOG Score', 'Op EOG Score', 'Away',
            'year'],)
        return df

    def correct_data(self):
        loaded_data = self.data_load()
        self.point_collection(loaded_data)
        point_fixed = self.point_column_creation(loaded_data)
        self.clean_data(point_fixed)