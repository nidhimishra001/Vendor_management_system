from django.contrib import admin
from django.urls import path
from . import views
from .views import VenderCreateApi,VenderListAPI,VenderByIdAPI,VenderUpdateAPI,VenderDeleteApi,PurchaseOrder_CreateApi,PurchaseOrderListAPI,\
PurchaseOrderByIdAPI,PurchaseOrderUpdateAPI,PurchaseOrderDeleteApi,VendorPerformanceAPIView,AcknowledgePurchaseOrderView,RegisterView,LoginAPI

urlpatterns = [
    # VENDER
    path('vender/create', VenderCreateApi.as_view()),
    path('vender/list', VenderListAPI.as_view()),
    path('vender/<int:id>', VenderByIdAPI.as_view()),
    path('vender/updateApi/<int:id>', VenderUpdateAPI.as_view()),
    path('vender/deleteApi/<int:id>', VenderDeleteApi.as_view()),

    # PURCHASE ORDER
    path('api/purchase_orders/', PurchaseOrder_CreateApi.as_view()),
    path('api/purchase_orders/list', PurchaseOrderListAPI.as_view()),
    path('api/purchase_orders/byId/<int:id>', PurchaseOrderByIdAPI.as_view()),
    path('api/purchase_orders/update/<int:id>', PurchaseOrderUpdateAPI.as_view()),
    path('api/purchase_orders/delete/<int:id>', PurchaseOrderDeleteApi.as_view()),

    path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor_performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),

    # AUTHENTICATION
    path("api/register/", RegisterView.as_view()),
	path("api/login/", LoginAPI.as_view()),
]