# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 11:52:24 2013
commenting rules:
'#%%' is used to create block or 'cell' of code that can be run at one go
### is used for test printing for variables
## is used for single line commenting
# is used for alternate code
@author: Biswanath Banik
"""
#%%
from collections import defaultdict
import numpy as np
#from decimal import Decimal

file1 = open('C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/All_Players.txt','r')
players = file1.readlines()
file1.close()

file2 = open('C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/All_Teams.txt','r')
teams = file2.readlines()
file2.close()

file3 = open('C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/All_Winners.txt','r')
winners = file3.readlines()
file3.close()

file11 = open('C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/all_matchups_converted.txt','r')
matchups = file11.readlines()
file11.close()

players_dict = defaultdict(list)
teams_dict = defaultdict(list)
winners_dict = defaultdict(list)
#%%
## Build the player dictionary with key: <Tournament_Name + Year>
for line in players:  
  line = line.strip()
  line = line.split(',')
  ###print str(len(line))+'\n'
  for i in range (1,len(line)-1,6):
        try :
            players_dict[str(line[0])+'|'+str(line[i])].append((str(line[i+1])+','+str(line[i+2])+','+str(line[i+3])+','+str(line[i+4])+','+str(line[i+5])))
        except ValueError,e :
            continue

## write the player dictionary into a temporary file
fh1 = open("C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/players_temp.txt", 'w') 

for key in players_dict :
  all_players = ''
  for player in list(players_dict[key]):
      all_players = all_players+str(player)+'|' 
  all_players = all_players[:-1]
  fh1.write(key+'|'+all_players+'\n')

fh1.close()
#%%
## Open the 1st temporary file and create a dictionary with key: <Tournament_name + year + playername>
fht1 = open('C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/players_temp.txt','r')
tournament_year = fht1.readlines()
fht1.close()
## create another dictionary
players_dict1 = defaultdict(list)
for line in tournament_year:
    line = line.strip()
    line = line.split('|')
    ###print str(len(line))+'\n'
    for i in range (2,len(line)-1):
        try:
            players_dict1[str(line[0])+'|'+str(line[1])+'|'+str(line[i].split(',')[0])].append((str(line[i].split(',')[1])+'|'+str(line[i].split(',')[2])+'|'+str(line[i].split(',')[3])+'|'+str(line[i].split(',')[4])))
        except ValueError,e:
            continue
        
## write the dictionary into another temporary file
fh11 = open("C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/players_temp1.txt", 'w') 

for key in players_dict1 :
    player_details = ''
    for player in list(players_dict1[key]):
        player_details = player_details+str(player)+'|' 
        player_details = player_details[:-1]
    fh11.write(key+'|'+player_details+'\n')
    #fh11.write(key+'|'+str(players_dict1[key])+'\n')
fh11.close()
#%%
## Create the individual player's data
## read the 2nd temporary file and search for present and past winnings of a player
fht2 = open('C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/players_temp1.txt','r')
tournament_year_player = fht2.readlines()
fht2.close()

player_dict = defaultdict(list)

for line in tournament_year_player:
    line = line.strip()
    line = line.split('|')
    player_name = line[2]
    height = int(line[3])
    if (height == -0): ## impute missing heights by the median of heights which is 185.0
        height = 185
        print 'imputing height'
    weight = int(line[4])
    if (weight == -0): ## impute missing weights by the median of weights which is 175.0
        weight = 175
        print 'imputing weight'
    if(line[5] == 'Left'):
        is_left_hand = 1
    else:
        is_left_hand = 0 # for both right handed and ambidextrous players & missing values
    current_year_grandslam_wins = 0
    past_wins = 0
    past_clay_wins = 0
    past_grass_wins = 0
    past_hard_wins = 0
    recentness = []
    last_year_clay_win = 0
    last_year_grass_win = 0
    last_year_hard_win = 0
    
    for matchup in matchups:
        matchup = matchup.strip()
        matchup = matchup.split(',')
        ## if the player is part of the winning team
        if((((player_name == matchup[2])|(player_name == matchup[3]))&(matchup[6] == 1)) | (((player_name == matchup[4])|(player_name == matchup[5]))&(matchup[6] == 0))):
            ## Find current year grand slam wins
            if(matchup[1] == line[1]): ## check for current year
                if((matchup[0] == 'Australian_Open') & ((line[0] == 'Roland_Garros') | (line[0] == 'Wimbledon') | (line[0] == 'US_Open'))):
                    current_year_grandslam_wins = current_year_grandslam_wins + 1
                    recentness.append(int(matchup[1]) - 1989)
                elif ((matchup[0] == 'Roland_Garros') & ((line[0] == 'Wimbledon') | (line[0] == 'US_Open'))):
                    current_year_grandslam_wins = current_year_grandslam_wins + 1
                    recentness.append(int(matchup[1]) - 1989)
                elif ((matchup[0] == 'Wimbledon') & (line[0] == 'US_Open')):
                    current_year_grandslam_wins = current_year_grandslam_wins + 1
                    recentness.append(int(matchup[1]) - 1989)
                    
            elif(matchup[1] < line[1]): ## for previous years
                past_wins = past_wins + 1
                if(matchup[0]=='Roland_Garros'):
                    past_clay_wins = past_clay_wins + 1
                    if (int(matchup[1]) == (int(line[1]) - 1)):
                        last_year_clay_win = last_year_clay_win + 1
                elif (matchup[0] == 'Wimbledon'):
                    past_grass_wins = past_grass_wins + 1
                    if (int(matchup[1]) == (int(line[1]) - 1)):
                        last_year_grass_win = last_year_grass_win + 1
                else:
                    past_hard_wins = past_hard_wins + 1
                    if (int(matchup[1]) == (int(line[1]) - 1)):
                        last_year_hard_win = last_year_hard_win + 1
                recentness.append(int(matchup[1]) - 1989)
                
    if(len(recentness) > 0):
        max_recentness = np.max(recentness)
    else:
        max_recentness = 0

    try:
        player_dict[str(line[0])+','+str(line[1])+','+str(line[2])].append((str(height)+','+str(weight)+','+str(is_left_hand)+','+str(line[6])+','+str(past_wins)+','+str(past_clay_wins)+','+str(past_grass_wins)+','+str(past_hard_wins)+','+str(max_recentness)+','+str(last_year_clay_win)+','+str(last_year_grass_win)+','+str(last_year_hard_win)+','+str(current_year_grandslam_wins)))
    
    except ValueError,e:
        continue

## write the final output file for individual player's details or Relational Data
fh111 = open("C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Individual.txt", 'w') 

for key in player_dict :
    player_details = ''
    for player in list(player_dict[key]):
        player_details = player_details+str(player)+',' 
        player_details = player_details[:-1]
    fh111.write(key+','+player_details+'\n')
    #fh11.write(key+'|'+str(players_dict1[key])+'\n')
fh111.close()             
#%%

## read each team's players list and compute composite variables
file4 = open('C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Individual.txt','r')
individual_records = file4.readlines()
file4.close()

team_dict = defaultdict(list)

for team in teams:
    team = team.strip()
    team = team.split(',')
    for i in range (1,len(team)-1,3):
        player1 = team[i+1]
        player2 = team[i+2]
        for record in individual_records:
            record = record.strip()
            record = record.split(',')
            if ((team[0] == record[0]) & (team[i] == record[1])): ## match tournament name and year
                if (record[2] == player1):
                    player1_height = int(record[3])
                    player1_weight = int(record[4])
                    player1_is_left_hand = int(record[5])
                    player1_country = record[6]
                    player1_past_wins = int(record[8])
                    player1_past_clay_wins = int(record[9])
                    player1_past_grass_wins = int(record[10])
                    player1_past_hard_wins = int(record[11])
                    player1_recentness = int(record[12])
                    player1_last_year_clay_win = int(record[13])
                    player1_last_year_grass_win = int(record[14])
                    player1_last_year_hard_win = int(record[15])
                    player1_current_year_grandslam_wins = int(record[16])
                elif (record[2] == player2):
                    player2_height = int(record[3])
                    player2_weight = int(record[4])
                    player2_is_left_hand = int(record[5])
                    player2_country = record[6]
                    player2_past_wins = int(record[8])
                    player2_past_clay_wins = int(record[9])
                    player2_past_grass_wins = int(record[10])
                    player2_past_hard_wins = int(record[11])
                    player2_recentness = int(record[12])
                    player2_last_year_clay_win = int(record[13])
                    player2_last_year_grass_win = int(record[14])
                    player2_last_year_hard_win = int(record[15])
                    player2_current_year_grandslam_wins = int(record[16])
                    # whether the team won the game or not
                    team_current_win = record[7]
        sum_height = (player1_height + player2_height)
        sum_weight = (player1_weight + player2_weight)
        diff_height = np.absolute(player1_height - player2_height)
        diff_weight = np.absolute(player1_weight - player2_weight)
        if (player1_is_left_hand | player2_is_left_hand):
            atleast_one_left_hand = 1
        else:
            atleast_one_left_hand = 0
        if (player1_country == player2_country):
            is_same_country = 1
        else:
            is_same_country = 0
        tot_past_wins_ind = (player1_past_wins + player2_past_wins)
        tot_past_clay_wins_ind= (player1_past_clay_wins + player2_past_clay_wins)
        tot_past_grass_wins_ind= (player1_past_grass_wins + player2_past_grass_wins)
        tot_past_hard_wins_ind= (player1_past_hard_wins + player2_past_hard_wins)
        if (player1_recentness > player2_recentness):
            max_recentness = player1_recentness
        else:
            max_recentness = player2_recentness
        tot_last_year_clay_win = (player1_last_year_clay_win + player2_last_year_clay_win)
        tot_last_year_grass_win = (player1_last_year_grass_win + player2_last_year_grass_win)
        tot_last_year_hard_win = (player1_last_year_hard_win + player2_last_year_hard_win)
        tot_current_year_grandslam_wins = (player1_current_year_grandslam_wins + player2_current_year_grandslam_wins)                      
        try:
            team_dict[str(team[0])+','+str(team[i])+','+str(player1)+','+str(player2)].append(str(sum_height)+','+str(diff_height)+','+str(sum_weight)+','+str(diff_weight)+','+str(atleast_one_left_hand)+','+str(is_same_country)+','+str(tot_past_wins_ind)+','+str(tot_past_clay_wins_ind)+','+str(tot_past_grass_wins_ind)+','+str(tot_past_hard_wins_ind)+','+str(max_recentness)+','+str(tot_last_year_clay_win)+','+str(tot_last_year_grass_win)+','+str(tot_last_year_hard_win)+','+str(tot_current_year_grandslam_wins)+','+str(team_current_win))
        except ValueError,e:
            continue

## write the final output file for team's Composite data
fh2 = open("C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Composite.txt", 'w') 
for key in team_dict :
    team_details = ''
    for team in list(team_dict[key]):
        team_details = team_details+str(team)+',' 
        team_details = team_details[:-1]
    fh2.write(key+','+team_details+'\n')
    #fh2.write(key+'|'+str(players_dict1[key])+'\n')
fh2.close() 
#%%
## compute Relational metrices
relational_dict = defaultdict(list)

for team in teams:
    team = team.strip()
    team = team.split(',')
    for i in range (1,len(team)-1,3):
        player1 = team[i+1]
        player2 = team[i+2]
        past_together_count = 0
        past_together_wins = 0
        recentness_together = []
        
        for line in teams:
            line = line.strip()
            line = line.split(',')
            for j in range (1,len(line)-1,3):
                if (line[j] < team[i]): ## for previous year matches
                    if(((player1==line[j+1])&(player2==line[j+2])) | ((player1==line[j+2])&(player2==line[j+1]))):
                        past_together_count = past_together_count + 1
                        
                        for winner in winners:
                            winner = winner.strip()
                            winner = winner.split(',')
                            if((line[0]==winner[0])&(line[j]==winner[1])):
                                for k in range(2,len(winner)-1,2):
                                    if(((player1==winner[k])&(player2==winner[k+1]))|((player1==winner[k+1])&(player2==winner[k]))):
                                        past_together_wins = past_together_wins + 1
                                        recentness_together.append(int(winner[1]) - 1989)
        if (past_together_wins>0):
            past_win_rate = past_together_wins / float(past_together_count)
        else:
            past_win_rate = 0
            
        if(len(recentness_together) > 0):
            max_recent_together = np.max(recentness_together)
        else:
            max_recent_together = 0
            
        ## Find out the current game result
        current_game_result = 0
        for winner in winners:
            winner = winner.strip()
            winner = winner.split(',')
            if ((winner[0] == team[0])&(winner[1] == team[i])):
                for k in range(2,len(winner)-1,2):
                                    if(((player1==winner[k])&(player2==winner[k+1]))|((player1==winner[k+1])&(player2==winner[k]))):
                                        current_game_result = 1
                
            
        try:
            relational_dict[str(team[0])+','+str(team[i])+','+str(player1)+','+str(player2)].append(str(past_together_count)+','+str(past_together_wins)+','+str(past_win_rate)+','+str(max_recent_together)+','+str(current_game_result))
        except ValueError,e:
            continue
## write the final output file for team's Relational data
fh3 = open("C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Relational.txt", 'w') 
for key in relational_dict:
    team_details = ''
    for team in list(relational_dict[key]):
        team_details = team_details+str(team)+',' 
        team_details = team_details[:-1]
    fh3.write(key+','+team_details+'\n')
    #fh2.write(key+'|'+str(players_dict1[key])+'\n')
fh3.close()

#%%
## Combine Composite and Relational metrices
combined_dict = defaultdict(list)

file5 = open('C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Composite.txt','r')
composites = file5.readlines()
file5.close()

file6 = open('C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Relational.txt','r')
relationals = file6.readlines()
file6.close()

for line1 in composites:
    line1 = line1.strip()
    line1 = line1.split(',')
    for line2 in relationals:
        line2 = line2.strip()
        line2 = line2.split(',')
        if (((line1[0]==line2[0])&(line1[1]==line2[1])&(line1[2]==line2[2])&(line1[3]==line2[3]))|((line1[0]==line2[0])&(line1[1]==line2[1])&(line1[2]==line2[3])&(line1[3]==line2[2]))):
            combined_dict[str(line1[0])+','+str(line1[1])+','+str(line1[2])+','+str(line1[3])].append(str(line1[4])+','+str(line1[5])+','+str(line1[6])+','+str(line1[7])+','+str(line1[8])+','+str(line1[9])+','+str(line1[10])+','+str(line1[11])+','+str(line1[12])+','+str(line1[13])+','+str(line1[14])+','+str(line1[15])+','+str(line1[16])+','+str(line1[17])+','+str(line1[18])+','+str(line2[4])+','+str(line2[5])+','+str(line2[6])+','+str(line2[7])+','+str(line1[19]))
        
## write the final output file for team's Relational data
fh4 = open("C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Combined.txt", 'w') 
for key in combined_dict:
    team_details = ''
    for team in list(combined_dict[key]):
        team_details = team_details+str(team)+',' 
        team_details = team_details[:-1]
    fh4.write(key+','+team_details+'\n')
fh4.close()

'''
#%%
## Compute Ecological metrices for only finalists teams (old data)
## First identify the playing two teams
file7 = open('C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Finalist_teams.txt','r')
finalists = file7.readlines()
file7.close()

ecology_dict = defaultdict(list)
###fh6 = open("C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Ecological_test.txt", 'w')

for line1 in finalists:
    line1 = line1.strip()
    line1 = line1.split(',')
    team1_with_team2 = []
    team2_with_team1 = []
    matches_with_A = 0
    matches_with_B = 0
    matches_with_C = 0
    matches_with_D = 0
    
    team1_against_team2 = []
    team2_against_team1 = []
    matches_against_A = 0
    matches_against_B = 0
    matches_against_C = 0
    matches_against_D = 0
    
    ## [line1[2]=A, line1[3]=B, line1[4]=C, line1[5]=D]; team1 = {A,B}, team2 = {C,D}
    
    ## for playing in the same team in the past
    
    for line2 in teams:
        line2 = line2.strip()
        line2 = line2.split(',')
        for i in range(1,len(line2)-1,3):
            ###fh6.write(str(line2[i])+'\n')
            if(line2[i] < line1[1]): ## for past playing years
                
                ## <A,C> pairings
                if(((line1[2]==line2[i+1])&(line1[4]==line2[i+2]))|((line1[2]==line2[i+2])&(line1[4]==line2[i+1]))): ## if <A,C> pair exists
                    team1_with_team2.append(str(line1[4]))
                    team2_with_team1.append(str(line1[2]))
                    matches_with_A = matches_with_A + 1
                    matches_with_C = matches_with_C + 1
                    ###fh6.write(str(matches_with_A)+','+str(matches_with_C)+'\n')
                
                ## <A,D> pairings 
                elif(((line1[2]==line2[i+1])&(line1[5]==line2[i+2]))|((line1[2]==line2[i+2])&(line1[5]==line2[i+1]))):
                    team1_with_team2.append(str(line1[5]))
                    team2_with_team1.append(str(line1[2]))
                    matches_with_A = matches_with_A + 1
                    matches_with_D = matches_with_D + 1
                    ###fh6.write(str(matches_with_A)+','+str(matches_with_D)+'\n')
                
                ## <B,C> pairings 
                elif(((line1[3]==line2[i+1])&(line1[4]==line2[i+2]))|((line1[3]==line2[i+2])&(line1[4]==line2[i+1]))):
                    team1_with_team2.append(str(line1[4]))
                    team2_with_team1.append(str(line1[3]))
                    matches_with_B = matches_with_B + 1
                    matches_with_C = matches_with_C + 1
                    ###fh6.write(str(matches_with_B)+','+str(matches_with_C)+'\n')
                    
                ## <B,D> pairings 
                elif(((line1[3]==line2[i+1])&(line1[5]==line2[i+2]))|((line1[3]==line2[i+2])&(line1[5]==line2[i+1]))):
                    team1_with_team2.append(str(line1[5]))
                    team2_with_team1.append(str(line1[3]))
                    matches_with_B = matches_with_B + 1
                    matches_with_D = matches_with_D + 1
                    ###fh6.write(str(matches_with_B)+','+str(matches_with_D)+'\n')
                ###else:
                    ###fh6.write('no match found'+'\n')
    
    ## for playing against each other in past
    
    for line3 in finalists:
        line3 = line3.strip()
        line3 = line3.split(',')
        #for i in range(2,5,2):
            
        if(line3[1] < line1[1]): ## for past playing years
                
            ## <A,C> pairings
            if((((line1[2]==line3[2])|(line1[2]==line3[3]))&((line1[4]==line3[4])|(line1[4]==line3[5])))|(((line1[2]==line3[4])|(line1[2]==line3[5]))&((line1[4]==line3[2])|(line1[4]==line3[3])))): 
                team1_against_team2.append(str(line1[4]))
                team2_against_team1.append(str(line1[2]))
                matches_against_A = matches_against_A + 1
                matches_against_C = matches_against_C + 1
                
                
            ## <A,D> pairings 
            if((((line1[2]==line3[2])|(line1[2]==line3[3]))&((line1[5]==line3[4])|(line1[5]==line3[5])))|(((line1[2]==line3[4])|(line1[2]==line3[5]))&((line1[5]==line3[2])|(line1[5]==line3[3])))): 
                team1_against_team2.append(str(line1[5]))
                team2_against_team1.append(str(line1[2]))
                matches_against_A = matches_against_A + 1
                matches_against_D = matches_against_D + 1
                
            ## <B,C> pairings 
            if((((line1[3]==line3[2])|(line1[3]==line3[3]))&((line1[4]==line3[4])|(line1[4]==line3[5])))|(((line1[3]==line3[4])|(line1[3]==line3[5]))&((line1[4]==line3[2])&(line1[4]==line3[3])))): 
                team1_against_team2.append(str(line1[4]))
                team2_against_team1.append(str(line1[3]))
                matches_against_B = matches_against_B + 1
                matches_against_C = matches_against_C + 1
                    
            ## <B,D> pairings 
            if((((line1[3]==line3[2])|(line1[3]==line3[3]))&((line1[5]==line3[4])|(line1[5]==line3[5])))|(((line1[3]==line3[4])|(line1[3]==line3[5]))&((line1[5]==line3[2])|(line1[5]==line3[3])))): 
                team1_against_team2.append(str(line1[5]))
                team2_against_team1.append(str(line1[3]))
                matches_against_B = matches_against_B + 1
                matches_against_D = matches_against_D + 1          
    
    sum_match_count_playing_together = matches_with_C + matches_with_D
    sum_match_count_playing_against = matches_against_C + matches_against_D
                    
    diff_player_count_playing_together = len(set(team1_with_team2)) - len(set(team2_with_team1))
    diff_player_count_playing_against = len(set(team1_against_team2)) - len(set(team2_against_team1))
    
    interaction_together = (diff_player_count_playing_together * sum_match_count_playing_together)
    
    interaction_against = (diff_player_count_playing_against * sum_match_count_playing_against)
    
    
    team1_win = 1
    
    try:
        ecology_dict[str(line1[0])+','+str(line1[1])].append(str(line1[2])+','+str(line1[3])+','+str(line1[4])+','+str(line1[5])+','+str(diff_player_count_playing_together)+','+str(sum_match_count_playing_together)+','+str(interaction_together)+','+str(diff_player_count_playing_against)+','+str(sum_match_count_playing_against)+','+str(interaction_against)+','+str(team1_win))
    except ValueError,e:
        continue
###fh6.close()

## write the final output file for team's Ecological data
fh5 = open("C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Ecological_old.txt", 'w') 
for key in ecology_dict:
    team_details = ''
    for team in list(ecology_dict[key]):
        team_details = team_details+str(team)+',' 
        team_details = team_details[:-1]
    fh5.write(key+','+team_details+'\n')
fh5.close()   
'''
#%%
## Compute Ecological metrices for Two Team Matchups (New Data)
## First identify the playing two teams

ecology_dict = defaultdict(list)
fh6 = open("C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Ecological_test.txt", 'w')

for line1 in matchups:
    line1 = line1.strip()
    line1 = line1.split(',')
    team1_with_team2 = []
    team2_with_team1 = []
    matches_with_A = 0
    matches_with_B = 0
    matches_with_C = 0
    matches_with_D = 0
    
    team1_against_team2 = []
    team2_against_team1 = []
    matches_against_A = 0
    matches_against_B = 0
    matches_against_C = 0
    matches_against_D = 0
    
  ## [line1[2]=A, line1[3]=B, line1[4]=C, line1[5]=D]; team1 = {A,B}, team2 = {C,D}, team1_win=line1[6]
    
    ## for playing in the same team in the past
    
    for line2 in teams:
        line2 = line2.strip()
        line2 = line2.split(',')
        for i in range(1,len(line2)-1,3):
            ###fh6.write(str(line2[i])+'\n')
            if(line2[i] < line1[1]): ## for past playing years
                                
                ## <A,C> pairings
                if(((line1[2]==line2[i+1])&(line1[4]==line2[i+2]))|((line1[2]==line2[i+2])&(line1[4]==line2[i+1]))): ## if <A,C> pair exists
                    team1_with_team2.append(str(line1[4]))
                    team2_with_team1.append(str(line1[2]))
                    matches_with_A = matches_with_A + 1
                    matches_with_C = matches_with_C + 1
                    fh6.write(str(matches_with_A)+','+str(matches_with_C)+'\n')
                
## We are using elif instead of if because each of past team form teams can match up to only one of the 4 pairs possible here.
                ## <A,D> pairings 
                elif(((line1[2]==line2[i+1])&(line1[5]==line2[i+2]))|((line1[2]==line2[i+2])&(line1[5]==line2[i+1]))):
                    team1_with_team2.append(str(line1[5]))
                    team2_with_team1.append(str(line1[2]))
                    matches_with_A = matches_with_A + 1
                    matches_with_D = matches_with_D + 1
                    fh6.write(str(matches_with_A)+','+str(matches_with_D)+'\n')
                
                ## <B,C> pairings 
                elif(((line1[3]==line2[i+1])&(line1[4]==line2[i+2]))|((line1[3]==line2[i+2])&(line1[4]==line2[i+1]))):
                    team1_with_team2.append(str(line1[4]))
                    team2_with_team1.append(str(line1[3]))
                    matches_with_B = matches_with_B + 1
                    matches_with_C = matches_with_C + 1
                    fh6.write(str(matches_with_B)+','+str(matches_with_C)+'\n')
                    
                ## <B,D> pairings 
                elif(((line1[3]==line2[i+1])&(line1[5]==line2[i+2]))|((line1[3]==line2[i+2])&(line1[5]==line2[i+1]))):
                    team1_with_team2.append(str(line1[5]))
                    team2_with_team1.append(str(line1[3]))
                    matches_with_B = matches_with_B + 1
                    matches_with_D = matches_with_D + 1
                    fh6.write(str(matches_with_B)+','+str(matches_with_D)+'\n')
                else:
                    fh6.write('no match found for same team'+'\n')
    
    ## for playing against each other in past
    
    for line3 in matchups:
        line3 = line3.strip()
        line3 = line3.split(',')
        #for i in range(2,5,2):
        pairing_found = 0
            
        if(line3[1] < line1[1]): ## for past playing years
                
            ## <A,C> pairings
            if((((line1[2]==line3[2])|(line1[2]==line3[3]))&((line1[4]==line3[4])|(line1[4]==line3[5])))|(((line1[2]==line3[4])|(line1[2]==line3[5]))&((line1[4]==line3[2])|(line1[4]==line3[3])))): 
                team1_against_team2.append(str(line1[4]))
                team2_against_team1.append(str(line1[2]))
                matches_against_A = matches_against_A + 1
                matches_against_C = matches_against_C + 1
                pairing_found = pairing_found + 1
                fh6.write(str(matches_against_A)+','+str(matches_against_C)+'\n')
                
                
            ## <A,D> pairings 
            if((((line1[2]==line3[2])|(line1[2]==line3[3]))&((line1[5]==line3[4])|(line1[5]==line3[5])))|(((line1[2]==line3[4])|(line1[2]==line3[5]))&((line1[5]==line3[2])|(line1[5]==line3[3])))): 
                team1_against_team2.append(str(line1[5]))
                team2_against_team1.append(str(line1[2]))
                matches_against_A = matches_against_A + 1
                matches_against_D = matches_against_D + 1
                pairing_found = pairing_found + 1
                fh6.write(str(matches_against_A)+','+str(matches_against_D)+'\n')
                
            ## <B,C> pairings 
            if((((line1[3]==line3[2])|(line1[3]==line3[3]))&((line1[4]==line3[4])|(line1[4]==line3[5])))|(((line1[3]==line3[4])|(line1[3]==line3[5]))&((line1[4]==line3[2])&(line1[4]==line3[3])))): 
                team1_against_team2.append(str(line1[4]))
                team2_against_team1.append(str(line1[3]))
                matches_against_B = matches_against_B + 1
                matches_against_C = matches_against_C + 1
                pairing_found = pairing_found + 1
                fh6.write(str(matches_against_B)+','+str(matches_against_C)+'\n')
                    
            ## <B,D> pairings 
            if((((line1[3]==line3[2])|(line1[3]==line3[3]))&((line1[5]==line3[4])|(line1[5]==line3[5])))|(((line1[3]==line3[4])|(line1[3]==line3[5]))&((line1[5]==line3[2])|(line1[5]==line3[3])))): 
                team1_against_team2.append(str(line1[5]))
                team2_against_team1.append(str(line1[3]))
                matches_against_B = matches_against_B + 1
                matches_against_D = matches_against_D + 1
                pairing_found = pairing_found + 1
                fh6.write(str(matches_against_B)+','+str(matches_against_D)+'\n')
        
        if(pairing_found == 0):
            fh6.write('no match found for playing against'+'\n')
        
    sum_match_count_playing_together = matches_with_C + matches_with_D
    sum_match_count_playing_against = matches_against_C + matches_against_D
                    
    diff_player_count_playing_together = len(set(team1_with_team2)) - len(set(team2_with_team1))
    diff_player_count_playing_against = len(set(team1_against_team2)) - len(set(team2_against_team1))
    
    sum_player_count_playing_together = len(set(team1_with_team2)) + len(set(team2_with_team1))
    sum_player_count_playing_against = len(set(team1_against_team2)) + len(set(team2_against_team1))
    
    interaction_together = (diff_player_count_playing_together * sum_match_count_playing_together)
    
    interaction_against = (diff_player_count_playing_against * sum_match_count_playing_against)
        
    team1_win = line1[6]
    
    try:
        ecology_dict[str(line1[0])+','+str(line1[1])+','+str(line1[2])+','+str(line1[3])+','+str(line1[4])+','+str(line1[5])].append(str(diff_player_count_playing_together)+','+str(sum_match_count_playing_together)+','+str(interaction_together)+','+str(diff_player_count_playing_against)+','+str(sum_match_count_playing_against)+','+str(interaction_against)+','+str(team1_win)+','+str(sum_player_count_playing_together)+','+str(sum_player_count_playing_against))
    except ValueError,e:
        continue
fh6.close()

## write the final output file for team's Ecological data
fh8 = open("C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Ecological.txt", 'w') 
for key in ecology_dict:
    team_details = ''
    for team in list(ecology_dict[key]):
        team_details = team_details+str(team)+',' 
        team_details = team_details[:-1]
    fh8.write(key+','+team_details+'\n')
fh8.close() 

#%%
## Create combined data at two-team level
file8 = open('C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Ecological.txt','r')
ecologicals = file8.readlines()
file8.close()

file9 = open('C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Combined.txt','r')
combined = file9.readlines()
file9.close()

ecology_combined_dict = defaultdict(list)
fh7 = open("C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Ecological_Combined_test.txt", 'w')

i = 1
for line1 in ecologicals:
    line1 = line1.strip()
    line1 = line1.split(',')
    counter = 0
    
    
    ## Performance improvement by stopping the inner for loop upon finding both the teams
    
    for line2 in combined:
        line2 = line2.strip()
        line2 = line2.split(',')
        
        #print str(line1)+str(line2)
           
        ## collect Team1 values
        if (((line1[0]==line2[0])&(line1[1]==line2[1])&(line1[2]==line2[2])&(line1[3]==line2[3]))|((line1[0]==line2[0])&(line1[1]==line2[1])&(line1[2]==line2[3])&(line1[3]==line2[2]))):
                       
            team1_Sum_height = int(line2[4])
            team1_Diff_height = int(line2[5])
            team1_Sum_weight = int(line2[6])
            team1_Diff_weight = int(line2[7])
            team1_atleast_one_left_hand = int(line2[8])
            team1_is_same_country = int(line2[9])
            team1_tot_past_wins_individual = int(line2[10])
            team1_tot_past_claycourt_wins_individual = int(line2[11])
            team1_tot_past_grasscourt_wins_individual = int(line2[12])
            team1_tot_past_hardcourt_wins_individual = int(line2[13])
            team1_max_recentness = int(line2[14])
            team1_tot_last_year_clay_win = int(line2[15])
            team1_tot_last_year_grass_win = int(line2[16])
            team1_tot_last_year_hard_win = int(line2[17])
            team1_tot_current_year_grandslam_wins = int(line2[18])
            team1_games_played_in_past_together = int(line2[19])
            team1_games_won_in_past_together = int(line2[20])
            team1_win_rate = float(line2[21])
            team1_max_recent_together = int(line2[22])
            counter = counter + 1
            print 'inside 1st if \n'
            
            
            
        ## collect Team2 values    
        elif(((line1[0]==line2[0])&(line1[1]==line2[1])&(line1[4]==line2[2])&(line1[5]==line2[3]))|((line1[0]==line2[0])&(line1[1]==line2[1])&(line1[4]==line2[3])&(line1[5]==line2[2]))):
                        
            team2_Sum_height = int(line2[4])
            team2_Diff_height = int(line2[5])
            team2_Sum_weight = int(line2[6])
            team2_Diff_weight = int(line2[7])
            team2_atleast_one_left_hand = int(line2[8])
            team2_is_same_country = int(line2[9])
            team2_tot_past_wins_individual = int(line2[10])
            team2_tot_past_claycourt_wins_individual = int(line2[11])
            team2_tot_past_grasscourt_wins_individual = int(line2[12])
            team2_tot_past_hardcourt_wins_individual = int(line2[13])
            team2_max_recentness = int(line2[14])
            team2_tot_last_year_clay_win = int(line2[15])
            team2_tot_last_year_grass_win = int(line2[16])
            team2_tot_last_year_hard_win = int(line2[17])
            team2_tot_current_year_grandslam_wins = int(line2[18])
            team2_games_played_in_past_together = int(line2[19])
            team2_games_won_in_past_together = int(line2[20])
            team2_win_rate = float(line2[21])
            team2_max_recent_together = int(line2[22])
            counter = counter + 1
            print 'inside 2nd if \n'
        
        if(counter == 2):
            fh7.write('info found for both the teams for row number:'+str(i)+'\n')
            break
    
    delta_Sum_height = team1_Sum_height - team2_Sum_height
    delta_Diff_height = team1_Diff_height - team2_Diff_height
    delta_Sum_weight = team1_Sum_weight - team2_Sum_weight
    delta_Diff_weight = team1_Diff_weight - team2_Diff_weight
    delta_atleast_one_left_hand = team1_atleast_one_left_hand - team2_atleast_one_left_hand
    delta_is_same_country = team1_is_same_country - team2_is_same_country
    delta_tot_past_wins_individual = team1_tot_past_wins_individual - team2_tot_past_wins_individual
    delta_tot_past_claycourt_wins_individual = team1_tot_past_claycourt_wins_individual - team2_tot_past_claycourt_wins_individual
    delta_tot_past_grasscourt_wins_individual = team1_tot_past_grasscourt_wins_individual - team2_tot_past_grasscourt_wins_individual
    delta_tot_past_hardcourt_wins_individual = team1_tot_past_hardcourt_wins_individual - team2_tot_past_hardcourt_wins_individual
    delta_max_recentness = team1_max_recentness - team2_max_recentness
    delta_tot_last_year_clay_win = team1_tot_last_year_clay_win - team2_tot_last_year_clay_win
    delta_tot_last_year_grass_win = team1_tot_last_year_grass_win - team2_tot_last_year_grass_win
    delta_tot_last_year_hard_win = team1_tot_last_year_hard_win - team2_tot_last_year_hard_win
    delta_tot_current_year_grandslam_wins = team1_tot_current_year_grandslam_wins - team2_tot_current_year_grandslam_wins
    delta_games_played_in_past_together = team1_games_played_in_past_together - team2_games_played_in_past_together
    delta_games_won_in_past_together = team1_games_won_in_past_together - team2_games_won_in_past_together
    delta_win_rate = team1_win_rate - team2_win_rate
    delta_max_recent_together = team1_max_recent_together - team2_max_recent_together
    
    fh7.write('variables created for matchups for row number:'+str(i)+'\n')
    
    ## create dummy variables 'Grass_Court' , 'Hard_Court' keeping 'Clay_Court' as base for regression analysis
    if (line1[0] == 'Roland_Garros'):
        Grass_Court = 0
        Hard_Court = 0
    elif (line1[0] == 'Wimbledon'):
        Grass_Court = 1
        Hard_Court = 0
    else: ## It is US_Open or Australian_Open
        Grass_Court = 0
        Hard_Court = 1
    fh7.write('Dummy variables created for row number:'+str(i)+'\n')
    
    try:
        
        ecology_combined_dict[str(line1[0])+','+str(line1[1])+','+str(line1[2])+','+str(line1[3])+','+str(line1[4])+','+str(line1[5])].append(str(line1[6])+','+str(line1[7])+','+str(line1[8])+','+str(line1[9])+','+str(line1[10])+','+str(line1[11])+','+str(delta_Sum_height)+','+str(delta_Diff_height)+','+str(delta_Sum_weight)+','+str(delta_Diff_weight)+','+str(delta_atleast_one_left_hand)+','+str(delta_is_same_country)+','+str(delta_tot_past_wins_individual)+','+str(delta_tot_past_claycourt_wins_individual)+','+str(delta_tot_past_grasscourt_wins_individual)+','+str(delta_tot_past_hardcourt_wins_individual)+','+str(delta_max_recentness)+','+str(delta_tot_last_year_clay_win)+','+str(delta_tot_last_year_grass_win)+','+str(delta_tot_last_year_hard_win)+','+str(delta_tot_current_year_grandslam_wins)+','+str(delta_games_played_in_past_together)+','+str(delta_games_won_in_past_together)+','+str(delta_win_rate)+','+str(delta_max_recent_together)+','+str(Grass_Court)+','+str(Hard_Court)+','+str(line1[12]))
        
        
    except ValueError,e:
        print 'inside exception\n'
        continue  
    fh7.write('Added to Dictionary for row number:'+str(i)+'\n')
    i = i + 1
fh7.close()
    
## write the final output file for team's Ecological Combined data
fh9 = open("C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Ecological_Combined.txt", 'w') 
for key in ecology_combined_dict:
    team_details = ''
    for team in list(ecology_combined_dict[key]):
        team_details = team_details+str(team)+',' 
        team_details = team_details[:-1]
    fh9.write(key+','+team_details+'\n')
fh9.close() 
#%%
''' 
#%%
## Randomize the Ecological Combined data set to have 50% rows where Team1 lost the game
file10 = open('C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Ecological_Combined.txt','r')
ec_data = file10.readlines()
file10.close()

ec_randomized_dict = defaultdict(list)
counter = 1

for line in ec_data:
    line = line.strip()
    line = line.split(',')
        
    if ((counter % 2) != 0):
        team1_player1 = line[2]
        team1_player2 = line[3]
        team2_player1 = line[4]
        team2_player2 = line[5]
        Diff_player_count_playing_together = int(line[6])
        Sum_match_count_playing_together = int(line[7])
        Interaction_together = int(line[8])
        Diff_player_count_playing_against = int(line[9])
        Sum_match_count_playing_against = int(line[10])
        Interaction_against = int(line[11])
        delta_Sum_height = int(line[12])
        delta_Diff_height = int(line[13])
        delta_Sum_weight = int(line[14])
        delta_Diff_weight = int(line[15])
        delta_atleast_one_left_hand = int(line[16])
        delta_is_same_country = int(line[17])
        delta_tot_past_wins_individual = int(line[18])
        delta_tot_past_claycourt_wins_individual = int(line[19])
        delta_tot_past_grasscourt_wins_individual = int(line[20])
        delta_tot_past_hardcourt_wins_individual = int(line[21])
        delta_max_recentness = int(line[22])
        delta_tot_last_year_clay_win = int(line[23])
        delta_tot_last_year_grass_win = int(line[24])
        delta_tot_last_year_hard_win = int(line[25])
        delta_tot_current_year_grandslam_wins = int(line[26])
        delta_games_played_in_past_together = int(line[27])
        delta_games_won_in_past_together = int(line[28])
        delta_win_rate = float(line[29])
        delta_max_recent_together = int(line[30])
        Team1_win = int(line[31])
        
    else:
        team1_player1 = line[4]
        team1_player2 = line[5]
        team2_player1 = line[2]
        team2_player2 = line[3]
        Diff_player_count_playing_together = int(line[6]) * (-1)
        Sum_match_count_playing_together = int(line[7])
        Interaction_together = int(line[8]) * (-1)
        Diff_player_count_playing_against = int(line[9]) * (-1)
        Sum_match_count_playing_against = int(line[10])
        Interaction_against = int(line[11]) * (-1)
        delta_Sum_height = int(line[12]) * (-1)
        delta_Diff_height = int(line[13]) * (-1)
        delta_Sum_weight = int(line[14]) * (-1)
        delta_Diff_weight = int(line[15]) * (-1)
        delta_atleast_one_left_hand = int(line[16]) * (-1)
        delta_is_same_country = int(line[17]) * (-1)
        delta_tot_past_wins_individual = int(line[18]) * (-1)
        delta_tot_past_claycourt_wins_individual = int(line[19]) * (-1)
        delta_tot_past_grasscourt_wins_individual = int(line[20]) * (-1)
        delta_tot_past_hardcourt_wins_individual = int(line[21]) * (-1)
        delta_max_recentness = int(line[22]) * (-1)
        delta_tot_last_year_clay_win = int(line[23]) * (-1)
        delta_tot_last_year_grass_win = int(line[24]) * (-1)
        delta_tot_last_year_hard_win = int(line[25]) * (-1)
        delta_tot_current_year_grandslam_wins = int(line[26]) * (-1)
        delta_games_played_in_past_together = int(line[27]) * (-1)
        delta_games_won_in_past_together = int(line[28]) * (-1)
        delta_win_rate = float(line[29]) * (-1)
        delta_max_recent_together = int(line[30]) * (-1)
        Team1_win = int(line[31]) - 1
    
    counter = counter + 1
    
    ## create dummy variables 'Grass_Court' , 'Hard_Court' keeping 'Clay_Court' as base
    if (line[0] == 'Roland_Garros'):
        Grass_Court = 0
        Hard_Court = 0
    elif (line[0] == 'Wimbledon'):
        Grass_Court = 1
        Hard_Court = 0
    else:
        Grass_Court = 0
        Hard_Court = 1
    
    try:
        ec_randomized_dict[str(line[0])+','+str(line[1])].append(str(team1_player1)+','+str(team1_player2)+','+str(team2_player1)+','+str(team2_player2)+','+str(Diff_player_count_playing_together)+','+str(Sum_match_count_playing_together)+','+str(Interaction_together)+','+str(Diff_player_count_playing_against)+','+str(Sum_match_count_playing_against)+','+str(Interaction_against)+','+str(delta_Sum_height)+','+str(delta_Diff_height)+','+str(delta_Sum_weight)+','+str(delta_Diff_weight)+','+str(delta_atleast_one_left_hand)+','+str(delta_is_same_country)+','+str(delta_tot_past_wins_individual)+','+str(delta_tot_past_claycourt_wins_individual)+','+str(delta_tot_past_grasscourt_wins_individual)+','+str(delta_tot_past_hardcourt_wins_individual)+','+str(delta_max_recentness)+','+str(delta_tot_last_year_clay_win)+','+str(delta_tot_last_year_grass_win)+','+str(delta_tot_last_year_hard_win)+','+str(delta_tot_current_year_grandslam_wins)+','+str(delta_games_played_in_past_together)+','+str(delta_games_won_in_past_together)+','+str(delta_win_rate)+','+str(delta_max_recent_together)+','+str(Grass_Court)+','+str(Hard_Court)+','+str(Team1_win))
        
    except ValueError,e:
        continue 


## write the final output file for team's Ecological Combined randomized data
fh7 = open("C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Data/Ecological_Combined_randomized.txt", 'w') 
for key in ec_randomized_dict:
    team_details = ''
    for team in list(ec_randomized_dict[key]):
        team_details = team_details+str(team)+',' 
        team_details = team_details[:-1]
    fh7.write(key+','+team_details+'\n')
fh7.close()        
               
#%%
## test code

#np.median(weights) #175
#np.mean(weights) #175.413
#np.mean(heights) # 185.1739
#np.median(heights) #185.0
'''
