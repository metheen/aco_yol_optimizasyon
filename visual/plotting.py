"""
Yol ve yakınsama grafikleri için görselleştirme fonksiyonları.

Bu modül, optimize edilmiş rotaları ve algoritmanın yakınsama
sürecini görselleştirmek için fonksiyonlar sağlar.
"""

import os
from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch


def plot_convergence(
    history: List[float],
    save_path: Optional[str] = None,
    title: str = "ACO Algoritması Yakınsama Grafiği",
) -> None:
    """
    Algoritmanın yakınsama sürecini görselleştirir.
    
    Args:
        history: Her iterasyondaki en iyi mesafe listesi
        save_path: Grafiği kaydetmek için dosya yolu (opsiyonel)
        title: Grafik başlığı
    """
    plt.figure(figsize=(12, 6))
    
    iterations = range(1, len(history) + 1)
    
    plt.plot(iterations, history, linewidth=2, color="#2E86AB", label="En İyi Mesafe")
    plt.fill_between(iterations, history, alpha=0.3, color="#2E86AB")
    
    # En iyi değeri işaretle
    best_idx = np.argmin(history)
    best_value = history[best_idx]
    plt.scatter(
        [best_idx + 1],
        [best_value],
        color="#A23B72",
        s=200,
        zorder=5,
        label=f"En İyi: {best_value:.2f} km",
    )
    
    plt.xlabel("İterasyon", fontsize=12, fontweight="bold")
    plt.ylabel("Mesafe (km)", fontsize=12, fontweight="bold")
    plt.title(title, fontsize=14, fontweight="bold", pad=20)
    plt.grid(True, alpha=0.3, linestyle="--")
    plt.legend(loc="best", fontsize=10)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Yakınsama grafiği kaydedildi: {save_path}")
    
    plt.close()


def plot_route(
    route: List[int],
    coordinates: dict,
    school_names: List[str],
    distance: float,
    save_path: Optional[str] = None,
    title: str = "Optimize Edilmiş Rota",
) -> None:
    """
    Optimize edilmiş rotayı 2D harita üzerinde görselleştirir.
    
    Args:
        route: Şehir indekslerinden oluşan rota listesi
        coordinates: Okul adı -> {'lat': float, 'lng': float} sözlüğü
        school_names: Okul isimleri listesi
        distance: Rotanın toplam mesafesi
        save_path: Grafiği kaydetmek için dosya yolu (opsiyonel)
        title: Grafik başlığı
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Rota koordinatlarını al
    route_coords = []
    route_labels = []
    for idx in route:
        school_name = school_names[idx]
        coords = coordinates[school_name]
        route_coords.append([coords["lng"], coords["lat"]])
        route_labels.append(school_name)
    
    # Başlangıç noktasına geri dön (kapalı tur)
    route_coords.append(route_coords[0])
    
    route_coords = np.array(route_coords)
    
    # Rota çizgisini çiz
    ax.plot(
        route_coords[:, 0],
        route_coords[:, 1],
        "o-",
        linewidth=3,
        markersize=12,
        color="#E63946",
        markerfacecolor="#F1FAEE",
        markeredgewidth=2,
        markeredgecolor="#E63946",
        label="Rota",
        zorder=2,
    )
    
    # Okulları numaralandır
    for i, (idx, school_name) in enumerate(zip(route, route_labels)):
        coords = coordinates[school_name]
        ax.annotate(
            f"{i+1}",
            xy=(coords["lng"], coords["lat"]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=10,
            fontweight="bold",
            color="white",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#E63946", alpha=0.8),
            zorder=3,
        )
    
    # Başlangıç noktasını özel işaretle
    start_coords = coordinates[route_labels[0]]
    ax.scatter(
        [start_coords["lng"]],
        [start_coords["lat"]],
        s=300,
        color="#06FF00",
        marker="*",
        edgecolors="black",
        linewidths=2,
        zorder=4,
        label="Başlangıç",
    )
    
    ax.set_xlabel("Boylam (Longitude)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Enlem (Latitude)", fontsize=12, fontweight="bold")
    ax.set_title(
        f"{title}\nToplam Mesafe: {distance:.2f} km",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(loc="best", fontsize=10)
    
    # Eksenleri eşit ölçekle (coğrafi görünüm için)
    ax.set_aspect("equal", adjustable="box")
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Rota grafiği kaydedildi: {save_path}")
    
    plt.close()


def plot_route_comparison(
    routes: List[List[int]],
    route_names: List[str],
    coordinates: dict,
    school_names: List[str],
    distances: List[float],
    save_path: Optional[str] = None,
) -> None:
    """
    Birden fazla rotayı karşılaştırmalı olarak görselleştirir.
    
    Args:
        routes: Karşılaştırılacak rotalar listesi
        route_names: Her rota için isim listesi
        coordinates: Okul koordinatları
        school_names: Okul isimleri
        distances: Her rotanın mesafesi
        save_path: Grafiği kaydetmek için dosya yolu (opsiyonel)
    """
    fig, axes = plt.subplots(1, len(routes), figsize=(6 * len(routes), 6))
    
    if len(routes) == 1:
        axes = [axes]
    
    colors = ["#E63946", "#2A9D8F", "#F77F00", "#7209B7"]
    
    for ax, route, name, distance, color in zip(
        axes, routes, route_names, distances, colors[: len(routes)]
    ):
        route_coords = []
        for idx in route:
            school_name = school_names[idx]
            coords = coordinates[school_name]
            route_coords.append([coords["lng"], coords["lat"]])
        
        route_coords.append(route_coords[0])
        route_coords = np.array(route_coords)
        
        ax.plot(
            route_coords[:, 0],
            route_coords[:, 1],
            "o-",
            linewidth=2,
            markersize=8,
            color=color,
            markerfacecolor="white",
            markeredgewidth=2,
        )
        
        ax.set_title(f"{name}\n{distance:.2f} km", fontweight="bold")
        ax.grid(True, alpha=0.3)
        ax.set_aspect("equal", adjustable="box")
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    
    plt.close()

