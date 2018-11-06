from bs4 import BeautifulSoup
from lxml import html
import requests

URL = 'https://stepik.org/course/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/63.0'
}


class CourseParsing:
    def __init__(self, course_id):
        self.bsobj = self._grab_course(course_id, HEADERS)

    @staticmethod
    def _grab_course(course_id, headers):
        try:
            rsp = requests.get(f'https://stepik.org/course/{course_id}', headers=headers)
        except requests.exceptions.HTTPError as e:
            raise e
        return BeautifulSoup(rsp.text, features="lxml")

    def is_an_error(self):
        course_existing = self.bsobj.find('div', class_='course-preview')
        return False if course_existing else True

    def get_course_title(self):
        if self.is_an_error():
            return None
        else:
            title = self.bsobj.find('title').text
            return title

    def get_course_rating(self):
        if self.get_course_title():
            rating = self.bsobj.find('strong', class_='course-index__rating')
            try:
                return rating.text
            except AttributeError:
                return None
        else:
            return None

    def get_course_description(self):
        if self.get_course_title():
            desc = self.bsobj.find('p', class_='course-index__short-desc')
            try:
                return desc.text
            except AttributeError:
                return None
        else:
            return None

    def get_course_organisation(self):
        if self.get_course_title():
            desc = self.bsobj.find('span', class_='user-avatar__name')
            try:
                return desc.text
            except AttributeError:
                return None
        else:
            return None

    def get_course_teachers(self):
        if self.get_course_title():
            teachers_block = self.bsobj.find('ol', class_='course-index__authors-list')
            try:
                teachers_block = teachers_block.find_all('a')
                teachers = [teacher.string for teacher in teachers_block]
                return teachers
            except AttributeError:
                return None


class StepikCourse:
    def __init__(self, course_id):
        current_course = CourseParsing(course_id)
        self._id = course_id
        self._title = current_course.get_course_title()
        self._rating = current_course.get_course_rating()
        self._description = current_course.get_course_description()
        self._organisator = current_course.get_course_organisation()
        self._teachers = current_course.get_course_teachers()

    def get_id(self):
        return self._id

    def get_title(self):
        if self._title:
            return self._title.replace('\n', '')
        else:
            return None

    def get_rating(self):
        return self._rating

    def get_description(self):
        if self._description:
            desc = self._description.replace(';', ',')
            return desc.replace('\n', '')
        else:
            return None

    def get_organisator(self):
        return self._organisator

    def get_teachers(self):
        if self._teachers:
            return ', '.join(self._teachers)
        else:
            return None

    def __str__(self):
        msg = f'ID: {self.get_id()}, ' \
              f'Title: {self.get_title()}, ' \
              f'Rating: {self.get_rating()}, ' \
              f'Organisator: {self.get_organisator()}, ' \
              f'Teachers: {self.get_teachers()}'
        return msg


def main():
    with open('courses.csv', 'w') as csv:
        csv.write('id;Title;Rating;Descriprion;Organisator;Teachers' + '\n')
        for i in range(1, 10000):
            course = StepikCourse(i)
            print(course)
            if course.get_title():
                print('Writing' + str(course.get_id()))
                line = f'{course.get_id()}; ' \
                       f'{course.get_title()}; ' \
                       f'{course.get_rating()}; ' \
                       f'{course.get_description()}; ' \
                       f'{course.get_organisator()}; ' \
                       f'{course.get_teachers()} \n'
                csv.write(line)
            else:
                continue


if __name__ == '__main__':
    main()
