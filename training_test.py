from pydantic import BaseModel
from pydantic import Field
from typing import Optional
from roles.roles import Roles

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

