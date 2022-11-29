import pytest
from django.contrib.auth.models import User
from notes.models import Notes
from .factories import UserFactory, NoteFactory

@pytest.fixture
def logged_user(client):
  user = UserFactory()
  client.login(username=user.username, password='password')
  return user

@pytest.mark.django_db
def test_list_endpoint_returns_user_notes(client, logged_user):
  note = NoteFactory(user=logged_user)
  note2 = NoteFactory(user=logged_user)
  res = client.get(path='/smart/notes')
  assert 200 == res.status_code
  content = str(res.content)
  assert note.title in content
  assert note2.title in content
  assert 2 == content.count('<h3>')

@pytest.mark.django_db
def test_list_endpoint_only_list_notes_from_authenticated_user(client, logged_user):

  jon = User.objects.create_user('Jon', 'jon@test.com', 'password')
  jons_note = NoteFactory(user=jon)

  note = NoteFactory(user=logged_user)
  note2 = NoteFactory(user=logged_user)
  res = client.get(path='/smart/notes')
  assert 200 == res.status_code
  content = str(res.content)
  assert note.title in content
  assert note2.title in content
  assert jons_note.title not in content
  assert 2 == content.count('<h3>')

@pytest.mark.django_db
def test_create_endpoint_receives_form_data(client, logged_user):
  form_data = {'title': 'Django', 'text': 'A text'}
  res = client.post(path='/smart/notes/new', data=form_data, follow=True)
  assert 200 == res.status_code
  print('****', res.template_name)
  assert 'notes/notes_list.html' in res.template_name
  assert 1 == logged_user.notes.count()
  assert 'Django' == logged_user.notes.first().title
