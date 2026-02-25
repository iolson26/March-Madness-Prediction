import requests
import pandas as pd
from datetime import date, timedelta

def get_games(begin_date,end_date):
    #This function gets all of the games between the two dates imput into the function.
    #Dates must be in the format of year,month,day
    
    #Set up the data frame and csv file
    #Change Collumn Names here if needed
    df = pd.DataFrame(columns=["Conferences"])
    df.to_csv("output_data.csv", index=False)
    
    

    current_date = begin_date
    #Iterate thru all the dates
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        day = current_date.day

        #get data from website and turn into JSON format so its easy to parse later
        url = f"https://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/{year}/{month:02d}/{day:02d}"
        response = requests.get(url)
        status_code = response.status_code
        print("Status code:", response.status_code)
        
        
        if status_code != 200:
            print("DAY SKIPPED, STATUS CODE != 200")
            current_date += timedelta(days=1)
            continue

        data = response.json()
        games = data.get("games", [])
        
        if len(games) >= 500:
            print("WAY TOO MANY GAMES FOR THIS DAY TO BE REAL DATA")
            current_date += timedelta(days=1)
            continue
        print(str(month)+"/"+str(day)+"/"+str(year) +" Number of games today:", len(games))

        #For each game in each particular day do this
        for g in games:
            
            confrences = set(
            pd.read_csv("d1_teams.csv")["Team"]
            )
            
            away_conference = g['game']['away']['conferences'][0]['conferenceName']
            
            if away_conference not in confrences:
                #Data frame the data we just got
                game_data = pd.DataFrame([{
                "Conference": away_conference
                }])
                #Append this dataframe to csv file
                game_data.to_csv(
                "output_data.csv",
                mode="a",
                index=False,
                header=False
                )
            home_conference = g['game']['home']['conferences'][0]['conferenceName']
            
            confrences = set(
            pd.read_csv("d1_teams.csv")["Team"]
            )
            if home_conference not in confrences:
                game_data = pd.DataFrame([{
                "Conference": home_conference
                }])
                #Append this dataframe to csv file
                game_data.to_csv(
                "output_data.csv",
                mode="a",
                index=False,
                header=False
                )
            #Iterate to next day
        current_date += timedelta(days=1)
    print("Games aquired")

#input the two dates here, formmat is in year/month/day
begin_date = date(2018, 11, 10)
end_date   = date(2018, 11, 20)
#call fxn
get_games(begin_date,end_date)