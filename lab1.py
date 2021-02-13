from datetime import datetime

now = datetime.now()

if now.hour >= 6 and now.hour < 12:
  print('Good morning')
elif now.hour >= 12 and now.hour < 18:
  print('Good afternoon')
elif now.hour >= 18 and now.hour < 23:
  print('Good evening')
else:
  print('Good night')