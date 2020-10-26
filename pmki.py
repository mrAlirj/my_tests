# import os
# os.system("start cmd /K dir")



# import subprocess
# subprocess.run('dir' , shell=True)

# import sys
import time
# for x in range(10):
#     time.sleep(3)
#     sys.stdout.write('\r'+str(x))
#     time.sleep(3)
#     sys.stdout.flush()

import sys 
print("FAILED...") 
time.sleep(3)
sys.stdout.write("\033[F") #back to previous line 
time.sleep(3)
sys.stdout.write("\033[K") #clear line 
print("SUCCESS!") 