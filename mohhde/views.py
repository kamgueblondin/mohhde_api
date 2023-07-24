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
from medias.models import Chain, Media
def accueil(request):
    return render(request, './templates/home.html')

#Views pour l'inscription
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from django.utils.crypto import get_random_string
from rest_framework import status
from django.db import transaction

@api_view(['POST'])
@transaction.atomic
def register_view(request):
    user_serializer = UserSerializer(data=request.data.get('user'))
    profile_serializer = ProfileSerializer(data=request.data.get('profile'))
    if user_serializer.is_valid(raise_exception=True) and profile_serializer.is_valid(raise_exception=True):
        user = user_serializer.save()
        # Utiliser set_password() pour hasher le mot de passe.
        user.set_password(user.password)
        # Enregistrer les modifications apportées à l'utilisateur.
        user.save()

        # Generate a random 60-digit code
        user_token = get_random_string(length=60)
        profile_data = {'user': user, 'user_token': user_token, **request.data['profile']}
        profile_instance = profile_serializer.create(profile_data)
        response_data = {
            'success': True,
            'user': UserSerializer(user).data,
            'profile': ProfileSerializer(profile_instance).data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    error_response_data = {
            'success': False,
            'user_errors': user_serializer.errors,
            'profile_errors': profile_serializer.errors,
     }
    return Response(error_response_data ,status=status.HTTP_400_BAD_REQUEST)

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
        response_data = {
            'success': True,
            'user': UserSerializer(user).data,
            'profile': ProfileSerializer(user.profile).data,
        }
        return Response(response_data)
    else:
        return Response({
            'success': False,
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
from django.shortcuts import get_object_or_404
# Vue basée sur une classe générique qui gère la création d'un nouvel objet utilisateur lorsqu'une requête POST est soumise.
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
                user.profile.save()
                user.save()
                response_data = {
                    'success': True,
                    'user': UserSerializer(user).data,
                    'profile': ProfileSerializer(user.profile).data,
                }
                return Response(response_data)
            else:
                return Response({'success': False, 'message': 'Incorrect reset code'})
        else:
            return Response({'success': False, 'message': 'No user with this email'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

#Profil de l'utilisateur
@csrf_exempt
@api_view(['GET'])
def infos_profile(request):
    if request.method == 'GET':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        if user.profile.user_token == user_token:
            response_data = {
                'success': True,
                'user': UserSerializer(user).data,
                'profile': ProfileSerializer(user.profile).data,
            }
            return Response(response_data)
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

#Mise à jour des informations du profil
@csrf_exempt
@api_view(['POST'])
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        if user.profile.user_token == user_token:
            #Modification start
            user.email=request.data.get('email')
            user.profile.phone=request.data.get('phone')
            user.profile.sex=request.data.get('sex')
            user.profile.email=request.data.get('email')
            user.profile.birthday=request.data.get('birthday')
            user.profile.save()
            user.save()
            response_data = {
                'success': True,
                'user': UserSerializer(user).data,
                'profile': ProfileSerializer(user.profile).data,
            }
            return Response(response_data)
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

#Changement de mot de passe
@csrf_exempt
@api_view(['POST'])
def change_password(request):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        if user.profile.user_token == user_token:
            #Modification start
            if not user.check_password(request.data.get("old_password")):
                return Response({'success': False, 'message': 'Le mot de passe actuel est incorrect.'})
            
             # Changer le mot de passe et sauvegarder l'utilisateur
            user.set_password(request.data.get("new_password"))
            user.save()
            response_data = {
                'success': True,
                'user': UserSerializer(user).data,
                'profile': ProfileSerializer(user.profile).data,
            }
            return Response(response_data)
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

#Ajouter la photo de profile de l'utilisateur

@csrf_exempt
@api_view(['POST'])
def media_profile_old(request):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        if user.profile.user_token == user_token:
            photo_title = request.data.get('title')
            photo_description = request.data.get('description')

            try:
                profile_chain = Chain.objects.get(name='profile', user=user)
            except Chain.DoesNotExist:
                # Créer une nouvelle chaîne "profile"
                profile_chain = Chain.objects.create(name='profile', description='Profile chain', type='I', user=user, is_system=True)


            media = Media.objects.create(title=photo_title, description=photo_description, type='I', user=user, chain=profile_chain)

            response_data = {
                'success': True,
                'chain': profile_chain.name,
                'media': media.title,
                "message": "Média ajouté avec succès."
            }
            return Response(response_data)
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

import base64
import os
import time

@csrf_exempt
@api_view(['POST'])
def media_profile(request):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        
        if user.profile.user_token == user_token:
            photo_title = request.data.get('title')
            image_ext = request.data.get('image_ext')

            try:
                profile_chain = Chain.objects.get(name='profile', user=user)
                 # Marquer tous les médias existants dans la chaîne comme archivés
                Media.objects.filter(chain=profile_chain).update(is_archived=True)
                
            except Chain.DoesNotExist:
                # Créer une nouvelle chaîne "profile"
                profile_chain = Chain.objects.create(name='profile', description='Profile chain', type='I', user=user, is_system=True)

            # Récupérer l'image en base64 depuis les données de la requête
            encoded_image_data = request.data.get('image_base64')
            
            # Convertir l'image en bytes
            image_data_bytes = base64.b64decode(encoded_image_data)
            
            # Générer un nom unique pour le fichier d'image (utilisation du titre + timestamp par exemple)
			
            unique_filename = f"{photo_title}_{int(time.time())}.{image_ext}"

			# Chemin complet vers le dossier public où vous souhaitez stocker les images téléchargées
			
            save_path = os.path.join("./templates/profile/", unique_filename)

			# Enregistrer l'image sur le disque dans le dossier public avec le nom unique généré 
			
            with open(save_path, 'wb') as file:
				
                file.write(image_data_bytes)

			# Création du média avec le titre et la description fournis
			
            media = Media.objects.create(title=photo_title, description=unique_filename, type='I', user=user, chain=profile_chain)

			
            response_data = {
				'success': True,
				'chain': profile_chain.name,
                'image': media.description,
				'media': media.title,
				'message': 'Média ajouté avec succès.'
			}
			
            return Response(response_data)
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message':'Invalid method'})

@csrf_exempt
@api_view(['POST'])
def media_galerie(request):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        
        if user.profile.user_token == user_token:
            photo_title = request.data.get('title')
            image_ext = request.data.get('image_ext')

            try:
                galerie_chain = Chain.objects.get(name='galerie', user=user)
                
            except Chain.DoesNotExist:
                # Créer une nouvelle chaîne "galerie"
                galerie_chain = Chain.objects.create(name='galerie', description='Galerie chain', type='I', user=user, is_system=True)

            # Récupérer l'image en base64 depuis les données de la requête
            encoded_image_data = request.data.get('image_base64')
            
            # Convertir l'image en bytes
            image_data_bytes = base64.b64decode(encoded_image_data)
            
            # Générer un nom unique pour le fichier d'image (utilisation du titre + timestamp par exemple)
			
            unique_filename = f"{photo_title}_{int(time.time())}.{image_ext}"

			# Chemin complet vers le dossier public où vous souhaitez stocker les images téléchargées
			
            save_path = os.path.join("./templates/galerie/", unique_filename)

			# Enregistrer l'image sur le disque dans le dossier public avec le nom unique généré 
			
            with open(save_path, 'wb') as file:
				
                file.write(image_data_bytes)

			# Création du média avec le titre et la description fournis
			
            media = Media.objects.create(title=photo_title, description=unique_filename, type='I', user=user, chain=galerie_chain)

			
            response_data = {
				'success': True,
				'chain': galerie_chain.name,
                'image': media.description,
				'media': media.title,
				'message': 'Média ajouté avec succès.'
			}
			
            return Response(response_data)
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message':'Invalid method'})

#Profil image de profil
@csrf_exempt
@api_view(['GET'])
def ma_photo_profile(request):
    if request.method == 'GET':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        if user.profile.user_token == user_token:
            try:
                profile_chain = Chain.objects.get(name='profile', user=user)
                # Récupérer le premier média non archivé (is_archived=False) de l'utilisateur
                media = Media.objects.filter(user=user, is_archived=False, chain=profile_chain).first()
                
                if media:
                    image_path = "./templates/profile/"+media.description
                    
                    with open(image_path, 'rb') as file:
                        encoded_image_data = base64.b64encode(file.read()).decode('utf-8')
                        
                    response_data ={
                        'success': True,
                        'media_title': media.description,
                        'image_base64': encoded_image_data
                    }
                    
                    return Response(response_data)
                
                else:
                    return Response({'success': False, 'message':'No profile media found for this user'})
            except Chain.DoesNotExist:
                return Response({'success': False, 'message':'No chain profile found for this user'})
        
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})


#Gallerie image
@csrf_exempt
@api_view(['GET'])
def mes_photos_galerie(request):
    if request.method == 'GET':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        if user.profile.user_token == user_token:
            try:
                galerie_chain = Chain.objects.get(name='galerie', user=user)
                # Récupérer tous les médias non archivés (is_archived=False) de la chaîne galerie de l'utilisateur
                media_list = Media.objects.filter(user=user, is_archived=False, chain=galerie_chain)
        
        
                
                if media_list:

                    response_data ={
                        'success': True,
                        'media_count': len(media_list),
                        'media': []
                    }
                    
                    for media in media_list:
                        image_path = "./templates/galerie/" + media.description
                        
                        with open(image_path, 'rb') as file:
                            encoded_image_data = base64.b64encode(file.read()).decode('utf-8')
                            
                        response_data['media'].append({
                            'title': media.description,
                            'image_base64': encoded_image_data
                        })
                        
                    return Response(response_data)
                
                else:
                    return Response({'success': False, 'message':'No galerie media found for this user'})
            except Chain.DoesNotExist:
                return Response({'success': False, 'message':'No chain galerie found for this user'})
        
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

#Archive image de profile
@csrf_exempt
@api_view(['GET'])
def archive_media_profile(request):
    if request.method == 'GET':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        if user.profile.user_token == user_token:
            try:
                profile_chain = Chain.objects.get(name='profile', user=user)
                # Récupérer le premier média non archivé (is_archived=False) de l'utilisateur
                media = Media.objects.filter(user=user, is_archived=False, chain=profile_chain).first()
                
                if media:
                    # Archiver le média en définissant is_archived=True
                    media.is_archived = True
                    media.save()
                    
                    return Response({'success': True, 'message':'Media archived successfully'})
            
                
                else:
                    return Response({'success': False, 'message':'No profile media found for this user'})
            except Chain.DoesNotExist:
                return Response({'success': False, 'message':'No chain profile found for this user'})
        
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

#Archive image de profile
@csrf_exempt
@api_view(['GET'])
def archive_media_profile(request):
    if request.method == 'GET':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        if user.profile.user_token == user_token:
            try:
                profile_chain = Chain.objects.get(name='profile', user=user)
                # Récupérer le premier média non archivé (is_archived=False) de l'utilisateur
                media = Media.objects.filter(user=user, is_archived=False, chain=profile_chain).first()
                
                if media:
                    # Archiver le média en définissant is_archived=True
                    media.is_archived = True
                    media.save()
                    
                    return Response({'success': True, 'message':'Media archived successfully'})
            
                
                else:
                    return Response({'success': False, 'message':'No profile media found for this user'})
            except Chain.DoesNotExist:
                return Response({'success': False, 'message':'No chain profile found for this user'})
        
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

#Archive image de profile
@csrf_exempt
@api_view(['GET'])
def archive_media_galerie(request):
    if request.method == 'GET':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        title = request.data.get('title')
        if user.profile.user_token == user_token:
            try:
                galerie_chain = Chain.objects.get(name='galerie', user=user)
                # Récupérer le premier média non archivé (is_archived=False) de l'utilisateur
                media = Media.objects.filter(user=user, is_archived=False, chain=galerie_chain, description=title).first()
                
                if media:
                    # Archiver le média en définissant is_archived=True
                    media.is_archived = True
                    media.save()
                    
                    return Response({'success': True, 'message':'Media archived successfully'})
            
                
                else:
                    return Response({'success': False, 'message':'No profile media found for this user'})
            except Chain.DoesNotExist:
                return Response({'success': False, 'message':'No chain profile found for this user'})
        
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

#Se deconnecté
@csrf_exempt
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        if user.profile.user_token == user_token:
            # Generate a random 60-digit code
            user_tokens = get_random_string(length=60)
            user.profile.user_token =user_tokens
            user.profile.save()
            return Response({'success': True, 'message':'Logout successfully'})
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})