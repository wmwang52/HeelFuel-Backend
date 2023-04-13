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
#Complete scraping code

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import threading


class foodItem:
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

    def __str__(self):
        return f"{self.name}\n{self.servingSize}\n{self.calories}\n{self.allergens}\n{self.ingredients}\n"

#This method should get all the food names from the given HTML file, need to add error handleing
def allFoodItemNames(pageLink):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"{pageLink}")

    diningHallPageData = driver.find_elements(By.CLASS_NAME, "menu-station")
    finalFoodList = []
    mealFoodList = []
    for MenuStation in diningHallPageData:
        MenuStation = MenuStation.get_attribute("innerHTML").split("tabindex=\"0\">")
        newList = []

        for i in MenuStation:
            if "</a>\n" in i:

                i = i.split("</a>\n")

                if "&amp" in i[0]:
                    i[0] = i[0].replace("&amp;", "&")
                    print(i[0])

                newList.append(i[0].strip())


        if "Strawberry Kiwi Juice" in newList:
            mealFoodList.append(newList)
            finalFoodList.append(mealFoodList)
            mealFoodList = []
        else:
            mealFoodList.append(newList)
    driver.quit()

    for i in finalFoodList:
        print(i)

    return finalFoodList

# This method returns all the raw data given, and cleans the ingredient data and allergen data.
def getData(foodItem, webpageLink):
    fullData = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    try:

        driver.get(f"{webpageLink}")
    except:
        exit("LINK IS INVALID")

    try:
        driver.find_element(By.LINK_TEXT, f"{foodItem}").click()
    except:
        print(foodItem)
        exit("Food Item is INVALID")

    time.sleep(1)

    NutritionData = driver.find_element(By.CLASS_NAME, "nutrition-facts-table").get_attribute("innerHTML")

    extraRawData = driver.find_elements(By.CSS_SELECTOR, "p")

    if "Ingredients" in extraRawData[0].get_attribute("innerHTML"):
        ingredients = extraRawData[0].get_attribute("innerHTML")
        ingredients = ingredients.replace("<strong>", "")
        ingredients = ingredients.replace("</strong>", "")
        ingredients = ingredients.title()
        fullData.append(NutritionData)
        fullData.append(ingredients)
    else:
        allergens = extraRawData[0].get_attribute("innerHTML")
        ingredients = extraRawData[1].get_attribute("innerHTML")
        ingredients = ingredients.replace("<strong>", "")
        ingredients = ingredients.replace("</strong>", "")
        ingredients = ingredients.title()
        fullData.append(NutritionData)
        fullData.append(allergens)
        fullData.append(ingredients)

    driver.quit()

    return fullData


# This method JUST cleans the raw data, and appends the allergens list and raw data list.
def cleanData(rawData, name):
    parsed = rawData[0].split("<th")
    nutritionList = []

    for item in parsed:
        firstItem = item.split("</th>")
        secondItem = firstItem[0].split("\n")
        if len(secondItem) > 2:
            if "<b>" in secondItem[1]:
                cleanedData = secondItem[1].replace("<b>", "")
                cleanedData = cleanedData.replace("</b>", "")
                cleanedData = cleanedData.replace("\t", "")
                nutritionList.append(cleanedData.strip() + ": " + secondItem[2].strip())
            elif "<strong>" in secondItem[1]:
                secondItem[1] = secondItem[1].replace("<strong>", "")
                secondItem[1] = secondItem[1].replace("</strong>", ":")
                nutritionList.append(secondItem[1].strip())
            else:
                nutritionList.append(secondItem[1].strip() + ": " + secondItem[2].strip())

    del nutritionList[0]

    if len(rawData) > 2:
        nutritionList.append(rawData[2])
        nutritionList.append(f"Allergens: {rawData[1]}")
        newFoodItem = foodItem(name, nutritionList[0], nutritionList[1], nutritionList[2], nutritionList[3],
                               nutritionList[4],
                               nutritionList[5], nutritionList[6], nutritionList[7], nutritionList[8], nutritionList[9],
                               nutritionList[10], nutritionList[11], nutritionList[12], nutritionList[13])
    else:
        nutritionList.append(rawData[1])
        newFoodItem = foodItem(name, nutritionList[0], nutritionList[1], nutritionList[2], nutritionList[3],
                               nutritionList[4],
                               nutritionList[5], nutritionList[6], nutritionList[7], nutritionList[8], nutritionList[9],
                               nutritionList[10], nutritionList[11], nutritionList[12])

    print(newFoodItem)
    return nutritionList


# This method is meant to write all the data given in a list to a file. Will not necessarily need after.
def writeToFile(textToWrite):
    with open("/Users/williamwang/Desktop/Test.txt", "a") as file:
        for i in textToWrite:
            file.write(i + "\n")
        file.close()