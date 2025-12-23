from __future__ import annotations

from typing import List, Tuple

import numpy as np

from config import ACOConfig


class AntColonyOptimizer:
    """
    Karınca Kolonisi Algoritması (ACO) ile TSP tabanlı rota optimizasyonu.

    Kullanım:
        from config import ACOConfig
        config = ACOConfig(n_ants=20, n_iterations=100)
        optimizer = AntColonyOptimizer(config)
        best_route, best_distance, history = optimizer.optimize(distance_matrix)
    """

    def __init__(self, config: ACOConfig) -> None:
        self.config = config
        if config.random_seed is not None:
            np.random.seed(config.random_seed)

    def _initialize_pheromones(self, n_cities: int) -> np.ndarray:
        # Başlangıçta tüm kenarlara küçük ve eşit feromon değeri veriyoruz.
        return np.ones((n_cities, n_cities), dtype=float)

    @staticmethod
    def _route_length(route: List[int], distance_matrix: np.ndarray) -> float:
        length = 0.0
        for i in range(len(route) - 1):
            length += distance_matrix[route[i], route[i + 1]]
        # Başlangıç noktasına geri dön (kapalı tur)
        length += distance_matrix[route[-1], route[0]]
        return length

    def _build_route(
        self,
        start_city: int,
        pheromones: np.ndarray,
        distance_matrix: np.ndarray,
    ) -> List[int]:
        n_cities = distance_matrix.shape[0]
        route = [start_city]
        unvisited = set(range(n_cities))
        unvisited.remove(start_city)

        alpha = self.config.alpha
        beta = self.config.beta

        while unvisited:
            current = route[-1]
            probs = []
            cities = list(unvisited)

            for j in cities:
                tau = pheromones[current, j] ** alpha
                # 1 / distance sezgisel bilgi (kısa mesafe daha cazip)
                eta = (1.0 / distance_matrix[current, j]) ** beta if distance_matrix[current, j] > 0 else 0.0
                probs.append(tau * eta)

            probs = np.array(probs, dtype=float)
            if probs.sum() == 0:
                # Sayısal olarak çökmemek için uniform seçim
                probs = np.ones_like(probs) / len(probs)
            else:
                probs = probs / probs.sum()

            next_city = np.random.choice(cities, p=probs)
            route.append(next_city)
            unvisited.remove(next_city)

        return route

    def optimize(
        self,
        distance_matrix: np.ndarray,
    ) -> Tuple[List[int], float, List[float]]:
        """
        Verilen mesafe matrisi için en iyi turu bulur.

        Args:
            distance_matrix: NxN boyutlu mesafe matrisi.

        Returns:
            best_route: Şehir indekslerinden oluşan en iyi tur.
            best_distance: En iyi turun toplam uzunluğu.
            history: Her iterasyondaki en iyi mesafe listesi.
        """
        n_cities = distance_matrix.shape[0]
        pheromones = self._initialize_pheromones(n_cities)

        best_route: List[int] | None = None
        best_distance = float("inf")
        history: List[float] = []

        for _ in range(self.config.n_iterations):
            all_routes: List[List[int]] = []
            all_lengths: List[float] = []

            # Her karınca için bir tur oluştur
            for k in range(self.config.n_ants):
                start_city = np.random.randint(0, n_cities)
                route = self._build_route(start_city, pheromones, distance_matrix)
                length = self._route_length(route, distance_matrix)
                all_routes.append(route)
                all_lengths.append(length)

                if length < best_distance:
                    best_distance = length
                    best_route = route

            # Feromon buharlaşması
            pheromones *= (1.0 - self.config.evaporation_rate)

            # Feromon takviyesi
            for route, length in zip(all_routes, all_lengths):
                delta_pheromone = self.config.q / length if length > 0 else 0.0
                for i in range(len(route) - 1):
                    a, b = route[i], route[i + 1]
                    pheromones[a, b] += delta_pheromone
                    pheromones[b, a] += delta_pheromone
                # Başlangıca dönüş kenarı
                a, b = route[-1], route[0]
                pheromones[a, b] += delta_pheromone
                pheromones[b, a] += delta_pheromone

            history.append(best_distance)

        assert best_route is not None
        return best_route, best_distance, history


