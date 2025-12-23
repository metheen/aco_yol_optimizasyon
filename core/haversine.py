"""
Haversine formülü kullanarak iki koordinat arasındaki mesafeyi hesaplama.

Bu modül, dünya üzerindeki iki nokta arasındaki büyük daire mesafesini
(büyük daire üzerindeki en kısa mesafe) hesaplamak için Haversine formülünü kullanır.
"""

import math
from typing import Tuple

import numpy as np


def haversine_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    İki koordinat arasındaki Haversine mesafesini kilometre cinsinden hesaplar.
    
    Haversine formülü, küresel bir yüzey üzerindeki iki nokta arasındaki
    en kısa mesafeyi (büyük daire mesafesi) hesaplar.
    
    Args:
        lat1: İlk noktanın enlemi (derece, -90 ile 90 arası)
        lon1: İlk noktanın boylamı (derece, -180 ile 180 arası)
        lat2: İkinci noktanın enlemi (derece, -90 ile 90 arası)
        lon2: İkinci noktanın boylamı (derece, -180 ile 180 arası)
    
    Returns:
        İki nokta arasındaki mesafe (kilometre)
    
    Example:
        >>> distance = haversine_distance(40.1959, 29.0604, 40.1917, 29.0663)
        >>> print(f"Mesafe: {distance:.2f} km")
    """
    # Dünya yarıçapı (kilometre)
    R = 6371.0
    
    # Dereceyi radyana çevir
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Enlem ve boylam farkları
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formülü
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Mesafe
    distance = R * c
    return distance


def build_distance_matrix_haversine(
    coordinates: dict[str, dict[str, float]],
) -> Tuple[np.ndarray, list[str]]:
    """
    Koordinatlardan Haversine formülü ile mesafe matrisi oluşturur.
    
    Bu fonksiyon, verilen koordinatlar arasındaki tüm mesafeleri
    Haversine formülü kullanarak hesaplar ve bir mesafe matrisi döndürür.
    
    Args:
        coordinates: Okul adı -> {'lat': float, 'lng': float} sözlüğü.
    
    Returns:
        distance_matrix: NxN boyutlu, kilometre cinsinden mesafeleri içeren matris.
        school_names: Matrise karşılık gelen okul isimleri listesi.
    
    Example:
        >>> coords = {
        ...     "Okul1": {"lat": 40.1959, "lng": 29.0604},
        ...     "Okul2": {"lat": 40.1917, "lng": 29.0663}
        ... }
        >>> matrix, names = build_distance_matrix_haversine(coords)
    """
    school_names = list(coordinates.keys())
    n = len(school_names)
    matrix = np.zeros((n, n), dtype=float)
    
    locations = [
        (coords["lat"], coords["lng"]) for coords in coordinates.values()
    ]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i, j] = 0.0
            else:
                lat1, lon1 = locations[i]
                lat2, lon2 = locations[j]
                matrix[i, j] = haversine_distance(lat1, lon1, lat2, lon2)
    
    return matrix, school_names

