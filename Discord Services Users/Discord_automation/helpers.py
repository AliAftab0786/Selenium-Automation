from utils import *
def clear_terminal():

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
def get_usernames_from_csv(file_path):
    usernames = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            if row:  # Ensure the row is not empty
                usernames.append(row[0])  # Assuming username is the first element
    return usernames
def starting():
    with open('userData.json', 'r', encoding='utf-8') as file:
        data_json = json.load(file)
    while True:
        print("Available options:")
        for i, data in enumerate(data_json['choices'], start=1):
            print(f"{i}. Account: {data['accounttitle']}")
            if i==1:
                MessageData = data['message']
        break
    return MessageData

def set_messages(num_of_account):
    assign_msg = []
    file_path = "./userDB/usernames.csv"
    users = get_usernames_from_csv(file_path)
    print("Usernames:", len(users))

    division = len(users) // num_of_account
    reminder = len(users) % num_of_account

    print("Division:", division)
    print("Reminder:", reminder)

    if reminder != 0:
        assign_msg = [division] * num_of_account
        index = random.randint(0, num_of_account - 1)
        assign_msg[index] += 1
        while sum(assign_msg) != len(users):
            index = random.randint(0, num_of_account - 1)
            if assign_msg[index] < division + 1:
                assign_msg[index] += 1
    else:
        assign_msg = [division] * num_of_account

    print("Assign Message:", assign_msg)
    return assign_msg