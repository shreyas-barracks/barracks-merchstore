from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import models

from .models import Product, CartItem
from order.models import OrderItem
from .serializers import ProductSerializer, CartItemSerializer


class AllProductsView(APIView):

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            user_position = "user"
        else:
            user_position = user.position
        
        # Get search query parameter
        search_query = request.query_params.get('search', '').strip()
        
        # Get all visible products
        all_products = Product.objects.filter(is_visible=True)
        
        # Apply search filter if query exists
        if search_query:
            all_products = all_products.filter(
                models.Q(name__icontains=search_query) | 
                models.Q(description__icontains=search_query)
            )
        
        # Filter by user position in Python (SQLite doesn't support contains lookup on JSONField)
        queryset = [product for product in all_products if user_position in product.for_user_positions]
        
        serializer = ProductSerializer(queryset, many=True, context={"user": user})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductView(APIView):
    def get(self, request, product_id):
        user = request.user
        if not user.is_authenticated:
            user_position = "user"
        else:
            user_position = user.position

        product = Product.objects.filter(id=product_id).first()
        if (
            not product
            or (
                user.is_authenticated
                and user_position not in product.for_user_positions
            )
            or not product.is_visible
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(product, context={"user": user})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        product = Product.objects.filter(id=product_id).first()
        user = request.user
        user_position = user.position
        quantity = int(request.data.get("quantity", 1))

        if (
            not product
            or user_position not in product.for_user_positions
            or CartItem.objects.filter(user=user, product=product).exists()
            or not product.is_visible
            or not product.accept_orders
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if quantity > product.max_quantity:
            return Response(
                {"error": "Quantity exceeds the maximum allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        printing_name = request.data.get("printing_name")
        size = request.data.get("size")
        image_url = request.data.get("image_url")

        if (
            (product.is_name_required and printing_name is None)
            or (product.is_size_required and size is None)
            or (product.is_image_required and image_url is None)
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cart_item = CartItem(
            product=product,
            user=user,
            quantity=quantity,
            printing_name=printing_name,
            size=size,
            image_url=image_url,
        )
        cart_item.save()
        return Response(status=status.HTTP_200_OK)


class ViewCart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        serializer = CartItemSerializer(cart_items, many=True)

        return Response(
            {
                "items": serializer.data,
                "total_amount": int(total_amount),
            },
            status=status.HTTP_200_OK,
        )


class RemoveFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_item_id = request.data.get("cart_item_id")
        cart_item = CartItem.objects.filter(id=cart_item_id).first()

        if not cart_item or cart_item.user != request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cart_item.delete()
        return Response(status=status.HTTP_200_OK)


class UpdateCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = request.data.get("cart_items", [])
        total_amount = 0

        for item_data in cart_items:
            cart_item = CartItem.objects.filter(
                id=item_data["id"], user=request.user
            ).first()
            if cart_item:
                cart_item.quantity = item_data["quantity"]
                cart_item.save()
                total_amount += cart_item.product.price * cart_item.quantity

        # Check if the total amount is negative
        if total_amount < 0:
            return Response(
                {"error": "Total amount cannot be negative."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)

        return Response(
            {
                "items": serializer.data,
                "total_amount": int(total_amount),
            },
            status=status.HTTP_200_OK,
        )
