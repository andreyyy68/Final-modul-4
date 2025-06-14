from pydantic import BaseModel
from pydantic import Field
from typing import Optional
from roles.roles import Roles
from playwright.sync_api import Playwright, sync_playwright, expect
import playwright

import pytest

class User(BaseModel):
    email: str = Field(..., description="@")
    fullName: str
    password: str = Field(..., min_length=8)
    passwordRepeat: str
    roles: list[Roles]
    banned: Optional[bool] = None
    verified: Optional[bool] = None

@pytest.mark.xfail
def test_user(test_user):
    user = User(**test_user)
    assert user.email == test_user['email']
    assert user.password == test_user['password']
    js_user = user.model_dump_json(exclude_unset=True)
    print(js_user)

@pytest.mark.xfail
def test_data(creation_user_data):
    data = User(**creation_user_data)
    assert data.email == creation_user_data['email']
    assert data.fullName == creation_user_data['fullName']
    js_data = data.model_dump_json()
    print(js_data)

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

product = Product(name= 'banana', price=999.99, in_stock=False)

product_json = product.model_dump_json()
print(product_json)

new_prod = Product.model_validate_json(product_json)
print(new_prod)

def test_text_box(page):
    page.goto('https://demoqa.com/text-box')

    username_locator = '#userName'
    email_locator = '#userEmail'
    currentAddress_locator = '#currentAddress'
    permanentAddress_locator = '#permanentAddress'

    page.fill(username_locator, 'testQA')
    page.fill(email_locator, 'test@qa.com')
    page.fill(currentAddress_locator, 'Volgograd')
    page.fill(permanentAddress_locator, 'Volgograd')

    page.click('button#submit')

    expect(page.locator('#output #name')).to_have_text('Name:testQA')
    expect(page.locator('#output #email')).to_have_text('Email:test@qa.com')
    expect(page.locator('#output #currentAddress')).to_have_text('Current Address :Volgograd')
    expect(page.locator('#output #permanentAddress')).to_have_text('Permananet Address :Volgograd')



def test_codgen_run(playwright: Playwright) -> None:
    username_locator = '#userName'
    email_locator = '#userEmail'
    currentAddress_locator = '#currentAddress'
    permanentAddress_locator = '#permanentAddress'

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demoqa.com/text-box")
    page.fill(username_locator, '312')
    page.fill(email_locator, 'nkl.rif@gmail.com')
    page.fill(currentAddress_locator, '123')
    page.fill(permanentAddress_locator, '123')
    page.click('button#submit')

    # ---------------------
    context.close()
    browser.close()


