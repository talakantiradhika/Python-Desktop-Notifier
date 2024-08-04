import time
import win32api
import win32con
import win32gui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def show_notification(title, message):
    # Create a notification window using win32gui
    win32gui.MessageBox(None, message, title, win32con.MB_ICONINFORMATION)


def get_whatsapp_notifications():
    # Path to your ChromeDriver executable
    chrome_driver_path = "C:\\chromedriver.exe"

    # Start Chrome in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver_service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)

    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com/")
    time.sleep(10)  # Wait for user to scan QR code and load WhatsApp

    # Get the chats
    chats = driver.find_elements(By.XPATH, '//div[@class="_2aBzC"]/div/div/div/div')

    # Loop through the chats and extract new message notifications
    for chat in chats:
        chat.click()
        time.sleep(1)  # Wait for chat to load

        # Get the unread message count
        unread_count_elem = driver.find_element(By.XPATH, '//span[@class="_31gEB"]')
        unread_count = int(unread_count_elem.text)

        # Get the last message in the chat
        messages = driver.find_elements(By.XPATH, '//div[@class="i0jNr selectable-text copyable-text"]')
        last_message = messages[-1].text if messages else ''

        # Display desktop notification for each new message
        if unread_count > 0:
            notification_title = 'WhatsApp Notification'
            notification_message = f'{unread_count} new messages\n\n{last_message}'
            show_notification(notification_title, notification_message)

    # Close the browser
    driver.quit()


# Call the function to start receiving WhatsApp notifications
get_whatsapp_notifications()
