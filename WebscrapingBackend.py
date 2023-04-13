from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import threading
import json
import os
import firebase_admin
from firebase_admin import credentials
import requests
from datetime import datetime


# This method is meant to write all the data given in a list to a file. Will not necessarily need after.
def writeToFile(textToWrite):
    with open("/Users/williamwang/Desktop/Test.txt", "a") as file:
        file.write(textToWrite)
        file.close()


class Food:
    def __init__(self, name, servingSize, calories, fatCalories, totalFat, saturatedFat, transFat, cholesterol, sodium,
                 totalCarbohydrate, dietaryFiber, sugars, protein, ingredients,
                 allergens="No common allergens. Look at ingredients List."):
        self.name = name
        self.servingSize = servingSize
        self.calories = calories
        self.caloriesFromFat = fatCalories
        self.totalFat = totalFat
        self.saturatedFat = saturatedFat
        self.transFat = transFat
        self.cholestrol = cholesterol
        self.sodium = sodium
        self.totalCarbohydrate = totalCarbohydrate
        self.dietaryFiber = dietaryFiber
        self.sugars = sugars
        self.protein = protein
        self.allergens = allergens
        self.ingredients = ingredients

    def toString(self):
        return f"{self.name}\n{self.servingSize}\n{self.calories}\n{self.allergens}\n{self.ingredients}\n\n\n"


# This method should get all the food names from the given HTML file, need to add error handling
def allFoodItemNames(pageLink):
    # Creates the options for the newly launched Chrome browser to be in the background.
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Creates the web driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"{pageLink}")

    html = driver.page_source
    time.sleep(1)
    soup = BeautifulSoup(html, 'html.parser')
    menu_stations = soup.find_all('div', class_='menu-station')
    totalMealPeriodList = []
    stationFoodList = []
    foodList = []
    for station in menu_stations:
        items = station.find_all('li')
        for item in items:
            food_name = item.find('a').text.strip()
            print(food_name)
            foodList.append(food_name)
        stationFoodList.append(foodList)

        if "Strawberry Kiwi Juice" in foodList:
            totalMealPeriodList.append(stationFoodList)
            stationFoodList = []
            foodList = []
        else:
            foodList = []

    driver.quit()
    return totalMealPeriodList


# This method returns all the raw data given, and cleans the ingredient data and allergen data.
def getData(foodItem, webpageLink, index):
    fullData = []
    fullData.append(foodItem)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Creates the web driver
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(webpageLink)
        driver.find_elements(By.CLASS_NAME, "c-tabs-nav__link")[index].click()
    except:
        driver.quit()
        raise ValueError("Invalid webpage link")

    try:
        driver.find_element(By.LINK_TEXT, foodItem).click()
    except:
        driver.quit()
        raise ValueError(f"Invalid food item: {foodItem}")

    time.sleep(0.25)

    try:
        NutritionData = driver.find_element(By.CLASS_NAME, "nutrition-facts-table").get_attribute("innerHTML")

        soup = BeautifulSoup(NutritionData, 'html.parser')
        NutritionList = []
        for row in soup.find_all('tr'):
            cells = row.find_all('th')
            NutritionList.append(cells[0].get_text().replace("\n", "").strip())

        fullData.append(NutritionList[0])
        for index in range(1, len(NutritionList)):
            tempValue = NutritionList[index].split("       ")
            tempValue[0] = tempValue[0].strip()
            tempValue[1] = tempValue[1].strip()
            NutritionList[index] = f"{tempValue[0]}:{tempValue[1]}"
            fullData.append(NutritionList[index])

        extraRawData = driver.find_elements(By.CSS_SELECTOR, "p")
    except:
        exit(f"{foodItem}")

    if "Ingredients" in extraRawData[0].get_attribute("innerHTML"):
        soup = BeautifulSoup(extraRawData[0].get_attribute("innerHTML"), 'html.parser')
        fullData.append(soup.get_text().title())
    else:
        soup = BeautifulSoup(extraRawData[1].get_attribute("innerHTML"), 'html.parser')
        fullData.append(soup.get_text().title())
        fullData.append(f"Allergens: {extraRawData[0].get_attribute('innerHTML')}")

    driver.quit()

    print(fullData)
    if "Ingredients" in fullData[-1]:

        foodItemNew = Food(fullData[0], fullData[1], fullData[2], fullData[3], fullData[4], fullData[5], fullData[6],
                           fullData[7], fullData[8], fullData[9], fullData[10], fullData[11], fullData[12],
                           fullData[13])
    else:
        foodItemNew = Food(fullData[0], fullData[1], fullData[2], fullData[3], fullData[4], fullData[5], fullData[6],
                           fullData[7], fullData[8], fullData[9], fullData[10], fullData[11], fullData[12],
                           fullData[13],
                           fullData[14])
    return foodItemNew


def webScrape(restaurant, mealSections):
    queryRestaurant = restaurant.lower().replace(" ", "-")
    date = str(datetime.today().strftime('%Y-%m-%d'))

    pageLink = f"https://dining.unc.edu/locations/{queryRestaurant}/?date={date}"
    foodList = allFoodItemNames(pageLink)

    FINALMEALLIST = []
    foodListFinal = []

    def finalFunction(item, link, index):
        foodListFinal.append(getData(item, f"{link}", index))

    for i in range(0, mealSections):

        threads = []

        for meal in foodList[i]:
            for food in meal:
                thread = threading.Thread(target=finalFunction, args=(food, pageLink, i))
                print(thread)
                threads.append(thread)
                thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

            for thread in threads:
                if thread.is_alive():
                    print("Thread is still running, stopping it now.")
                    thread.stop()

        FINALMEALLIST.append(foodListFinal)
        foodListFinal = []

    json_data = json.dumps([[item.__dict__ for item in inner_list] for inner_list in FINALMEALLIST])

    data = json.loads(json_data)

    cred = credentials.Certificate(
        '/Users/williamwang/Downloads/foodforthought-741c2-firebase-adminsdk-rqj46-4d105d5f9d.json')
    firebase_admin.initialize_app(cred)

    response = requests.put(f"https://foodforthought-741c2-default-rtdb.firebaseio.com/{restaurant.title()}Menu.json",
                            json=data)
    print(response.status_code)


webScrape("Chase",6)
