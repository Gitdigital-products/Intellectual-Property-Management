from datetime import datetime, date
from sqlalchemy import Column, String, Integer, DateTime, Date, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class IPAsset(Base):
    """Base model for Intellectual Property assets"""
    __tablename__ = 'ip_assets'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    ip_type = Column(String(50), nullable=False)  # copyright, patent, trademark, etc.
    registration_number = Column(String(100), unique=True)
    status = Column(String(50), default='draft')
    
    # Dates
    creation_date = Column(Date, nullable=False)
    registration_date = Column(Date)
    expiration_date = Column(Date)
    
    # Ownership
    created_by = Column(String(200), nullable=False)
    owners = Column(JSON)  # List of owner information
    
    # Additional metadata
    jurisdiction = Column(String(10))  # Country code
    tags = Column(JSON)  # List of tags for categorization
    metadata = Column(JSON)  # Additional flexible data
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rights = relationship("IPRights", back_populates="asset")
    documents = relationship("IPDocument", back_populates="asset")
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'ip_type': self.ip_type,
            'registration_number': self.registration_number,
            'status': self.status,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None,
            'expiration_date': self.expiration_date.isoformat() if self.expiration_date else None,
            'created_by': self.created_by,
            'owners': self.owners,
            'jurisdiction': self.jurisdiction,
            'tags': self.tags,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class IPRights(Base):
    """Model for managing rights associated with IP assets"""
    __tablename__ = 'ip_rights'
    
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('ip_assets.id'), nullable=False)
    rights_type = Column(String(50), nullable=False)  # ownership, license, assignment, etc.
    holder = Column(String(200), nullable=False)  # Person or organization holding the right
    percentage = Column(Integer)  # Percentage of rights (for ownership)
    
    # Dates
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    
    # Terms and conditions
    terms = Column(Text)
    restrictions = Column(JSON)
    
    # Financial information
    royalty_rate = Column(String(50))  # e.g., "5%", "fixed amount"
    payment_terms = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    asset = relationship("IPAsset", back_populates="rights")
    
    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'rights_type': self.rights_type,
            'holder': self.holder,
            'percentage': self.percentage,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'terms': self.terms,
            'restrictions': self.restrictions,
            'royalty_rate': self.royalty_rate,
            'payment_terms': self.payment_terms,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class IPDocument(Base):
    """Model for storing documents related to IP assets"""
    __tablename__ = 'ip_documents'
    
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('ip_assets.id'), nullable=False)
    document_type = Column(String(100), nullable=False)  # registration, agreement, certificate, etc.
    file_name = Column(String(500), nullable=False)
    file_path = Column(String(1000))
    file_size = Column(Integer)
    mime_type = Column(String(100))
    
    # Document metadata
    title = Column(String(500))
    description = Column(Text)
    version = Column(String(50), default='1.0')
    
    created_by = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    asset = relationship("IPAsset", back_populates="documents")
    
    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'document_type': self.document_type,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'title': self.title,
            'description': self.description,
            'version': self.version,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat()
        }
