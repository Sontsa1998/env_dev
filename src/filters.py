"""
Module de gestion des filtres.
Gère l'état des filtres et les options disponibles.
"""

from typing import Dict, List
from src.database import DuckDBManager


class FilterManager:
    """Gestionnaire des filtres pour l'application."""
    
    def __init__(self, db_manager: DuckDBManager):
        """
        Initialise le gestionnaire de filtres.
        
        Args:
            db_manager: Instance du gestionnaire de base de données
        """
        self.db_manager = db_manager
    
    def get_available_filters(self) -> Dict[str, List[str]]:
        """
        Récupère les options de filtres disponibles.
        
        Returns:
            Dictionnaire avec les options de filtres
        """
        return {
            'brand': self.db_manager.get_distinct_values('brand'),
            'segment': self.db_manager.get_distinct_values('segment'),
            'car_body_type': self.db_manager.get_distinct_values('car_body_type'),
        }
    
    def apply_filters(self, selected_filters: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Applique les filtres sélectionnés.
        
        Args:
            selected_filters: Dictionnaire des filtres sélectionnés
            
        Returns:
            Dictionnaire des filtres validés
        """
        # Valider que les filtres ne sont pas vides
        validated_filters = {}
        for key, values in selected_filters.items():
            if values:
                validated_filters[key] = values
        
        return validated_filters
    
    def get_filter_summary(self, filters: Dict[str, List[str]]) -> str:
        """
        Retourne un résumé lisible des filtres appliqués.
        
        Args:
            filters: Dictionnaire des filtres
            
        Returns:
            Résumé des filtres en texte
        """
        if not filters:
            return "Aucun filtre appliqué"
        
        summary_parts = []
        for key, values in filters.items():
            if values:
                summary_parts.append(f"{key}: {', '.join(values)}")
        
        return " | ".join(summary_parts) if summary_parts else "Aucun filtre appliqué"
