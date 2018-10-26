from django_messages.models import Message
def get_messages(request):
    if request.user.is_authenticated():
        message_list = Message.objects.inbox_for(request.user)
    else:
        message_list = ''
    return {
        'message_list' : message_list,
    }