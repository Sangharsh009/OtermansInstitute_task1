import json
import pandas as pd
import numpy as np

with open("task.json", encoding='utf-8') as f:
    task = json.load(f)

User_purchasing_info = {
    title: [] for title in ["User_ID","User_Name", "ItemCost", 'ItemName','PurchaseDate']
}

user_details = {
    title: [] for title in ["User_ID","User_Name", "Skill_Level", "Total_Coins", "User_Age"]
}

game_session_details = {
    title: [] for title in ["User_ID","User_Name", "Date", "CourseTitle", "GameMode", "GameSessionId", "Station",  "Time_Taken", "Total_Correct_Attempt","Total_Error_Attempt", "Total_Question_Attempt"]
}

overall_session_details = {
    title: [] for title in ["User_ID","User_Name", "Date", "Session_ID", "Overall_Correct_Attempt","Overall_Error_Attempt", "Overall_Question_Attempt", "Overall_Time_Taken"]
}

time_spent_on_details = {
    title: [] for title in ["User_ID","User_Name", "TimeSpentOn_AI","TimeSpentOn_FillintheBlanks","TimeSpentOn_Lesson","TimeSpentOn_MainMenu","TimeSpentOn_Map","TimeSpentOn_MatchFollowings","TimeSpentOn_Quiz","TimeSpentOn_Selection","TimeSpentOn_Store","TimeSpentOn_TrueFalse","TimeSpentOn_Unscramble"]
}

for user_id in task.keys():
    purchase_info = task[user_id] 
    user_n = purchase_info['UserDetails']
    user_name = user_n.get("UserName", None)
    if purchase_info and "PurchaseDetails" in purchase_info.keys():
        purchase_details = purchase_info['PurchaseDetails']
    else:
        continue
    for purchase in purchase_details:
        User_purchasing_info['User_ID'].append(user_id)
        User_purchasing_info['User_Name'].append(user_name)
        if purchase and "ItemCost" in purchase.keys():
            User_purchasing_info['ItemCost'].append(float(purchase.get('ItemCost', 0)))
        else:
            User_purchasing_info['ItemCost'].append(0)
        if purchase and 'ItemName' in purchase.keys():
            User_purchasing_info['ItemName'].append(purchase.get('ItemName', " "))
        else:
            User_purchasing_info['ItemName'].append(" ")
        if purchase and 'PurchaseDate' in purchase.keys():
            User_purchasing_info['PurchaseDate'].append(purchase.get('PurchaseDate', 0))
        else:
            User_purchasing_info['PurchaseDate'].append(0)

df = pd.DataFrame(User_purchasing_info)

for user_id in task.keys():
     main_user_info = task[user_id]
     if main_user_info and "UserDetails" in main_user_info.keys():
          main_user_details = main_user_info['UserDetails']
     else:
          continue
     if main_user_details and 'UserID' in main_user_details.keys():
          user_details['User_ID'].append(main_user_details.get('UserID', " "))
     if main_user_details and 'UserName' in main_user_details.keys():
          user_details['User_Name'].append(main_user_details.get('UserName', " "))
     if main_user_details and 'SkillLevel' in main_user_details.keys():
          user_details['Skill_Level'].append(main_user_details.get('SkillLevel', " "))
     if main_user_details and 'TotalCoins' in main_user_details.keys():
          user_details['Total_Coins'].append(main_user_details.get('TotalCoins', 0))
     if main_user_details and 'UserAge' in main_user_details.keys():
          user_details['User_Age'].append(main_user_details.get('UserAge', 0))          

user_info_df = pd.DataFrame(user_details)

