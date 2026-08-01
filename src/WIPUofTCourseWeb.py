#THIS IS A WORK IN PROGRESS!! THIS PROGRAM IS NOT COMPLETE!!

import requests
from bs4 import BeautifulSoup
import re

global_courses_list = []  # type: course
visited = set()
notes = []
regex_course_format_stg_all = r'minimum\s*of\s*([0-9]{1,2}|100)%\s*in\s*[A-Z]{3}[0-9]{3}[H|Y]1|[A-Z]{3}[0-9]{3}[H|Y]1\s*\(([0-9]{1,2}|100)%\)|[A-Z]{3,4}\d{3}[H|Y]\d|(;)|(\()|(\))|(/)|,|and'
regex_course_format_ONLY_stg = r'[A-Z]{3}\d{3}[H|Y]\d'
regex_percent_format = r'\d+%'
no_engineering_string = 'Prerequisite for Faculty of Applied Science and Engineering students:'
course_no_more = 'Sorry, this course is not in the current Calendar.'
is_debug = False;


class Course:
    #    course_name=""
    #    course_prereq= []
    #    course_unlocks=[]
    #    prereq_min_grade={}

    def __init__(self, course_name):
        self.course_name = course_name
        self.course_prereq = []
        self.course_unlocks = []
        self.prereq_min_grade = {}

        self.prereq_tree = None;

    def __eq__(self, other):
        if isinstance(other, Course):
            return self.course_name == other.course_name
        return False

    def __repr__(self):
        return str(self.course_name)

    def __hash__(self):
        return hash(self.course_name)

    def get_course_name(self):
        return self.course_name

    def add_prereq_list(self, courses_list):
        self.course_prereq.extend(courses_list)

    def add_unlock(self, unlocks):
        if unlocks not in self.course_unlocks:
            self.course_unlocks.append(unlocks)

    def prereq_min_grade_map_add(self, course, grade):
        self.prereq_min_grade[course] = grade

    def print_course_name(self):
        print(self.course_name)

    def print_course_prereq(self):
        print(f"{self.course_name}: {self.course_prereq}")

    #   print(self.course_prereq)
    def print_min_grade_map(self):
        print(f"{self.course_name}: {self.prereq_min_grade}")


    def print_unlocks(self):
        print(*self.course_unlocks)


def get_courses():

    global_courses_list.append(Course("CSC311H1"))
    global_courses_list.append(Course("ECO220Y1"))
    #global_courses_list.append(Course("STA255H1"))
    '''
    global_courses_list.append(Course("ECO220Y1"))
    global_courses_list.append(Course("CSC384H1"))
    global_courses_list.append(Course("CSC436H1"))
    global_courses_list.append(Course("STA465H1"))
    global_courses_list.append(Course("STA457H1"))
    global_courses_list.append(Course("MAT457H1"))
    global_courses_list.append(Course("MAT367H1"))'''


