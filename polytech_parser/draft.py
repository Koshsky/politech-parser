from datetime import datetime

# >>> dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
dt = datetime.strptime("2023-07-14T17:27:35", '%Y-%m-%dT%H:%M:%S')

print(dt.strftime('%A, %d. %B %Y %I:%M%p'))
