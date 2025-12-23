from __future__ import annotations

from typing import Dict, Tuple


SchoolCoordinates = Dict[str, Dict[str, float]]


def get_school_coordinates() -> SchoolCoordinates:
    """
    Kampüs içindeki ring otobüsü duraklarının yaklaşık koordinatlarını döndürür.

    Not:
        Koordinatlar örnek bir üniversite kampüsü (temsili) için verilmiştir.
        Gerçek dünya uygulamasında bunları kendi kampüsünüzün koordinatlarıyla
        güncellemeniz tavsiye edilir.
    """
    return {
        "Mühendislik Fakültesi": {
            "lat": 40.2255,
            "lng": 28.8821,
        },
        "İktisadi ve İdari Bilimler Fakültesi": {
            "lat": 40.2238,
            "lng": 28.8854,
        },
        "Fen-Edebiyat Fakültesi": {
            "lat": 40.2221,
            "lng": 28.8802,
        },
        "Tıp Fakültesi": {
            "lat": 40.2203,
            "lng": 28.8879,
        },
        "Merkezi Kütüphane": {
            "lat": 40.2242,
            "lng": 28.8785,
        },
        "Öğrenci Yurdu A": {
            "lat": 40.2210,
            "lng": 28.8768,
        },
        "Öğrenci Yurdu B": {
            "lat": 40.2194,
            "lng": 28.8829,
        },
        "Spor Kompleksi": {
            "lat": 40.2178,
            "lng": 28.8796,
        },
        "Teknokent": {
            "lat": 40.2270,
            "lng": 28.8872,
        },
        "Rektörlük Binası": {
            "lat": 40.2230,
            "lng": 28.8830,
        },
    }


def get_school_names() -> Tuple[str, ...]:
    """Okul isimlerini sıralı bir demet (tuple) olarak döndürür."""
    coords = get_school_coordinates()
    return tuple(coords.keys())


