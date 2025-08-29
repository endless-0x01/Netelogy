from typing import Optional, Dict, Any


class UserStateManager:
    def __init__(self) -> None:
        self.user_states: Dict[int, str] = {}
        self.user_data: Dict[int, Dict[str, Any]] = {}

    def set_state(self, user_id: int, state: str) -> None:
        self.user_states[user_id] = state

    def get_state(self, user_id: int) -> Optional[str]:
        return self.user_states.get(user_id)

    def set_data(self, user_id: int, key: str, value: Any) -> None:
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        self.user_data[user_id][key] = value

    def get_data(self, user_id: int, key: str) -> Optional[Any]:
        return self.user_data.get(user_id, {}).get(key)

    def clear_user(self, user_id: int) -> None:
        self.user_states.pop(user_id, None)
        self.user_data.pop(user_id, None)
