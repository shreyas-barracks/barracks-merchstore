import os
import shutil
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from products.models import Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate database with default products from assets folder'

    def handle(self, *args, **kwargs):
        # Define default products based on the assets available
        products_data = [
            {
                'name': 'Gaming Mousepad',
                'price': Decimal('499.00'),
                'max_quantity': 5,
                'description': 'Premium gaming mousepad with anti-slip base and smooth surface for precise mouse control.',
                'is_name_required': False,
                'is_size_required': False,
                'is_image_required': False,
                'accept_orders': True,
                'is_visible': True,
                'for_user_positions': ['user'],
                'images': ['Mousepad-Final-Size.png', 'Mousepad-mockup.png']
            },
            {
                'name': 'Samurai Sticker',
                'price': Decimal('99.00'),
                'max_quantity': 10,
                'description': 'High-quality waterproof samurai-themed sticker. Perfect for laptops, water bottles, and more.',
                'is_name_required': False,
                'is_size_required': False,
                'is_image_required': False,
                'accept_orders': True,
                'is_visible': True,
                'for_user_positions': ['user'],
                'images': ['samurai-full.png', 'sticker-3-report.png']
            },
        ]

        assets_dir = os.path.join(settings.BASE_DIR, 'assets')
        
        if not os.path.exists(assets_dir):
            self.stdout.write(self.style.ERROR(f'Assets directory not found: {assets_dir}'))
            return

        for product_data in products_data:
            # Check if product already exists
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'price': product_data['price'],
                    'max_quantity': product_data['max_quantity'],
                    'description': product_data['description'],
                    'is_name_required': product_data['is_name_required'],
                    'is_size_required': product_data['is_size_required'],
                    'is_image_required': product_data['is_image_required'],
                    'accept_orders': product_data['accept_orders'],
                    'is_visible': product_data['is_visible'],
                    'for_user_positions': product_data['for_user_positions'],
                }
            )

            if created:
                # Add images if product was just created
                images = product_data.get('images', [])
                
                # Add image1
                if len(images) > 0:
                    image1_path = os.path.join(assets_dir, images[0])
                    if os.path.exists(image1_path):
                        with open(image1_path, 'rb') as f:
                            product.image1.save(images[0], File(f), save=False)
                
                # Add image2
                if len(images) > 1:
                    image2_path = os.path.join(assets_dir, images[1])
                    if os.path.exists(image2_path):
                        with open(image2_path, 'rb') as f:
                            product.image2.save(images[1], File(f), save=False)
                
                product.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully created product: {product.name}'))
            else:
                # Update existing product's for_user_positions if it's empty
                if not product.for_user_positions:
                    product.for_user_positions = product_data['for_user_positions']
                    product.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated product positions: {product.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Product already exists: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Finished populating products!'))
