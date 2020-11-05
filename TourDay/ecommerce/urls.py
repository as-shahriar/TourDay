from django.urls import path
from ecommerce.views import (
    store, cart, checkout, staff_pages, product_table, order_table,
    order_details, user_order, product_edit, add_product, product_delete, checkout_message, ViewPDF,DownloadPDF)

urlpatterns = [
    path('', store, name='store'),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('staff/', staff_pages, name='staff_pages'),
    path('addproduct/', add_product, name='add_product'),
    path('allproduct/', product_table, name='all_product'),
    path('product/edit/<int:id>', product_edit, name='product_edit'),
    path('product/delete/<int:id>', product_delete, name='product_delete'),
    path('allorder/', order_table, name='all_order'),
    path('order/details/<int:id>', order_details, name='order_details'),
    path('user/order/', user_order, name='user_order'),

    path('checkout/message/', checkout_message, name='checkout_message'),

    path('pdf_view/', ViewPDF.as_view(), name="pdfview"),
    path('pdf_download/', DownloadPDF.as_view(), name="pdf_download"),

]
