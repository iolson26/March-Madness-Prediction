import requests
import pandas as pd
from datetime import date, timedelta

def get_games(begin_date,end_date):
    #This function gets all of the games between the two dates imput into the function.
    #Dates must be in the format of year,month,day
    
    #Set up the data frame and csv file
    #Change Collumn Names here if needed
    df = pd.DataFrame(columns=["GameID", "Date", "Year", "Home_team", "Away_Team", "Home_winner?","Away_Winner?"])
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
            #In this section get all of the data about the game
            #Its a little clunky bc how I delt with JSON format
            game_code = g['game']['gameID']
            start_date = g['game']['startDate']
            away_team = g['game']['away']['names']['short']
            away_conference = g.get("game", {}).get("away", {}).get("conferenceNames", {}).get("conferenceDivision")
            away_result = g['game']['away']['winner']
            home_team = g['game']['home']['names']['short']
            home_conference = g.get("game", {}).get("home", {}).get("conferenceNames", {}).get("conferenceDivision")
            home_result = g['game']['home']['winner']
            if home_result ==  away_result:
                print("SKIPPING THIS GAME BC BOTH TEAMS HAVE SAME RESULT")
                continue
            #Data frame the data we just got
            game_data = pd.DataFrame([{
            "GameID": game_code,
            "Date": start_date,
            "Year": year,
            "Home_team": home_team,
            "Away_Team": away_team,
            "Home_winner?": home_result,
            "Away_Winner?": away_result,
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
begin_date = date(2023, 3, 13)
end_date   = date(2023, 4, 4)
#call fxn
get_games(begin_date,end_date)