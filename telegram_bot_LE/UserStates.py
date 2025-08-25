class UserStateManager:
    def __init__(self) -> None:
        self.user_states = {}
        self.user_data = {}

    def set_state(self, user_id, state):
        self.user_states[user_id] = state
    
    def get_state(self, user_id):
        return self.user_states.get(user_id)
    
    def set_data(self, user_id, key, value):
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        self.user_data[user_id][key] = value
    
    def get_data(self, user_id, key):
        return self.user_data.get(user_id, {}).get(key)
    
    def clear_user(self, user_id):
        self.user_states.pop(user_id, None)
        self.user_data.pop(user_id, None)