from __future__ import annotations

import os
import streamlit as st
import numpy as np
import pydeck as pdk
import pandas as pd
from typing import List, Tuple

from data.coordinates import get_school_coordinates
from core.distance_manager import build_distance_matrix
from core.ant_algorithm import AntColonyOptimizer
from config import ACOConfig, DEFAULT_CONFIG
from visual.plotting import plot_convergence, plot_route


def create_route_map(
    route: List[int],
    school_names: List[str],
    coordinates: dict,
    distance: float,
) -> None:
    """
    Optimize edilmiş rotayı pydeck ile harita üzerinde görselleştirir.
    """
    # Rota koordinatlarını sırayla al
    route_coords = []
    for idx in route:
        school_name = school_names[idx]
        coords = coordinates[school_name]
        route_coords.append([coords["lng"], coords["lat"]])

    # Başlangıç noktasına geri dön (kapalı tur)
    route_coords.append(route_coords[0])

    # Harita için merkez noktası (Bursa'nın yaklaşık merkezi)
    center_lat = np.mean([c["lat"] for c in coordinates.values()])
    center_lng = np.mean([c["lng"] for c in coordinates.values()])

    # Rota çizgisi için veri
    route_df = pd.DataFrame(
        {
            "coordinates": [route_coords],
        }
    )

    # Okul noktaları için veri
    points_data = []
    for idx in route:
        school_name = school_names[idx]
        coords = coordinates[school_name]
        points_data.append(
            {
                "name": school_name,
                "lon": coords["lng"],
                "lat": coords["lat"],
                "order": route.index(idx) + 1,
            }
        )

    points_df = pd.DataFrame(points_data)

    # Harita katmanları
    route_layer = pdk.Layer(
        "PathLayer",
        route_df,
        get_path="coordinates",
        get_color=[255, 0, 0, 200],
        width_min_pixels=4,
        pickable=True,
    )

    points_layer = pdk.Layer(
        "ScatterplotLayer",
        points_df,
        get_position=["lon", "lat"],
        get_color=[0, 0, 255, 180],
        get_radius=80,  # daire boyutu küçültüldü
        pickable=True,
    )

    # Harita görünümü
    view_state = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lng,
        zoom=14,  # kampüs ölçeğinde daha yakın görünüm
        pitch=0,
    )

    deck = pdk.Deck(
        initial_view_state=view_state,
        layers=[route_layer, points_layer],
        map_provider="carto",  # Mapbox tokensuz çalışır
        map_style="dark",
        tooltip={"text": "{name}\nSıra: {order}"},  # type: ignore
    )

    st.pydeck_chart(deck)

    # Rota detayları
    st.subheader("📋 Rota Detayları")
    route_details = []
    for i, idx in enumerate(route):
        school_name = school_names[idx]
        route_details.append(f"{i+1}. {school_name}")
    route_details.append(f"{len(route)+1}. {school_names[route[0]]} (Başlangıç)")

    st.write("\n".join(route_details))
    st.metric("Toplam Mesafe", f"{distance:.2f} km")


