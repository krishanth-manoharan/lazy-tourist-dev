"""Mock hotel data for testing"""

# Mock hotel data organized by destination
MOCK_HOTELS = {
    "PARIS": [
        {
            "name": "Hotel Le Marais Boutique",
            "stars": 4,
            "price_per_night": 180,
            "location": "Le Marais",
            "rating": 4.6,
            "reviews": 1247,
            "amenities": ["WiFi", "Breakfast", "Air Conditioning", "24h Reception"],
            "distance_to_center": "1.2 km",
            "image_url": "https://example.com/hotel1.jpg",
            "description": "Charming boutique hotel in the historic Marais district"
        },
        {
            "name": "Montparnasse Grand Hotel",
            "stars": 4,
            "price_per_night": 210,
            "location": "Montparnasse",
            "rating": 4.4,
            "reviews": 892,
            "amenities": ["WiFi", "Restaurant", "Bar", "Gym", "Parking"],
            "distance_to_center": "2.5 km",
            "image_url": "https://example.com/hotel2.jpg",
            "description": "Modern hotel near Montparnasse Tower with city views"
        },
        {
            "name": "Eiffel View Apartments",
            "stars": 3,
            "price_per_night": 150,
            "location": "Trocadéro",
            "rating": 4.8,
            "reviews": 543,
            "amenities": ["WiFi", "Kitchen", "Washing Machine", "Eiffel View"],
            "distance_to_center": "3.0 km",
            "image_url": "https://example.com/hotel3.jpg",
            "description": "Cozy apartments with stunning Eiffel Tower views"
        },
        {
            "name": "Luxury Palace Saint-Germain",
            "stars": 5,
            "price_per_night": 450,
            "location": "Saint-Germain-des-Prés",
            "rating": 4.9,
            "reviews": 2156,
            "amenities": ["WiFi", "Spa", "Pool", "Michelin Restaurant", "Concierge"],
            "distance_to_center": "0.8 km",
            "image_url": "https://example.com/hotel4.jpg",
            "description": "Five-star luxury in the heart of Paris"
        }
    ],
    "BALI": [
        {
            "name": "Ubud Forest Retreat",
            "stars": 4,
            "price_per_night": 120,
            "location": "Ubud",
            "rating": 4.7,
            "reviews": 834,
            "amenities": ["WiFi", "Pool", "Spa", "Yoga Classes", "Breakfast"],
            "distance_to_center": "5 km from Ubud center",
            "image_url": "https://example.com/bali1.jpg",
            "description": "Peaceful retreat surrounded by rice terraces"
        },
        {
            "name": "Seminyak Beach Resort",
            "stars": 5,
            "price_per_night": 280,
            "location": "Seminyak",
            "rating": 4.8,
            "reviews": 1521,
            "amenities": ["Beach Access", "Infinity Pool", "Spa", "3 Restaurants", "Butler Service"],
            "distance_to_center": "Beachfront",
            "image_url": "https://example.com/bali2.jpg",
            "description": "Luxury beachfront resort with world-class amenities"
        },
        {
            "name": "Canggu Surf Villa",
            "stars": 3,
            "price_per_night": 90,
            "location": "Canggu",
            "rating": 4.5,
            "reviews": 412,
            "amenities": ["WiFi", "Pool", "Surfboard Rental", "Breakfast", "Yoga"],
            "distance_to_center": "2 km to beach",
            "image_url": "https://example.com/bali3.jpg",
            "description": "Trendy villa perfect for surf enthusiasts"
        }
    ],
    "TOKYO": [
        {
            "name": "Shibuya Modern Hotel",
            "stars": 4,
            "price_per_night": 200,
            "location": "Shibuya",
            "rating": 4.6,
            "reviews": 1892,
            "amenities": ["WiFi", "Restaurant", "Bar", "City Views", "24h Reception"],
            "distance_to_center": "In Shibuya center",
            "image_url": "https://example.com/tokyo1.jpg",
            "description": "Contemporary hotel in the heart of Shibuya"
        },
        {
            "name": "Traditional Ryokan Asakusa",
            "stars": 3,
            "price_per_night": 180,
            "location": "Asakusa",
            "rating": 4.9,
            "reviews": 654,
            "amenities": ["Onsen", "Traditional Breakfast", "Tatami Rooms", "Tea Ceremony"],
            "distance_to_center": "1 km",
            "image_url": "https://example.com/tokyo2.jpg",
            "description": "Authentic Japanese ryokan experience"
        }
    ],
    "DEFAULT": [
        {
            "name": "City Center Hotel",
            "stars": 4,
            "price_per_night": 150,
            "location": "City Center",
            "rating": 4.5,
            "reviews": 500,
            "amenities": ["WiFi", "Breakfast", "Gym", "Restaurant"],
            "distance_to_center": "0.5 km",
            "image_url": "https://example.com/default.jpg",
            "description": "Comfortable hotel in convenient location"
        },
        {
            "name": "Budget Inn Downtown",
            "stars": 3,
            "price_per_night": 80,
            "location": "Downtown",
            "rating": 4.2,
            "reviews": 300,
            "amenities": ["WiFi", "24h Reception"],
            "distance_to_center": "1 km",
            "image_url": "https://example.com/default2.jpg",
            "description": "Affordable and clean accommodation"
        }
    ]
}

