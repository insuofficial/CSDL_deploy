from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.db.models import Count, Q
from django.views.generic import ListView
from datetime import date

from django.contrib.auth.models import User
from .models import *
from .forms import *

########################################
#           template functions         #
########################################

# For new post
def posting(request, form, repage, template):
    if request.method == "POST":
        postform = form(request.POST, request.FILES)
        if postform.is_valid():
            postform.save()
            return redirect(repage)

    else:
        postform = form()

    return render(request, template, {
        'form': postform,
    })



# For edit post
def editing(request, pk, model, form, repage, with_pk, template):
    postmodel = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        postform = form(request.POST, request.FILES, instance=postmodel)
        if postform.is_valid():
            pk_update = dict() #for update pk
            fields = list(postform.fields.keys())
            for field in fields:
                if field != "_state":
                    if postmodel.__dict__[field] == postmodel.pk:
                        pk_update[str(field)] = postform.cleaned_data[str(field)]
                    else:
                        postmodel.__dict__[field] = postform.cleaned_data[str(field)]
            model.objects.filter(pk=pk).update(**pk_update)
            postmodel.save()

            if with_pk:
                return redirect(repage, postmodel.pk)
            else:
                return redirect(repage)

    else:
        postform = form(instance=postmodel)

    return render(request, template, {
        'form': postform,
    })


# For paginator
def paging(request, queryset, page_num, template):

    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, page_num)

    try:
        components = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        components = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        components = paginator.page(paginator.num_pages)
    return render(request, template, {
        'components': components,
    })


# Create your views here.
def test_page(request):
    return render(request, 'homepage/test.html')

def main_page(request):
    main = Main.objects.first()
    images = Main_image.objects.all()
    project = Project.objects.order_by('-term_start').first()
    journals = Journal.objects.order_by('-year').filter(submitted=False).all()
    return render(request, 'homepage/main.html', {
        'main': main,
        'images': images,
        'project': project,
        'journals': journals,
    })

