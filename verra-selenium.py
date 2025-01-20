import json
import random
import time
from urllib.parse import quote

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from collections import defaultdict

project_id = 5401

def get_project_id(driver: webdriver.Chrome):
    id = driver.find_element(by=By.XPATH, value="/html/body/apx-root/div/div/apx-project-detail/div/div/div[1]/div[1]/div/apx-breadcrumb/nav/span")

    id_text = id.text.replace("Project ", "")

    return id_text

def get_project_title(driver: webdriver.Chrome):
    title = driver.find_element(by=By.CLASS_NAME, value="card-header")

    return title.text

def get_project_description(driver: webdriver.Chrome):
    title = driver.find_element(by=By.CLASS_NAME, value="card-text")

    return title.text

def get_project_summary(driver: webdriver.Chrome):
    summary = defaultdict()
    summary["state"] = driver.find_element(by=By.CSS_SELECTOR, value="tr.attr-row:nth-child(4)").text

    vcs = defaultdict(str)

    vcs["proponent"] = driver.find_element(by=By.CSS_SELECTOR, value="tr.attr-row:nth-child(3)").text
    
    vcs["status"] = driver.find_element(by=By.CSS_SELECTOR, value="tr.attr-row:nth-child(5)").text

    vcs["estimatedAnnualEmissionReductions"] = int(driver.find_element(by=By.CSS_SELECTOR, value="tr.attr-row:nth-child(7)").text)

    vcs["projectType"] = driver.find_element(by=By.CSS_SELECTOR, value="tr.attr-row:nth-child(9)").text

    vcs["afoluActivity"] = driver.find_element(by=By.CSS_SELECTOR, value="tr.attr-row:nth-child(11)").text
    vcs["methodology"] = driver.find_element(by=By.CSS_SELECTOR, value="tr.attr-row:nth-child(13)").text

    areaWithUnits = driver.find_element(by=By.CSS_SELECTOR, value="tr.attr-row:nth-child(15)").text

    value = int(areaWithUnits[: areaWithUnits.find(" ")])
    unit = areaWithUnits[areaWithUnits.find(" ")+1 : ]

    area = defaultdict(str)
    area["value"] = value
    area["unit"] = unit

    vcs["area"] = area

    cp = driver.find_element(by=By.CSS_SELECTOR, value="tr.attr-row:nth-child(17)").text

    term = cp[: cp.find(",")]
    startDate = cp[cp.find(",")+1 : cp.find("-")].strip()
    endDate = cp[cp.find("-")+1 : ].strip()

    creditingPeriod = defaultdict(str)
    creditingPeriod["term"] = term
    creditingPeriod["startDate"] = startDate
    creditingPeriod["endDate"] = endDate

    vcs["creditingPeriod"] = creditingPeriod

    summary["vcs"] = vcs

    return summary




project = defaultdict(str)

project["id"] = str(project_id)
project["title"] = get_project_title()
project["description"] = get_project_description()
project["summary"] = get_project_summary()
project["documents"] = get_project_documents()

