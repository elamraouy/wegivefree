import hashlib
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from api.gserializers import GiftSerializer
from gifts.models import Mygifts, Profile, GiftRequest, Notifictaion
from gifts.views import email_validator


# return all post to gserialiser -> android app
class SinguUp(APIView):
    @staticmethod
    def post(request):
        if request.method == 'POST':
            save = True
            errors = ""
            user_name = request.POST.get('username')
            user_lname = request.POST.get('last_name')
            user_fname = request.POST.get('first_name')
            user_email = request.POST.get('email')
            user_password = request.POST.get('password')
            if len(User.objects.filter(username=user_name)) > 0:
                save = False
                errors += user_name + " is already used choose an other and retry \n "
            if len(User.objects.filter(email=user_email)) > 0:
                save = False
                errors += "Email is already registred \n "
            if save:
                user = User.objects.create_user(username=user_name,
                                                email=user_email,
                                                first_name=user_fname,
                                                last_name=user_lname,
                                                password=user_password)
                user.save()
                token = Token.objects.create(user=user)
                token.save()
                preferred_avatar_size_pixels = 256
                picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
                    hashlib.md5(user.email.encode('UTF-8')).hexdigest(),
                    preferred_avatar_size_pixels
                )
                profile = Profile(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    user_image=picture_url)
                profile.save()
                data = {"success": True,
                        "username": user_fname + " " + user_lname,
                        "user_uid": user.id,
                        "user_name": user_name,
                        "user_image": profile.user_image,
                        "message": "welcome to give fro free " + user_fname + " " + user_lname
                        }
                return Response(data)
            else:
                data = {
                    "success": False,
                    "message": errors
                }
                return Response(data)
        else:
            data = {
                "success": False,
                "message": "No data received"
            }
            return Response(data)


class SocialAuth(APIView):
    @staticmethod
    def post(request):
        if request.method == 'POST':
            uid = request.POST.get('user_uid')
            user_name = request.POST.get('user_name')
            user_email = request.POST.get('user_email')
            user_first_name = request.POST.get('first_name')
            user_last_name = request.POST.get('last_name')
            pic_url = request.POST.get('pic_url')
            if not uid == "null":
                social_account = SocialAccount.objects.filter(uid=uid).first()
                if social_account is not None:
                    token = Token.objects.get(user_id=social_account.user_id)
                    user = User.objects.get(id=token.user_id)
                    user_name = user.first_name + " " + user.last_name
                    profile = Profile.objects.get(user=user)
                    data = {"success": True,
                            "token": token.key,
                            "user_uid": user.id,
                            "user_name": user_name,
                            "user_image": profile.user_image,
                            "message": "user authenticated"}
                    return Response(data)
                else:
                    user = User.objects.create_user(username=user_name,
                                                    email=user_email,
                                                    first_name=user_first_name,
                                                    last_name=user_last_name,
                                                    password='nopasswordset')
                    user.save()
                    token = Token.objects.create(user=user)
                    token.save()
                    profile = Profile(
                        user=user,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        user_image=pic_url)
                    profile.save()
                    social_account = SocialAccount.objects.create(
                        user=user,
                        provider="facebook",
                        uid=uid
                    )
                    social_account.save()
                    data = {"success": True,
                            "token": token.key,
                            "user_uid": user.id,
                            "user_name": user_name,
                            "user_image": profile.user_image,
                            "message": "user authenticated"}
                    return Response(data)
            else:
                data = {"success": False,
                        "token": "no token to manage",
                        "message": "missing token in the request"}
                return Response(data)
        else:
            data = {"success": False,
                    "token": "no request at all",
                    "message": "missing post in the request"
                    }
            return Response(data)


# auth user by token <- android app
class AuthUsers(APIView):
    @staticmethod
    def post(request):
        if request.method == 'POST':
            token = request.POST.get('token')
            if not token == "null":
                istoken = Token.objects.get(pk=token)
                if istoken is not None:
                    user = User.objects.get(id=istoken.user_id)
                    user_name = user.first_name + " " + user.last_name
                    profile = Profile.objects.get(user=user)
                    data = {"success": True,
                            "token": token,
                            "user_uid": user.id,
                            "user_name": user_name,
                            "user_image": profile.user_image,
                            "user_email": user.email,
                            "message": "user authenticated"}
                    return Response(data)
                else:
                    error = {"success": False,
                             "message": "Token invalide ",
                             "token": token}
                    return Response(error)
            else:
                username = request.POST.get('user_name')
                password = request.POST.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        istoken = Token.objects.get(user=user)
                        profile = Profile.objects.get(user=user)
                        data = {"success": True,
                                "token": istoken.key,
                                "user_uid": user.id,
                                "user_email": user.email,
                                "user_image": profile.user_image,
                                "user_name": user.first_name + " " + user.last_name,
                                "message": "user authenticated"}
                        return Response(data)
                    else:
                        data = {"success": False,
                                "token": "null",
                                "message": "disabled account"}
                        return Response(data)

                else:
                    data = {"success": False,
                            "token": "null",
                            "message": "invalid credentials"}
                    return Response(data)
        else:
            data = {"success": False, "token": "no post", "message": "no Post"}
            return Response(data)


