from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
from dotenv import load_dotenv
import googlemaps
import os


def _load_api_key() -> str:
    """
    Ortam değişkenlerinden Google Maps API anahtarını yükler.
    
    Returns:
        API anahtarı
    
    Raises:
        RuntimeError: API anahtarı bulunamazsa
    """
    load_dotenv()
    api_key = os.getenv("Maps_API_KEY") or os.getenv("MAPS_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Google Maps API anahtarı bulunamadı. "
            "Lütfen .env dosyanıza `Maps_API_KEY=YOUR_KEY_HERE` satırını ekleyin. "
            "Google Cloud Console'da billing'in aktif olduğundan emin olun: "
            "https://console.cloud.google.com/project/_/billing/enable"
        )
    return api_key


def build_distance_matrix(
    coordinates: Dict[str, Dict[str, float]],
) -> Tuple[np.ndarray, List[str]]:
    """
    Google Maps Distance Matrix API kullanarak gerçek sürüş mesafelerini hesaplar.
    
    Sadece Google Maps API kullanılır. API key yoksa veya hata varsa exception fırlatılır.
    
    Not: Google Maps API'nin MAX_ELEMENTS_EXCEEDED hatasını önlemek için,
    matris parçalara bölünerek birden fazla API çağrısı yapılır.
    (Maksimum 100 element per request limiti nedeniyle)

    Args:
        coordinates: Okul adı -> {'lat': float, 'lng': float} sözlüğü.

    Returns:
        distance_matrix: NxN boyutlu, kilometre cinsinden mesafeleri içeren matris.
        school_names: Matrise karşılık gelen okul isimleri listesi.

    Raises:
        RuntimeError: API anahtarı yoksa veya API çağrısı başarısız olursa
    """
    api_key = _load_api_key()
    
    try:
        client = googlemaps.Client(key=api_key)

        school_names = list(coordinates.keys())
        locations = [
            (coords["lat"], coords["lng"]) for coords in coordinates.values()
        ]
        
        n = len(school_names)
        matrix = np.zeros((n, n), dtype=float)
        
        # Google Maps API limiti: maksimum 100 element per request
        # 12x12 = 144 element olduğu için parçalara bölmemiz gerekiyor
        # Her 8 origin için bir çağrı yapalım (8x12 = 96 element < 100)
        batch_size = 8
        
        print(f"🔄 Mesafe matrisi oluşturuluyor ({n}x{n} = {n*n} element)...")
        print(f"   API limiti nedeniyle {((n + batch_size - 1) // batch_size)} parça halinde çağrı yapılıyor...")
        
        # Matrisi parçalara bölerek API çağrıları yap
        for start_idx in range(0, n, batch_size):
            end_idx = min(start_idx + batch_size, n)
            origins_batch = locations[start_idx:end_idx]
            
            # Her batch için tüm destination'ları kullan
            response = client.distance_matrix(
                origins=origins_batch,
                destinations=locations,  # Tüm destination'lar
                mode="driving",
                units="metric",
                region="tr",
            )
            
            rows = response.get("rows", [])
            if len(rows) != (end_idx - start_idx):
                raise RuntimeError(f"Distance Matrix API beklenmeyen bir cevap döndürdü. Beklenen {end_idx - start_idx} satır, alınan {len(rows)} satır.")
            
            # Matrisi doldur
            for batch_row_idx, row in enumerate(rows):
                i = start_idx + batch_row_idx
                elements = row.get("elements", [])
                if len(elements) != n:
                    raise RuntimeError(
                        f"Distance Matrix API satır sayısı ile sütun sayısı uyumsuz. "
                        f"Satır {i}: beklenen {n} element, alınan {len(elements)} element."
                    )
                
                for j, element in enumerate(elements):
                    status = element.get("status")
                    if status != "OK":
                        # Erişilemeyen konumlar için çok büyük bir mesafe
                        matrix[i, j] = 1e9
                    else:
                        # metre -> kilometre
                        distance_meters = element["distance"]["value"]
                        matrix[i, j] = distance_meters / 1000.0
            
            print(f"   ✅ {start_idx+1}-{end_idx}. satırlar tamamlandı ({end_idx - start_idx}x{n} = {(end_idx - start_idx)*n} element)")

        # Diyagonal elemanlar 0 olmalı (okuldan okula mesafe)
        np.fill_diagonal(matrix, 0.0)
        
        print(f"✅ Mesafe matrisi başarıyla oluşturuldu!")

        return matrix, school_names
        
    except googlemaps.exceptions.ApiError as e:
        error_msg = str(e)
        if "REQUEST_DENIED" in error_msg or "billing" in error_msg.lower():
            raise RuntimeError(
                f"Google Maps API hatası: {error_msg}\n\n"
                f"Lütfen Google Cloud Console'da billing'i aktifleştirin: "
                f"https://console.cloud.google.com/project/_/billing/enable"
            )
        else:
            raise RuntimeError(f"Google Maps API hatası: {error_msg}")
    except Exception as e:
        raise RuntimeError(
            f"Google Maps API çağrısı başarısız oldu: {str(e)}\n\n"
            f"Lütfen API anahtarınızın doğru olduğundan ve billing'in aktif olduğundan emin olun."
        )


