from __future__ import unicode_literals
from tests.app.models import Office, Issue
from tests.app.factories import UserFactory, OfficeFactory, IssueFactory, \
    default_password
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
import pytest
import json

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


def test_manager_user_list_office(client, user):
    OfficeFactory.create(manager=user)
    assert client.login(username=user.username, password=default_password) == True
    response = client.get('/offices/')
    assert response.status_code == 200
    assert len(response.data) == 1


def test_admin_user_list_office(client, office, user):
    user.is_staff = True
    user.save()
    assert client.login(username=user.username, password=default_password) == True
    response = client.get('/offices/')
    assert response.status_code == 200
    assert len(response.data) == 1


def test_superuser_list_office(client, office, user):
    user.is_superuser = True
    user.save()
    assert client.login(username=user.username, password=default_password) == True
    response = client.get('/offices/')
    assert response.status_code == 200
    assert len(response.data) == 1


def test_unauthenticated_retrieve_office(client, office):
    response = client.get(f'/offices/{office.id}/')
    assert response.status_code == 403


def test_simple_user_retrieve_office(client, office, user):
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/offices/{office.id}/')
    assert response.status_code == 200


def test_manager_retrieve_office(client, user):
    office = OfficeFactory.create(manager=user)
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/offices/{office.id}/')
    assert response.status_code == 200


def test_admin_retrieve_office(client, office, user):
    user.is_staff = True
    user.save()
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/offices/{office.id}/')
    assert response.status_code == 200


def test_superuser_retrieve_office(client, office, user):
    user.is_superuser = True
    user.save()
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/offices/{office.id}/')
    assert response.status_code == 200


def test_unauthenticated_create_office(client):
    payload = {'name': 'office 1'}
    response = client.post('/offices/', payload)
    assert response.status_code == 403


def test_simple_user_create_office(client, user):
    user_url = reverse('user-detail', args=[user.id])
    payload = {'name': 'office 1', 'manager': user_url}
    assert client.login(username=user.username, password=default_password) == True
    response = client.post('/offices/', payload)
    assert response.status_code == 403


def test_manager_create_office(client, user):
    OfficeFactory.create(manager=user)
    user_url = reverse('user-detail', args=[user.id])
    payload = {'name': 'office 1', 'manager': user_url}
    assert client.login(username=user.username, password=default_password) == True
    response = client.post('/offices/', payload)
    assert response.status_code == 201
    

def test_admin_create_office(client, user):
    user.is_staff = True
    user.save()
    user_url = reverse('user-detail', args=[user.id])
    payload = {'name': 'office 1', 'manager': user_url}
    assert client.login(username=user.username, password=default_password) == True
    response = client.post('/offices/', payload)
    assert response.status_code == 201


def test_superuser_create_office(client, user):
    user.is_superuser = True
    user.save()
    user_url = reverse('user-detail', args=[user.id])
    payload = {'name': 'office 1', 'manager': user_url}
    assert client.login(username=user.username, password=default_password) == True
    response = client.post('/offices/', payload)
    assert response.status_code == 201


def test_unauthenticated_update_office(client, office):
    payload = {'name': 'office 1'}
    response = client.put(f'/offices/{office.id}/', payload)
    assert response.status_code == 403

def test_simple_user_update_office(client, office):
    user = UserFactory.create()
    user_url = reverse('user-detail', args=[user.id])
    payload = json.dumps({'name': 'office 1', 'user': user_url})
    assert client.login(username=user.username, password=default_password) == True
    response = client.put(f'/offices/{office.id}/', payload, 'application/json')
    assert response.status_code == 403


def test_manager_update_office(client, office, user):
    user_url = reverse('user-detail', args=[user.id])
    payload = json.dumps({'name': 'office 1', 'manager': user_url})
    assert client.login(username=user.username, password=default_password) == True
    response = client.put(f'/offices/{office.id}/', payload, 'application/json')
    assert response.status_code == 200
    

