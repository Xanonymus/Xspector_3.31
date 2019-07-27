import imaplib
import time
from Mcheck.Code.isMail import is_hena, is_live, is_sogo, is_gmail
from Mcheck.webbot import Browser

""" --- Main and only class to simplify the code on other files --- """
class Mail:
    # Global class variable : used for most mail boxes, except gmail...of course.
    box = 'INBOX'
    search_em = '(UNSEEN)'
    available = ['GMAIL', 'SOGO', 'OUTLOOK', 'LIVE', 'HOTMAIL', 'HENALLUX']

    # To run the code we ask for : username, password, mailbox type,
    # But we also need imap and website domain, website link (no need to ask the user)
    # To optimise the use of the app we also need: account name, imaplib functions (box, search_em)
    def __init__(self, name, account, id, password):
        self.name = name
        self.account = account
        self.id = id
        self.password = password

        if is_gmail(self.name):
            self.ima = 'imap.gmail.com'
            self.search_em = '(X-GM-RAW "category:primary" UNSEEN)'
            self.site = "https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmai"\
                        "l%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin"

        elif is_sogo(self.name):
            self.ima = 'imap.unamur.be'
            self.site = "https://sogo.unamur.be/SOGo/so/"

        elif is_hena(self.name):
            self.ima = 'imap-mail.outlook.com'
            self.site = 'https://login.microsoftonline.com/common/oauth2/authorize?client_id=00000006-0000-0ff1-ce00' \
                        '-000000000000&response_mode=form_post&response_type=code+id_token&scope=openid+profile&state='\
                        'OpenIdConnect.AuthenticationProperties%3ddSDRJ7OQc801s8-0gWoAJ-r6tgPt1ubHkrqcXLdwDMPTBd7UWb8y'\
                        'FLqPUjxyhGfaXBhzb8XHXrqB_6SZuSHhy_6qSnSrbMbSC6IeppRFC99rYHs1iY2FofarY9JO6iZLUmBecOXb91fMoDMh' \
                        '6X8K32HbSuO2f2wmLCCytohDLno&nonce=636989147334010536.MDZmNTkxZWMtYjk5MS00YWM0LWI4ZDUtZmE2YjQ3'\
                        'OWMzYzNkMWYxOTZjYzktYWEwYS00OGUwLWI2MGItZmE5Y2EzZTM2N2Q5&redirect_uri=https%3a%2f%2fportal.of'\
                        'fice.com%2flanding&ui_locales=fr-FR&mkt=fr-FR&client-request-id=99cb4a4c-5fd2-4665-828d-4be6' \
                        'bf9c221e&sso_reload=true'

        elif is_live(self.name):
            self.ima = 'imap-mail.outlook.com'
            self.site = 'https://login.live.com/'

    # Ask the user to disable 'less secure app' on gmail, and open the window to do it (we want to give the choice)
    # Once done, return true
    def lSecure(self):

        if is_gmail(self.name):
            answer = input("Avez vous déjà autorisé ' L'accès moins sécurisé des applications ' de Gmail? [oui/non] ")

            if answer.lower() == 'non':
                print(" Pour Gmail, nous avons besoin de votre autorisation pour automatiser la vérification d'email. "
                      "Dans quelques secondes, une fenêtre s'ouvrira. Veuillez suivre les étapes suivantes:")
                print("- Déscendez en bas de la page, et allez dans 'Accès moins sécurisé des applications'")
                print("- Accordez l'accès")
                print("- Une fois cela fait, répondez 'oui' dans le terminal et validez :")

                time.sleep(4)
                web = Browser(custom="mcheck")
                web.go_to('https://myaccount.google.com/security')
                web.click('Connexion')
                time.sleep(0.5)
                web.type(self.id, into="E-mail")
                web.click('Suivant', tag='span')
                time.sleep(0.5)
                web.type(self.password, into="mot de passe")
                web.click('Suivant', tag='span')

                answer2 = input("C'est fait?")
                if answer2.lower() == "oui":
                    return True
            else:
                return True
        else:
            return True

    # Test if password and username are correct for the mail box
    def test(self):
        try:
            imap_url = self.ima
            imap = imaplib.IMAP4_SSL(imap_url, 993)
            imap.login(self.id, self.password)
            return True

        except:
            print("Boite mail, identifiant ou mot de passe incorrecte")
            return False

    # Check and count how many mail are new (unseen)
    def unseen_mail(self):
        try:
            imap_url = self.ima
            imap = imaplib.IMAP4_SSL(imap_url, 993)
            imap.login(self.id, self.password)

            # select mailbox to check
            imap.select(self.box)
            status, response = imap.search(None, self.search_em)
            unread_msg_nums = response[0].split()

            # Print the count of all unread messages
            new = len(unread_msg_nums)
            return new
        except:
            print("%s ne réponds pas" % self.name)
            return "( x ) "

    # Functions to open mailbox within Chrome automaticaly if there are new mail
    # FUTUR : open in private navigation?
    def go_to(self, driver, unseen):

        if isinstance(unseen, int):
            if unseen > 0:
                web = driver
                web.go_to(self.site)

                if is_gmail(self.name):
                    web.type(self.id, into='Email')
                    web.click(id='identifierNext', tag='span')
                    time.sleep(1)
                    web.click(id='data-initial-value')
                    web.type(self.password, id='data-initial-value')
                    web.click(id='passwordNext', tag='span')

                elif is_sogo(self.name):
                    time.sleep(1)
                    web.click(id='input_1')
                    web.type(self.id, id='input_1')
                    web.click(id='input_2')
                    web.type(self.password, id='input_2')
                    web.press(web.Key.ENTER)

                elif is_live(self.name) or is_hena(self.name):
                    time.sleep(2)
                    web.type(self.id, into='E-mail')
                    web.click(id='idSIButton9', tag='span')
                    time.sleep(2)
                    web.click(id='i0118')
                    web.type(self.password, id='i0118')
                    web.click(id='idSIButton9', tag='span')

            else:
                pass
        else:
            pass


if __name__ == '__main__':
    print(Mail.available)
    office365 = ['OFFICE365', 'outlook.office365.com', '']
