import allure
from pydantic import ValidationError
from core.models.Booking import BookingResponse
import requests


@allure.feature('Test Create Booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data

    response = api_client.create_booking(booking_data)
    print(response)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response was not validated: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test Create Booking')
@allure.story('Positive: creating booking with different checkin and checkout dates')
def test_create_booking_with_different_dates(api_client, booking_dates):
    booking_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": booking_dates,
        "additionalneeds": "Lunch"
    }

    response = api_client.create_booking(booking_data)
    print(response)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response was not validated: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test Create Booking')
@allure.story('Negative: creating booking with unknown field')
def test_create_booking_with_unknown_field(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    booking_data['unknown_field'] = 'Invalid data'
    response = api_client.create_booking(booking_data)
    print(response)
    assert 'unknown_field' not in response['booking'], "Unknown field found in the response"
    try:
        BookingResponse(**response)
    except ValidationError as e:
        assert str(e).contains('unknown_field')


@allure.feature('Test Create Booking')
@allure.story('Negative: creating booking with missing required field')
def test_create_booking_with_missing_required_field(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    del booking_data['firstname']  # Убираем firstname

    try:
        # Пытаемся отправить запрос
        response = api_client.create_booking(booking_data)
        print(response)

        # Если ошибка 400, это ожидаемо, а если 500, то это ошибка на сервере
        assert response.status_code == 400, f"Expected 400 error, got {response.status_code}"
        assert 'firstname' in response.text, "Expected 'firstname' validation error"

    except requests.exceptions.HTTPError as e:
        # В случае других ошибок, ловим их и показываем в тесте
        assert "500 Server Error" in str(e), f"Unexpected error: {e}"


@allure.feature('Test Create Booking')
@allure.story('Negative: creating booking with missing required field "lastname"')
def test_create_booking_with_missing_lastname(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    del booking_data['lastname']  # Убираем lastname

    try:
        # Пытаемся отправить запрос
        response = api_client.create_booking(booking_data)
        print(response)

        # Если ошибка 400, это ожидаемо, а если 500, то это ошибка на сервере
        assert response.status_code == 400, f"Expected 400 error, got {response.status_code}"
        assert 'lastname' in response.text, "Expected 'lastname' validation error"

    except requests.exceptions.HTTPError as e:
        # В случае других ошибок, ловим их и показываем в тесте
        assert "500 Server Error" in str(e), f"Unexpected error: {e}"
