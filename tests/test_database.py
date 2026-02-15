"""
Tests unitaires pour le module database.py
"""

import pytest
import pandas as pd
import os
from pathlib import Path
from src.database import DuckDBManager


@pytest.fixture
def db_manager():
    """Fixture pour créer une instance de DuckDBManager avec une BD de test."""
    db_path = "test_ev_database.duckdb"
    manager = DuckDBManager(db_path)
    yield manager
    manager.close()
    # Nettoyer le fichier de test
    if Path(db_path).exists():
        Path(db_path).unlink()


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


class TestDuckDBManager:
    """Tests pour la classe DuckDBManager."""
    
    def test_initialization(self, db_manager):
        """Test l'initialisation du gestionnaire de base de données."""
        assert db_manager.db_path == "test_ev_database.duckdb"
        assert db_manager.conn is not None
    
    def test_create_schema(self, db_manager):
        """Test la création du schéma."""
        # Vérifier que la table existe
        result = db_manager.conn.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = 'vehicle_data'
        """).fetchone()
        assert result[0] == 1
    
    def test_load_csv(self, db_manager, sample_csv):
        """Test le chargement d'un fichier CSV."""
        record_count = db_manager.load_csv(sample_csv)
        assert record_count == 4
        
        # Vérifier que les données sont bien chargées
        total = db_manager.get_record_count()
        assert total == 4
    
    def test_get_distinct_values(self, db_manager, sample_csv):
        """Test la récupération des valeurs distinctes."""
        db_manager.load_csv(sample_csv)
        
        brands = db_manager.get_distinct_values('brand')
        assert len(brands) == 3
        assert 'Tesla' in brands
        assert 'BMW' in brands
        assert 'Audi' in brands
    
    def test_query_with_filters_no_filters(self, db_manager, sample_csv):
        """Test la requête sans filtres."""
        db_manager.load_csv(sample_csv)
        
        result = db_manager.query_with_filters({})
        assert len(result) == 4
    
    def test_query_with_filters_single_brand(self, db_manager, sample_csv):
        """Test la requête avec un filtre sur la marque."""
        db_manager.load_csv(sample_csv)
        
        result = db_manager.query_with_filters({'brand': ['Tesla']})
        assert len(result) == 2
        assert all(result['brand'] == 'Tesla')
    
    def test_query_with_filters_multiple_brands(self, db_manager, sample_csv):
        """Test la requête avec plusieurs marques."""
        db_manager.load_csv(sample_csv)
        
        result = db_manager.query_with_filters({'brand': ['Tesla', 'BMW']})
        assert len(result) == 3
    
    def test_query_with_filters_body_type(self, db_manager, sample_csv):
        """Test la requête avec filtre sur le type de carrosserie."""
        db_manager.load_csv(sample_csv)
        
        result = db_manager.query_with_filters({'car_body_type': ['SUV']})
        assert len(result) == 2
        assert all(result['car_body_type'] == 'SUV')
    
    def test_calculate_kpi_1_range_by_segment(self, db_manager, sample_csv):
        """Test le calcul du KPI 1 (plage par segment)."""
        db_manager.load_csv(sample_csv)
        
        result = db_manager.calculate_kpi_1_range_by_segment({})
        assert not result.empty
        assert 'segment' in result.columns
        assert 'average_range_km' in result.columns
        assert len(result) > 0
    
    def test_calculate_kpi_1_with_filters(self, db_manager, sample_csv):
        """Test le calcul du KPI 1 avec filtres."""
        db_manager.load_csv(sample_csv)
        
        result = db_manager.calculate_kpi_1_range_by_segment({'brand': ['Tesla']})
        assert not result.empty
    
    def test_calculate_kpi_2_acceleration_by_brand(self, db_manager, sample_csv):
        """Test le calcul du KPI 2 (accélération par marque)."""
        db_manager.load_csv(sample_csv)
        
        result = db_manager.calculate_kpi_2_acceleration_by_brand({})
        assert not result.empty
        assert 'brand' in result.columns
        assert 'average_acceleration_s' in result.columns
    
    def test_calculate_kpi_3_battery_vs_efficiency(self, db_manager, sample_csv):
        """Test le calcul du KPI 3 (batterie vs efficacité)."""
        db_manager.load_csv(sample_csv)
        
        result = db_manager.calculate_kpi_3_battery_vs_efficiency({})
        assert not result.empty
        assert 'battery_capacity_kWh' in result.columns
        assert 'efficiency_wh_per_km' in result.columns
        assert 'segment' in result.columns
    
    def test_calculate_kpi_4_distribution_by_body_type(self, db_manager, sample_csv):
        """Test le calcul du KPI 4 (distribution par type)."""
        db_manager.load_csv(sample_csv)
        
        result = db_manager.calculate_kpi_4_distribution_by_body_type({})
        assert not result.empty
        assert 'car_body_type' in result.columns
        assert 'count' in result.columns
        assert 'percentage' in result.columns
        
        # Vérifier que les pourcentages totalisent 100%
        total_percentage = result['percentage'].sum()
        assert abs(total_percentage - 100.0) < 0.01
    
    def test_clear_all_data(self, db_manager, sample_csv):
        """Test la suppression de toutes les données."""
        db_manager.load_csv(sample_csv)
        assert db_manager.get_record_count() == 4
        
        db_manager.clear_all_data()
        assert db_manager.get_record_count() == 0
    
    def test_get_record_count(self, db_manager, sample_csv):
        """Test le comptage des enregistrements."""
        assert db_manager.get_record_count() == 0
        
        db_manager.load_csv(sample_csv)
        assert db_manager.get_record_count() == 4
    
    def test_empty_query_result(self, db_manager, sample_csv):
        """Test une requête qui ne retourne aucun résultat."""
        db_manager.load_csv(sample_csv)
        
        result = db_manager.query_with_filters({'brand': ['NonExistent']})
        assert result.empty
    
    def test_kpi_with_empty_result(self, db_manager, sample_csv):
        """Test les KPI avec des résultats vides."""
        db_manager.load_csv(sample_csv)
        
        # Filtre qui ne retourne rien
        result = db_manager.calculate_kpi_1_range_by_segment({'brand': ['NonExistent']})
        assert result.empty
