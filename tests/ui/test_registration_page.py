import pytest
import time
import allure

from playwright.sync_api import Page, sync_playwright, expect
from random import randint
from datetime import datetime
from utils.data_generator import DataGenerator
from models.page_object import CinescopeRegisterPage, LoginPage


def test_registration(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    username_locator = '[data-qa-id="register_full_name_input"]'
    email_locator = '[data-qa-id="register_email_input"]'
    password_locator = '[data-qa-id="register_password_input"]'
    repeat_password_locator = '[data-qa-id="register_password_repeat_input"]'

    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    page.fill(username_locator, random_name)
    page.fill(email_locator, random_email)
    page.fill(password_locator, random_password)
    page.fill(repeat_password_locator, random_password)

    page.get_by_role('button', name='Зарегистрироваться').click()

    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login', timeout=10000)
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)


def test_locator(page: Page):
    page.goto('https://demoqa.com/webtables', wait_until='domcontentloaded')

    page.locator('button').filter(has_text='Add')

    page.locator('#addNewRecordButton').click()

    form_title = page.locator('.modal-content .modal-header .modal-title')
    expect(form_title).to_be_visible()
    expect(page.get_by_text("Registration Form")).to_be_visible(visible=True)

    loc = page.get_by_placeholder('First Name')
    loc.fill('Andrew')
    page.fill('#lastName', 'Meow')
    page.fill('#userEmail', 'antoshka@gmail.com')
    page.fill('#age', '22')
    page.fill('#salary', '123')
    page.fill('#department', 'QA')
    loc_submit = page.get_by_role('button', name='Submit')
    loc_submit.click()


def test_form(page: Page):
    page.goto('https://demoqa.com/automation-practice-form', wait_until='domcontentloaded')

    page.wait_for_selector('#firstName')

    today = datetime.today().strftime("%Y-%m-%d")
    value = page.get_attribute('#dateOfBirthInput', 'value')
    assert value == "05 Jun 2025", 'Даты не равны'

    page.fill('#firstName', 'andrew')
    page.type('#lastName', 'Gav')
    page.fill('#userEmail', 'qAteam@gmail.com')

    page.locator('label[for="gender-radio-1"]').click()

    page.fill('#userNumber', '2222222222')

    page.locator('#dateOfBirthInput').click()
    page.locator('.react-datepicker__year-select').select_option('2025')
    page.locator('.react-datepicker__month-select').select_option('5')
    page.locator('.react-datepicker__day--004:not(.react-datepicker__day--outside-month)').click()

    page.fill('#subjectsInput', 'English')
    page.locator('.subjects-auto-complete__menu-list').get_by_text('English').click()

    page.locator('label[for="hobbies-checkbox-1"]').click()

    page.fill('#currentAddress', 'Volgograd st')

    page.locator('#state').click()
    page.locator('#stateCity-wrapper').get_by_text('NCR', exact=True).click()

    page.locator('#city').click()
    page.locator('#stateCity-wrapper').get_by_text('Delhi', exact=True).click()

    page.locator('#submit').click()

    footer = page.locator('footer').text_content()

    assert footer == '© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED.', 'Надписи в футере не равны'


def test_visibility(page: Page):
    page.goto('https://demoqa.com/radio-button', wait_until='domcontentloaded')
    page.wait_for_selector('#yesRadio')

    assert page.is_enabled('#yesRadio'), 'Radio Button not activated'
    assert page.is_enabled('#impressiveRadio'), 'Radio Button not activated'
    assert page.is_disabled('#noRadio'), 'Radio button activated'


def test_new_visibility(page: Page):
    page.goto('https://demoqa.com/checkbox', wait_until='domcontentloaded')

    assert page.is_visible('text=Home'), 'Home не виден'
    assert not page.is_visible('text=Desktop'), 'Desktop виден'
    page.click('button[aria-label="Toggle"]')
    assert page.is_visible('text=Desktop'), 'Desktop не виден'

def test_time_visibility(page: Page):
    page.goto('https://demoqa.com/dynamic-properties', wait_until='domcontentloaded')

    assert not page.is_visible('#visibleAfter'), 'Элемента нет'
    page.wait_for_selector('#visibleAfter')

def test_expect(page: Page):
    page.goto('https://demoqa.com/radio-button', wait_until='domcontentloaded')

    yes_radio = page.get_by_role("radio", name="Yes")
    impressive_radio = page.get_by_role("radio", name="Impressive")
    no_radio = page.get_by_role("radio", name="No")
    expect(no_radio).to_be_disabled()  # проверяем, что не доступен
    expect(yes_radio).to_be_enabled()  # проверяем, что доступен
    expect(impressive_radio).to_be_enabled()  # проверяем, что доступен
    page.locator('[for="yesRadio"]').click()  # тут хитрый лейбл не позволяет кликнуть прямо на инпут, обращаемся по лейблу
    expect(yes_radio).to_be_checked()  # проверяем, что отмечен
    expect(impressive_radio).not_to_be_checked()  # проверяем, что не отмечен


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestLoginPage:
    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self, registered_user, page):

        login_page = LoginPage(page)  # Создаем объект страницы Login

        login_page.open()
        login_page.login(registered_user.email, registered_user.password)  # Осуществяем вход

        login_page.assert_was_redirect_to_home_page()  # Проверка редиректа на домашнюю страницу
        login_page.make_screenshot_and_attach_to_allure()  # Прикрепляем скриншот
        login_page.assert_allert_was_pop_up()  # Проверка появления и исчезновения алерта

            # Пауза для визуальной проверки (нужно удалить в реальном тестировании)
        time.sleep(5)


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
    @allure.title("Проведение успешной регистрации")
    def test_register_by_ui(self, page):

        # Подготовка данных для регистрации
        random_email = DataGenerator.generate_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_random_password()


        register_page = CinescopeRegisterPage(page)
        register_page.open()
        register_page.register(f"PlaywrightTest {random_name}", random_email, random_password,
                                   random_password)

        register_page.assert_was_redirect_to_login_page()  #
        register_page.make_screenshot_and_attach_to_allure()
        register_page.assert_allert_was_pop_up()























