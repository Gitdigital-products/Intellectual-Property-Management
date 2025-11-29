"""Constants for IP Management System"""

# IP Types
IP_TYPE_COPYRIGHT = "copyright"
IP_TYPE_PATENT = "patent"
IP_TYPE_TRADEMARK = "trademark"
IP_TYPE_TRADE_SECRET = "trade_secret"
IP_TYPE_DESIGN = "design_patent"

IP_TYPES = [
    IP_TYPE_COPYRIGHT,
    IP_TYPE_PATENT,
    IP_TYPE_TRADEMARK,
    IP_TYPE_TRADE_SECRET,
    IP_TYPE_DESIGN
]

# IP Status
STATUS_DRAFT = "draft"
STATUS_PENDING = "pending"
STATUS_REGISTERED = "registered"
STATUS_EXPIRED = "expired"
STATUS_RENEWED = "renewed"
STATUS_ABANDONED = "abandoned"

IP_STATUSES = [
    STATUS_DRAFT,
    STATUS_PENDING,
    STATUS_REGISTERED,
    STATUS_EXPIRED,
    STATUS_RENEWED,
    STATUS_ABANDONED
]

# Rights Types
RIGHT_OWNERSHIP = "ownership"
RIGHT_LICENSE = "license"
RIGHT_ASSIGNMENT = "assignment"
RIGHT_MORTGAGE = "mortgage"

RIGHTS_TYPES = [
    RIGHT_OWNERSHIP,
    RIGHT_LICENSE,
    RIGHT_ASSIGNMENT,
    RIGHT_MORTGAGE
]

# Countries (sample)
COUNTRIES = {
    "US": "United States",
    "GB": "United Kingdom",
    "DE": "Germany",
    "FR": "France",
    "JP": "Japan",
    "CN": "China",
    "IN": "India"
}
