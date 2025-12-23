"""
ACO (Ant Colony Optimization) parametre ayarları.

Bu modül, Karınca Kolonisi Algoritması için kullanılan tüm parametreleri
merkezi bir yerden yönetmeyi sağlar.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ACOConfig:
    """
    Ant Colony Optimization algoritması için yapılandırma sınıfı.
    
    Attributes:
        n_ants: Her iterasyonda kullanılacak karınca sayısı
        n_iterations: Algoritmanın çalışacağı iterasyon sayısı
        alpha: Feromon izlerinin seçim üzerindeki etkisi (ne kadar yüksek, o kadar güçlü)
        beta: Mesafenin (sezgisel bilgi) seçim üzerindeki etkisi (ne kadar yüksek, kısa mesafe o kadar cazip)
        evaporation_rate: Her iterasyonda feromonların ne kadarının buharlaşacağı (0-1 arası)
        q: Feromon güncelleme sabiti (ne kadar yüksek, o kadar fazla feromon bırakılır)
        random_seed: Rastgele sayı üreteci için seed değeri (tekrarlanabilirlik için)
    """
    n_ants: int = 20
    n_iterations: int = 100
    alpha: float = 1.0
    beta: float = 5.0
    evaporation_rate: float = 0.5
    q: float = 100.0
    random_seed: Optional[int] = None

    def to_dict(self) -> dict:
        """Yapılandırmayı sözlük olarak döndürür."""
        return {
            "n_ants": self.n_ants,
            "n_iterations": self.n_iterations,
            "alpha": self.alpha,
            "beta": self.beta,
            "evaporation_rate": self.evaporation_rate,
            "q": self.q,
            "random_seed": self.random_seed,
        }

    @classmethod
    def from_dict(cls, config_dict: dict) -> "ACOConfig":
        """Sözlükten yapılandırma oluşturur."""
        return cls(**config_dict)


# Varsayılan yapılandırma
DEFAULT_CONFIG = ACOConfig()

