from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView

from .models import Notes
from .forms import NotesForm
class NotesListView(ListView):
  model = Notes
  context_object_name = 'notes'
  template_name = 'notes/notes_list.html'

class NotesDetailView(DetailView):
  model = Notes
  context_object_name = 'note'

class NotesCreateView(CreateView):
  model = Notes
  # fields = ['title', 'text']
  form_class = NotesForm
  success_url = '/smart/notes'

class NotesUpdateView(UpdateView):
  model = Notes
  form_class = NotesForm
  success_url = '/smart/notes'

class NotesDeleteView(DeleteView):
  model = Notes
  success_url = '/smart/notes'
  template_name: str = 'notes/notes_delete.html'

# def list(request):
#   all_notes = Notes.objects.all()
#   return render(request, 'notes/notes_list.html', {'notes': all_notes})

# def detail(request, pk):
#   try:
#     note = Notes.objects.get(pk=pk)
#   except Notes.DoesNotExist:
#     raise Http404('Note does not exist')
#   return render(request, 'notes/notes_detail.html', {'note': note})