for user_id in task.keys():
     session_info = task[user_id]
     user_n = session_info['UserDetails']
     user_name = user_n.get("UserName", None)
     if session_info and "SessionDetails" in session_info.keys():
          session_info_detailed = session_info["SessionDetails"]
     else:
          continue
     for session in session_info_detailed:
          if session and "GameSessionDetails" in session.keys():
               for game_sessions in session['GameSessionDetails']:
                    game_session_details['User_ID'].append(user_id)
                    game_session_details['User_Name'].append(user_name)
                    game_session_details["Date"].append(session.get("Date", np.nan))  
                    if game_sessions and "CourseTitle" in game_sessions.keys():
                         game_session_details['CourseTitle'].append(game_sessions.get("CourseTitle", " "))
                    if game_sessions and "GameMode" in game_sessions.keys():
                         game_session_details['GameMode'].append(game_sessions.get("GameMode", " "))
                    if game_sessions and "GameSessionId" in game_sessions.keys():
                         game_session_details['GameSessionId'].append(game_sessions.get("GameSessionId", " "))
                    if game_sessions and "Station" in game_sessions.keys():
                         game_session_details['Station'].append(game_sessions.get("Station", " "))
                    if game_sessions and "TimeTaken" in game_sessions.keys():
                         game_session_details['Time_Taken'].append(game_sessions.get("TimeTaken", np.nan))
                    if game_sessions and "TotalCorrectAttempt" in game_sessions.keys():
                         game_session_details['Total_Correct_Attempt'].append(game_sessions.get("TotalCorrectAttempt", np.nan))
                    if game_sessions and "TotalErrorAttempt" in game_sessions.keys():
                         game_session_details['Total_Error_Attempt'].append(game_sessions.get("TotalErrorAttempt", np.nan))
                    if game_sessions and "TotalQuestionAttempt" in game_sessions.keys():
                         game_session_details['Total_Question_Attempt'].append(game_sessions.get("TotalQuestionAttempt",np.nan))
          if session and "OverallResult" in session.keys():
               overall_session_details['User_ID'].append(user_id)
               overall_session_details['User_Name'].append(user_name)
               overall_session_details["Date"].append(session.get("Date", np.nan)) 
               overall_session_details['Overall_Correct_Attempt'].append(session['OverallResult'].get('TotalCorrectAttempts', np.nan))
               overall_session_details['Overall_Error_Attempt'].append(session['OverallResult'].get('TotalErrorAttempts', np.nan))
               overall_session_details['Overall_Question_Attempt'].append(session['OverallResult'].get('TotalQuestionAttempts', np.nan))
               overall_session_details['Overall_Time_Taken'].append(session['OverallResult'].get('TotalTimeSpent', np.nan))
               overall_session_details["Session_ID"].append(session.get("SessionID", np.nan))
          if session and "TimeSpent" in session.keys():
               time_spent_on_details['User_ID'].append(user_id)
               time_spent_on_details['User_Name'].append(user_name)
               time_spent_on_details["TimeSpentOn_AI"].append(session['TimeSpent'].get("AI", np.nan))
               time_spent_on_details["TimeSpentOn_FillintheBlanks"].append(session['TimeSpent'].get("FillintheBlanks", np.nan))
               time_spent_on_details["TimeSpentOn_Lesson"].append(session['TimeSpent'].get("Lesson", np.nan))
               time_spent_on_details["TimeSpentOn_MainMenu"].append(session['TimeSpent'].get("MainMenu", np.nan))
               time_spent_on_details["TimeSpentOn_Map"].append(session['TimeSpent'].get("Map", np.nan))
               time_spent_on_details["TimeSpentOn_MatchFollowings"].append(session['TimeSpent'].get("MatchFollowings", np.nan))
               time_spent_on_details["TimeSpentOn_Quiz"].append(session['TimeSpent'].get("Quiz", np.nan))
               time_spent_on_details["TimeSpentOn_Selection"].append(session['TimeSpent'].get("Selection", np.nan))
               time_spent_on_details["TimeSpentOn_Store"].append(session['TimeSpent'].get("Store", np.nan))
               time_spent_on_details["TimeSpentOn_TrueFalse"].append(session['TimeSpent'].get("TrueFalse", np.nan))
               time_spent_on_details["TimeSpentOn_Unscramble"].append(session['TimeSpent'].get("Unscramble", np.nan))

game_session_df = pd.DataFrame(game_session_details)
overall_session_df = pd.DataFrame(overall_session_details)
time_spent_on_details_df = pd.DataFrame(time_spent_on_details)

df.to_csv('user_purchase_details.csv', index=False)
user_info_df.to_csv('user_information.csv', index=False)
game_session_df.to_csv('game_session_details.csv', index=False)
overall_session_df.to_csv('overall_session_details.csv', index=False)
time_spent_on_details_df.to_csv('user_time_spent_details.csv', index=False)

