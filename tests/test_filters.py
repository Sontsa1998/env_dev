"""
Tests unitaires pour le module filters.py
"""

import pytest
from pathlib import Path
from src.database import DuckDBManager
from src.filters import FilterManager


@pytest.fixture
def db_manager():
    """Fixture pour créer une instance de DuckDBManager avec une BD de test."""
    db_path = "test_ev_database_filters.duckdb"
    manager = DuckDBManager(db_path)
    yield manager
    manager.close()
    if Path(db_path).exists():
        Path(db_path).unlink()


@pytest.fixture
def filter_manager(db_manager):
    """Fixture pour créer une instance de FilterManager."""
    return FilterManager(db_manager)


@pytest.fixture
def sample_csv(tmp_path):
    """Fixture pour créer un fichier CSV de test."""
    csv_content = """brand,model,top_speed_kmh,battery_capacity_kWh,battery_type,number_of_cells,torque_nm,efficiency_wh_per_km,range_km,acceleration_0_100_s,fast_charging_power_kw_dc,fast_charge_port,towing_capacity_kg,cargo_volume_l,seats,drivetrain,segment,length_mm,width_mm,height_mm,car_body_type,source_url
Tesla,Model 3,225,75.0,Lithium-ion,4680,450,150,500,5.1,170,CCS,0,425,5,RWD,C - Medium,4694,1849,1443,Sedan,https://example.com/tesla-model-3
Tesla,Model Y,225,75.0,Lithium-ion,4680,450,160,480,5.8,170,CCS,1600,425,5,RWD,JC - Medium,4751,1921,1624,SUV,https://example.com/tesla-model-y
BMW,i4,200,81.5,Lithium-ion,4680,400,170,450,5.5,200,CCS,0,495,5,RWD,C - Medium,4783,1852,1454,Sedan,https://example.com/bmw-i4
Audi,e-tron,200,100.0,Lithium-ion,4680,450,180,500,5.2,150,CCS,1800,660,5,AWD,JC - Medium,4901,1935,1616,SUV,https://example.com/audi-etron
"""
    csv_file = tmp_path / "test_vehicles.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)


class TestFilterManager:
    """Tests pour la classe FilterManager."""
    
    def test_initialization(self, filter_manager):
        """Test l'initialisation du gestionnaire de filtres."""
        assert filter_manager.db_manager is not None
    
    def test_get_available_filters_empty_db(self, filter_manager):
        """Test la récupération des filtres disponibles avec une BD vide."""
        filters = filter_manager.get_available_filters()
        
        assert 'brand' in filters
        assert 'segment' in filters
        assert 'car_body_type' in filters
        assert len(filters['brand']) == 0
    
    def test_get_available_filters_with_data(self, filter_manager, db_manager, sample_csv):
        """Test la récupération des filtres disponibles avec des données."""
        db_manager.load_csv(sample_csv)
        
        filters = filter_manager.get_available_filters()
        
        assert len(filters['brand']) > 0
        assert 'Tesla' in filters['brand']
        assert 'BMW' in filters['brand']
        assert 'Audi' in filters['brand']
    
    def test_apply_filters_empty(self, filter_manager):
        """Test l'application de filtres vides."""
        result = filter_manager.apply_filters({})
        assert result == {}
    
    def test_apply_filters_single_brand(self, filter_manager):
        """Test l'application d'un filtre sur une marque."""
        selected = {'brand': ['Tesla']}
        result = filter_manager.apply_filters(selected)
        
        assert result == {'brand': ['Tesla']}
    
    def test_apply_filters_multiple_values(self, filter_manager):
        """Test l'application de filtres avec plusieurs valeurs."""
        selected = {
            'brand': ['Tesla', 'BMW'],
            'car_body_type': ['SUV']
        }
        result = filter_manager.apply_filters(selected)
        
        assert result == selected
    
    def test_apply_filters_with_empty_lists(self, filter_manager):
        """Test l'application de filtres avec des listes vides."""
        selected = {
            'brand': ['Tesla'],
            'segment': [],
            'car_body_type': []
        }
        result = filter_manager.apply_filters(selected)
        
        # Les listes vides ne doivent pas être incluses
        assert 'brand' in result
        assert 'segment' not in result
        assert 'car_body_type' not in result
    
    def test_get_filter_summary_empty(self, filter_manager):
        """Test le résumé des filtres vides."""
        summary = filter_manager.get_filter_summary({})
        assert summary == "Aucun filtre appliqué"
    
    def test_get_filter_summary_single_filter(self, filter_manager):
        """Test le résumé avec un filtre."""
        filters = {'brand': ['Tesla']}
        summary = filter_manager.get_filter_summary(filters)
        
        assert 'brand' in summary
        assert 'Tesla' in summary
    
    def test_get_filter_summary_multiple_filters(self, filter_manager):
        """Test le résumé avec plusieurs filtres."""
        filters = {
            'brand': ['Tesla', 'BMW'],
            'car_body_type': ['SUV']
        }
        summary = filter_manager.get_filter_summary(filters)
        
        assert 'brand' in summary
        assert 'car_body_type' in summary
        assert 'Tesla' in summary or 'BMW' in summary
    
    def test_get_filter_summary_with_empty_lists(self, filter_manager):
        """Test le résumé avec des listes vides."""
        filters = {
            'brand': ['Tesla'],
            'segment': [],
            'car_body_type': []
        }
        summary = filter_manager.get_filter_summary(filters)
        
        assert 'brand' in summary
        assert 'Tesla' in summary
