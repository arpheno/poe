import datetime


user_input = input("When do you want to meet?").strip()
meeting_hour, meeting_minutes = user_input.split(':')
now = datetime.datetime.now()
meeting_datetime = datetime.datetime(now.year,now.month,now.day,int(meeting_hour),int(meeting_minutes))
print(meeting_datetime)
timestamp = int(meeting_datetime.timestamp())
print(f'Let\'s meet at <t:{timestamp}>')