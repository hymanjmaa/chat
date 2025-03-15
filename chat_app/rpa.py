from datetime import datetime

print("RPA execute success")
with open('rpa_{}.txt'.format(datetime.now()), 'w') as f:
    f.write(str(datetime.now()))
