from time import sleep
from selenium import webdriver
from secrets import pw


class InstaBot:
    def __init__(self, username, pw):
        self.username = username
        self.driver = webdriver.Chrome()
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(2)

    def _load_scrollbox(self, xpath):
        scroll_box = self.driver.find_element_by_xpath(xpath)
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight""", scroll_box)
        return scroll_box

    def _get_names(self):
        scroll_box = self._load_scrollbox("/html/body/div[4]/div/div[2]")
        profiles = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in profiles if name.text != '']
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        return names

    def _confirm_unfollow(self, not_following_back: list):
        scroll_box = self._load_scrollbox("/html/body/div[4]/div/div[2]")
        sleep(10)
        profiles = scroll_box.find_elements_by_tag_name('li')
        for profile in profiles:
            elements = profile.find_elements_by_tag_name('a')
            name = elements[0].text if elements[0].text != '' else elements[1].text
            if name in not_following_back:
                profile.find_elements_by_xpath("//button[contains(text(), 'Following')]")[profiles.index(profile)].click()
                sleep(2)
                # self.driver.find_element_by_xpath("/html/body/div[5]/div/div")\
                #    .find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
                not_following_back.remove(name)
        return

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(self.username)).click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href, '/following')]").click()
        sleep(2)
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href, '/followers')]").click()
        sleep(2)
        followers = self._get_names()
        not_following_back = [user for user in following if user not in followers]
        # print(not_following_back)
        self._confirm_unfollow(not_following_back)


# create a separate file secrets.py and specify the value of pw.
# e.g: pw = "your password"
# replace with your username
ig_bot = InstaBot('your username', pw)
ig_bot.get_unfollowers()
