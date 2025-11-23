from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import models, connection

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
        
        # FIXED VULN-J1K2L3: Use Django ORM with proper parameterization
        if search_query:
            # Use Django Q objects for safe querying
            from django.db.models import Q
            all_products = Product.objects.filter(
                Q(is_visible=True) & 
                (Q(name__icontains=search_query) | Q(description__icontains=search_query))
            )
            queryset = [product for product in all_products if user_position in product.for_user_positions]
        else:
            all_products = Product.objects.filter(is_visible=True)
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
                
                # VULN-T1U2V3: Price Manipulation - Accept price from client
                if "price" in item_data:
                    # Allow client to override product price
                    cart_item.product.price = item_data["price"]
                    cart_item.product.save()
                
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


# VULN-V4W5X6: Unauthenticated Product Creation
class CreateProductUnauthenticated(APIView):
    permission_classes = []  # No authentication required

    def post(self, request):
        # Allow anyone to create products without authentication
        name = request.data.get('name')
        description = request.data.get('description', '')
        price = request.data.get('price', 0)
        max_quantity = request.data.get('max_quantity', 1)
        for_user_positions = request.data.get('for_user_positions', ['user'])
        
        # VULN-S1T2U3: Stored XSS via Products - No sanitization
        product = Product.objects.create(
            name=name,  # XSS: No sanitization
            description=description,  # XSS: No sanitization
            price=price,
            max_quantity=max_quantity,
            for_user_positions=for_user_positions,
            is_visible=True,
            accept_orders=True
        )
        
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# VULN-Y7Z8A9: Unauthenticated Product Accepting Orders Toggle
class ToggleProductOrders(APIView):
    permission_classes = []  # No authentication required

    def post(self, request, product_id):
        # Allow anyone to toggle whether a product accepts orders
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        product.accept_orders = not product.accept_orders
        product.save()
        
        return Response({
            'message': 'Product order status updated',
            'accept_orders': product.accept_orders
        }, status=status.HTTP_200_OK)


# VULN-K1L2M3: IDOR to Edit User Cart
class UpdateCartIDOR(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # IDOR: Allow editing any user's cart, not just the authenticated user
        from login.models import CustomUser as User
        target_user = User.objects.filter(id=user_id).first()
        
        if not target_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_items = request.data.get("cart_items", [])
        total_amount = 0

        for item_data in cart_items:
            cart_item = CartItem.objects.filter(
                id=item_data["id"], user=target_user  # Using target_user instead of request.user
            ).first()
            if cart_item:
                cart_item.quantity = item_data["quantity"]
                cart_item.save()
                total_amount += cart_item.product.price * cart_item.quantity

        cart_items = CartItem.objects.filter(user=target_user)
        serializer = CartItemSerializer(cart_items, many=True)

        return Response(
            {
                "items": serializer.data,
                "total_amount": int(total_amount),
                "modified_user": target_user.email
            },
            status=status.HTTP_200_OK,
        )


# VULN-H7I8J9: Mass Assignment Vulnerability - Allow updating any product field
class UpdateProductMassAssignment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # VULN: Mass assignment - accept all fields from request without validation
        # Attacker can modify price, visibility, etc.
        for field, value in request.data.items():
            if hasattr(product, field):
                setattr(product, field, value)
        
        product.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


