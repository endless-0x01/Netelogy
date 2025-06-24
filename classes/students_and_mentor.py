class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def _get_average_rate(self):
        if not self.grades:
            return 0
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return round(sum(all_grades) / len(all_grades), 1)

    def rate_lecture(self, lecture, course, grade):
        if (
            isinstance(lecture, Lecturer)
            and course in self.courses_in_progress
            and course in lecture.courses_attached
        ):

            lecture.grades.setdefault(course, []).append(grade)
        else:
            return "Ошибка"

    def __lt__(self, other):
        if not isinstance(other, Student):
            return "Ошибка"
        return self._get_average_rate() < other._get_average_rate()

    def __le__(self, other):
        if not isinstance(other, Student):
            return "Ошибка"
        return self._get_average_rate() <= other._get_average_rate()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return "Ошибка"
        return self._get_average_rate() == other._get_average_rate()

    def __ge__(self, other):
        if not isinstance(other, Student):
            return "Ошибка"
        return self._get_average_rate() >= other._get_average_rate()

    def __ne__(self, other):
        if not isinstance(other, Student):
            return "Ошибка"
        return self._get_average_rate() != other._get_average_rate()

    def __gt__(self, other):
        if not isinstance(other, Student):
            return "Ошибка"
        return self._get_average_rate() > other._get_average_rate()

    def __str__(self):
        return (
            f"Имя {self.name}\n"
            f"Фамилия {self.surname}\n"
            f"Средняя оценка за домашние задания: {self._get_average_rate()}\n"
            f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
            f"Завершенные курсы: {', '.join(self.finished_courses)}\n"
        )


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def show_grades(self):
        return "\n".join((f"{c}: {gr}" for c, gr in self.grades.items()))

    def _get_average_rate(self):
        if not self.grades:
            return 0

        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return round(sum(all_grades) / len(all_grades), 1)

    def __str__(self):
        return (
            f"Имя {self.name}\n"
            f"Фамилия {self.surname}\n"
            f"Средняя оценка за лекции: {self._get_average_rate()}\n"
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return "Ошибка"
        return self._get_average_rate() < other._get_average_rate()

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return "Ошибка"
        return self._get_average_rate() <= other._get_average_rate()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return "Ошибка"
        return self._get_average_rate() == other._get_average_rate()

    def __ge__(self, other):
        if not isinstance(other, Lecturer):
            return "Ошибка"
        return self._get_average_rate() >= other._get_average_rate()

    def __ne__(self, other):
        if not isinstance(other, Lecturer):
            return "Ошибка"
        return self._get_average_rate() != other._get_average_rate()

    def __gt__(self, other):
        if not isinstance(other, Lecturer):
            return "Ошибка"
        return self._get_average_rate() > other._get_average_rate()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (
            isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
        ):

            student.grades.setdefault(course, []).append(grade)
        else:
            return "Ошибка"

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"
    



def average_student(students: Student, course):
    all_grades = []
    
    for student in students:
        if course in student.grades:
            all_grades.extend(student.grades[course])

    return round(sum(all_grades) / len(all_grades) , 1) if all_grades else 0

def average_lectors(lectors: Lecturer, course):
    all_grades = []
    for lecter in lectors:
        if course in lecter.grades:
            all_grades.extend(lecter.grades[course])
    
    return round(sum(all_grades) / len(all_grades) , 1) if all_grades else 0



lecturer1 = Lecturer("Иван", "Иванов")
lecturer2 = Lecturer("Петр", "Петров")
reviewer1 = Reviewer("Сергей", "Сергеев")
reviewer2 = Reviewer("Анна", "Аннова")
student1 = Student("Ольга", "Ольгова", "ж")
student2 = Student("Алексей", "Алексеев", "м")


lecturer1.courses_attached += ["Python", "Java"]
lecturer2.courses_attached += ["Python", "C++"]
reviewer1.courses_attached += ["Python", "Java"]
reviewer2.courses_attached += ["C++", "Git"]
student1.courses_in_progress += ["Python", "Java"]
student2.courses_in_progress += ["Python", "C++"]
student1.finished_courses += ["Введение в программирование"]
student2.finished_courses += ["Основы ООП"]


reviewer1.rate_hw(student1, "Python", 9)
reviewer1.rate_hw(student1, "Java", 8)
reviewer2.rate_hw(student2, "C++", 7)
reviewer1.rate_hw(student1, "Python", 10)


student1.rate_lecture(lecturer1, "Python", 10)
student2.rate_lecture(lecturer1, "Python", 9)
student2.rate_lecture(lecturer2, "Python", 8)


print(lecturer1.grades)
print(lecturer2.grades)
print("*********** student ***********")
print(student1.grades)
print(student2.grades)

print(student1 > student2)
print(student1 == student2)
print(lecturer1 > lecturer2)
print(lecturer2 < lecturer1)


print(student1)
print(student2)
print(f"******Лекторы************")
print(lecturer1)
print(lecturer2)



students = [student1, student2]
lecturers = [lecturer1, lecturer2]
print("\nСредняя оценка студентов по Python:", average_student(students, 'Python'))
print("Средняя оценка лекторов по Python:", average_lectors(lecturers, 'Python'))