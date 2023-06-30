from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import *


# Create your views here.

@login_required
def section_list(request, section_id=None):
    # print('elo')
    # Note.objects.create(title='straczki', content='xd', parent_id=11)
    # Note.objects.create(title='czerwone', content='xd', parent_id=12)
    # Note.objects.create(title='z witamina C', content='xd', parent_id=12)
    # Note.objects.create(title='slodkie', content='xd', parent_id=12)
    # Note.objects.create(title='kwasne', content='xd', parent_id=12)
    # Note.objects.create(title='o X', content='xd', parent_id=4)
    #Section.objects.create(name='matematyka')
    sections = Section.objects.all().prefetch_related('notes')

    # print(sections)
    # sections.notes.all()
    # s = Section.notes
    # print(s)
    # print(sections)
    # print(s.get_family())
    # print(s.notes.get_children())
    # print(s.get_descendants())
    # print(s.get_root())
    # a = Section.objects.get(name='angielski')
    # print(a.get_children())
    # print(a.get_descendants())
    # print(a.get_family())
    # a.delete()
    # jo = Section.objects.create(name='jezyki obce')
    # mat = Section.objects.create(name='matematyka')
    # ang = Section.objects.create(name='angielski', parent=jo)
    # alg = Section.objects.create(name='algebra', parent=mat)
    # Section.objects.create(name='geometria', parent=mat)
    # slowa = Section.objects.create(name='slowa', parent=ang)
    # Section.objects.create(name='czasy', parent=ang)
    # x = Section.objects.create(name='X', parent=alg)
    # y = Section.objects.create(name='Y', parent=alg)
    # rosliny = Section.objects.create(name='rosliny', parent=slowa)
    # warz = Section.objects.create(name='warzywa', parent=rosliny)
    # owoc = Section.objects.create(name='owoce', parent=rosliny)
    # jo = Section.objects.create(name='jezyki obce', parent=x)
    # mat = Section.objects.create(name='matematyka', parent=x)
    # ang = Section.objects.create(name='angielski', parent=jo)
    # alg = Section.objects.create(name='algebra', parent=mat)
    # Section.objects.create(name='geometria', parent=mat)
    # slowa = Section.objects.create(name='slowa', parent=ang)
    # Section.objects.create(name='czasy', parent=ang)
    # Section.objects.create(name='X', parent=alg)
    # Section.objects.create(name='Y', parent=alg)
    # rosliny = Section.objects.create(name='rosliny', parent=slowa)
    # warz = Section.objects.create(name='warzywa', parent=rosliny)
    # owoc = Section.objects.create(name='owoce', parent=rosliny)
    # def get_all_parents(node):
    #     parents = []
    #     while node.parentsection is not None:
    #         node = node.parentsection
    #         parents.append(node)
    #     return parents
    # s = Section.objects.get(id=7)
    # s.get_ancestors()
    # parents = get_all_parents(s)
    # print(parents)
    # print(s.stara.all())
    # for x in s.parentsection:
    #     print(x)
    # #print(s.parentsection)
    # sections = Section.objects.filter(parent_section=section_id)
    # notes = None
    # if not sections:
    #     notes = Note.objects.filter(section=section_id)
    return render(request, 'base_my_notes.html', {'sections': sections})