def test_admin_update_office(client, office):
    user = UserFactory.create(is_staff=True)
    user_url = reverse('user-detail', args=[user.id])
    payload = json.dumps({'name': 'office 1', 'manager': user_url})
    assert client.login(username=user.username, password=default_password) == True
    response = client.put(f'/offices/{office.id}/', payload, 'application/json')
    assert response.status_code == 200


def test_superuser_update_office(client, office):
    user = UserFactory.create(is_superuser=True)
    user_url = reverse('user-detail', args=[user.id])
    payload = json.dumps({'name': 'office 1', 'manager': user_url})
    assert client.login(username=user.username, password=default_password) == True
    response = client.put(f'/offices/{office.id}/', payload, 'application/json')
    assert response.status_code == 200


def test_unauthenticated_partial_update_office(client, office):
    payload = {'name': 'office 1'}
    response = client.patch(f'/offices/{office.id}/', payload)
    assert response.status_code == 403


def test_simple_user_partial_update_office(client, office):
    user = UserFactory.create()
    payload = json.dumps({'name': 'office 1'})
    assert client.login(username=user.username, password=default_password) == True
    response = client.patch(f'/offices/{office.id}/', payload)
    assert response.status_code == 403


def test_manager_partial_update_office(client, office, user):
    payload = json.dumps({'name': 'office 1'})
    assert client.login(username=user.username, password=default_password) == True
    response = client.patch(f'/offices/{office.id}/', payload, 'application/json')
    assert response.status_code == 200
    

def test_admin_partial_update_office(client, office):
    user = UserFactory.create(is_staff=True)
    payload = json.dumps({'name': 'office 1'})
    assert client.login(username=user.username, password=default_password) == True
    response = client.patch(f'/offices/{office.id}/', payload, 'application/json')
    assert response.status_code == 200


def test_superuser_partial_update_office(client, office):
    user = UserFactory.create(is_superuser=True)
    payload = json.dumps({'name': 'office 1'})
    assert client.login(username=user.username, password=default_password) == True
    response = client.patch(f'/offices/{office.id}/', payload, 'application/json')
    assert response.status_code == 200


def test_unauthenticated_destroy_office(client, office):
    response = client.delete(f'/offices/{office.id}/')
    assert response.status_code == 403


def test_simple_user_destroy_office(client, office):
    user = UserFactory.create()
    assert client.login(username=user.username, password=default_password) == True
    response = client.delete(f'/offices/{office.id}/')
    response.status_code == 403


def test_manager_destroy_office(client, office, user):
    assert client.login(username=user.username, password=default_password) == True
    response = client.delete(f'/offices/{office.id}/')
    assert response.status_code == 204
    

