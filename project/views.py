from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .serializers import ProjetSerializer
from .models import User, Projet

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
        return Response({'success': False, 'message': 'Invalid method'})                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         7
                                                                                                                                                                                                                                              