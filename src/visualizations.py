"""
Module de visualisations des données avec Plotly.
Crée les quatre KPI visualisations.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional


class VisualizationEngine:
    """Moteur de visualisation pour les KPI."""
    
    @staticmethod
    def render_kpi_1_range_by_segment(data: pd.DataFrame) -> Optional[go.Figure]:
        """
        Crée un graphique en barres : Plage moyenne par segment.
        
        Args:
            data: DataFrame avec segment et average_range_km
            
        Returns:
            Figure Plotly ou None si données vides
        """
        if data.empty:
            return None
        
        fig = px.bar(
            data,
            x='segment',
            y='average_range_km',
            title='Plage moyenne par segment (km)',
            labels={'segment': 'Segment', 'average_range_km': 'Plage moyenne (km)'},
            color='average_range_km',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            hovermode='x unified',
            height=400,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def render_kpi_2_acceleration_by_brand(data: pd.DataFrame) -> Optional[go.Figure]:
        """
        Crée un graphique en barres : Accélération moyenne par marque.
        
        Args:
            data: DataFrame avec brand et average_acceleration_s
            
        Returns:
            Figure Plotly ou None si données vides
        """
        if data.empty:
            return None
        
        # Limiter à top 15 marques pour la lisibilité
        data = data.head(15)
        
        fig = px.bar(
            data,
            x='brand',
            y='average_acceleration_s',
            title='Accélération moyenne par marque (0-100 km/h)',
            labels={'brand': 'Marque', 'average_acceleration_s': 'Accélération (s)'},
            color='average_acceleration_s',
            color_continuous_scale='RdYlGn_r'
        )
        
        fig.update_layout(
            hovermode='x unified',
            height=400,
            xaxis_tickangle=-45,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def render_kpi_3_battery_vs_efficiency(data: pd.DataFrame) -> Optional[go.Figure]:
        """
        Crée un graphique de dispersion : Capacité batterie vs efficacité.
        
        Args:
            data: DataFrame avec battery_capacity_kWh, efficiency_wh_per_km et segment
            
        Returns:
            Figure Plotly ou None si données vides
        """
        if data.empty:
            return None
        
        fig = px.scatter(
            data,
            x='battery_capacity_kWh',
            y='efficiency_wh_per_km',
            color='segment',
            hover_data=['brand', 'model'],
            title='Capacité batterie vs Efficacité énergétique',
            labels={
                'battery_capacity_kWh': 'Capacité batterie (kWh)',
                'efficiency_wh_per_km': 'Efficacité (Wh/km)',
                'segment': 'Segment'
            }
        )
        
        fig.update_layout(
            hovermode='closest',
            height=400
        )
        
        return fig
    
    @staticmethod
    def render_kpi_4_distribution_by_body_type(data: pd.DataFrame) -> Optional[go.Figure]:
        """
        Crée un graphique en camembert : Distribution par type de carrosserie.
        
        Args:
            data: DataFrame avec car_body_type, count et percentage
            
        Returns:
            Figure Plotly ou None si données vides
        """
        if data.empty:
            return None
        
        fig = px.pie(
            data,
            values='count',
            names='car_body_type',
            title='Distribution des véhicules par type de carrosserie',
            labels={'car_body_type': 'Type de carrosserie', 'count': 'Nombre'},
            hover_data={'percentage': ':.2f'}
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='label+percent'
        )
        
        fig.update_layout(height=400)
        
        return fig
    
    @staticmethod
    def render_no_data_message(kpi_name: str) -> str:
        """
        Retourne un message quand aucune donnée n'est disponible.
        
        Args:
            kpi_name: Nom du KPI
            
        Returns:
            Message d'erreur
        """
        return f"❌ Aucune donnée disponible pour {kpi_name}"
