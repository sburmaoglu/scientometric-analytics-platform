"""
Configuration settings for Patent & Publication Analytics Platform
"""

# App Settings
APP_NAME = "Patent & Publication Analytics"
APP_VERSION = "1.0.0"
MAX_FILE_SIZE_MB = 200

# Data Source Settings
SUPPORTED_SOURCES = {
    'lens.org': {
        'name': 'Lens.org',
        'enabled': True,
        'file_format': 'csv'
    },
    # Future additions
    # 'scopus': {'name': 'Scopus', 'enabled': False},
    # 'wos': {'name': 'Web of Science', 'enabled': False},
}

# lens.org Expected Columns (flexible matching)
LENS_COLUMNS = {
    'required': [
        'title',  # Publication/Patent title
        'year',   # Publication year
    ],
    'optional': [
        'authors',
        'citation_count',
        'abstract',
        'keywords',
        'doi',
        'source_title',  # Journal/Conference name
        'patent_number',
        'applicant',
        'inventor',
        'publication_date',
        'filing_date',
        'grant_date',
        'classifications',
    ]
}

# Column name variations (for fuzzy matching)
COLUMN_ALIASES = {
    'title': ['title', 'publication_title', 'patent_title'],
    'year': ['year', 'publication_year', 'year_published'],
    'authors': ['authors', 'author', 'author_names'],
    'citations': ['citations', 'citation_count', 'cited_by_count', 'times_cited'],
    'abstract': ['abstract', 'description', 'summary'],
    'keywords': ['keywords', 'author_keywords', 'index_keywords'],
}

# Analytics Settings
BASIC_ANALYTICS = {
    'enabled': True,
    'features': [
        'publication_trends',
        'citation_statistics',
        'author_collaboration',
        'keyword_analysis',
        'temporal_analysis',
    ]
}

ADVANCED_ANALYTICS = {
    'enabled': True,
    'requires_subscription': True,
    'features': [
        'ai_insights',
        'predictive_analysis',
        'advanced_networks',
        'topic_modeling',
        'trend_forecasting',
    ]
}

# Subscription Tiers
SUBSCRIPTION_TIERS = {
    'free': {
        'name': 'Free',
        'max_records': 10000,
        'max_uploads_per_day': 10,
        'features': BASIC_ANALYTICS['features'],
    },
    'premium': {
        'name': 'Premium',
        'max_records': None,  # Unlimited
        'max_uploads_per_day': None,  # Unlimited
        'features': BASIC_ANALYTICS['features'] + ADVANCED_ANALYTICS['features'],
    }
}

# Visualization Settings
VIZ_CONFIG = {
    'color_scheme': 'plotly',
    'default_height': 500,
    'network_layout': 'spring',
}

# AI API Settings (for Phase 2)
AI_CONFIG = {
    'provider': 'anthropic',  # or 'openai'
    'model': 'claude-3-5-sonnet-20241022',
    'max_tokens': 4000,
    'temperature': 0.7,
}

# Export Settings
EXPORT_FORMATS = ['csv', 'excel', 'json']
