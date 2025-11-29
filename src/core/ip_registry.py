from datetime import datetime, date
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..models.ip_assets import IPAsset, IPRights, IPDocument
from config.constants import IP_TYPES, IP_STATUSES, COUNTRIES

class IPRegistry:
    """Core system for IP asset registration and management"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def register_asset(self, asset_data: Dict) -> IPAsset:
        """Register a new IP asset"""
        
        # Validate IP type
        if asset_data.get('ip_type') not in IP_TYPES:
            raise ValueError(f"Invalid IP type. Must be one of: {IP_TYPES}")
        
        # Generate registration number if not provided
        if not asset_data.get('registration_number'):
            asset_data['registration_number'] = self._generate_registration_number(
                asset_data['ip_type']
            )
        
        # Create asset
        asset = IPAsset(**asset_data)
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        
        return asset
    
    def update_asset(self, asset_id: int, update_data: Dict) -> IPAsset:
        """Update an existing IP asset"""
        asset = self.db.query(IPAsset).filter(IPAsset.id == asset_id).first()
        
        if not asset:
            raise ValueError(f"IP asset with ID {asset_id} not found")
        
        for key, value in update_data.items():
            if hasattr(asset, key):
                setattr(asset, key, value)
        
        asset.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(asset)
        
        return asset
    
    def get_asset(self, asset_id: int) -> Optional[IPAsset]:
        """Get IP asset by ID"""
        return self.db.query(IPAsset).filter(IPAsset.id == asset_id).first()
    
    def search_assets(self, filters: Dict) -> List[IPAsset]:
        """Search IP assets with filters"""
        query = self.db.query(IPAsset)
        
        if 'ip_type' in filters:
            query = query.filter(IPAsset.ip_type == filters['ip_type'])
        
        if 'status' in filters:
            query = query.filter(IPAsset.status == filters['status'])
        
        if 'jurisdiction' in filters:
            query = query.filter(IPAsset.jurisdiction == filters['jurisdiction'])
        
        if 'created_by' in filters:
            query = query.filter(IPAsset.created_by == filters['created_by'])
        
        if 'tags' in filters:
            query = query.filter(IPAsset.tags.contains(filters['tags']))
        
        if 'search_text' in filters:
            search_text = f"%{filters['search_text']}%"
            query = query.filter(
                or_(
                    IPAsset.title.ilike(search_text),
                    IPAsset.description.ilike(search_text),
                    IPAsset.registration_number.ilike(search_text)
                )
            )
        
        return query.all()
    
    def get_expiring_assets(self, days_threshold: int = 30) -> List[IPAsset]:
        """Get assets expiring within the specified number of days"""
        threshold_date = date.today() + timedelta(days=days_threshold)
        
        return self.db.query(IPAsset).filter(
            and_(
                IPAsset.expiration_date.isnot(None),
                IPAsset.expiration_date <= threshold_date,
                IPAsset.expiration_date >= date.today(),
                IPAsset.status == 'registered'
            )
        ).all()
    
    def _generate_registration_number(self, ip_type: str) -> str:
        """Generate a unique registration number"""
        prefix = {
            'copyright': 'COPY',
            'patent': 'PAT',
            'trademark': 'TM',
            'trade_secret': 'TS',
            'design_patent': 'DES'
        }.get(ip_type, 'IP')
        
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return f"{prefix}-{timestamp}"
    
    def add_document(self, asset_id: int, document_data: Dict) -> IPDocument:
        """Add a document to an IP asset"""
        asset = self.get_asset(asset_id)
        if not asset:
            raise ValueError(f"IP asset with ID {asset_id} not found")
        
        document = IPDocument(asset_id=asset_id, **document_data)
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        return document
    
    def get_asset_documents(self, asset_id: int) -> List[IPDocument]:
        """Get all documents for an IP asset"""
        return self.db.query(IPDocument).filter(
            IPDocument.asset_id == asset_id
        ).all()
