from django.core.management.base import BaseCommand
from booking.models import ServiceCategory


class Command(BaseCommand):
    help = 'Populate initial service categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'General Service',
                'description': 'Regular maintenance and general service',
                'base_price': 1500.00
            },
            {
                'name': 'Oil Change',
                'description': 'Engine oil and filter change',
                'base_price': 800.00
            },
            {
                'name': 'Brake Service',
                'description': 'Brake pad replacement and brake fluid check',
                'base_price': 2500.00
            },
            {
                'name': 'Tire Service',
                'description': 'Tire rotation, balancing, and replacement',
                'base_price': 1200.00
            },
            {
                'name': 'Battery Replacement',
                'description': 'Battery check and replacement',
                'base_price': 3000.00
            },
            {
                'name': 'AC Service',
                'description': 'Air conditioning system service and repair',
                'base_price': 2000.00
            },
            {
                'name': 'Engine Repair',
                'description': 'Engine diagnostics and repair',
                'base_price': 5000.00
            },
            {
                'name': 'Car Wash',
                'description': 'Exterior and interior car cleaning',
                'base_price': 500.00
            },
        ]

        created_count = 0
        for category_data in categories:
            category, created = ServiceCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'base_price': category_data['base_price']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} new categories!')
        )



