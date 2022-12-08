from classes.database import UsersDatabase
from json import load


def main():
    with open('data.json', encoding='utf-8') as f:
        data = load(f)
    with UsersDatabase() as users:
        users.create_tables()
        for user in data:
            users.add_user(**user)
        clementina = users.find_user(first_name='Clementina')
        if clementina:
            users.add_phone('+7 (999) 999-9999', clementina[0][0])
        aurthur = users.find_user(last_name='Gook')
        if aurthur:
            users.change_user(aurthur[0][0], first_name='Aurthur')
            users.add_phone('+7 (666) 666-6666', aurthur[0][0])
        users.delete_phone('+49 (626) 149-6321')
        users.delete_user(4)
        users.delete_user(8)


if __name__ == '__main__':
    main()
