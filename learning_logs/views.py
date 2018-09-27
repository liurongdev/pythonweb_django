from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required


from .models import Topic ,Entry
from .forms import TopicForm,EntryForm
# Create your views here.


def index(request):
    """学习笔记的主页"""
    return render(request,'learning_logs/index.html')


@login_required
def topics(request):
    topics=Topic.objects.filter(owner=request.user).order_by('data_added')
    content={"topics":topics}

    return render(request,"learning_logs/topics.html",content)

@login_required
def topic(request,topic_id):
    topic=Topic.objects.get(id=topic_id)
    if topic.owner !=request.user:
        raise Http404
    entries=topic.entry_set.order_by('-date_added')
    content={"topic":topic,"entries":entries}

    return render(request,"learning_logs/topic.html",content)

@login_required
def new_topic(request):

    if request.method !="POST":
        form=TopicForm()
    else:
        form=TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse("learning_logs:topics"))
    content={"form":form}
    return render(request,"learning_logs/new_topic.html",content)

@login_required
def new_entry(request,topic_id):
    """在特定的主题中添加条目"""
    topic=Topic.objects.get(id=topic_id)

    if request.method !="POST":
        form=EntryForm()
    else:
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.save()


            return HttpResponseRedirect(reverse("learning_logs:topic",args=[topic_id]))
    content={"topic":topic,"form":form}
    return render(request,"learning_logs/new_entry.html",content)


@login_required
def edit_entry(request,entry_id):
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method !="POST":
        form=EntryForm(instance=entry)
    else:
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("learning_logs:topic", args=[topic.id]))


    content={"entry":entry,"topic":topic,"form":form}

    return render(request,"learning_logs/edit_entry.html",content)


