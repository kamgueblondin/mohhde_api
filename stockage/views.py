from rest_framework.views import APIView
from rest_framework.response import Response

from stockage.models import Stock,Element 
from .serializers import StockSerializer, ElementSerializer 

class StorageInfo(APIView):

   def get(self,request,user_id=None,*args,**kwargs):  
       stock_info = Stock.objects.get(user=user_id)             
       serializer =  StockSerializer(stock_info)                      
       return Response(serializer.data)

   def post(self,request,user_id=None,*args,**kwargs):       
       element_data = request.data                            
       element_data['user'] = user_id   
        
       serializer =	ElementSerializer(data=request.data)   

       if serializer.is_valid():                                      
           element_size = request.data.get('size')           
           current_stock = Stock.objects.get(user=user_id)   
           current_stock.used_space += element_size                      
           current_stock.save()                                        
           serializer.save()                                            
       return Response(serializer.data)