import time
import datetime
import os.path
from Mcheck.Code.Setup import setup
from Mcheck.Code.Info import info

txt = "XspectorFile.txt"
print("Bonjour!")

while 1:
    # Check if Xspector file exist : current way to check if setup made
    if not os.path.isfile(txt):
        setup(txt)
        print("Okay, on est prêt!")

    # Run main script to check mails
    else:
        now = datetime.datetime.now()
        hour = now.strftime("%H:%M:%S")

        # In case of unpredicted events
        try:
            pause = info(txt)

        except:
            print("ERROR: un problème de connexion est survenue. Prochain test dans 10 min")
            pause = 596

        print("Dernier test effectué à %s" % hour)
        print(" ")
        time.sleep(pause)
