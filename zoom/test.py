from datetime import datetime
import time

now = datetime.now()
time.sleep(5)
d = (now - datetime.now()).total_seconds()
print(abs(d))


