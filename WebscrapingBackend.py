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
