import math


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Haversine 공식을 사용하여 두 지점 간의 거리 (km)를 계산
    """
    R = 6371  # 지구의 반지름 (킬로미터)

    # 위도와 경도를 라디안으로 변환
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine 공식
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # 두 지점 사이의 거리 계산
    distance = R * c

    return distance
