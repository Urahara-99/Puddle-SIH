from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from item.models import Class
from .forms import ConversationMessageForm
from .models import Conversation

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Class, pk=item_pk)

    # Prevent the item creator from starting a conversation with themselves
    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    # Check if a conversation already exists between the user and the item creator
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations.exists():
        # If a conversation exists, redirect to the conversation detail
        return redirect('conversation:detail', pk=conversations.first().id)

    # Handle form submission
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            # Create the conversation
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            # Save the conversation message
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            # Redirect to the item detail page after creating the conversation
            return redirect('item:detail', pk=item_pk)
    
    else:
        # Display an empty form if it's a GET request
        form = ConversationMessageForm()
    
    # Render the new conversation form
    return render(request, 'conversation/new.html', {
        'form': form
    })


@login_required
def inbox(request):
    # Fetch all conversations the user is a part of
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })


@login_required
def detail(request, pk):
    # Ensure the user is a member of the conversation they are trying to access
    conversation = get_object_or_404(Conversation.objects.filter(members__in=[request.user.id]), pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            # Save the new message to the conversation
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            conversation.save()

            return redirect('conversation:detail', pk=pk)
    
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })
