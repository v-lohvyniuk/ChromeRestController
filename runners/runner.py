from initialization import driver
from runners.commands import DriverCommand
from runners.models import ResponseModel
from runners import properties
import time
import threading


class ChromeCommander:
    REFRESH_TIME_SEC = properties.DRIVER_REFRESH_AVG_DELAY

    def __init__(self):
        self.driver = None
        self.is_awaken = False

        self.COMMANDS = {DriverCommand.START: self.__start,
                         DriverCommand.GET: self.__get,
                         DriverCommand.CLICK: self.__click,
                         DriverCommand.GET_ELEMENT_TEXT: self.__get_element_text,
                         DriverCommand.SEND_KEYS: self.__send_keys,
                         DriverCommand.TYPE: self.__type,
                         DriverCommand.GET_ATTR: self.__get_attr,
                         DriverCommand.GET_PAGE_SOURCE: self.__get_page_source
                         }

    def run_command(self, command: DriverCommand, kwargs):
        if not self.COMMANDS[command]:
            raise Exception(f"No handler found for command: {command}")
        self.__awake()
        response = ResponseModel()
        try:
            result = self.COMMANDS[command](kwargs)
            response.result = result
        except Exception as e:
            response.errors = e.__str__()

        self.__start_waiting()

        return response

    def __awake(self):
        self.is_awaken = True

    def __start_waiting(self):
        self.is_awaken = False
        thread = threading.Thread(target=self.wait_in_extra_thread)
        thread.daemon = True
        thread.start()

    def wait_in_extra_thread(self):
        delay_between_refreshes = ChromeCommander.REFRESH_TIME_SEC
        while True:
            for _ in range(0, delay_between_refreshes):
                time.sleep(1)
                if self.is_awaken:
                    break

            if self.is_awaken:
                break

            self.driver.refresh()

    def __start(self, kwargs):
        self.driver = driver.DriverManager.get_driver()

    def __get(self, kwargs):
        url = kwargs["url"]
        driver.DriverManager.get_driver().get(url)

    def __click(self, kwargs):
        xpath = kwargs["xpath"]
        self.driver.find_element_by_xpath(xpath).click()

    def __get_element_text(self, kwargs):
        xpath = kwargs["xpath"]
        return self.driver.find_element_by_xpath(xpath).text

    def __type(self, kwargs):
        xpath = kwargs["xpath"]
        keys = kwargs["keys"]
        web_element = self.driver.find_element_by_xpath(xpath)
        web_element.clear()
        web_element.send_keys(keys)

    def __send_keys(self, kwargs):
        xpath = kwargs["xpath"]
        keys = kwargs["keys"]
        web_element = self.driver.find_element_by_xpath(xpath)
        web_element.send_keys(keys)

    def __get_attr(self, kwargs):
        xpath = kwargs["xpath"]
        attr_name = kwargs["attr_name"]
        web_element = self.driver.find_element_by_xpath(xpath)
        return web_element.get_attribute(attr_name)

    def __get_page_source(self, kwargs):
        return self.driver.page_source
