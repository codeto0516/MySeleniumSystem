from .Chrome import Chrome
from .Wait import Wait
from .Window import Window

class MySeleniumSystem:
    def __init__(self, *args, **kwargs) -> None:
        self.chrome = Chrome(args, kwargs)
        self.chrome.active()
        self.driver = self.chrome.driver

        self.wait = Wait(self.driver)
        self.window = Window(self.driver)
