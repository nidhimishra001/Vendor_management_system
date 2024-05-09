from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView, UpdateAPIView,DestroyAPIView
from rest_framework.views import APIView
from .serializers import VenderSerializer,PurchaseOrderSerializer,VendorPerformanceSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Vendor,PurchaseOrder
from django.db.models import F
from rest_framework import generics
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class VenderCreateApi(CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = VenderSerializer

    def post(self, request, *args, **kwargs):
        vender_data = request.data
        try:
            vender_data = vender_data.dict()
        except:
            vender_data = vender_data
        serializer = self.serializer_class(data=vender_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Data inserted successfully'}, status=status.HTTP_201_CREATED)
    
class VenderListAPI(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = VenderSerializer

    def list(self, request, *args, **kwargs):
        data = Vendor.objects.all()
        serializer = self.serializer_class(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class VenderByIdAPI(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = VenderSerializer

    def list(self, request, *args, **kwargs):
        data = Vendor.objects.get(id=self.kwargs['id'])
        serializer = self.serializer_class(data)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class VenderUpdateAPI(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = VenderSerializer

    def put(self, request, *args, **kwargs):
        vendor =Vendor.objects.get(id=self.kwargs['id'])
        serializer = self.serializer_class(vendor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Data updated successfully'}, status=status.HTTP_200_OK)
    

class VenderDeleteApi(DestroyAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = VenderSerializer

    def delete(self, request, *args, **kwargs):
        try:
            vendor = Vendor.objects.get(id=self.kwargs['id'])
        except Vendor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        vendor.delete()
        return Response({'message:deleted'},status=status.HTTP_204_NO_CONTENT)
    


class PurchaseOrder_CreateApi(CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = PurchaseOrderSerializer

    def post(self, request, *args, **kwargs):
        po_data = request.data
        try:
            po_data = po_data.dict()
        except:
            po_data = po_data
        serializer = self.serializer_class(data=po_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Data inserted successfully'}, status=status.HTTP_201_CREATED)
    
class PurchaseOrderListAPI(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = PurchaseOrderSerializer

    def list(self, request, *args, **kwargs):
        data = PurchaseOrder.objects.all()
        serializer = self.serializer_class(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class PurchaseOrderByIdAPI(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = PurchaseOrderSerializer

    def list(self, request, *args, **kwargs):
        data = PurchaseOrder.objects.get(id=self.kwargs['id'])
        serializer = self.serializer_class(data)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class PurchaseOrderUpdateAPI(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = PurchaseOrderSerializer

    def put(self, request, *args, **kwargs):
        po_data =PurchaseOrder.objects.get(id=self.kwargs['id'])
        serializer = self.serializer_class(po_data, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Data updated successfully'}, status=status.HTTP_200_OK)
    

class PurchaseOrderDeleteApi(DestroyAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = PurchaseOrderSerializer

    def delete(self, request, *args, **kwargs):
        try:
            po_data = PurchaseOrder.objects.get(id=self.kwargs['id'])
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        po_data.delete()
        return Response({'message:deleted'},status=status.HTTP_204_NO_CONTENT)



class VendorPerformanceAPIView(generics.RetrieveAPIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, vendor_id):
        vendor = Vendor.objects.get(pk=vendor_id)
        serializer = VendorPerformanceSerializer(vendor)
        return Response(serializer.data)


class AcknowledgePurchaseOrderView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, po_id):
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
        purchase_order.acknowledgment_date = timezone.now()
        print(purchase_order.acknowledgment_date)
        purchase_order.save()
        return Response(status=status.HTTP_200_OK)


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        token = Token.objects.create(user=user)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    

class LoginAPI(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username,password)
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)    
        