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
