# Standard libraries
import shutil

# Selenium exceptions
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import SessionNotCreatedException


def chrome():
    from selenium.webdriver import Chrome
    from selenium.webdriver import ChromeOptions

    service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1']

    options = ChromeOptions()

    # options.binary_location = '/usr/bin/google-chrome'
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    # options.add_argument('--enable-precise-memory-info')
    # options.add_argument('--remote-debugging-port=9225')

    chrome = Chrome(
        options=options,
        executable_path='bin/chromedriver.exe',
        service_args=service_args,
    )
    # chrome.set_page_load_timeout(BROWSER_PAGE_LOAD_TIMEOUT)
    # chrome.set_window_position(2000, 50)

    return chrome


def firefox():
    # Doesn't work. Eat cum.
    from selenium.webdriver import Firefox

    try:
        return Firefox('bin/geckodriver')

    except (OSError, WebDriverException, SessionNotCreatedException):
        from webdriver_manager.firefox import GeckoDriverManager

        path = GeckoDriverManager().install()
        shutil.move(path, 'bin/geckodriver')

        return Firefox('bin/geckodriver')


def get_driver(driver):
    """ mega useful manager """
    method = globals().get(driver)

    if not method:
        raise KeyError('Method not found! Aborting.')

    return method