# return all post to gserialiser -> android app
class GiftViewSet(APIView):
    @staticmethod
    def post(request):
        display_type = request.POST.get("display_type")
        if display_type == "all":
            gift = Mygifts.objects.all()
            serialiser = GiftSerializer(gift, many=True)
            return Response(serialiser.data)
        elif display_type == "by_user":
            user_id = request.POST.get("user_id")
            user = User.objects.get(id=user_id)
            gift = Mygifts.objects.filter(gived_by=user)
            serialiser = GiftSerializer(gift, many=True)
            return Response(serialiser.data)
        else:
            return Response("No data to display! ")


class AddNewGift(APIView):
    @staticmethod
    def post(request):
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            title = request.POST.get('title')
            domaine = request.POST.get('domaine')
            city = request.POST.get('city')
            body = request.POST.get('body')
            image = request.POST.get('image')
            user = User.objects.get(pk=user_id)
            profile = Profile.objects.get(user=user)
            gift = Mygifts.objects.create(
                gived_by=user,
                domaine=domaine,
                city=city,
                title=title,
                body=body,
                image=image,
                user_name=user.first_name + " " + user.last_name,
                user_image=profile.user_image
            )
            gift.save()
            if gift:
                data = {"success": True,
                        "id": gift.id}
                return Response(data)
            else:
                data = {"success": False,
                        "message": "error adding new gift"
                        }
                return Response(data)
        else:
            data = {"success": False,
                    "message": "get request"}
            return Response(data)


class UpdateImage(APIView):
    @staticmethod
    def post(request):
        if request.method == 'POST':
            gift_id = request.POST.get('gift_id')
            image_url = request.POST.get('image')
            gift = Mygifts.objects.get(id=gift_id)
            gift.image = image_url
            gift.save()
            data = {"success": True}
            return Response(data)


# ajouter une demande
class NewRequest(APIView):
    @staticmethod
    def post(request):
        if request.method == "POST":
            errors = {}
            save = True
            uid = request.POST.get('user_id')
            oid = request.POST.get('owner_id')
            gid = request.POST.get('gift_id')
            user_name = request.POST.get('user_name')
            user_message = request.POST.get('user_message')
            user_email = request.POST.get('user_email')
            user_city = request.POST.get('user_city')
            user_phone = request.POST.get('user_phone')
            user = User.objects.get(pk=uid)
            gift = Mygifts.objects.get(pk=gid)
            owner = User.objects.get(pk=oid)

            # test if already requested
            test2 = GiftRequest.objects.filter(Q(gift=gift) & Q(user=user))
            if len(test2) > 0:
                errors.update({'gift': 'vous avez déja demandé cet offre'})
                save = False
            if not email_validator(user_email):
                errors.update({'gift': 'Email non valide'})
                save = False
            if save:
                post = GiftRequest(user=user,
                                   gift=gift,
                                   owner=owner.id,
                                   user_name=user_name,
                                   user_city=user_city,
                                   user_email=user_email,
                                   user_message=user_message,
                                   user_phone=user_phone)
                post.save()
                absolute_url = request.build_absolute_uri(reverse('users'))
                verb = user.first_name + ' a envoyé une demande sur votre offre'
                notify = Notifictaion.objects.create(sender=user,
                                                     receiver=owner,
                                                     target=post.id,
                                                     type='demande',
                                                     level='info',
                                                     absolute_url=absolute_url + '?sec=gifts',
                                                     verb=verb)
                notify.save()
                data = {"success": True,
                        "message": "Demande bien ajouté"}
                return Response(data)
            else:
                data = {"success": False, "errors": errors}
                return Response(data)


class DisplayRequests(APIView):
    @staticmethod
    def post(request):
        if request.method == "POST":
            uid = request.POST.get("uid")
            user = User.objects.get(pk=uid)
            display_type = request.POST.get("display_type")
            if display_type == "sent":
                all_requests = GiftRequest.objects.filter(Q(user=user) & ~Q(owner=user.id)).order_by('-date_add')
            else:
                all_requests = GiftRequest.objects.filter(owner=user.id).order_by('-date_add')
            requests = list(all_requests.values("id",
                                                "user_name",
                                                "user",
                                                "owner",
                                                "user__profile__user_image",
                                                "user_message",
                                                "user_city",
                                                "user_phone",
                                                "user_email",
                                                "gift__title",
                                                "gift__user_name",
                                                "stats",
                                                "date_add"))
            if len(requests) > 0:
                data = {'success': True, 'req': requests}
                return JsonResponse(data, safe=False)
            else:
                data = {'success': True, 'req': "no requests"}
                return JsonResponse(data, safe=False)
        else:
            pass
