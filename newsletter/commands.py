from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from driver_manager import get_driver

def press_tab():
    driver = get_driver()
    ActionChains(driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()

def press_ctrl_enter():
    driver = get_driver()
    ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.ENTER).key_up(Keys.CONTROL).key_up(Keys.ENTER).perform()

def press_key_chain(*keys):
    driver = get_driver()
    chain = ActionChains(driver)
    for key in keys:
        _key = getattr(Keys,key) if hasattr(Keys,key) else key
        chain.key_down(_key)
    for key in keys:
        _key = getattr(Keys,key) if hasattr(Keys,key) else key
        chain.key_up(_key)
    chain.perform()

def copy():
    press_key_chain("CONTROL","c")

def select_all():
    press_key_chain("CONTROL","a")

def paste():
    press_key_chain("CONTROL","v")

def new_tab(url=None):
    driver = get_driver()
    dest = url if url is not None else ""
    current_handles = driver.window_handles
    driver.execute_script("window.open({});".format(dest))
    new_handles = driver.window_handles
    for handle in current_handles:
        if handle in new_handles:
            new_handles.remove(handle)
        else:
            raise Exception("Page was close without consent, old pages : {}, new pages : {}".format(current_handles,new_handles))
    assert len(new_handles)==1, "More than 1 page was created! old pages : {}, new pages : {}".format(current_handles,new_handles)
    return new_handles[0]

def go_to_tab(index):
    driver = get_driver()
    driver.switch_to.window(driver.window_handles[index])
