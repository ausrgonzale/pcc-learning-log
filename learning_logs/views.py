from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    print("INDEX VIEW HIT")
    print("User authenticated:", request.user.is_authenticated)
    """ The home page for Learning Log """
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """ Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """ Show a single topic and all its entries. """
    topic = get_object_or_404(Topic, id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entries.order_by('-date_added') # type: ignore

    paginator = Paginator(entries, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {'topic': topic, "entries": page_obj}

    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """ Add a new topic. """
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
        
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """ Add a new entry for a particular topic. """
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
        
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """ Edit an existing entry. """
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted, process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic' : topic, 'form' : form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def confirm_delete_entry(request, entry_id):
    """Display confirmation page before deleting an entry."""

    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    # Security check
    if topic.owner != request.user:
        raise Http404

    context = {
        'entry': entry,
        'topic': topic,
    }

    return render(
        request,
        'learning_logs/delete_entry.html',
        context
    )


@login_required
def delete_entry(request, entry_id):
    """Delete an entry (used for automation cleanup or future UI)."""

    entry = get_object_or_404(Entry, id=entry_id)

    # Security check
    if entry.topic.owner != request.user:
        raise Http404

    if request.method == "POST":
        topic_id = entry.topic.pk
        entry.delete()

        return HttpResponseRedirect(
            reverse(
                'learning_logs:topic',
                args=[topic_id]
            )
        )

    # Only allow POST
    raise Http404


