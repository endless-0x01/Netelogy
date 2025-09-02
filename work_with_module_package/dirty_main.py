from application.salary import *
from application.db.people import *
from datetime import *
   
if __name__ == '__main__':
    calculate_salary()
    get_employees()
    print(f'Запуск через dirty_main: {datetime.now(timezone.utc)}')