def main() -> None:
    st.set_page_config(
        page_title="Kampüs Ring Otobüsü Rota Optimizasyonu",
        page_icon="🗺️",
        layout="wide",
    )

    st.title("🗺️ Üniversite Kampüsü Ring Otobüsü Rota Optimizasyonu")
    st.markdown(
        """
        Bu uygulama, **Karınca Kolonisi Algoritması (ACO)** kullanarak kampüs içindeki 10 durak
        (fakülteler, yurtlar, spor kompleksi vb.) arasında en kısa ve verimli ring otobüsü rotasını bulur.
        """
    )

    # Sidebar - Parametreler
    st.sidebar.header("⚙️ Algoritma Parametreleri")

    n_ants = st.sidebar.slider(
        "Karınca Sayısı",
        min_value=5,
        max_value=50,
        value=20,
        step=5,
        help="Her iterasyonda kaç karınca rota oluşturacak",
    )

    n_iterations = st.sidebar.slider(
        "İterasyon Sayısı",
        min_value=10,
        max_value=200,
        value=100,
        step=10,
        help="Algoritmanın kaç kez çalışacağı",
    )

    alpha = st.sidebar.slider(
        "Alpha (Feromon Etkisi)",
        min_value=0.1,
        max_value=3.0,
        value=1.0,
        step=0.1,
        help="Feromon izlerinin seçim üzerindeki etkisi",
    )

    beta = st.sidebar.slider(
        "Beta (Mesafe Etkisi)",
        min_value=1.0,
        max_value=10.0,
        value=5.0,
        step=0.5,
        help="Mesafenin seçim üzerindeki etkisi (yüksek değer kısa mesafeleri tercih eder)",
    )

    evaporation_rate = st.sidebar.slider(
        "Buharlaşma Oranı",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.05,
        help="Her iterasyonda feromonların ne kadarının buharlaşacağı",
    )

    # Grafik kaydetme seçeneği
    save_plots = st.sidebar.checkbox("Grafikleri Kaydet", value=False)

    # Optimize butonu
    if st.sidebar.button("🚀 Optimize Et", type="primary", use_container_width=True):
        with st.spinner("Mesafe matrisi hesaplanıyor..."):
            try:
                coordinates = get_school_coordinates()
                distance_matrix, school_names = build_distance_matrix(coordinates)
                st.success("✅ Mesafe matrisi Google Maps API ile gerçek sürüş mesafeleri kullanılarak oluşturuldu!")
            except Exception as e:
                st.error(f"❌ Hata: {str(e)}")
                st.stop()

        with st.spinner("Rota optimizasyonu yapılıyor..."):
            config = ACOConfig(
                n_ants=n_ants,
                n_iterations=n_iterations,
                alpha=alpha,
                beta=beta,
                evaporation_rate=evaporation_rate,
            )

            optimizer = AntColonyOptimizer(config)
            best_route, best_distance, history = optimizer.optimize(distance_matrix)

            # Sonuçları göster
            st.success("✅ Optimizasyon tamamlandı!")

            # Grafikleri kaydet
            if save_plots:
                os.makedirs("figure", exist_ok=True)
                plot_convergence(history, save_path="figure/convergence.png")
                plot_route(
                    best_route,
                    coordinates,
                    school_names,
                    best_distance,
                    save_path="figure/rota.png",
                )
                st.info("📁 Grafikler 'figure/' klasörüne kaydedildi!")

            # Harita görselleştirmesi
            st.subheader("🗺️ Optimize Edilmiş Rota Haritası")
            create_route_map(best_route, school_names, coordinates, best_distance)

            # İterasyon grafiği
            st.subheader("📊 İterasyon Bazlı Mesafe Değişimi")
            history_df = pd.DataFrame(
                {
                    "İterasyon": range(1, len(history) + 1),
                    "En İyi Mesafe (km)": history,
                }
            )
            st.line_chart(history_df.set_index("İterasyon"))

            # İstatistikler
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Toplam Mesafe", f"{best_distance:.2f} km")
            with col2:
                st.metric("Ortalama Mesafe", f"{np.mean(history):.2f} km")
            with col3:
                improvement = ((history[0] - history[-1]) / history[0] * 100) if history[0] > 0 else 0
                st.metric("İyileşme", f"{improvement:.2f}%")

            # Rota detay tablosu
            st.subheader("📋 Optimize Edilmiş Rota Detayları")
            route_rows = []
            for i, idx in enumerate(best_route):
                school_name = school_names[idx]
                coords = coordinates[school_name]
                route_rows.append(
                    {
                        "Sıra": i + 1,
                        "Okul": school_name,
                        "Enlem": coords["lat"],
                        "Boylam": coords["lng"],
                    }
                )
            route_rows.append(
                {
                    "Sıra": len(best_route) + 1,
                    "Okul": f"{school_names[best_route[0]]} (Başlangıç)",
                    "Enlem": coordinates[school_names[best_route[0]]]["lat"],
                    "Boylam": coordinates[school_names[best_route[0]]]["lng"],
                }
            )
            st.dataframe(pd.DataFrame(route_rows))

            # Mesafe matrisi gösterimi
            st.subheader("🧭 Okullar Arası Mesafe Matrisi (km)")
            safe_matrix = np.where(distance_matrix >= 1e8, np.nan, distance_matrix)
            matrix_df = pd.DataFrame(safe_matrix, columns=school_names, index=school_names)
            st.dataframe(matrix_df)

    # Bilgi bölümü
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        ### 📚 Hakkında
        Bu proje, Bursa Belediyesi'nin geri dönüşüm araçları için 
        rota optimizasyonu yapmak amacıyla geliştirilmiştir.
        
        **Algoritma:** Karınca Kolonisi Optimizasyonu (ACO)
        """
    )


if __name__ == "__main__":
    main()

