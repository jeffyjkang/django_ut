from django.contrib.auth.models import User
import pytest

def test_home_endpoint_returns_welcome_page(client):
  res = client.get(path='/')
  assert res.status_code == 200
  assert 'Welcome to SmartNotes!' in str(res.content)

def test_signup_endpoint_returns_form_for_unauthenticated_user(client):
  res = client.get(path='/signup')
  assert res.status_code == 200
  assert 'home/register.html' in res.template_name

@pytest.mark.django_db
def test_signup_endpoint_redirects_authenticated_user(client):
  '''
    When a user is authenticated and tries to access the
    signup page they are redirected to the list of their notes.
  '''
  user = User.objects.create_user('Clara', 'clara@example.com', 'password')
  client.login(username=user.username, password='password')
  res = client.get(path='/signup', follow=True)
  assert res.status_code == 200
  assert 'notes/notes_list.html' in res.template_name
