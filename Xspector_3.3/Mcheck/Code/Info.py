import tkinter as tk
from tkinter import messagebox, simpledialog
from Mcheck.webbot import Browser
from Mcheck.Code.Encryption import decrypt
from Mcheck.Code.classM import Mail


def info(path):
    # Check and take info within txt file
    data = open(path, "r").readlines()

    # Temporaly store informations
    mail = []
    count = [] # used to show how many new messages we have
    count2 = [] # used to know how many tab we should open in Chrome
    account_name = []
    for i in data:
        dsplit = i.split()
        result = Mail(dsplit[0], dsplit[1], dsplit[2], decrypt(dsplit[3]))
        count.append(result.unseen_mail())
        a = count[-1]

        if isinstance(a, int):
            if a > 0:
                count2.append(a)
        account_name.append(result.account)
        mail.append(result)

    # If new mails window appears and warn the user. If he clicks yes, we open all mailbox with new mail only . If he
    # clicks no, we ask when we the application should warn the user again.
    if sum(count2) > 0:
        print("###################################")
        print("#        Nouveaux messages        #")
        print("###################################")

        window = tk.Tk()
        window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
        window.attributes("-topmost", True)
        window.withdraw()

        if messagebox.askyesno('Mail info', ' Hello! Vous avez %s nouveaux messages sur %s. '
                                            'Voulez-vous tous les voir?' % ((', '.join(map(str, count)),
                                                                             ', '.join(map(str, account_name))))):
            web = Browser()
            maxi = len(count2)
            mini = 1
            for result in mail:
                result.go_to(web, result.unseen_mail())
                # open mailboxes in different tab of the browser
                if mini < maxi:
                    web.execute_script('''window.open();''')
                    web.switch_to_tab(mini + 1)
                    mini += 1
            pause = 9.9

        else:
            pause = simpledialog.askstring("Mail info", "Dans combien de temps voulez-vous un rappel ? (min)",
                                            parent=window)

        window.deiconify()
        window.destroy()
        window.quit()

    else:
        print("-----------------------------------")
        print("-        Pas de messages          -")
        print("-----------------------------------")
        pause = 9.9

    return float(pause) * 60


if __name__ == '__main__':
    info("XspectorFile.txt")
