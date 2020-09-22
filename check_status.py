import requests
import pandas as pd
import holidays
import datetime
import enda_util as e

url = 'https://traininfo.jreast.co.jp/train_info/e/kanto.aspx'
train_line = 'Keihin-Tōhoku Line'

def is_holiday(date) :
# Select country 
  jp_holidays = holidays.Japan() 
  
  
# If it is a holidays then it returns True else False 
  return ( date in jp_holidays)


def get_status(line):
  status = requests.get(url)

  df_list = pd.read_html(status.text) # this parses all the tables in webpages to a list
  df1=df_list[0]
  df2=df_list[1]


  df3=df1.append(df2)
  df3.columns =['line','status']



  #print(df3)
  df4=df3.loc[df3['line'] == line]
  df4.index =['For Tokyo', 'For Yokohama']

  return_df =df4.loc[df4['status'] != 'Normal operation']
  
  return(return_df)

today = datetime.date.today()
#print(today)

def isworkday(date):
    #return false is today is Japanese holiday or Saturday / Sunday    
    if  is_holiday(today) or today.isoweekday() in (6,7):
    #if  today.isoweekday() in (6,7):
      return False
    return True

status = get_status(train_line)

if isworkday(today) and len(status) > 0 :
  #print(get_status('Keihin-Tōhoku Line'))
  #print(str(status['status']) + '\n\n' + url)
  
  # send via line message. This can be replace with email etc.
  e.send_line(str(status['status']) + '\n\n' + url)

