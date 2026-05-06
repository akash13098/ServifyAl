import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius (km)

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

def calculate_provider_score(provider, distance):
    
    rating_score = provider.rating * 2
    experience_score = provider.experience_years * 0.5

    availability_score = 5 if provider.is_available else 0

    distance_score = max(0, 10 - distance)

    total_score = rating_score + experience_score + availability_score + distance_score

    return total_score