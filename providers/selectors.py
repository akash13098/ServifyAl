from .models import Provider
from .models import ProviderLocation
from .utils import calculate_distance

def get_verified_providers():
    return Provider.objects.filter(is_verified=True, is_available=True)


def get_nearby_providers(user_lat, user_lon, radius=5):
    providers = ProviderLocation.objects.select_related('provider').all()

    nearby = []

    for p in providers:
        dist = calculate_distance(user_lat, user_lon, p.latitude, p.longitude)

        if dist <= radius:
            nearby.append({
                "provider": p.provider,
                "distance": dist
            })

    return sorted(nearby, key=lambda x: x["distance"])

from .utils import calculate_provider_score

def get_ranked_providers(user_lat, user_lon, radius=5):

    providers = ProviderLocation.objects.select_related('provider').all()

    results = []

    for p in providers:
        dist = calculate_distance(user_lat, user_lon, p.latitude, p.longitude)

        if dist <= radius:
            score = calculate_provider_score(p.provider, dist)

            results.append({
                "provider": p.provider,
                "distance": dist,
                "score": score
            })

    return sorted(results, key=lambda x: x["score"], reverse=True)