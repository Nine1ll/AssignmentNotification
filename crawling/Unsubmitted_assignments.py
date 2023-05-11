from bs4 import BeautifulSoup
import time
from selenium import webdriver


MJU_ID = "ID"
MJU_PASSWORD = "PASSWORD"


def login(dr):
    url = 'https://home.mju.ac.kr/user/index.action'
    dr.get(url)
    time.sleep(2)
    dr.find_element("xpath", '//*[@id="classlogin"]/div/div[2]/div[1]/div[2]/a[1]').click()
    time.sleep(3)

    dr.find_element('name', 'id').send_keys(MJU_ID)
    dr.find_element('name', 'passwrd').send_keys(MJU_PASSWORD)
    time.sleep(2)
    dr.find_element('xpath', '//*[@id="loginButton"]').click()


def unsubmitted_assignments():
    """제출하지 않은 과제만 과목명 {과목명 : 과제 이름}으로 불러오는 파일"""
    driver = webdriver.Chrome(executable_path='/Users/nine1ll/Documents/Python/homework_control/crawling/chromedriver')
    driver2 = webdriver.Chrome(executable_path='/Users/nine1ll/Documents/Python/homework_control/crawling/chromedriver')
    try:
        login(driver2)
        url = 'https://home.mju.ac.kr/user/index.action'
        driver.get(url)
        time.sleep(2)
        driver.find_element("xpath", '//*[@id="classlogin"]/div/div[2]/div[1]/div[2]/a[1]').click()
        time.sleep(3)

        driver.find_element('name', 'id').send_keys(MJU_ID)
        driver.find_element('name', 'passwrd').send_keys(MJU_PASSWORD)
        time.sleep(2)
        driver.find_element('xpath', '//*[@id="loginButton"]').click()

        request = driver.page_source
        soup = BeautifulSoup(request, 'html.parser')

        assignments = []
        unsubmitted_assignments = []

        url_assignments = []
        subject_names = []
        assignment_names=[]
        submit_ox = []
        deadline_list = []

        # page 수
        pages = soup.select(".eClassList .paging li:nth-child(2) ul li")
        for i, page in enumerate(pages):

            page_assignment = []
            urls_assignment = []
            # 과제 pages 수
            if i != 0:
                url_assignments_page = f"https://home.mju.ac.kr/mainIndex/myHomeworkList.action?page={i + 1}&tab=homework"
                driver.get(url_assignments_page)
                time.sleep(3)
                request = driver.page_source
                soup = BeautifulSoup(request, 'html.parser')
            # 과제 이름
            assignments_names = soup.select("dt a strong")
            for name in assignments_names:
                # 안 -> 페이지 마다 반복됨.
                page_assignment.append(name.text.strip())
                # 과목명
                subject_name = name.text.strip().split(']')[0][1:]
                subject_names.append(subject_name)
                # 과제명
                page_assignment_name = name.text.strip().split(']')[1]
                assignment_names.append(page_assignment_name)
                # 밖
                assignments.append(name.text.strip())
            # 과제 url
            links = soup.select("dt a", href=True)
            for link in links:
                # 안
                urls_assignment.append(link['href'])
                # # 밖
                url_assignments.append(link['href'])
            # 과제 제출 여부
            submitted = soup.select(".information p:nth-child(3) span:nth-child(2)")
            for index, submit in enumerate(submitted):
                submit_ox.append(submit.text.strip())
                if submit.text.strip() == "미제출":
                    url_link = urls_assignment[index]
                    #과제 기한
                    url_page = f"https://home.mju.ac.kr{url_link}"
                    driver2.get(url_page)
                    time.sleep(2)
                    request2 = driver2.page_source
                    soup2 = BeautifulSoup(request2, 'html.parser')
                    deadlines = soup2.select("#FrameRight > div.UIlistSort > div.sortR > dl > dd:nth-child(6)")
                    for deadline in deadlines:
                        deadline_split = deadline.text.split()
                        length = len(deadline_split)

                        deadline_time = deadline_split[length-1]
                        deadline_date = deadline_split[length-2]
                        deadline_temp = f"{deadline_date}, {deadline_time}"
                        deadline_list.append(deadline_temp)
                else:
                    pass

        for i, submit_x in enumerate(submit_ox):
            if submit_x == "미제출":
                index = 0

                subject = {subject_names[i]: {
                    "과제명": assignment_names[i],
                    "기한": deadline_list[index],
                    "url": f'https://home.mju.ac.kr{url_assignments[i]}'
                }}
                unsubmitted_assignments.append(subject)
                index+=1
        print(f"미제출 과제 : {unsubmitted_assignments}, {len(unsubmitted_assignments)}\n")
    except AttributeError as e:
        print(e)


unsubmitted_assignments()
