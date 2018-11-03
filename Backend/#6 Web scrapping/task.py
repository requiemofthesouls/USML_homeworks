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
        course_existing = self.bsobj.find('div', {'class': 'course-preview'})
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

    def get_course_descriptor(self):
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
        self._description = current_course.get_course_descriptor()
        self._organisator = current_course.get_course_organisation()
        self._teachers = current_course.get_course_teachers()

    def __str__(self):
        msg = f'ID: {self._id}, Title: {self._title}, Rating: {self._rating}, Organisator: {self._organisator}, Teachers: {self._teachers}'
        return msg


def main():
    for i in range(1, 100):
        c = StepikCourse(i)
        print(c)


if __name__ == '__main__':
    main()
