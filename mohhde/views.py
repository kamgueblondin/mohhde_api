# Le fichier home pour la page d'accueil
# Envoit de mail
def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/sandboxca40a2920a854f7ca1a2fe9c157392e8.mailgun.org/messages",
		auth=("api", "78e529cb9703e06da07fd20ef1ea0df3-db4df449-7b4ed0dd"),
		data={"from": "Mailgun Sandbox <postmaster@sandboxca40a2920a854f7ca1a2fe9c157392e8.mailgun.org>",
			"to": "KAMGUE Blondin <mohhint@gmail.com>",
			"subject": "Hello KAMGUE Blondin",
			"text": "Congratulations KAMGUE Blondin, you just sent an email with Mailgun!  You are truly awesome!"})

# You can see a record of this email in your logs: https://app.mailgun.com/app/logs.

# You can send up to 300 emails/day from this sandbox server.
# Next, you should add your own domain so you can send 10000 emails/month for free.
from django.shortcuts import render
def accueil(request):
    return render(request, 'home.html')

#Views pour l'inscription
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
        
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#Views pour la connexion
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
 
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return Response({'message': 'Vous êtes maintenant connecté.', 'user_token': user.profile.pruser_token})
    else:
        return Response({
            'error': 'Nom d\'utilisateur ou mot de passe invalide.'
        }, status=status.HTTP_401_UNAUTHORIZED)
        
#Views pour la réinitialisation du mot de passe :

#Envoyer l'email avec un code généré
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

@csrf_exempt
@api_view(['POST'])
def send_reset_password_email(request):
    if request.method == 'POST':
        #email = request.POST.get('email')
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # Generate a random 6-digit code
            reset_code = get_random_string(length=6)
            # Set the reset code for the user
            user.profile.reset_code = reset_code
            user.profile.save()
            # Send the reset code to the user's email address
            subject = 'Password reset code for {}'.format(settings.PROJECT_NAME)
            message = 'Your password reset code is {}'.format(reset_code)
            from_email = settings.EMAIL_SENDER_USER
            recipient_list = [email]
            
            try:
                # Send Email
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                return Response({'success': True})
            except Exception as e:
                # Error sending
                return Response({'success': False, 'message': e})
            
        else:
            return Response({'success': False, 'message': 'No user with this email'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

#Vérifier si le code est correct
@csrf_exempt
@api_view(['POST'])
def check_reset_password_code(request):
    if request.method == 'POST':
        email = request.data.get('email')
        reset_code = request.data.get('reset_code')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.profile.reset_code == reset_code:
                return Response({'success': True})
            else:
                return Response({'success': False, 'message': 'Incorrect reset code'})
        else:
            return Response({'success': False, 'message': 'No user with this email'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

#Réinitialiser le mot de passe
@csrf_exempt
@api_view(['POST'])
def reset_password(request):
    if request.method == 'POST':
        email = request.data.get('email')
        reset_code = request.data.get('reset_code')
        new_password = request.data.get('new_password')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.profile.reset_code == reset_code:
                user.set_password(new_password)
                user.profile.reset_code = ''
                user.save()
                return Response({'success': True})
            else:
                return Response({'success': False, 'message': 'Incorrect reset code'})
        else:
            return Response({'success': False, 'message': 'No user with this email'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})