def test_admin_destroy_office(client, office):
    user = UserFactory.create(is_staff=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.delete(f'/offices/{office.id}/')
    assert response.status_code == 204


def test_superuser_destroy_office(client, office):
    user = UserFactory.create(is_superuser=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.delete(f'/offices/{office.id}/')
    assert response.status_code == 204


def test_unauthenticated_list_issue(client, issue):
    response = client.get('/issues/')
    assert response.status_code == 403


def test_simple_user_list_issue(client, issue):
    user = UserFactory.create()
    assert client.login(username=user.username, password=default_password) == True
    response = client.get('/issues/')
    assert response.status_code == 200


def test_manager_user_list_issue(client, office, user, issue):
    assert client.login(username=user.username, password=default_password) == True
    response = client.get('/issues/')
    assert response.status_code == 200


def test_admin_user_list_issue(client, issue):
    user = UserFactory.create(is_staff=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.get('/issues/')
    assert response.status_code == 200


def test_superuser_list_issue(client, issue):
    user = UserFactory.create(is_superuser=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.get('/issues/')
    assert response.status_code == 200


def test_unauthenticated_retrieve_issue(client, issue):
    response = client.get(f'/issues/{issue.id}/')
    assert response.status_code == 403


def test_simple_user_retrieve_issue(client, issue):
    user = UserFactory.create()
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/')
    assert response.status_code == 200


def test_manager_retrieve_issue(client, office, user, issue):
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/')
    assert response.status_code == 200


def test_admin_retrieve_issue(client, issue):
    user = UserFactory.create(is_staff=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/')
    assert response.status_code == 200


def test_superuser_retrieve_issue(client, issue):
    user = UserFactory.create(is_superuser=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/')
    assert response.status_code == 200


def test_unauthenticated_create_issue(client):
    payload = {'description': 'desc'}
    response = client.post('/issues/', payload, 'application/json')
    assert response.status_code == 403


def test_simple_user_create_issue(client, office):
    user = UserFactory.create()
    payload = json.dumps(get_issue_serialized(office, user))
    assert client.login(username=user.username, password=default_password) == True
    response = client.post('/issues/', payload, 'application/json')
    assert response.status_code == 201


def test_manager_create_issue(client, office, user):
    payload = json.dumps(get_issue_serialized(office, user))
    assert client.login(username=user.username, password=default_password) == True
    response = client.post('/issues/', payload, 'application/json')
    assert response.status_code == 201
    

def test_admin_create_issue(client, office):
    user = UserFactory.create(is_staff=True)
    payload = json.dumps(get_issue_serialized(office, user))
    assert client.login(username=user.username, password=default_password) == True
    response = client.post('/issues/', payload, 'application/json')
    assert response.status_code == 201


def test_superuser_create_issue(client, office):
    user = UserFactory.create(is_superuser=True)
    payload = json.dumps(get_issue_serialized(office, user))
    assert client.login(username=user.username, password=default_password) == True
    response = client.post('/issues/', payload, 'application/json')
    assert response.status_code == 201


def test_unauthenticated_update_issue(client, issue):
    payload = json.dumps({'description': ''})
    response = client.put(f'/issues/{issue.id}/', payload, 'application/json')
    assert response.status_code == 403


def test_simple_user_update_issue(client, issue):
    user = UserFactory.create()
    office = OfficeFactory.create()
    payload = json.dumps(get_issue_serialized(office, user))
    assert client.login(username=user.username, password=default_password) == True
    response = client.put(f'/issues/{issue.id}/', payload, 'application/json')
    assert response.status_code == 403


def test_manager_update_issue(client, office, user, issue):
    payload = json.dumps(get_issue_serialized(office, user))
    assert client.login(username=user.username, password=default_password) == True
    response = client.put(f'/issues/{issue.id}/', payload, 'application/json')
    assert response.status_code == 200
    

def test_admin_update_issue(client, office, issue):
    user = UserFactory.create(is_staff=True)
    payload = json.dumps(get_issue_serialized(office, user))
    assert client.login(username=user.username, password=default_password) == True
    response = client.put(f'/issues/{issue.id}/', payload, 'application/json')
    assert response.status_code == 200


def test_superuser_update_issue(client, office, issue):
    user = UserFactory.create(is_superuser=True)
    payload = json.dumps(get_issue_serialized(office, user))
    assert client.login(username=user.username, password=default_password) == True
    response = client.put(f'/issues/{issue.id}/', payload, 'application/json')
    assert response.status_code == 200


def test_unauthenticated_partial_update_issue(client, issue):
    payload = json.dumps({'description': 'update'})
    response = client.patch(f'/issues/{issue.id}/', payload, 'application/json')
    assert response.status_code == 403


def test_simple_user_partial_update_issue(client, issue):
    user = UserFactory()
    payload = json.dumps({'description': 'update'})
    assert client.login(username=user.username, password=default_password) == True
    response = client.patch(f'/issues/{issue.id}/', payload, 'application/json')
    assert response.status_code == 403


def test_manager_partial_update_issue(client, office, user, issue):
    payload = json.dumps({'description': 'update'})
    assert client.login(username=user.username, password=default_password) == True
    response = client.patch(f'/issues/{issue.id}/', payload, 'application/json')
    assert response.status_code == 200
    

def test_admin_partial_update_issue(client, issue):
    user = UserFactory(is_staff=True)
    payload = json.dumps({'description': 'update'})
    assert client.login(username=user.username, password=default_password) == True
    response = client.patch(f'/issues/{issue.id}/', payload, 'application/json')
    assert response.status_code == 200


def test_superuser_partial_update_issue(client, issue):
    user = UserFactory(is_superuser=True)
    payload = json.dumps({'description': 'update'})
    assert client.login(username=user.username, password=default_password) == True
    response = client.patch(f'/issues/{issue.id}/', payload, 'application/json')
    assert response.status_code == 200


def test_unauthenticated_destroy_issue(client, issue):
    response = client.delete(f'/issues/{issue.id}/')
    assert response.status_code == 403


def test_simple_user_destroy_issue(client, issue):
    user = UserFactory()
    assert client.login(username=user.username, password=default_password) == True
    response = client.delete(f'/issues/{issue.id}/')
    assert response.status_code == 403


def test_manager_destroy_issue(client, office, user, issue):
    assert client.login(username=user.username, password=default_password) == True
    response = client.delete(f'/issues/{issue.id}/')
    assert response.status_code == 403
    

def test_admin_destroy_issue(client, issue):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.delete(f'/issues/{issue.id}/')
    assert response.status_code == 403



def test_superuser_destroy_issue(client, issue):
    user = UserFactory(is_superuser=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.delete(f'/issues/{issue.id}/')
    assert response.status_code == 403


def test_unauthenticated_start_issue(client, issue):
    response = client.get(f'/issues/{issue.id}/start/')
    assert response.status_code == 403


def test_simple_user_start_issue(client, issue):
    user = UserFactory()
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/start/')
    assert response.status_code == 403


def test_manager_start_issue(client, office, user, issue):
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/start/')
    assert response.status_code == 200
    

def test_admin_start_issue(client, issue):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/start/')
    assert response.status_code == 200


def test_superuser_start_issue(client, issue):
    user = UserFactory(is_superuser=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/start/')
    assert response.status_code == 200

def test_owner_start_issue(client, issue):
    user = issue.owner
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/start/')
    assert response.status_code == 200


def test_unauthenticated_finish_issue(client, issue):
    response = client.get(f'/issues/{issue.id}/finish/')
    assert response.status_code == 403


def test_simple_user_finish_issue(client, issue):
    user = UserFactory()
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/finish/')
    assert response.status_code == 403


def test_manager_finish_issue(client, office, user, issue):
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/finish/')
    assert response.status_code == 200
    

def test_admin_finish_issue(client, issue):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/finish/')
    assert response.status_code == 200


def test_superuser_finish_issue(client, issue):
    user = UserFactory(is_superuser=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/finish/')
    assert response.status_code == 200


def test_owner_finish_issue(client, issue):
    user = issue.owner
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/finish/')
    assert response.status_code == 200


def test_unauthenticated_cancel_issue(client, issue):
    response = client.get(f'/issues/{issue.id}/cancel/')
    assert response.status_code == 403


def test_simple_user_cancel_issue(client, issue):
    user = UserFactory()
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/cancel/')
    assert response.status_code == 403


def test_manager_cancel_issue(client, office, user, issue):
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/cancel/')
    assert response.status_code == 200
    

def test_admin_cancel_issue(client, issue):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/cancel/')
    assert response.status_code == 200


def test_superuser_cancel_issue(client, issue):
    user = UserFactory(is_superuser=True)
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/cancel/')
    assert response.status_code == 200

def test_owner_cancel_issue(client, issue):
    user = issue.owner
    assert client.login(username=user.username, password=default_password) == True
    response = client.get(f'/issues/{issue.id}/cancel/')
    assert response.status_code == 200


def get_issue_serialized(office, user):
    return {
        'description': 'desc',
        'owner': reverse('user-detail', args=[user.id]),
        'office': reverse('office-detail', args=[office.id])
    }