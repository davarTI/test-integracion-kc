from behave import fixture, use_fixture
from selenium import webdriver


@fixture
def selenium_browser_chrome(context):
    context.browser = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.CHROME,
                                       command_executor='http://selenium:4444/wd/hub')
    context.browser.implicitly_wait(15)
    yield context.browser
    context.browser.quit()


def before_feature(context, feature):
    use_fixture(selenium_browser_chrome, context)
