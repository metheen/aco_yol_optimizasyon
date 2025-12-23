"""
Mesafe matrisi için yardımcı fonksiyonlar.

Bu modül, mesafe matrisleri üzerinde çeşitli işlemler yapmak için
yardımcı fonksiyonlar sağlar.
"""

import numpy as np
from typing import List, Tuple


def validate_distance_matrix(matrix: np.ndarray) -> bool:
    """
    Mesafe matrisinin geçerli olup olmadığını kontrol eder.
    
    Args:
        matrix: Kontrol edilecek mesafe matrisi
    
    Returns:
        Matris geçerliyse True, değilse False
    """
    if matrix.shape[0] != matrix.shape[1]:
        return False
    
    if not np.allclose(matrix, matrix.T):
        # Simetrik olmalı (i->j ve j->i mesafeleri aynı olmalı)
        return False
    
    if not np.all(np.diag(matrix) == 0):
        # Diyagonal elemanlar 0 olmalı (bir noktadan kendisine mesafe 0)
        return False
    
    if np.any(matrix < 0):
        # Negatif mesafe olamaz
        return False
    
    return True


def calculate_route_distance(route: List[int], distance_matrix: np.ndarray) -> float:
    """
    Verilen bir rota için toplam mesafeyi hesaplar.
    
    Args:
        route: Şehir indekslerinden oluşan rota listesi
        distance_matrix: Mesafe matrisi
    
    Returns:
        Rotanın toplam mesafesi (kilometre)
    """
    if len(route) < 2:
        return 0.0
    
    total_distance = 0.0
    
    # Rota boyunca mesafeleri topla
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i], route[i + 1]]
    
    # Başlangıç noktasına geri dön (kapalı tur)
    total_distance += distance_matrix[route[-1], route[0]]
    
    return total_distance


def get_nearest_neighbors(
    city_index: int, distance_matrix: np.ndarray, k: int = 5
) -> List[Tuple[int, float]]:
    """
    Belirli bir şehre en yakın k şehri bulur.
    
    Args:
        city_index: Şehir indeksi
        distance_matrix: Mesafe matrisi
        k: Bulunacak en yakın şehir sayısı
    
    Returns:
        (şehir_indeksi, mesafe) çiftlerinden oluşan liste, mesafeye göre sıralı
    """
    distances = distance_matrix[city_index, :]
    
    # Kendisini hariç tut (mesafe 0)
    distances[city_index] = np.inf
    
    # En yakın k şehri bul
    nearest_indices = np.argsort(distances)[:k]
    
    neighbors = [
        (idx, distances[idx]) for idx in nearest_indices if distances[idx] != np.inf
    ]
    
    return neighbors


def normalize_distance_matrix(matrix: np.ndarray) -> np.ndarray:
    """
    Mesafe matrisini normalize eder (0-1 aralığına getirir).
    
    Args:
        matrix: Normalize edilecek mesafe matrisi
    
    Returns:
        Normalize edilmiş mesafe matrisi
    """
    max_distance = np.max(matrix)
    if max_distance == 0:
        return matrix
    
    normalized = matrix / max_distance
    return normalized


def get_matrix_statistics(matrix: np.ndarray) -> dict:
    """
    Mesafe matrisi için istatistikler hesaplar.
    
    Args:
        matrix: İstatistikleri hesaplanacak mesafe matrisi
    
    Returns:
        İstatistikleri içeren sözlük
    """
    # Diyagonal elemanları hariç tut
    mask = ~np.eye(matrix.shape[0], dtype=bool)
    distances = matrix[mask]
    
    stats = {
        "min": float(np.min(distances)),
        "max": float(np.max(distances)),
        "mean": float(np.mean(distances)),
        "median": float(np.median(distances)),
        "std": float(np.std(distances)),
    }
    
    return stats

