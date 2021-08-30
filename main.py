def average_all_grades(list_persons, subject):
    sum = 0
    quantity = 0
    for person in list_persons:
        for grades_in_subject in person.grades.get(subject, [0]):
            if type(grades_in_subject) == list:
                for grades_in_list in grades_in_subject:
                    sum += grades_in_list
                    quantity += 1
            else:
                sum += grades_in_subject
                quantity += 1
    if quantity == 0:
        print('Нет оценок по указанной дисциплине')
    else:
        print(sum / quantity)

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecturer(self, lecturer, course, grade):
        if 0 <= grade <= 10:
            if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
                if course in lecturer.grades:
                    lecturer.grades[course] += [grade]
                else:
                    lecturer.grades[course] = [grade]
            else:
                print('Ошибка')
        else:
            print('Оценка должна быть по десятибальной шкале')

    def __str__(self):
        res = f'Имя: {self.name}\n' \
              f'Фамилия: {self.surname}\n' \
              f'Средняя оценка: {self.average()}\n' \
              f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n' \
              f'Завершенные курсы: {", ".join(self.finished_courses)}'
        return res

    def average(self, subject="any"):
        if subject == "any":
            sum = 0
            quantity = 0
            for number in self.grades.values():
                if type(number) == list:
                    for number_in_list in number:
                        sum += number_in_list
                        quantity += 1
                else:
                    sum += number
                    quantity += 1
            return sum / quantity
        else:
            sum_subject = 0
            for number_subject in self.grades.get(subject):
                sum_subject += number_subject
            return sum_subject / len(self.grades.get(subject))

    def __lt__(self, other):
        return self.average() < other.average()

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка: {self.average()}'
        return res

    def average(self):
        sum = 0
        quantity = 0
        for number in self.grades.values():
            if type(number) == list:
                for number_in_list in number:
                    sum += number_in_list
                    quantity += 1
            else:
                sum += number
                quantity += 1
        return sum / quantity

    def __lt__(self, other):
        return self.average() < other.average()

class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(self, Reviewer):
            if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
                if course in student.grades:
                    student.grades[course] += [grade]
                else:
                    student.grades[course] = [grade]
            else:
                return 'Ошибка'
        else:
            return 'Вы не Ревьюер'
    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}'
        return res

student1 = Student('Ivan', 'Ivanov', 'Man')
student2 = Student('Maxim', 'Sergeev', 'Man')

lecturer1 = Lecturer('Dmitry', 'Kuznecov')
lecturer2 = Lecturer('Sergey', 'Vasilev')

reviewer1 = Reviewer('Some', 'Buddy')
reviewer2 = Reviewer('Viktor', 'Karaev')

student1.courses_in_progress += ['Python']
student1.courses_in_progress += ['Scala']
student2.courses_in_progress += ['Python']
student2.courses_in_progress += ['Scala']

lecturer1.courses_attached += ['Python']
lecturer2.courses_attached += ['Python']

student1.add_courses('Java')
student2.add_courses('Java')

reviewer1.courses_attached += ['Python']
reviewer1.courses_attached += ['Scala']
reviewer2.courses_attached += ['Python']

student1.rate_lecturer(lecturer1, 'Python', 8)
student2.rate_lecturer(lecturer2, 'Python', 9)
student1.rate_lecturer(lecturer1, 'Python', 7)
student2.rate_lecturer(lecturer2, 'Python', 10)

reviewer1.rate_hw(student1, 'Python', 7)
reviewer1.rate_hw(student1, 'Python', 6)
reviewer2.rate_hw(student2, 'Python', 8)
reviewer1.rate_hw(student1, 'Scala', 8)
reviewer1.rate_hw(student2, 'Scala', 7)
reviewer1.rate_hw(student2, 'Scala', 7)

print(student1)
print(student2)

print(lecturer1)
print(lecturer2)

print(reviewer1)

print(student1 > student2)
print(lecturer1 < lecturer2)

list_persons_lecturer = [lecturer1, lecturer2]
list_persons_students = [student1, student2]

average_all_grades(list_persons_students, 'Scala')
average_all_grades(list_persons_lecturer, 'Python')


