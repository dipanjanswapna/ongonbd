from src.models.user import db
from datetime import datetime

class Farmer(db.Model):
    __tablename__ = 'farmers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=True, nullable=False)
    farm_size_acres = db.Column(db.Numeric(8, 2))
    farming_experience_years = db.Column(db.Integer)
    primary_crops = db.Column(db.JSON)  # Array of crop names
    farming_methods = db.Column(db.JSON)  # organic, conventional, mixed
    land_ownership = db.Column(db.String(20))  # owned, leased, shared
    irrigation_access = db.Column(db.Boolean, default=False)
    equipment_owned = db.Column(db.JSON)  # Array of equipment
    annual_income = db.Column(db.Numeric(12, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='farmer_profile')
    farms = db.relationship('Farm', backref='farmer', cascade='all, delete-orphan')
    products = db.relationship('AgriculturalProduct', backref='farmer', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else None,
            'farm_size_acres': float(self.farm_size_acres) if self.farm_size_acres else None,
            'farming_experience_years': self.farming_experience_years,
            'primary_crops': self.primary_crops,
            'farming_methods': self.farming_methods,
            'land_ownership': self.land_ownership,
            'irrigation_access': self.irrigation_access,
            'equipment_owned': self.equipment_owned,
            'annual_income': float(self.annual_income) if self.annual_income else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Farm(db.Model):
    __tablename__ = 'farms'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    name = db.Column(db.String(255))
    location_address = db.Column(db.Text)
    location_coordinates = db.Column(db.String(100))  # "lat,lng" format
    total_area_acres = db.Column(db.Numeric(8, 2))
    soil_type = db.Column(db.String(50))
    water_source = db.Column(db.String(50))
    infrastructure = db.Column(db.JSON)  # Array of infrastructure items
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    crop_cycles = db.relationship('CropCycle', backref='farm', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farmer_name': self.farmer.user.full_name if self.farmer and self.farmer.user else None,
            'name': self.name,
            'location_address': self.location_address,
            'location_coordinates': self.location_coordinates,
            'total_area_acres': float(self.total_area_acres) if self.total_area_acres else None,
            'soil_type': self.soil_type,
            'water_source': self.water_source,
            'infrastructure': self.infrastructure,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Crop(db.Model):
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(150))
    category = db.Column(db.String(50))  # cereal, vegetable, fruit, cash_crop
    growing_season = db.Column(db.String(20))  # kharif, rabi, zaid
    maturity_days = db.Column(db.Integer)
    water_requirements = db.Column(db.String(20))  # low, medium, high
    soil_requirements = db.Column(db.Text)
    climate_requirements = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    crop_cycles = db.relationship('CropCycle', backref='crop')
    products = db.relationship('AgriculturalProduct', backref='crop')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'scientific_name': self.scientific_name,
            'category': self.category,
            'growing_season': self.growing_season,
            'maturity_days': self.maturity_days,
            'water_requirements': self.water_requirements,
            'soil_requirements': self.soil_requirements,
            'climate_requirements': self.climate_requirements,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CropCycle(db.Model):
    __tablename__ = 'crop_cycles'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'))
    area_planted_acres = db.Column(db.Numeric(8, 2))
    planting_date = db.Column(db.Date)
    expected_harvest_date = db.Column(db.Date)
    actual_harvest_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='planned')  # planned, planted, growing, harvested
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    yields = db.relationship('CropYield', backref='crop_cycle', cascade='all, delete-orphan')
    
    @property
    def is_completed(self):
        return self.status == 'harvested' and self.actual_harvest_date is not None
    
    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'farm_name': self.farm.name if self.farm else None,
            'crop_id': self.crop_id,
            'crop_name': self.crop.name if self.crop else None,
            'area_planted_acres': float(self.area_planted_acres) if self.area_planted_acres else None,
            'planting_date': self.planting_date.isoformat() if self.planting_date else None,
            'expected_harvest_date': self.expected_harvest_date.isoformat() if self.expected_harvest_date else None,
            'actual_harvest_date': self.actual_harvest_date.isoformat() if self.actual_harvest_date else None,
            'status': self.status,
            'is_completed': self.is_completed,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CropYield(db.Model):
    __tablename__ = 'crop_yields'
    
    id = db.Column(db.Integer, primary_key=True)
    crop_cycle_id = db.Column(db.Integer, db.ForeignKey('crop_cycles.id'), nullable=False)
    quantity_harvested = db.Column(db.Numeric(10, 2))
    unit = db.Column(db.String(20))  # kg, ton, quintal
    quality_grade = db.Column(db.String(20))
    market_price = db.Column(db.Numeric(8, 2))
    total_revenue = db.Column(db.Numeric(12, 2))
    production_cost = db.Column(db.Numeric(12, 2))
    profit = db.Column(db.Numeric(12, 2))
    harvest_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def profit_margin(self):
        if self.total_revenue and self.production_cost:
            return ((self.total_revenue - self.production_cost) / self.total_revenue) * 100
        return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'crop_cycle_id': self.crop_cycle_id,
            'quantity_harvested': float(self.quantity_harvested) if self.quantity_harvested else None,
            'unit': self.unit,
            'quality_grade': self.quality_grade,
            'market_price': float(self.market_price) if self.market_price else None,
            'total_revenue': float(self.total_revenue) if self.total_revenue else None,
            'production_cost': float(self.production_cost) if self.production_cost else None,
            'profit': float(self.profit) if self.profit else None,
            'profit_margin': self.profit_margin,
            'harvest_date': self.harvest_date.isoformat() if self.harvest_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True)
    location_coordinates = db.Column(db.String(100))  # "lat,lng" format
    date = db.Column(db.Date)
    temperature_min = db.Column(db.Numeric(4, 1))
    temperature_max = db.Column(db.Numeric(4, 1))
    humidity = db.Column(db.Numeric(5, 2))
    rainfall_mm = db.Column(db.Numeric(6, 2))
    wind_speed = db.Column(db.Numeric(5, 2))
    weather_condition = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'location_coordinates': self.location_coordinates,
            'date': self.date.isoformat() if self.date else None,
            'temperature_min': float(self.temperature_min) if self.temperature_min else None,
            'temperature_max': float(self.temperature_max) if self.temperature_max else None,
            'humidity': float(self.humidity) if self.humidity else None,
            'rainfall_mm': float(self.rainfall_mm) if self.rainfall_mm else None,
            'wind_speed': float(self.wind_speed) if self.wind_speed else None,
            'weather_condition': self.weather_condition,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AgriculturalAdvisory(db.Model):
    __tablename__ = 'agricultural_advisories'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    advisory_type = db.Column(db.String(50))  # weather, pest, disease, market
    target_crops = db.Column(db.JSON)  # Array of crop names
    target_regions = db.Column(db.JSON)  # Array of regions
    severity_level = db.Column(db.String(20))  # info, warning, alert
    valid_from = db.Column(db.Date)
    valid_until = db.Column(db.Date)
    issued_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    issuer = db.relationship('User', backref='issued_advisories')
    
    @property
    def is_active(self):
        today = datetime.utcnow().date()
        if self.valid_from and today < self.valid_from:
            return False
        if self.valid_until and today > self.valid_until:
            return False
        return True
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'advisory_type': self.advisory_type,
            'target_crops': self.target_crops,
            'target_regions': self.target_regions,
            'severity_level': self.severity_level,
            'valid_from': self.valid_from.isoformat() if self.valid_from else None,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'is_active': self.is_active,
            'issued_by': self.issued_by,
            'issuer_name': self.issuer.full_name if self.issuer else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AgriculturalProduct(db.Model):
    __tablename__ = 'agricultural_products'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    quantity_available = db.Column(db.Numeric(10, 2))
    unit = db.Column(db.String(20))
    price_per_unit = db.Column(db.Numeric(8, 2))
    quality_grade = db.Column(db.String(20))
    harvest_date = db.Column(db.Date)
    location_address = db.Column(db.Text)
    location_coordinates = db.Column(db.String(100))  # "lat,lng" format
    images = db.Column(db.JSON)  # Array of image URLs
    is_organic = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inquiries = db.relationship('ProductInquiry', backref='product', cascade='all, delete-orphan')
    
    @property
    def inquiry_count(self):
        return len(self.inquiries)
    
    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farmer_name': self.farmer.user.full_name if self.farmer and self.farmer.user else None,
            'crop_id': self.crop_id,
            'crop_name': self.crop.name if self.crop else None,
            'title': self.title,
            'description': self.description,
            'quantity_available': float(self.quantity_available) if self.quantity_available else None,
            'unit': self.unit,
            'price_per_unit': float(self.price_per_unit) if self.price_per_unit else None,
            'quality_grade': self.quality_grade,
            'harvest_date': self.harvest_date.isoformat() if self.harvest_date else None,
            'location_address': self.location_address,
            'location_coordinates': self.location_coordinates,
            'images': self.images,
            'is_organic': self.is_organic,
            'is_available': self.is_available,
            'inquiry_count': self.inquiry_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ProductInquiry(db.Model):
    __tablename__ = 'product_inquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('agricultural_products.id'), nullable=False)
    buyer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    quantity_requested = db.Column(db.Numeric(10, 2))
    offered_price = db.Column(db.Numeric(8, 2))
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    buyer = db.relationship('User', backref='product_inquiries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_title': self.product.title if self.product else None,
            'buyer_id': self.buyer_id,
            'buyer_name': self.buyer.full_name if self.buyer else None,
            'quantity_requested': float(self.quantity_requested) if self.quantity_requested else None,
            'offered_price': float(self.offered_price) if self.offered_price else None,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

