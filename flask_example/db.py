# Учебный проект. Вместо реальной БД используются cookie


def create(users, new_user):
    new_user['id'] = 1 if len(users) == 0 else users[-1]['id'] + 1
    users.append(new_user)


def get_user(users, id: int):
    for user in users:
        if user['id'] == id:
            return user


def delete(users, id: int):
    for i, user in enumerate(users):
        if user['id'] == id:
            users.pop(i)
            break


def patch(users, user_data, id: int):
    for user in users:
        if user['id'] == id:
            user['name'] = user_data['name']
            user['email'] = user_data['email']
            break
