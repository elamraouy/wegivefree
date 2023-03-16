from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from .models import *
from .forms import AddGift
from django.contrib.auth.models import User
import markdown


def save_profile(request,):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_id = int(request.user.id)
            myuser = User.objects.get(pk=user_id)
            first_name = myuser.first_name
            avatar = request.POST.get('avatar')
            if len(Profile.objects.filter(user=myuser)) == 0:
                new_profile = Profile.objects.create(user_id=user_id, first_name=first_name, user_image=avatar)
                new_profile.save()
            data = {"picture_url": avatar, "name": first_name}
            return JsonResponse(data)
    else:
        return HttpResponse("not connected")


def send_message(sender, receiver, conversation, message):
    new_message = Messages.objects.create(sender=sender, receiver=receiver, conversation=conversation, message=message)
    new_message.save()


def send_response_to(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user1 = User.objects.get(id=request.user.id)
            response = request.POST.get('response')
            conversation = Conversation.objects.get(pk=int(request.POST.get('conversation')))
            user2 = conversation.c_guest
            if user1 == user2:
                receiver = conversation.c_host
            else:
                receiver = conversation.c_guest
            new_message = Messages.objects.create(sender=user1, receiver=receiver, conversation=conversation,
                                                  message=response)
            new_message.save()
            verb = user1.first_name + ' ' + user1.last_name + ' vous a envoyé un message'
            notify = Notifictaion.objects.create(sender=user1,
                                                 receiver=receiver,
                                                 target=conversation.id,
                                                 type='message',
                                                 level='warning',
                                                 verb=verb)
            notify.save()
            last_message = Messages.objects.filter(pk=new_message.id).values(
                "id", "conversation", "sender", "sender__id", "message", "date_send", "date_read",
                "sender__last_name", "sender__profile__user_image", "sender__first_name",
                "conversation__gift__gived_by"
            )
            data = list(last_message)
            return JsonResponse({"success": True, "message": data})


# manage notifications
def manage_notifications(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            noty_id = request.POST.get('id')
            notification = Notifictaion.objects.get(id=noty_id)
            notification.unread = False
            notification.save(update_fields=['unread'])
            return JsonResponse({"success": True, "message": "successfly updated"})


def show_all_notifications(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        notifications = Notifictaion.objects.filter(receiver=user) \
            .values("id",
                    "type",
                    "sender__profile__user_image",
                    "verb", "unread", "target",
                    "level", "date_send", "absolute_url")
        if request.method == "GET":
            return render(request, 'notifications.html', context=dict(notifications=notifications))
        else:
            task = request.POST.get('task')
            unread = notifications.filter(unread=True)
            notifications_count = len(unread)
            if task == 'get_count':
                return JsonResponse({"success": True, "count": notifications_count})
            elif task == 'get_unread':
                return JsonResponse({"success": True, "count": notifications_count, "unread": list(unread)})
            else:
                pass
    else:
        pass


# manage requests / accept / reject / send auto message
def manage_requests(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = {}
            request_id = request.POST.get('request_id')
            request_user = int(request.POST.get('request_user'))
            gift_id = request.POST.get('gift_id')
            sender = User.objects.get(id=request.user.id)
            receiver = User.objects.get(id=request_user)
            gift = Mygifts.objects.get(id=gift_id)
            my_request = GiftRequest.objects.get(id=request_id)
            my_request.stats = "accepted"
            my_request.save(update_fields=['stats'])
            data.update(result="Demande bien accéptée <br>"
                               " un message a été envoyé a " + receiver.first_name + receiver.last_name)
            conversation = Conversation.objects.create(c_host=sender, request=my_request, c_guest=receiver, gift=gift)
            conversation.save()
            absolute_url = request.build_absolute_uri(reverse('users'))
            verb = ' Votre demande a propos de : "'+gift.title+'" est accpetée'
            notify = Notifictaion.objects.create(sender=sender,
                                                 receiver=receiver,
                                                 target=request_id,
                                                 type='demande',
                                                 level='success',
                                                 absolute_url=absolute_url+'?sec=request#req'+str(request_id),
                                                 verb=verb)
            notify.save()
            gift_conversations = list(Conversation.objects.filter(id=conversation.id).values(
                "c_guest__last_name", "id", "c_guest__profile__user_image", "date_start",
                "c_guest__first_name", "c_host__profile__user_image", "gift__title", "gift__image",
                "c_host__last_name", "c_host__first_name"
            ))
            data.update(conversation=gift_conversations)
            send_message(sender, receiver, conversation, "Mabrook .. Votre demande est acceptée")
            return JsonResponse({"success": True, "message": data})


# get user messages related to a specific gift
def get_all_conversation(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = User.objects.get(pk=request.user.id)
            gift = Mygifts.objects.get(pk=request.POST.get('gift_id'))
            gift_conversations = list(Conversation.objects.filter(Q(gift=gift) &
                                                                  (Q(c_host=user) | Q(c_guest=user))).values(
                    "c_guest__last_name", "id", "c_guest__profile__user_image", "date_start",
                    "c_guest__first_name", "c_host__profile__user_image", "gift__title", "gift__image",
                    "c_host__last_name", "c_host__first_name"
                    ))
            return JsonResponse(gift_conversations, safe=False)


# get user messages related to a specific gift
def get_gift_messages(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user.id
            conversation = get_object_or_404(Conversation, pk=request.POST.get('conversation'))
            if conversation:
                if user == conversation.c_host_id or user == conversation.c_guest_id:
                    guest = conversation.c_guest_id
                    if user == guest:
                        user_guest = Profile.objects.filter(id=conversation.c_host_id)\
                            .values("first_name", "user_image")
                    else:
                        user_guest = Profile.objects.filter(id=conversation.c_guest_id)\
                            .values("first_name", "user_image")
                    all_messages = Messages.objects.filter(conversation=conversation)
                    for message in all_messages:
                        if not user == message.sender:
                            message.is_seen = 1
                            message.save(update_fields=['is_seen'])
                    all_messages = all_messages.values(
                        "id", "sender", "sender__id", "message", "date_send", "date_read",
                        "sender__last_name", "sender__profile__user_image", "sender__first_name",
                        "conversation__gift__gived_by"
                    )
                    received_messages = list(all_messages)
                    return JsonResponse({'received_messages': received_messages, 'guest': list(user_guest)}, safe=False)
                else:
                    return JsonResponse({})
            else:
                return JsonResponse({})


# upfate message view
def update_messages(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user.id
            conversation = Conversation.objects.filter(pk=request.POST.get('conversation')).first()
            if conversation:
                all_messages = Messages.objects.filter(Q(conversation=conversation) & Q(is_seen=0))
                messages_values = all_messages.values(
                    "id", "sender", "is_seen", "sender__id", "message", "date_send", "date_read",
                    "sender__last_name", "sender__profile__user_image", "sender__first_name",
                    "conversation__gift__gived_by"
                )
                received_messages = list(messages_values)
                owner = False
                for message in all_messages:
                    if not message.sender_id == user:
                        message.is_seen = 1
                        message.save(update_fields=['is_seen'])
                        owner = True
                if owner:
                    return JsonResponse(received_messages, safe=False)
                else:
                    received_messages = {}
                    return JsonResponse(received_messages, safe=False)
            else:
                return JsonResponse({})


# return requests of a gift json format
def display_requests(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            gift_id = request.POST.get('gift_id')
            all_requests = list(GiftRequest.objects.filter(gift__id=gift_id)
                                .values("id", "user_name", "gift__id", "conversation", "user__profile__user_image",
                                        "gift__user_name", "gift__user_image", "user", "user_message",
                                        "user_city", "user_phone", "user_email", "stats", "date_add"))
            if len(all_requests) > 0:
                data = {'success': True, 'req': all_requests}
                return JsonResponse(data, safe=False)
            else:
                data = {'success': False, 'req': 'no requests'}
                return JsonResponse(data, safe=False)
        else:
            data = {'success': False, 'req': 'no requests'}
            return JsonResponse(data, safe=False)


def email_validator(email):
    from django.core.exceptions import ValidationError
    from django.core.validators import validate_email
    try:
        validate_email(email)
    except ValidationError:
        return False
    else:
        return True


# ajouter une demande
def new_gift_request(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = {}
            errors = {}
            save = True
            user = User.objects.get(pk=request.user.id)
            gift = Mygifts.objects.get(pk=request.POST.get('gift'))
            gift_owner = request.POST.get('owner')
            receiver = User.objects.get(pk=gift.gived_by_id)
            user_name = request.POST.get('user_name')
            user_message = request.POST.get('user_message')
            user_email = request.POST.get('user_email')
            user_city = request.POST.get('user_city')
            user_phone = request.POST.get('user_phone')
            # test if already requested
            test2 = GiftRequest.objects.filter(Q(gift=gift) & Q(user=user))
            if len(test2) > 0:
                errors.update({'gift': 'vous avez déja demandé cet offre'})
                save = False
            if not email_validator(user_email):
                errors.update({'gift': 'Email non valide'})
                save = False
            if save:
                post = GiftRequest(
                    user=user, gift=gift, owner=gift_owner, user_name=user_name, user_city=user_city,
                    user_email=user_email, user_message=user_message, user_phone=user_phone)
                post.save()
                data.update({'success': True})
                absolute_url = request.build_absolute_uri(reverse('users'))
                verb = user.first_name+' a envoyé une demande sur votre offre'
                notify = Notifictaion.objects.create(sender=user,
                                                     receiver=receiver,
                                                     target=post.id,
                                                     type='demande',
                                                     level='info',
                                                     absolute_url=absolute_url + '?sec=gifts',
                                                     verb=verb)
                notify.save()
                return JsonResponse(data)
            else:
                data.update({'success': False, 'errors': errors})
                return JsonResponse(data)
    else:
        return HttpResponseRedirect('/')


# ajouter un offre
def new_gift(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            gift_form = AddGift(request.POST, request.FILES)
            gift_form = gift_form.save(commit=False)
            gift_form.user_name = request.user.first_name + ' ' + request.user.last_name
            gift_form.gived_by = User.objects.get(id=request.user.id)
            gift_form.user_image = request.POST.get('user_image', None)
            data = {}
            errors = {}
            save = True
            if len(gift_form.title) < 12:
                errors.update({'title': 'title trop court: Minimum 12 lettres'})
                save = False
            if len(gift_form.body) < 40:
                errors.update({'body': 'Description trop courte: Minimum 40 lettres'})
                save = False
            if save:
                gift_form.body = markdown.markdown(gift_form.body, extensions=['nl2br'])
                gift_form.save()
                data.update({'success': True, 'id': gift_form.id})
                return JsonResponse(data)
            else:
                data.update({'success': False, 'errors': errors})
                return JsonResponse(data)
        else:
            gift_form = AddGift()
            return render(request, 'add.html', {'newGiftForm': gift_form})
    else:
        return HttpResponseRedirect('/gifts')


# list all gits
def index(request):
    search_query = request.GET.get('search', '')
    userfilter = request.GET.get('domaine', '')
    if search_query:
        gifts = Mygifts.objects.filter(Q(title__contains=search_query) | Q(body__contains=search_query))
        last_gifts = Mygifts.objects.all().order_by('-date_add')[:4]
        extra = f'&search={search_query}'
        words = search_query
    elif userfilter:
        gifts = Mygifts.objects.filter(domaine=userfilter)
        extra = f'&domaine={userfilter}'
        words = ''
        last_gifts = Mygifts.objects.all().order_by('-date_add')[:4]
    else:
        gifts = Mygifts.objects.all()
        last_gifts = Mygifts.objects.all().order_by('-date_add')[:4]
        userfilter = ''
        extra = ''
        words = ''
    paginator = Paginator(gifts, 12)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    if page.has_next():
        next_url = f'?page={page.next_page_number()}{extra}'
    else:
        next_url = ''
    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}{extra}'
    else:
        prev_url = ''
    return render(request, 'index.html',
                  context=dict(page=page, last=last_gifts, domaine=userfilter, words=words, next_page_url=next_url,
                               prev_page_url=prev_url))


# render 3 last gifts
def home(request):
    last_gifts = Mygifts.objects.all().order_by('-date_add')[:3]
    return render(request, 'home.html', context={'last': last_gifts})


# Afficher offre by id
def show_gift(request):
    gift_id = request.GET.get('id')
    gift = Mygifts.objects.filter(id=gift_id).first()
    if gift:
        same_domaine = Mygifts.objects.filter(domaine=gift.domaine).exclude(pk=gift_id)
        same_city = Mygifts.objects.filter(city=gift.city).exclude(pk=gift_id)
        related = Mygifts.objects\
            .filter(Q(title__icontains=gift.title) | Q(body__icontains=gift.title)).exclude(pk=gift_id)
        # test if already requested
        extra = {'requested': False}
        if request.user.is_authenticated:
            test1 = GiftRequest.objects.filter(Q(gift=gift_id) & Q(user=request.user.id))
            if len(test1) > 0:
                extra.update({'requested': True})
            elif int(request.user.id) == int(gift.gived_by_id):
                extra.update({'owner': True})
            else:
                extra.update({'owner': False})
        return render(request, 'show_gift.html', {'gift': gift,
                                                  'extra': extra,
                                                  'related': related,
                                                  'same_city': same_city,
                                                  'same_domaine': same_domaine
                                                  })

    else:
        return HttpResponseRedirect('/')


# user gifts
def user_gifts(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_gift = Mygifts.objects.filter(gived_by=user.id)
        my_requests = GiftRequest.objects.filter(user=user.id)
        sdict = {"w": 0, "a": 0}
        for req in my_requests:
            if req.stats == "waiting":
                sdict.update(w=sdict['w'] + 1)
            elif req.stats == "accepted":
                sdict.update(a=sdict['a'] + 1)
            else:
                pass
        my_requests = list(my_requests
                           .values("id", "gift__id", "gift__user_name",
                                   "gift__user_image",
                                   "gift__title",
                                   "gift__image",
                                   "conversation",
                                   "user_message",
                                   "user__first_name",
                                   "user__last_name",
                                   "user__profile__user_image",
                                   "stats",
                                   "date_add"))
        return render(request, 'users_gifts.html',
                      context={"user_gifts": user_gift,
                               "stats": sdict,
                               "goto": request.GET.get('sec'),
                               "user_requests": my_requests})
    else:
        return HttpResponseRedirect('/')


def check_auth(request):
    if request.user.is_authenticated:
        return HttpResponse('success')
    else:
        return HttpResponse('failure')


def delete_gift(request):
    gift_id = request.POST.get('gift_id')
    Mygifts.objects.get(pk=gift_id).delete()
    return HttpResponse('success')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