def signup_page(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_page')
    else:
        form = SignUpForm()
    return render(request, 'homepage/account/signup.html', {
        'form': form,
    })

@login_required
def profile_page(request):
    profile = User.objects.get(username__exact=request.user)
    return render(request, 'homepage/account/profile.html', {
        'profile': profile,
    })

#date_joined, email, first_name, groups, id, is_active, is_staff, is_superuser, last_login,
# last_name, logentry, password, post, user_permissions, username
@login_required
def profile_update(request):
    profilemodel = User.objects.get(username__exact=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profilemodel)
        if form.is_valid():
            username = request.user
            password = request.POST['password2']
            User.objects.filter(username__exact=request.user).update(email=request.POST["email"])
            profilemodel.set_password(password)
            profilemodel.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('main_page')
    else:
        form = ProfileForm(instance=profilemodel)
    return render(request, 'homepage/account/profile_update.html', {
        'form': form,
    })


######################################
#             People part            #
######################################
def professor_page(request):
    profile = Member.objects.filter(position='professor').first()
    return render(request, 'homepage/people/professor.html', {
        'profile': profile,
    })

def member_page(request):
    members_phd = Member.objects.filter(position='member-PHD').order_by('position_num').all()
    members_ms = Member.objects.filter(position='member-MS').order_by('position_num').all()
    members_intern = Member.objects.filter(position='member-INTERN').order_by('position_num').all()
    return render(request, 'homepage/people/member.html', {
        'members_phd': members_phd,
        'members_ms': members_ms,
        'members_intern': members_intern,
    })

def alumni_page(request):
    alumni_phd = Member.objects.filter(position='alumni-PHD').order_by('position_num').all()
    alumni_ms = Member.objects.filter(position='alumni-MS').order_by('position_num').all()
    return render(request, 'homepage/people/alumni.html', {
        'alumni_phd': alumni_phd,
        'alumni_ms': alumni_ms,
    })


######################################
#            Research part           #
######################################
def overview_list(request):
    research_areas = ResearchArea.objects.all()
    researches = Research.objects.order_by('research_area').all()
    return render(request, 'homepage/research/overview_list.html', {
        'research_areas': research_areas,
        'researches': researches,
    })

def overview_detail(request, pk):
    research_area = ResearchArea.objects.get(research_area=pk)
    researches = Research.objects.filter(research_area=pk).all()
    return render(request, 'homepage/research/overview_detail.html', {
        'research_area': research_area,
        'researches': researches,
    })

def project_list(request):
    now = date.today()
    projects_going = Project.objects.filter(Q(term_end__gte=now) | Q(term_end__isnull=True)).order_by('-term_start').all()
    projects_complete = Project.objects.filter(term_end__lt=now).order_by('-term_start').all()
    return render(request, 'homepage/research/project_list.html', {
        'projects_going': projects_going,
        'projects_complete': projects_complete,
    })

@staff_member_required
def project_post(request):
    return posting(request, Projectform, 'project_list', 'homepage/research/project_post.html')

@staff_member_required
def project_edit(request, pk):
    return editing(request, pk, Project, Projectform, 'project_list', False, 'homepage/research/project_post.html')


####################################
#           Publication            #
####################################
def journal_list(request):
    years = [i for (i,j) in Journal.year_choices]
    years.reverse()
    journals_submitted = Journal.objects.filter(submitted=True).order_by('-year').all()
    journals = Journal.objects.filter(submitted=False).order_by('-year').all()
    return render(request, 'homepage/publication/journal_list.html', {
        'journals_submitted': journals_submitted,
        'journals': journals,
        'years': years,
    })

@staff_member_required
def journal_post(request):
    return posting(request, Journalform, 'journal_list', 'homepage/publication/journal_post.html')

@staff_member_required
def journal_edit(request, pk):
    return editing(request, pk, Journal, Journalform, 'journal_list', False, 'homepage/publication/journal_post.html')


def conference_list(request):
    conference = Conference.objects.first()
    return render(request, 'homepage/publication/conference_list.html', {
        'conference': conference,
    })


@staff_member_required
def conference_edit(request, pk):
    return editing(request, pk, Conference, Conferenceform, 'conference_list', False, 'homepage/publication/conference_post.html')


def patent_list(request):
    patents_international = Patent.objects.filter(location='International Patent').order_by('-year').all()
    patents_korean = Patent.objects.filter(location='Korean Patent').order_by('-year').all()
    return render(request, 'homepage/publication/patent_list.html', {
        'patents_korean': patents_korean,
        'patents_international': patents_international,
    })

@staff_member_required
def patent_post(request):
    return posting(request, Patentform, 'patent_list', 'homepage/publication/patent_post.html')

@staff_member_required
def patent_edit(request, pk):
    return editing(request, pk, Patent, Patentform, 'patent_list', False, 'homepage/publication/patent_post.html')

######################################
#             Board part             #
######################################
def notice_list(request):
    queryset = Notice.objects.order_by('-published_date')
    return paging(request, queryset, 10, 'homepage/board/notice_list.html')

def notice_detail(request, pk):
    notice_detail = Notice.objects.get(pk=pk)
    notice_detail.views += 1
    notice_detail.save()
    return render(request, 'homepage/board/notice_detail.html', {
        'notice_detail': notice_detail
    })

@staff_member_required
def notice_post(request):
    if request.method == "POST":
        postform = Noticeform(request.POST)
        if postform.is_valid():
            post = postform.save(commit=False)
            post.user = request.user
            post.title = request.POST["title"]
            post.content = request.POST["content"]
            post.publish()
            return redirect('notice_list')

    else:
        postform = Noticeform()

    return render(request, 'homepage/board/notice_post.html', {
        'postform': postform,
    })


def notice_edit(request, pk):
    return editing(request, pk, Notice, Noticeform, 'notice_detail', True, 'homepage/board/notice_post.html')

def seminar_list(request):
    queryset = Seminar.objects.order_by('-date')
    return paging(request, queryset, 10, 'homepage/board/seminar_list.html')


@staff_member_required
def seminar_post(request):
    return posting(request, Seminarform, 'seminar_list', 'homepage/board/seminar_post.html')

@staff_member_required
def seminar_edit(request, pk):
    return editing(request, pk, Seminar, Seminarform, 'seminar_list', False, 'homepage/board/seminar_post.html')

def album_list(request):
    albums = Album.objects.order_by('-date').all()
    return render(request, 'homepage/board/album_list.html', {
        'albums': albums,
    })

def album_detail(request, pk):
    album_detail = Album.objects.get(pk=pk)
    return render(request, 'homepage/board/album_detail.html', {
        'album_detail': album_detail,
    })

@staff_member_required
def album_post(request):
    return posting(request, Albumform, 'album_list', 'homepage/board/album_post.html')

@staff_member_required
def album_edit(request, pk):
    return editing(request, pk, Album, Albumform, 'album_detail', True, 'homepage/board/album_post.html')


######################################
#             contact part           #
######################################
def contact_page(request):
    contact = Contact.objects.first()
    return render(request, 'homepage/contact/contact.html', {
        'contact': contact,
    })

