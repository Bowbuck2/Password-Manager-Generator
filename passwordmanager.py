import passwordgen as passgen
import json

accounts = []


class Account:

    def __init__(self, username, password, passwords):
        self.username = username
        self.password = password
        self.passwords = passwords

    def addPassword(self, username, password, description, website):
        self.passwords.append(Password(username, password, website, description, 0))

    def largestStr(self) -> list:
        count = [0, 0, 0, 0]
        for password in self.passwords:
            if len(password.pass_user) > count[0]:
                count[0] = len(password.pass_user)
            if len(password.pass_pass) > count[1]:
                count[1] = len(password.pass_pass)
            if len(password.pass_desc) > count[2]:
                count[2] = len(password.pass_desc)
            if len(password.pass_web) > count[3]:
                count[3] = len(password.pass_web)
        return count

    def passReadout(self):
        strLen = self.largestStr()
        for p in self.passwords:
            p.index = self.passwords.index(p)
            print('-' * sum(
                strLen) + '-' * 53 + f'\n|I: {p.index}   |Website: {p.pass_web.ljust(strLen[3])} |Desc: {p.pass_desc.ljust(strLen[2])} |Username: {p.pass_user.ljust(strLen[0])} |Password: {p.pass_pass.ljust(strLen[1])}  |')

    def __dict__(self):
        return {'username': self.username, 'password': self.password,
                'passwords': [password.__dict__() for password in self.passwords]}


class Password:
    def __init__(self, pass_user: str, pass_pass: str, pass_desc: str, pass_web: str, index: int):
        self.pass_user = pass_user
        self.pass_pass = pass_pass
        self.pass_desc = pass_desc
        self.pass_web = pass_web
        self.index = index

    def __dict__(self):
        return {'username': self.pass_user, 'password': self.pass_pass, 'website': self.pass_web,
                'description': self.pass_desc}


def catchType(message, err_msg, t):
    while True:
        try:
            return t(t(input(message)))
        except ValueError:
            print(err_msg)
            pass


def newPassword(account):
    print(
        '''
        ============
        New Password
        ============

        '''
    )
    website = catchType('Please enter a website: ', '', str)
    description = catchType('Please enter a description: ', '', str)
    username = catchType('Please enter a username: ', '', str)
    generate = catchType(
        '''
        Would you like the manager to generate the password?
        1: Yes
        2: No
        '''
        , '', int)
    if generate == 1:
        password = passgen.main()
        account.addPassword(str(username), str(password), str(website), str(description))
    else:
        password = catchType('Please enter your password: ', '', str)
        account.addPassword(str(username), str(password), str(website), str(description))
    manager(account)


def editPassword(account):
    print(
        '''
        =============
        Edit Password 
        =============        
        '''
    )
    account.passReadout()
    select = catchType("Please enter a password to edit (digit): ", "Please enter a digit", int)
    if select <= len(account.passwords):
        print(
            f'''
                              Edit Password                    
            =================================================
            1: Username | {account.passwords[select].pass_user}
            2: Password | {account.passwords[select].pass_pass}
            3: Desc.    | {account.passwords[select].pass_desc}
            4: Website  | {account.passwords[select].pass_web}

            5: Delete Password from Manager
            6: Cancel Edit
            ================================================
            '''
        )
        attribute = catchType("Please enter a password to edit (digit): ", "Please enter a digit", int)
        if attribute == 1:
            edit = catchType("Please enter a new username: ", "", str)
            account.passwords[select].pass_user = edit
        if attribute == 2:
            edit = catchType("Please enter a new password: ", "", str)
            account.passwords[select].pass_pass = edit
        if attribute == 3:
            edit = catchType("Please enter a new description: ", "", str)
            account.passwords[select].pass_desc = edit
        if attribute == 4:
            edit = catchType("Please enter a new website: ", "", str)
            account.passwords[select].pass_web = edit
        if attribute == 5:
            account.passwords.pop()
        manager(account)
    else:
        print("Index not found")
        editPassword(account)


def manager(account):
    print(
        '''
        ================
        Password Manager
        ================

        1: Create New Password
        2: Edit Password
        3: Exit Manager
        '''
    )
    account.passReadout()
    select = catchType("Please enter a digit: ", "Please enter a digit", int)
    if select == 1:
        newPassword(account)
    if select == 2:
        editPassword(account)
    if select == 3:
        return main()


def create():
    print(
        '''
        ==============
        Create Account
        ==============
        '''
    )
    username = catchType('Please enter a username: ', '', str)
    if len(username) >= 3:
        for account in accounts:
            if username == account.username:
                print("Username Already Exists!")
                create()
        password = catchType('Please enter a Master Password: ', '', str)
        accounts.append(Account(username, password, []))
    else:
        print("Username must be longer than 3 characters")
        create()
    main()


def login():
    print(
        '''
        ==============
        Password Login
        ==============

        1: Return to Main
        '''
    )
    username = catchType('Please enter a username: ', '', str)
    if username == '1':
        return main()
    for account in accounts:
        if account.username == username:
            password = catchType('Please enter a Master Password: ', '', str)
            if account.password == password:
                print('Loading Password Manager!')
                manager(account)
            else:
                print("Inccorect password")
                login()
        else:
            continue
    print("username not found")
    login()


def main():
    print(
        f'''
        ================
        Password Manager
        ================

        1: Login
        2: Create Account
        3: Exit Application
        '''
    )
    select = catchType("Please enter a digit: ", "Please enter a digit", int)
    if select == 1:
        if accounts:
            return login()
        else:
            print('No Accounts in database')
            return main()
    elif select == 2:
        return create()
    elif select == 3:
        return saveData()
    else:
        print("Please enter a value in the menu")
        return main()


def saveData():
    with open("db.json", "w", encoding="utf-8") as w:
        temp = []
        for a in accounts:
            temp.append(a.__dict__())

        json.dump(temp, w, ensure_ascii=False, indent=4)
    print("Have a great day!")
    exit()


try:
    read = open("db.json", "r")
    f = json.load(read)
    for ac in f:
        temp = []
        for password in ac['passwords']:
            temp.append(
                Password(password['username'], password['password'], password['description'], password['website'], 0))
        data = Account(ac['username'], ac['password'], temp)
        accounts.append(data)
except IOError:
    print("No Database Found")

main()