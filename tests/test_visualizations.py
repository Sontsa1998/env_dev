"""
Tests unitaires pour le module visualizations.py
"""

import pytest
import pandas as pd
from src.visualizations import VisualizationEngine


class TestVisualizationEngine:
    """Tests pour la classe VisualizationEngine."""
    
    @pytest.fixture
    def viz_engine(self):
        """Fixture pour créer une instance de VisualizationEngine."""
        return VisualizationEngine()
    
    @pytest.fixture
    def sample_kpi1_data(self):
        """Fixture pour les données du KPI 1."""
        return pd.DataFrame({
            'segment': ['C - Medium', 'JC - Medium', 'B - Compact'],
            'average_range_km': [500.0, 480.0, 320.0]
        })
    
    @pytest.fixture
    def sample_kpi2_data(self):
        """Fixture pour les données du KPI 2."""
        return pd.DataFrame({
            'brand': ['Tesla', 'BMW', 'Audi', 'Mercedes'],
            'average_acceleration_s': [5.1, 5.5, 5.2, 5.8]
        })
    
    @pytest.fixture
    def sample_kpi3_data(self):
        """Fixture pour les données du KPI 3."""
        return pd.DataFrame({
            'battery_capacity_kWh': [75.0, 81.5, 100.0, 60.0],
            'efficiency_wh_per_km': [150, 170, 180, 160],
            'segment': ['C - Medium', 'C - Medium', 'JC - Medium', 'B - Compact'],
            'brand': ['Tesla', 'BMW', 'Audi', 'Renault'],
            'model': ['Model 3', 'i4', 'e-tron', 'Zoe']
        })
    
    @pytest.fixture
    def sample_kpi4_data(self):
        """Fixture pour les données du KPI 4."""
        return pd.DataFrame({
            'car_body_type': ['Sedan', 'SUV', 'Hatchback'],
            'count': [50, 35, 15],
            'percentage': [50.0, 35.0, 15.0]
        })
    
    def test_render_kpi_1_range_by_segment(self, viz_engine, sample_kpi1_data):
        """Test la visualisation du KPI 1."""
        fig = viz_engine.render_kpi_1_range_by_segment(sample_kpi1_data)
        
        assert fig is not None
        assert fig.data is not None
        assert len(fig.data) > 0
    
    def test_render_kpi_1_empty_data(self, viz_engine):
        """Test la visualisation du KPI 1 avec données vides."""
        empty_df = pd.DataFrame(columns=['segment', 'average_range_km'])
        fig = viz_engine.render_kpi_1_range_by_segment(empty_df)
        
        assert fig is None
    
    def test_render_kpi_2_acceleration_by_brand(self, viz_engine, sample_kpi2_data):
        """Test la visualisation du KPI 2."""
        fig = viz_engine.render_kpi_2_acceleration_by_brand(sample_kpi2_data)
        
        assert fig is not None
        assert fig.data is not None
        assert len(fig.data) > 0
    
    def test_render_kpi_2_empty_data(self, viz_engine):
        """Test la visualisation du KPI 2 avec données vides."""
        empty_df = pd.DataFrame(columns=['brand', 'average_acceleration_s'])
        fig = viz_engine.render_kpi_2_acceleration_by_brand(empty_df)
        
        assert fig is None
    
    def test_render_kpi_2_more_than_15_brands(self, viz_engine):
        """Test la visualisation du KPI 2 avec plus de 15 marques."""
        data = pd.DataFrame({
            'brand': [f'Brand{i}' for i in range(20)],
            'average_acceleration_s': [5.0 + i*0.1 for i in range(20)]
        })
        
        fig = viz_engine.render_kpi_2_acceleration_by_brand(data)
        
        assert fig is not None
        # Vérifier que seules les 15 premières marques sont affichées
        assert len(fig.data[0].x) <= 15
    
    def test_render_kpi_3_battery_vs_efficiency(self, viz_engine, sample_kpi3_data):
        """Test la visualisation du KPI 3."""
        fig = viz_engine.render_kpi_3_battery_vs_efficiency(sample_kpi3_data)
        
        assert fig is not None
        assert fig.data is not None
        assert len(fig.data) > 0
    
    def test_render_kpi_3_empty_data(self, viz_engine):
        """Test la visualisation du KPI 3 avec données vides."""
        empty_df = pd.DataFrame(columns=['battery_capacity_kWh', 'efficiency_wh_per_km', 'segment'])
        fig = viz_engine.render_kpi_3_battery_vs_efficiency(empty_df)
        
        assert fig is None
    
    def test_render_kpi_4_distribution_by_body_type(self, viz_engine, sample_kpi4_data):
        """Test la visualisation du KPI 4."""
        fig = viz_engine.render_kpi_4_distribution_by_body_type(sample_kpi4_data)
        
        assert fig is not None
        assert fig.data is not None
        assert len(fig.data) > 0
    
    def test_render_kpi_4_empty_data(self, viz_engine):
        """Test la visualisation du KPI 4 avec données vides."""
        empty_df = pd.DataFrame(columns=['car_body_type', 'count', 'percentage'])
        fig = viz_engine.render_kpi_4_distribution_by_body_type(empty_df)
        
        assert fig is None
    
    def test_render_no_data_message(self, viz_engine):
        """Test le message d'absence de données."""
        message = viz_engine.render_no_data_message("KPI 1")
        
        assert "Aucune donnée" in message
        assert "KPI 1" in message
    
    def test_kpi_1_title(self, viz_engine, sample_kpi1_data):
        """Test que le titre du KPI 1 est correct."""
        fig = viz_engine.render_kpi_1_range_by_segment(sample_kpi1_data)
        
        assert "Plage moyenne par segment" in fig.layout.title.text
    
    def test_kpi_2_title(self, viz_engine, sample_kpi2_data):
        """Test que le titre du KPI 2 est correct."""
        fig = viz_engine.render_kpi_2_acceleration_by_brand(sample_kpi2_data)
        
        assert "Accélération moyenne par marque" in fig.layout.title.text
    
    def test_kpi_3_title(self, viz_engine, sample_kpi3_data):
        """Test que le titre du KPI 3 est correct."""
        fig = viz_engine.render_kpi_3_battery_vs_efficiency(sample_kpi3_data)
        
        assert "Capacité batterie vs Efficacité" in fig.layout.title.text
    
    def test_kpi_4_title(self, viz_engine, sample_kpi4_data):
        """Test que le titre du KPI 4 est correct."""
        fig = viz_engine.render_kpi_4_distribution_by_body_type(sample_kpi4_data)
        
        assert "Distribution des véhicules par type de carrosserie" in fig.layout.title.text
