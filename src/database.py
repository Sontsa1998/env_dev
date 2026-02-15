"""
Module de gestion de la base de données DuckDB.
Gère la connexion, la création du schéma et les requêtes SQL.
"""

import duckdb
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any


class DuckDBManager:
    """Gestionnaire de base de données DuckDB pour les véhicules électriques."""
    
    def __init__(self, db_path: str = "ev_database.duckdb"):
        """
        Initialise la connexion à la base de données DuckDB.
        
        Args:
            db_path: Chemin vers le fichier de base de données
        """
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        self._create_schema()
    
    def _create_schema(self) -> None:
        """Crée le schéma de la table vehicle_data s'il n'existe pas."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS vehicle_data (
                brand VARCHAR,
                model VARCHAR,
                top_speed_kmh DECIMAL(6,2),
                battery_capacity_kWh DECIMAL(6,2),
                battery_type VARCHAR,
                number_of_cells INTEGER,
                torque_nm DECIMAL(8,2),
                efficiency_wh_per_km DECIMAL(6,2),
                range_km DECIMAL(8,2),
                acceleration_0_100_s DECIMAL(5,2),
                fast_charging_power_kw_dc DECIMAL(6,2),
                fast_charge_port VARCHAR,
                towing_capacity_kg DECIMAL(8,2),
                cargo_volume_l DECIMAL(8,2),
                seats INTEGER,
                drivetrain VARCHAR,
                segment VARCHAR,
                length_mm DECIMAL(8,2),
                width_mm DECIMAL(8,2),
                height_mm DECIMAL(8,2),
                car_body_type VARCHAR,
                source_url VARCHAR
            )
        """)
        
        # Créer les index pour les colonnes fréquemment interrogées
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_brand ON vehicle_data(brand)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_segment ON vehicle_data(segment)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_car_body_type ON vehicle_data(car_body_type)")
    
    def load_csv(self, csv_path: str) -> int:
        """
        Charge les données CSV dans la base de données.
        
        Args:
            csv_path: Chemin vers le fichier CSV
            
        Returns:
            Nombre de lignes insérées
        """
        df = pd.read_csv(csv_path)
        
        # Colonnes numériques à convertir
        numeric_columns = [
            'top_speed_kmh', 'battery_capacity_kWh', 'number_of_cells',
            'torque_nm', 'efficiency_wh_per_km', 'range_km',
            'acceleration_0_100_s', 'fast_charging_power_kw_dc',
            'towing_capacity_kg', 'cargo_volume_l', 'seats',
            'length_mm', 'width_mm', 'height_mm'
        ]
        
        # Convertir les colonnes numériques, remplacer les valeurs invalides par NaN
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Filtrer les lignes avec des valeurs manquantes dans les colonnes critiques
        # Garder les lignes où au moins brand, model et segment sont présents
        df = df.dropna(subset=['brand', 'model', 'segment', 'car_body_type'], how='any')
        
        # Insérer les données
        if len(df) > 0:
            self.conn.register('temp_df', df)
            self.conn.execute("""
                INSERT INTO vehicle_data 
                SELECT * FROM temp_df
            """)
        
        return len(df)
    
    def get_distinct_values(self, column: str) -> List[str]:
        """
        Récupère les valeurs distinctes d'une colonne.
        
        Args:
            column: Nom de la colonne
            
        Returns:
            Liste des valeurs distinctes
        """
        result = self.conn.execute(f"""
            SELECT DISTINCT {column} FROM vehicle_data 
            WHERE {column} IS NOT NULL
            ORDER BY {column}
        """).fetchall()
        
        return [row[0] for row in result]
    
    def query_with_filters(self, filters: Dict[str, List[str]]) -> pd.DataFrame:
        """
        Exécute une requête avec filtres appliqués.
        
        Args:
            filters: Dictionnaire des filtres {colonne: [valeurs]}
            
        Returns:
            DataFrame avec les résultats filtrés
        """
        query = "SELECT * FROM vehicle_data WHERE 1=1"
        
        for column, values in filters.items():
            if values:
                placeholders = ','.join([f"'{v}'" for v in values])
                query += f" AND {column} IN ({placeholders})"
        
        return self.conn.execute(query).df()
    
    def calculate_kpi_1_range_by_segment(self, filters: Dict[str, List[str]]) -> pd.DataFrame:
        """
        Calcule la plage moyenne par segment.
        
        Args:
            filters: Dictionnaire des filtres
            
        Returns:
            DataFrame avec segment et range_km moyen
        """
        df = self.query_with_filters(filters)
        
        if df.empty:
            return pd.DataFrame(columns=['segment', 'average_range_km'])
        
        result = df.groupby('segment')['range_km'].mean().reset_index()
        result.columns = ['segment', 'average_range_km']
        result = result.sort_values('average_range_km', ascending=False)
        
        return result
    
    def calculate_kpi_2_acceleration_by_brand(self, filters: Dict[str, List[str]]) -> pd.DataFrame:
        """
        Calcule l'accélération moyenne par marque.
        
        Args:
            filters: Dictionnaire des filtres
            
        Returns:
            DataFrame avec brand et acceleration_0_100_s moyen
        """
        df = self.query_with_filters(filters)
        
        if df.empty:
            return pd.DataFrame(columns=['brand', 'average_acceleration_s'])
        
        result = df.groupby('brand')['acceleration_0_100_s'].mean().reset_index()
        result.columns = ['brand', 'average_acceleration_s']
        result = result.sort_values('average_acceleration_s')
        
        return result
    
    def calculate_kpi_3_battery_vs_efficiency(self, filters: Dict[str, List[str]]) -> pd.DataFrame:
        """
        Récupère les données batterie vs efficacité.
        
        Args:
            filters: Dictionnaire des filtres
            
        Returns:
            DataFrame avec battery_capacity_kWh, efficiency_wh_per_km et segment
        """
        df = self.query_with_filters(filters)
        
        if df.empty:
            return pd.DataFrame(columns=['battery_capacity_kWh', 'efficiency_wh_per_km', 'segment'])
        
        result = df[['battery_capacity_kWh', 'efficiency_wh_per_km', 'segment', 'brand', 'model']].dropna()
        
        return result
    
    def calculate_kpi_4_distribution_by_body_type(self, filters: Dict[str, List[str]]) -> pd.DataFrame:
        """
        Calcule la distribution des véhicules par type de carrosserie.
        
        Args:
            filters: Dictionnaire des filtres
            
        Returns:
            DataFrame avec car_body_type, count et percentage
        """
        df = self.query_with_filters(filters)
        
        if df.empty:
            return pd.DataFrame(columns=['car_body_type', 'count', 'percentage'])
        
        result = df['car_body_type'].value_counts().reset_index()
        result.columns = ['car_body_type', 'count']
        result['percentage'] = (result['count'] / result['count'].sum() * 100).round(2)
        result = result.sort_values('count', ascending=False)
        
        return result
    
    def clear_all_data(self) -> None:
        """Supprime toutes les données de la table."""
        self.conn.execute("DELETE FROM vehicle_data")
    
    def get_record_count(self) -> int:
        """Retourne le nombre total de véhicules dans la base de données."""
        result = self.conn.execute("SELECT COUNT(*) FROM vehicle_data").fetchone()
        return result[0] if result else 0
    
    def close(self) -> None:
        """Ferme la connexion à la base de données."""
        self.conn.close()
