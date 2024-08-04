import time
import win10toast
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class WhatsAppNotifier:
    def _init_(self):
        self.last_message_time = None

    def check_messages(self):
        # Path to your ChromeDriver executable
        chrome_driver_path = "C:\\chromedriver.exe"

        # Start Chrome in headless mode
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)

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
                title = f"New Message from {chat.text}"
                message = f"{unread_count} new messages\n\n{last_message}"
                toaster.show_toast(title, message, duration=5)

        # Close the browser
        driver.quit()


# Example usage
app = WhatsAppNotifier()
app.check_messages()