# Database Management for Users and Todos

class InMemoryDatabase:
    def __init__(self):
        self.users = {}
        self.todos = {}

    def add_user(self, user_id, user_info):
        self.users[user_id] = user_info

    def get_user(self, user_id):
        return self.users.get(user_id, None)

    def add_todo(self, todo_id, todo_info):
        self.todos[todo_id] = todo_info

    def get_todo(self, todo_id):
        return self.todos.get(todo_id, None)

    def get_all_users(self):
        return self.users

    def get_all_todos(self):
        return self.todos

# Example usage:
# db = InMemoryDatabase()
# db.add_user(1, {'name': 'Alice'})
# db.add_todo(1, {'task': 'Do laundry'})
