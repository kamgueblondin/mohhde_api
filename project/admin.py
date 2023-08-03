from django.contrib import admin

# Register your models here.
from .models import Projet,Etape,SourceFinancement,GarantieFinancement,Investisseur,Souscription,Financement,Commentaire,CleinOeilMohhde,Like,Partage

admin.site.register(Projet)
admin.site.register(Etape)
admin.site.register(SourceFinancement)
admin.site.register(GarantieFinancement)
admin.site.register(Investisseur)
admin.site.register(Souscription)
admin.site.register(Financement)
admin.site.register(Commentaire)
admin.site.register(Like)
admin.site.register(Partage)
admin.site.register(CleinOeilMohhde)
