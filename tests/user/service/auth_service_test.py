import re
import pytest
from src.common.exception.BusinessException import BusinessException, BusinessExceptionEnum
from src.user.controller.request.signupRequest import SignupRequest

from src.user.controller.request.loginRequest import LoginRequest
from src.user.model.user import User
from src.user.repository.user_repository import UserRepository
from src.user.service.auth_service import AuthService
from src.user.utils.pcrypt import pcrypt


@pytest.fixture
def user():
    return User(
        id=1,
        name='Test User',
        email='test@example.com',
        password=pcrypt('password123', salt='somesalt'),
        salt='somesalt',
        active=True
    )


@pytest.fixture
def user_repository_mock(mocker, user):
    mock_repo = mocker.Mock(UserRepository)
    mock_repo.get_user_by_email.return_value = user
    mock_repo.query_user_by_email.return_value = None
    return mock_repo


@pytest.fixture
def invalid_singup_request():
    return SignupRequest("john@example.com", "simple password")


@pytest.fixture
def valid_singup_request():
    return SignupRequest("john@example.com", "9eNLBWpws6TCGk8_ibQn")


def test_login_success(user_repository_mock, app, user):
    with app.app_context():
        auth_service = AuthService(user_repository_mock)
        login_request = LoginRequest(email=user.email, password='password123')
        login_response = auth_service.login(login_request)
    assert login_response.access_token is not None


def test_login_failure_with_not_invited_email(user_repository_mock, app):
    with app.app_context():
        auth_service = AuthService(user_repository_mock)
        user_repository_mock.get_user_by_email.return_value = None
        wrong_email_login_request = LoginRequest(email='wrong@example.com', password='password123')
        with pytest.raises(BusinessException, match=re.compile(BusinessExceptionEnum.UserNotInPilot.name)):
            auth_service.login(wrong_email_login_request)


def test_login_failure_with_not_sign_up_email(user_repository_mock, app, user):
    with app.app_context():
        auth_service = AuthService(user_repository_mock)
        user_repository_mock.get_user_by_email.return_value = user.copy(active=False)
        email_not_sign_up_login_request = LoginRequest(email=user.email, password='password123')
        with pytest.raises(BusinessException, match=re.compile(BusinessExceptionEnum.UserEmailIsNotSignup.name)):
            auth_service.login(email_not_sign_up_login_request)


def test_login_failure_with_wrong_password(user_repository_mock, app, user):
    with app.app_context():
        auth_service = AuthService(user_repository_mock)
        login_request = LoginRequest(email=user.email, password='password1234')
        with pytest.raises(BusinessException, match=re.compile(BusinessExceptionEnum.UserPasswordIncorrect.name)):
            auth_service.login(login_request)


def test_signup_should_failed_when_user_password_is_invalid(user_repository_mock, invalid_singup_request):
    auth_service = AuthService(user_repository_mock)

    with pytest.raises(BusinessException, match=re.compile(BusinessExceptionEnum.UserPasswordInvalid.name)):
        auth_service.signup(invalid_singup_request)


def test_signup_should_failed_when_user_not_in_pilot(user_repository_mock, valid_singup_request):
    auth_service = AuthService(user_repository_mock)

    with pytest.raises(BusinessException, match=re.compile(BusinessExceptionEnum.UserNotInPilot.name)):
        auth_service.signup(valid_singup_request)


def test_signup_should_failed_when_user_already_signup(user, user_repository_mock, valid_singup_request):
    auth_service = AuthService(user_repository_mock)
    user_repository_mock.query_user_by_email.return_value = user.copy(active=True)

    with pytest.raises(BusinessException, match=re.compile(BusinessExceptionEnum.UserEmailIsAlreadySignup.name)):
        auth_service.signup(valid_singup_request)
