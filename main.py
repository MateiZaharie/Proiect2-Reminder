import json
from datetime import datetime
from json import JSONDecodeError

try:
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)
except FileNotFoundError:
    tasks = []


class MainMenu:

    def __init__(self, username):
        self.username = username
        self.setreminders = []
        self.tasks = tasks  # Initialize an empty list for tasks
        self.reminders = []

    def save_tasks_to_file(self):
        file_name = f"{self.username}_tasks.json"
        with open(file_name, 'w') as file:
            json.dump(self.tasks, file)
        print(f'Tasks saved to {file_name}')

    def show_main_menu(self):
        print(f"Hello, {self.username}!\nLet's schedule your day.")
        print("""1. View Tasks
2. Add Task
3. Set Reminder
4. View Reminders
5. Exit""")

        user_choice = input("Please enter the number corresponding to your choice: ")
        if user_choice == '1':
            self.view_tasks()
        elif user_choice == '2':
            self.add_tasks()
        elif user_choice == '3':
            self.add_reminders()
        elif user_choice == '4':
            self.view_reminders()
        elif user_choice == '5':
            sys.exit()



    def view_tasks(self):
        file_name=f'{self.username}_tasks.json'
        try:
            with open(file_name, 'r') as file:
                tasks_database = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            tasks_database = {}
        print(f">>>>>>{self.username} tasks<<<<<<<<")
        # sorted_tasks = sorted(self.tasks, key=lambda task: task['Dateandtime'], reverse=True)

        for i, task in enumerate(tasks_database, 1):
            print(f"{i}. {task}/{tasks_database[task]}")
        view_task_input = input('Type "x" if you want to go back to the menu: ')
        if view_task_input == 'x':
            self.show_main_menu()

    def add_tasks(self):
        task_description = input('Describe your task: ')
        while True:
            try:
                task_date = input('Give the Date of your task (YYYY-MM-DD): ')
                task_time = input('Give the time of your task (HH:MM): ')
                datetime_str = f'{task_date} {task_time}'
                datetime_task = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                break  # Break out of the loop if the input is valid
            except ValueError:
                print('Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.')

        self.tasks.append({'Dateandtime': datetime_task, "Taskdescription": task_description})
        file_name = f"{self.username}_tasks.json"
        try:
            with open(file_name, 'r') as file:
                tasks_database = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            tasks_database = {}
        with open(file_name, 'w') as file:
            tasks_database[task_description]=datetime_str
            json.dump(tasks_database, file)
        print(f'Tasks saved to {file_name}')
        print('Task added successfully')
        add_tasks_input = input('Type "x" if you want to go back to the menu: ')
        if add_tasks_input == 'x':
            self.show_main_menu()

    def add_reminders(self):
        print('In the following steps, you will set your reminder')
        while True:
            try:
                reminder_date = input('Give the Date of your reminder (YYYY-MM-DD): ')
                reminder_time = input('Give the time of your reminder (HH:MM): ')
                datetime_str2 = f'{reminder_date} {reminder_time}'
                datetime_task2 = datetime.strptime(datetime_str2, "%Y-%m-%d %H:%M")
                break  # Break out of the loop if the input is valid
            except ValueError:
                print('Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.')
        reminder_description = input('Describe your reminder: ')
        self.reminders.append({'Dateandtime': datetime_task2, "Reminderdescription": reminder_description})
        print("""Reminder added successfully!
         You will receive 2 notifications 
         one an hour in advance and the second one at the chosen time""")
        add_reminders_input = input('Type "x" if you want to go back to the menu: ')
        if add_reminders_input == 'x':
            self.show_main_menu()

    def view_reminders(self):
        print(f">>>>>>{self.username} reminders<<<<<<<<")
        sorted_reminders = sorted(self.reminders, key=lambda reminder: reminder['Dateandtime'], reverse=True)
        for i, reminder in enumerate(sorted_reminders, 1):
            print(f"{i}. {reminder['Reminderdescription']} - {reminder['Dateandtime']}")
        view_reminder_input = input('Type "x" if you want to go back to the menu: ')
        if view_reminder_input == 'x':
            self.show_main_menu()
    def pop_reminders(self):
        date_time_now = datetime.now()
        reminders_to_remove = [reminder for reminder in self.reminders if reminder['Dateandtime'] < date_time_now]

        for reminder in reminders_to_remove:
            self.reminders.remove(reminder)

        print("Reminders removed successfully")
        self.show_main_menu()

    def notif_reminders(self):
        date_time_now = datetime.now()
        reminders_to_notif = [reminder for reminder in self.reminders if reminder['Dateandtime'] == date_time_now]
        for reminder in reminders_to_notif:
            print(f">>>Notification: {reminder['Reminderdescription']}")
# Try to load existing user data from a file
try:
    with open('user_database.json', 'r') as file:
        user_database = json.load(file)
except FileNotFoundError:
    user_database = {}

Introduction = """Welcome to your task scheduling and reminder app,
Access your account or create a new one to get started.
"""

print(Introduction)

sign_login = input("""Press 1 if you already have an account
Press 2 if you want to sign up: """)

if sign_login == '1':
    while True:
        existing_username = input('Type your existing username in: ')
        existing_password = input('Type your password in: ')
        if existing_username in user_database and user_database[existing_username] == existing_password:
            print('Login successful')

            main_menu_instance = MainMenu(existing_username)

            while True:
                main_menu_instance.show_main_menu()
                main_menu_instance.notif_reminders()
                main_menu_instance.pop_reminders()
        else:
            print('Invalid username or password. Please try again')

elif sign_login == '2':
    while True:
        new_username = input('Please select a unique username: ')
        new_password = input('Please select a unique password: ')
        if new_username not in user_database:
            print('Your account was successfully created')
            user_database[new_username] = new_password
            with open('user_database.json', 'w') as file:
                json.dump(user_database, file)
            main_menu_instance2 = MainMenu(new_username)
            while True:
                main_menu_instance2.show_main_menu()
                main_menu_instance.notif_reminders()
                main_menu_instance.pop_reminders()
        else:
            print('Username already taken. Please choose a different one.')