from Mcheck.Code.Encryption import encrypt
from Mcheck.Code.classM import Mail
from getpass import getpass


def setup(txt):
    path = txt

# Check if file text already has data: True if empty
    def empty_txt(link):
        open(link, 'a')
        with open(link) as file:
            file.seek(0)
            first_char = file.read(1)
            if not first_char:
                return True

            else:
                file.seek(0)
                return False

# Check if data already created: True if empty file or username not used yet
    def line_check(link, entry):
        if empty_txt(link):
            return True

        file = open(link, "r")
        users = []
        for line in file:
            user = line.split()[2]
            users.append(user)

        if entry not in users:
            file.close()
            return True

        else:
            file.close()
            return False

# Useful function to loop over "write()" and create new accounts
    def restart():

        response = input("Voulez vous créer un autre compte?[oui/non]").lower()

        if response == "oui":
            write()

        elif response == "non":
            print("Enregistrement...")

        else:
            print("Nous n'avons pas compris")
            restart()

# Ask to create account
    def write():

        a = Mail.available

        name = input("Choisissez une boite mail parmis %s :" % ', '.join(map(str, a)))
        id = input("Quel est votre identifiant? :")
        password = getpass("Quel est votre mot de passe? (par sécurité, celui-ci ne sera pas affiché) :")
        account = input("Comment voulez-vous nommer votre compte? :")
        # Check if account already created
        if line_check(path, id):
            info = Mail(name, account, id, password)
            # Check less secure of gmail deactivated
            if info.lSecure():
                # Check if account informations are correct
                if info.test():
                    # write down informations on txt file
                    file = open(path, "a")
                    for i in [name, account, id, encrypt(password)]:
                        file.write(i)
                        file.write(" ")
                    file.write("\n")
                    file.close()

                else:
                    print("---ERROR---")

            else:
                print("C'est vous qui décidez")

        else:
            print("Ce compte est déjà créé")

        restart()

    write()


if __name__ == '__main__':
    setup("Xspector.txt")
