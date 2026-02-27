from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.hotels.models import Hotel, Room

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample hotels, rooms and users'

    def handle(self, *args, **options):
        self.stdout.write('=== Seeding StayEase Data ===\n')

        # Admin user
        if not User.objects.filter(email='admin@stayease.com').exists():
            u = User.objects.create_superuser(
                username='admin', email='admin@stayease.com',
                password='Admin@123456', first_name='Admin', last_name='StayEase',
            )
            u.is_email_verified = True
            u.balance = 99999
            u.save()
            self.stdout.write(self.style.SUCCESS('Created admin: admin@stayease.com / Admin@123456'))

        # Test user
        if not User.objects.filter(email='user@stayease.com').exists():
            u = User.objects.create_user(
                username='testuser', email='user@stayease.com',
                password='User@123456', first_name='John', last_name='Doe',
                is_active=True,
            )
            u.is_email_verified = True
            u.balance = 5000
            u.save()
            self.stdout.write(self.style.SUCCESS('Created user: user@stayease.com / User@123456'))

        # Hotels
        hotels = [
            {
                'name': 'The Grand Palace Hotel',
                'description': 'A luxury 5-star hotel in the heart of New York City.',
                'address': '123 Grand Boulevard', 'city': 'New York', 'country': 'USA',
                'star_rating': 5, 'amenities': 'Pool, Spa, WiFi, Gym, Restaurant, Parking',
                'rooms': [
                    {'room_number': '101', 'room_type': 'single', 'price_per_night': 150, 'capacity': 1},
                    {'room_number': '102', 'room_type': 'double', 'price_per_night': 250, 'capacity': 2},
                    {'room_number': '201', 'room_type': 'suite',  'price_per_night': 500, 'capacity': 4},
                ]
            },
            {
                'name': 'Seaside Paradise Resort',
                'description': 'Beautiful beachfront resort with stunning ocean views.',
                'address': '456 Ocean Drive', 'city': 'Miami', 'country': 'USA',
                'star_rating': 4, 'amenities': 'Beach, Pool, Water Sports, Restaurant, WiFi',
                'rooms': [
                    {'room_number': 'A101', 'room_type': 'single', 'price_per_night': 120, 'capacity': 1},
                    {'room_number': 'A102', 'room_type': 'double', 'price_per_night': 220, 'capacity': 2},
                    {'room_number': 'B201', 'room_type': 'suite',  'price_per_night': 450, 'capacity': 4},
                ]
            },
            {
                'name': 'Mountain View Lodge',
                'description': 'Cozy mountain lodge with breathtaking views and hiking trails.',
                'address': '789 Alpine Road', 'city': 'Denver', 'country': 'USA',
                'star_rating': 3, 'amenities': 'Hiking, Fireplace, WiFi, Restaurant',
                'rooms': [
                    {'room_number': '1', 'room_type': 'single', 'price_per_night': 80,  'capacity': 1},
                    {'room_number': '2', 'room_type': 'double', 'price_per_night': 140, 'capacity': 2},
                    {'room_number': '3', 'room_type': 'suite',  'price_per_night': 280, 'capacity': 4},
                ]
            },
        ]

        for h in hotels:
            rooms = h.pop('rooms')
            hotel, created = Hotel.objects.get_or_create(name=h['name'], defaults=h)
            if created:
                for r in rooms:
                    Room.objects.create(hotel=hotel, **r)
                self.stdout.write(self.style.SUCCESS(f'Created hotel: {hotel.name}'))
            else:
                self.stdout.write(f'Already exists: {hotel.name}')

        self.stdout.write(self.style.SUCCESS('\n=== Done! ==='))
        self.stdout.write('Admin: admin@stayease.com / Admin@123456')
        self.stdout.write('User:  user@stayease.com  / User@123456')
