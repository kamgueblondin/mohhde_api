from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .serializers import ProjetSerializer
from .models import User, Projet
from together.models import Friendship
from medias.models import Chain, Media

@api_view(['POST'])
def projet_add_api(request):
    if request.method == 'POST':
        username = request.data.get('username')
        user_token = request.data.get('user_token')

        user = get_object_or_404(User, username=username)

        if user.profile.user_token == user_token:

            titre = request.data.get('titre')
            description = request.data.get('description')
            code_securite = request.data.get('code_securite')
            cible = request.data.get('cible')
            objectif = request.data.get('objectif')
            cout_total = request.data.get('cout_total')
            nombre_cycles = request.data.get('nombre_cycles')
            echeance = request.data.get('echeance')
            proprietaire = user                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
            utilise_fonds_physiques = request.data.get('utilise_fonds_physiques')
            #chaine_mise_avant = request.data.get('chaine_mise_avant')
            #chaine_couverture = request.data.get('chaine_couverture')
            #chaine_media = request.data.get('chaine_media')

            #chaine_mise_avant=chaine_mise_avant,
            #chaine_couverture=chaine_couverture,
            #chaine_media=chaine_media

            # Votre logique ici pour vérifier les conditions et créer le projet en conséquence

            projet = Projet.objects.create(
                titre=titre,
                description=description,
                code_securite=code_securite,
                cible=cible,
                objectif=objectif,
                cout_total=cout_total,
                nombre_cycles=nombre_cycles,                                                                         
                echeance=echeance,
                proprietaire=proprietaire,
                utilise_fonds_physiques=utilise_fonds_physiques,
            )

            serializer = ProjetSerializer(projet)
            response_data = {
                'success': True,
                'projet': serializer.data,
            }
            return Response(response_data)
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

@api_view(['GET'])
def get_projects(request):
    if request.method == 'GET':
        username = request.data.get('username')
        user_token = request.data.get('user_token')

        user = get_object_or_404(User, username=username)

        if user.profile.user_token == user_token:
            # Récupère les projets de l'utilisateur paginés de 5 en 5
            # Remplace cette partie avec ta logique de récupération des projets paginés [:5]

            projects = Projet.objects.filter(proprietaire=user).order_by('id')
            serializer = ProjetSerializer(projects, many=True)

            response_data ={
                'success': True,
                'projets': serializer.data
            }
            
            return Response(response_data)
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

@api_view(['GET'])
def get_all_projects(request):
    if request.method == 'GET':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')

        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})

        friendships = Friendship.objects.filter(user=user,status='accepted')
        friend_data = []
        friend_data.append(user.id)

        for friendship in friendships:
            friend_data.append(friendship.friend.id)
        user_ids = friend_data  # Obtient la liste des IDs des utilisateurs

        users = User.objects.filter(id__in=user_ids)  # Récupère les utilisateurs correspondants aux IDs
        projects = Projet.objects.filter(proprietaire__in=users)  # Récupère les projets des utilisateurs

        serializer = ProjetSerializer(projects, many=True)
            
        response_data ={
            'success': True,
            'projets': serializer.data
        }
        
        return Response(response_data)
    else:
        return Response({'success': False, 'message': 'Invalid method'})

import base64
import os
import time


@api_view(['POST'])
def media_projet(request):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        projet_id = request.data.get('projet_id')
        
        if user.profile.user_token == user_token:
            photo_title = request.data.get('title')
            image_ext = request.data.get('image_ext')
            try:
                project = Projet.objects.get(proprietaire=user,id=projet_id)
            
                try:
                    project_chain = Chain.objects.get(name='chainemediaprojet'+projet_id, user=user)
                    # Marquer tous les médias existants dans la chaîne comme archivés
                    Media.objects.filter(chain=project_chain, user=user).update(is_archived=True)
                    
                except Chain.DoesNotExist:
                    # Créer une nouvelle chaîne "projet"
                    project_chain = Chain.objects.create(name='chainemediaprojet'+projet_id, description='Projet media chain', type='I', user=user, is_system=True)

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
                
                media = Media.objects.create(title=photo_title, description=unique_filename, type='I', user=user, chain=project_chain)
                project.chaine_media=project_chain
                project.save()
                
                response_data = {
                    'success': True,
                    'chain': project_chain.name,
                    'image': media.description,
                    'media': media.title,
                    'message': 'Média ajouté avec succès.'
                }
                
                return Response(response_data)
            except Projet.DoesNotExist:
                return Response({'success': False, 'message': 'No projet with this key'})
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message':'Invalid method'})

#Profil image de projet
@api_view(['GET'])
def recup_projet(request):
    if request.method == 'GET':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        projet_id = request.data.get('projet_id')
        if user.profile.user_token == user_token:
            try:
                projet_chain = Chain.objects.get(name='chainemediaprojet'+projet_id)
                #, user=user
                # Récupérer le premier média non archivé (is_archived=False) de l'utilisateur
                media = Media.objects.filter(is_archived=False, chain=projet_chain).first()
                #user=user,
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
                    return Response({'success': False, 'message':'No projet media found for this user'})
            except Chain.DoesNotExist:
                return Response({'success': False, 'message':'No chain projet found for this user'})
        
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})
