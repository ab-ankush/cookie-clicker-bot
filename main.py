from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")
money = driver.find_element(By.ID, "money")

items = driver.find_elements(By.CSS_SELECTOR, "#store div")
items_id = [item.get_attribute("id") for item in items]


timeout = time.time() + 2
five_min = time.time() + 60 * 10

while (money.text != "500"):
    cookie.click()

    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []
        for price in all_prices:
            if price.text != "":
                item_prices.append(
                    int(price.text.split("-")[1].strip().replace(",", "")))

        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = items_id[n]
        # print(cookie_upgrades)

        money_amount = int(money.text.replace(",", ""))
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if money_amount > cost:
                affordable_upgrades[cost] = id

        highest_affordable_upgrade = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_affordable_upgrade]

        driver.find_element(By.ID, to_purchase_id).click()

        timeout = time.time() + 5

        if time.time() > five_min:
            cookie_per_s = driver.find_element(By.ID, "cps").text
            print(cookie_per_s)
            break


driver.quit()
