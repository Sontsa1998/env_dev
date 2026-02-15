"""
Application Streamlit principale pour le tableau de bord des véhicules électriques.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from src.database import DuckDBManager
from src.filters import FilterManager
from src.visualizations import VisualizationEngine
from typing import Dict



class DashboardApp:
    """Application principale du tableau de bord."""
    
    def __init__(self):
        """Initialise l'application et les composants."""
        self.db_manager = DuckDBManager("ev_database.duckdb")
        self.filter_manager = FilterManager(self.db_manager)
        self.viz_engine = VisualizationEngine()
        self._initialize_session_state()
    
    def _initialize_session_state(self) -> None:
        """Initialise l'état de session Streamlit."""
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        if 'record_count' not in st.session_state:
            st.session_state.record_count = 0
    
    def render_header(self) -> None:
        """Affiche l'en-tête de l'application."""
        st.set_page_config(
            page_title="EV Analytics Dashboard",
            page_icon="⚡",
            layout="wide"
        )
        
        st.title("⚡ Tableau de Bord Analytique des Véhicules Électriques")
        st.markdown("""
        Explorez les données des véhicules électriques avec des visualisations interactives.
        Filtrez par marque, segment et type de carrosserie pour analyser les performances.
        """)
    
    def render_file_upload_section(self) -> None:
        """Affiche la section de téléchargement de fichier."""
        st.subheader("📁 Charger les données")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Sélectionnez un fichier CSV",
                type=['csv'],
                help="Téléchargez le fichier electric_vehicles_spec_2025.csv"
            )
        
        with col2:
            if st.button("🔄 Charger les données", use_container_width=True):
                if uploaded_file is not None:
                    try:
                        # Sauvegarder le fichier temporaire
                        temp_path = "temp_upload.csv"
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Charger dans DuckDB
                        record_count = self.db_manager.load_csv(temp_path)
                        st.session_state.data_loaded = True
                        st.session_state.record_count = record_count
                        
                        if record_count > 0:
                            st.success(f"✅ {record_count} véhicules chargés avec succès!")
                        else:
                            st.warning("⚠️ Aucun véhicule valide trouvé dans le fichier. Vérifiez que les colonnes brand, model, segment et car_body_type ne sont pas vides.")
                        
                        # Nettoyer le fichier temporaire
                        Path(temp_path).unlink()
                    except Exception as e:
                        error_msg = str(e)
                        # Améliorer le message d'erreur
                        if "Conversion Error" in error_msg or "Could not convert" in error_msg:
                            st.error(f"❌ Erreur de format de données : {error_msg}\n\nVérifiez que toutes les colonnes numériques contiennent des nombres valides.")
                        elif "Constraint Error" in error_msg or "NOT NULL" in error_msg:
                            st.error(f"❌ Erreur de données manquantes : {error_msg}\n\nVérifiez que les colonnes brand, model, segment et car_body_type ne sont pas vides.")
                        else:
                            st.error(f"❌ Erreur lors du chargement: {error_msg}")
                else:
                    st.warning("⚠️ Veuillez sélectionner un fichier CSV")
        
        # Afficher le statut
        if st.session_state.data_loaded:
            record_count = self.db_manager.get_record_count()
            st.info(f"📊 Base de données: {record_count} véhicules disponibles")
    
    def render_filter_section(self) -> Dict[str, list]:
        """
        Affiche la section des filtres dans la barre latérale.
        
        Returns:
            Dictionnaire des filtres sélectionnés
        """
        st.sidebar.subheader("🔍 Filtres")
        
        filters = {}
        
        if st.session_state.data_loaded:
            available_filters = self.filter_manager.get_available_filters()
            
            # Filtre par marque
            selected_brands = st.sidebar.multiselect(
                "Marque",
                options=available_filters.get('brand', []),
                help="Sélectionnez une ou plusieurs marques"
            )
            if selected_brands:
                filters['brand'] = selected_brands
            
            # Filtre par segment
            selected_segments = st.sidebar.multiselect(
                "Segment",
                options=available_filters.get('segment', []),
                help="Sélectionnez un ou plusieurs segments"
            )
            if selected_segments:
                filters['segment'] = selected_segments
            
            # Filtre par type de carrosserie
            selected_body_types = st.sidebar.multiselect(
                "Type de carrosserie",
                options=available_filters.get('car_body_type', []),
                help="Sélectionnez un ou plusieurs types"
            )
            if selected_body_types:
                filters['car_body_type'] = selected_body_types
            
            # Afficher le résumé des filtres
            filter_summary = self.filter_manager.get_filter_summary(filters)
            st.sidebar.info(f"📌 {filter_summary}")
        else:
            st.sidebar.warning("⚠️ Chargez d'abord les données")
        
        return filters
    
    def render_kpi_grid(self, filters: Dict[str, list]) -> None:
        """
        Affiche la grille des 4 KPI.
        
        Args:
            filters: Dictionnaire des filtres appliqués
        """
        if not st.session_state.data_loaded:
            st.warning("⚠️ Veuillez charger les données pour voir les visualisations")
            return
        
        st.subheader("📊 Indicateurs Clés de Performance (KPI)")
        
        # Créer une grille 2x2
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        
        # KPI 1: Plage moyenne par segment
        with col1:
            st.markdown("### KPI 1: Plage par Segment")
            try:
                data = self.db_manager.calculate_kpi_1_range_by_segment(filters)
                if not data.empty:
                    fig = self.viz_engine.render_kpi_1_range_by_segment(data)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(self.viz_engine.render_no_data_message("KPI 1"))
            except Exception as e:
                st.error(f"Erreur KPI 1: {str(e)}")
        
        # KPI 2: Accélération moyenne par marque
        with col2:
            st.markdown("### KPI 2: Accélération par Marque")
            try:
                data = self.db_manager.calculate_kpi_2_acceleration_by_brand(filters)
                if not data.empty:
                    fig = self.viz_engine.render_kpi_2_acceleration_by_brand(data)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(self.viz_engine.render_no_data_message("KPI 2"))
            except Exception as e:
                st.error(f"Erreur KPI 2: {str(e)}")
        
        # KPI 3: Batterie vs Efficacité
        with col3:
            st.markdown("### KPI 3: Batterie vs Efficacité")
            try:
                data = self.db_manager.calculate_kpi_3_battery_vs_efficiency(filters)
                if not data.empty:
                    fig = self.viz_engine.render_kpi_3_battery_vs_efficiency(data)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(self.viz_engine.render_no_data_message("KPI 3"))
            except Exception as e:
                st.error(f"Erreur KPI 3: {str(e)}")
        
        # KPI 4: Distribution par type de carrosserie
        with col4:
            st.markdown("### KPI 4: Distribution par Type")
            try:
                data = self.db_manager.calculate_kpi_4_distribution_by_body_type(filters)
                if not data.empty:
                    fig = self.viz_engine.render_kpi_4_distribution_by_body_type(data)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(self.viz_engine.render_no_data_message("KPI 4"))
            except Exception as e:
                st.error(f"Erreur KPI 4: {str(e)}")
    
    def render_reset_button(self) -> None:
        """Affiche le bouton de réinitialisation."""
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🗑️ Effacer les données", use_container_width=True):
                self.db_manager.clear_all_data()
                st.session_state.data_loaded = False
                st.session_state.record_count = 0
                st.success("✅ Données effacées avec succès!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Actualiser", use_container_width=True):
                st.rerun()
    
    def run(self) -> None:
        """Lance l'application principale."""
        self.render_header()
        self.render_file_upload_section()
        
        filters = self.render_filter_section()
        self.render_kpi_grid(filters)
        
        st.divider()
        self.render_reset_button()
        
        # Pied de page
        st.markdown("""
        ---
        **Tableau de Bord Analytique des Véhicules Électriques** | 
        Données: electric_vehicles_spec_2025.csv | 
        Technologie: Streamlit + DuckDB + Plotly
        """)


def main():
    """Point d'entrée principal de l'application."""
    app = DashboardApp()
    app.run()


if __name__ == "__main__":
    main()