def parse_single_course(course_code):
    course_code_name = course_code.get_course_name()
    UofT_course_url = f"https://artsci.calendar.utoronto.ca/course/{course_code_name}"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com"}

    page = requests.get(UofT_course_url, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    if course_no_more in soup.find('h1', class_='page-title').get_text(strip=True):
        message = f"{course_code_name}: This course is no longer in the academic calender"
        debug_controls_msg(message, False)
        notes.append(message)
        return
    course_prereq_page_list = soup.find('div', class_=re.compile(r'field--name-field-prerequisite'))
    if course_prereq_page_list:
        course_prereq_page_list = course_prereq_page_list.get_text(strip=True, separator=" ")
    else:
        message = f"{course_code_name}: No university-level / course-specific prerequisites."
        debug_controls_msg(message, False)
        notes.append(message)
        return

    if "Prerequisite" in course_prereq_page_list:
        course_prereq_page_list = course_prereq_page_list.split("Prerequisite")[1]
    if no_engineering_string in course_prereq_page_list:
        course_prereq_page_list = course_prereq_page_list.split(no_engineering_string)[0]
    if "Note" in course_prereq_page_list:
        course_prereq_page_list = course_prereq_page_list.split("Note")[0]

    parse_prereq_text_rewrite(course_code, course_prereq_page_list)

def parse_prereq_text_rewrite(course_code, course_prereq_page_list):
    currently_added=[]
    this_course_prereq = []
    current_prereq_group = []
    parenthesis_group = []
    is_in_parenthesis = False;
    is_parenthesis_or = False
    is_first_or = True
    parenthesis_or = []
    min_grade=0
    regex_course_with_minimum_as_text_format = r'minimum\s*of\s*([0-9]{1,2}|100)%\s*in\s*[A-Z]{3}[0-9]{3}[H|Y]1' #Format: minimum of ##% in XXX###H1
    regex_course_with_grade_number_only_format = r'^[A-Z]{3}[0-9]{3}[H|Y]1\s*\(([0-9]{1,2}|100)%\)$' #Format: XXX###H1 (##%) or XXX###H1(##%)
    regex_course_with_min_grade_format_all = r'minimum\s*of\s*([0-9]{1,2}|100)%\s*in\s*[A-Z]{3}[0-9]{3}[H|Y]1|^[A-Z]{3}[0-9]{3}[H|Y]1\s*\(([0-9]{1,2}|100)%\)$'

    for match in re.finditer(regex_course_format_stg_all, course_prereq_page_list):
        course=match.group()

        #various flags

        if course.endswith('5'):
            continue
        if course == '/' :
            if is_in_parenthesis:
                is_parenthesis_or = True
            continue
        elif course == ',' or course=='and':
            if is_parenthesis_or and parenthesis_or:
                parenthesis_group.append(parenthesis_or)
                is_parenthesis_or = False
                parenthesis_or = []
                is_first_or = True
                continue
        elif (course == ';'):
            this_course_prereq.append(current_prereq_group)
            current_prereq_group = []
            continue
        elif (course == '('):
            is_in_parenthesis = True;
        elif (course == ')' ):
            if parenthesis_or and parenthesis_or:
                parenthesis_group.append(parenthesis_or)
            if parenthesis_group:
                current_prereq_group.append(parenthesis_group)
            is_in_parenthesis = False;
            is_parenthesis_or = False
            is_first_or = True
            parenthesis_group = []
            parenthesis_or = []
            continue


        #check if there is a minimum grade req
        elif re.search(regex_course_with_min_grade_format_all,course):
            min_grade =re.search(regex_percent_format,course)
            course = re.search(regex_course_format_ONLY_stg,course).group(0)

        #check if the course object alr exist, if not create new one
        #manage min grade if there is one
        if re.match(regex_course_format_ONLY_stg, course):
            check_existing = next((x for x in global_courses_list if x.course_name == course), None)

            if check_existing is None:
                course = Course(course)
                global_courses_list.append(course)
            else:
                course = check_existing

            if course in currently_added:
                continue
            else:
                currently_added.append(course)

            debug_controls_msg(course, False)

            course.add_unlock(course_code)
            if min_grade != 0:
                course.prereq_min_grade_map_add(course_code, min_grade)
                min_grade = 0

        if (is_in_parenthesis):
            if is_parenthesis_or and parenthesis_group:
                if is_first_or:
                    prev_course = parenthesis_group.pop()
                    parenthesis_or.append(prev_course)
                    is_first_or = False
                parenthesis_or.append(course)

            elif isinstance(course,Course):
                parenthesis_group.append(course)
        elif isinstance(course, Course):
            current_prereq_group.append(course)

    if current_prereq_group:
        this_course_prereq.append(current_prereq_group)
    course_code.add_prereq_list(this_course_prereq)

def debug_controls_msg(message, is_debug):
    if is_debug:
        print(message)


if __name__ == '__main__':
    get_courses()
    for c in global_courses_list:
        if c.course_name in visited:
            continue
        visited.add(c.course_name)
        parse_single_course(c)
        c.print_course_prereq()
        #c.print_min_grade_map()

    for c in global_courses_list:
        c.print_min_grade_map()
    print(*global_courses_list)


	#should export to JSON (?)
from collections import Counter

counts = Counter(c.course_name for c in global_courses_list)
print([(k, v) for k, v in counts.items() if v >= 1])

'''
(ECO101H1(63%), ECO102H1(63%))
 ECO105Y1(80%)
; 
MAT133Y1
( MAT130H1/ MAT135H1, MAT136H1)
 ( MAT148H1, MAT149H1/ MAT137Y1)
  ( MAT158H1, MAT159H1/ MAT157Y1) 
  
Expected Output:
 [
 [
    [ECE101H1, ECE102H1],
    ECO105Y1
 ],
 [
    MAT133Y1,
    [[MAT130H1, MAT135H1],MAT136H1]
    [MAT148H1,[ MAT149H1, MAT137Y1]]
    [MAT158H1,[MAT159H1,MAT157Y1]
 ]
 ]
  ECO220Y1: [[[ECO101H1, ECO102H1], ECO105Y1], [MAT133Y1, [[MAT130H1, MAT135H1], MAT136H1], [MAT148H1], [MAT158H1, [MAT149H1, MAT137Y1]]]]

'''
