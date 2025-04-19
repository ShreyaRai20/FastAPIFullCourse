auth_prefix = f'/api/v1/auth'

def test_user_creation( fake_session, fake_user_service, test_client):
    signup_data = {
            "firstname": "string",
            "lastname": "string",
            "username": "string",
            "email": "shreya200199@gmail.com",
            "password": "123456"
        }
    response = test_client.post(
        url=f'{auth_prefix}/signup',
        json= signup_data
    )
    
    assert fake_user_service.user_exits_called_once()
    assert fake_user_service.user_exits_called_once_with(signup_data['email'])