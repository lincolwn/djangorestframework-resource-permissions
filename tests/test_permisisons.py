from tests.app.models import Office, Issue
from tests.app.factories import UserFactory, OfficeFactory, IssueFactory, \
    default_password
from django.contrib.auth.models import User
import pytest

pytestmark = pytest.mark.django_db


def test_unauthenticated_list_office(client):
    OfficeFactory.create()
    response = client.get('/offices/')
    assert response.status_code == 403


def test_simple_user_list_office(client, office, user):
    assert client.login(username=user.username, password=default_password) == True
    response = client.get('/offices/')
    assert response.status_code == 200
    assert len(response.data) == 1


def test_manager_user_list_office(client):
    pass


def test_admin_user_list_office(client):
    pass


def test_superuser_list_office(client):
    pass


def test_unauthenticated_retrieve_office(client):
    pass


def test_simple_user_retrieve_office(client):
    pass


def test_manager_retrieve_office(client):
    pass


def test_admin_retrieve_office(client):
    pass


def test_superuser_retrieve_office(client):
    pass


def test_unauthenticated_create_office(client):
    pass


def test_simple_user_create_office(client):
    pass


def test_manager_create_office(client):
    pass
    

def test_admin_create_office(client):
    pass


def test_superuser_create_office(client):
    pass


def test_unauthenticated_update_office(client):
    pass


def test_simple_user_update_office(client):
    pass


def test_manager_update_office(client):
    pass
    

def test_admin_update_office(client):
    pass


def test_superuser_update_office(client):
    pass


def test_unauthenticated_partial_update_office(client):
    pass


def test_simple_user_partial_update_office(client):
    pass


def test_manager_partial_update_office(client):
    pass
    

def test_admin_partial_update_office(client):
    pass


def test_superuser_partial_update_office(client):
    pass


def test_unauthenticated_destroy_office(client):
    pass


def test_simple_user_destroy_office(client):
    pass


def test_manager_destroy_office(client):
    pass
    

def test_admin_destroy_office(client):
    pass


def test_superuser_destroy_office(client):
    pass


####
def test_unauthenticated_list_issue(client):
    pass


def test_simple_user_list_issue(client):
    pass


def test_manager_user_list_issue(client):
    pass


def test_admin_user_list_issue(client):
    pass


def test_superuser_list_issue(client):
    pass


def test_unauthenticated_retrieve_issue(client):
    pass


def test_simple_user_retrieve_issue(client):
    pass


def test_manager_retrieve_issue(client):
    pass


def test_admin_retrieve_issue(client):
    pass


def test_superuser_retrieve_issue(client):
    pass


def test_unauthenticated_create_issue(client):
    pass


def test_simple_user_create_issue(client):
    pass


def test_manager_create_issue(client):
    pass
    

def test_admin_create_issue(client):
    pass


def test_superuser_create_issue(client):
    pass


def test_unauthenticated_update_issue(client):
    pass


def test_simple_user_update_issue(client):
    pass


def test_manager_update_issue(client):
    pass
    

def test_admin_update_issue(client):
    pass


def test_superuser_update_issue(client):
    pass


def test_unauthenticated_partial_update_issue(client):
    pass


def test_simple_user_partial_update_issue(client):
    pass


def test_manager_partial_update_issue(client):
    pass
    

def test_admin_partial_update_issue(client):
    pass


def test_superuser_partial_update_issue(client):
    pass


def test_unauthenticated_destroy_issue(client):
    pass


def test_simple_user_destroy_issue(client):
    pass


def test_manager_destroy_issue(client):
    pass
    

def test_admin_destroy_issue(client):
    pass


def test_superuser_destroy_issue(client):
    pass


def test_unauthenticated_start_issue(client):
    pass


def test_simple_user_start_issue(client):
    pass


def test_manager_start_issue(client):
    pass
    

def test_admin_start_issue(client):
    pass


def test_superuser_start_issue(client):
    pass


def test_unauthenticated_finish_issue(client):
    pass


def test_simple_user_finish_issue(client):
    pass


def test_manager_finish_issue(client):
    pass
    

def test_admin_finish_issue(client):
    pass


def test_superuser_finish_issue(client):
    pass


def test_unauthenticated_cancel_issue(client):
    pass


def test_simple_user_cancel_issue(client):
    pass


def test_manager_cancel_issue(client):
    pass
    

def test_admin_cancel_issue(client):
    pass


def test_superuser_cancel_issue(client):
    pass