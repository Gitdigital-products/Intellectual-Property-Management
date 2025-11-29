from datetime import datetime, date
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from ..models.ip_assets import IPRights
from config.constants import RIGHTS_TYPES

class RightsManager:
    """System for managing IP rights and assignments"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def assign_rights(self, rights_data: Dict) -> IPRights:
        """Assign rights to an IP asset"""
        
        if rights_data.get('rights_type') not in RIGHTS_TYPES:
            raise ValueError(f"Invalid rights type. Must be one of: {RIGHTS_TYPES}")
        
        rights = IPRights(**rights_data)
        self.db.add(rights)
        self.db.commit()
        self.db.refresh(rights)
        
        return rights
    
    def update_rights(self, rights_id: int, update_data: Dict) -> IPRights:
        """Update existing rights"""
        rights = self.db.query(IPRights).filter(IPRights.id == rights_id).first()
        
        if not rights:
            raise ValueError(f"Rights with ID {rights_id} not found")
        
        for key, value in update_data.items():
            if hasattr(rights, key):
                setattr(rights, key, value)
        
        rights.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(rights)
        
        return rights
    
    def get_asset_rights(self, asset_id: int) -> List[IPRights]:
        """Get all rights for an IP asset"""
        return self.db.query(IPRights).filter(
            IPRights.asset_id == asset_id
        ).all()
    
    def get_rights_holders(self, asset_id: int) -> List[Dict]:
        """Get all rights holders for an asset"""
        rights = self.get_asset_rights(asset_id)
        
        holders = {}
        for right in rights:
            if right.holder not in holders:
                holders[right.holder] = {
                    'holder': right.holder,
                    'rights': [],
                    'total_percentage': 0
                }
            
            holders[right.holder]['rights'].append({
                'type': right.rights_type,
                'percentage': right.percentage,
                'start_date': right.start_date,
                'end_date': right.end_date
            })
            
            if right.percentage:
                holders[right.holder]['total_percentage'] += right.percentage
        
        return list(holders.values())
    
    def validate_ownership(self, asset_id: int) -> bool:
        """Validate that ownership percentages sum to 100%"""
        ownership_rights = self.db.query(IPRights).filter(
            and_(
                IPRights.asset_id == asset_id,
                IPRights.rights_type == 'ownership'
            )
        ).all()
        
        total_percentage = sum(
            right.percentage or 0 for right in ownership_rights
        )
        
        return total_percentage == 100
    
    def get_active_licenses(self, asset_id: int) -> List[IPRights]:
        """Get all active licenses for an asset"""
        today = date.today()
        
        return self.db.query(IPRights).filter(
            and_(
                IPRights.asset_id == asset_id,
                IPRights.rights_type == 'license',
                IPRights.start_date <= today,
                or_(
                    IPRights.end_date.is_(None),
                    IPRights.end_date >= today
                )
            )
        ).all()
