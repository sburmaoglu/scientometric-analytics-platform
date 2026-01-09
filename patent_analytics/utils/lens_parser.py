"""
Lens.org Data Parser and Preprocessor

Handles both publication and patent data from lens.org exports.
Automatically detects data type and maps columns appropriately.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

# Lens.org column mapping for publications
PUBLICATION_COLUMN_MAP = {
    'authors': [
        'Authors', 'Author', 'authors', 'author',
        'Author(s)', 'Authors (Full Names)', 'Full Author Name'
    ],
    'title': [
        'Title', 'title', 'Publication Title', 'Document Title'
    ],
    'year': [
        'Year Published', 'Publication Year', 'Year', 'year',
        'Date Published', 'Publication Date'
    ],
    'citations': [
        'Citing Works Count', 'Times Cited', 'Citation Count',
        'Cited by Count', 'citations', 'Times Cited (All Databases)'
    ],
    'keywords': [
        'Keywords', 'Author Keywords', 'keywords', 'Index Keywords',
        'Subject', 'Subjects', 'MeSH Terms', 'Fields of Study'
    ],
    'abstract': [
        'Abstract', 'abstract', 'Summary', 'Description'
    ],
    'doi': [
        'DOI', 'doi', 'Digital Object Identifier'
    ],
    'source': [
        'Source Title', 'Journal', 'Publication Name', 'Conference',
        'Source', 'Venue', 'Book Title'
    ],
    'lens_id': [
        'Lens ID', 'lens_id', 'ID'
    ]
}

# Lens.org column mapping for patents
PATENT_COLUMN_MAP = {
    'inventors': [
        'Inventors', 'Inventor', 'inventors', 'inventor',
        'Inventor(s)', 'Inventor Names'
    ],
    'applicants': [
        'Applicants', 'Applicant', 'applicants', 'applicant',
        'Assignee', 'Assignees', 'Owner', 'Patent Holder'
    ],
    'title': [
        'Title', 'title', 'Patent Title', 'Invention Title'
    ],
    'year': [
        'Publication Year', 'Year Published', 'Year', 'year',
        'Grant Date', 'Filing Year'
    ],
    'citations': [
        'Citing Patents Count', 'Forward Citations', 'Times Cited',
        'Citation Count', 'Cited by Count'
    ],
    'keywords': [
        'Title', 'title', 'Abstract', 'Claims',  # Patents often use title/abstract as keywords
        'IPC Classifications', 'CPC Classifications'
    ],
    'abstract': [
        'Abstract', 'abstract', 'Summary', 'Description', 'Claims'
    ],
    'patent_number': [
        'Publication Number', 'Patent Number', 'Application Number',
        'patent_number', 'Pub Number', 'Publication No'
    ],
    'jurisdiction': [
        'Jurisdiction', 'Country', 'jurisdiction', 'Publication Country'
    ],
    'filing_date': [
        'Filing Date', 'Application Date', 'filing_date', 'Priority Date'
    ],
    'grant_date': [
        'Grant Date', 'Publication Date', 'Issue Date', 'grant_date'
    ],
    'lens_id': [
        'Lens ID', 'lens_id', 'ID'
    ],
    'classifications': [
        'IPC Classifications', 'CPC Classifications', 'Classifications',
        'Technology Field', 'IPC', 'CPC'
    ]
}


def detect_data_type(df: pd.DataFrame) -> Tuple[str, float]:
    """
    Detect if data is publication or patent data
    
    Returns:
        Tuple of (data_type, confidence)
        data_type: 'publication' or 'patent'
        confidence: float between 0 and 1
    """
    columns_lower = [col.lower() for col in df.columns]
    
    # Patent indicators
    patent_keywords = [
        'inventor', 'applicant', 'assignee', 'patent', 'filing', 'grant',
        'jurisdiction', 'ipc', 'cpc', 'claims', 'publication number'
    ]
    
    # Publication indicators
    publication_keywords = [
        'author', 'journal', 'doi', 'issn', 'volume', 'issue', 
        'conference', 'publisher', 'cited by', 'source title'
    ]
    
    patent_score = sum(1 for keyword in patent_keywords 
                       if any(keyword in col for col in columns_lower))
    
    pub_score = sum(1 for keyword in publication_keywords 
                    if any(keyword in col for col in columns_lower))
    
    # Check for specific lens.org identifiers
    has_lens_id = any('lens' in col and 'id' in col for col in columns_lower)
    
    total_indicators = len(patent_keywords) + len(publication_keywords)
    
    if patent_score > pub_score:
        confidence = (patent_score / len(patent_keywords))
        if has_lens_id:
            confidence = min(confidence + 0.2, 1.0)
        return 'patent', confidence
    else:
        confidence = (pub_score / len(publication_keywords))
        if has_lens_id:
            confidence = min(confidence + 0.2, 1.0)
        return 'publication', confidence


def find_column(df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
    """
    Find a column in the dataframe that matches one of the possible names
    
    Returns:
        Column name if found, None otherwise
    """
    df_columns_lower = {col.lower(): col for col in df.columns}
    
    for name in possible_names:
        if name.lower() in df_columns_lower:
            return df_columns_lower[name.lower()]
    
    return None


def parse_authors_inventors(series: pd.Series, separator: str = ';') -> pd.Series:
    """
    Parse author/inventor strings into clean, separated lists
    
    Handles various formats:
    - "Author A; Author B; Author C"
    - "Author A, Author B, Author C"
    - "Author A|Author B|Author C"
    """
    def clean_names(text):
        if pd.isna(text):
            return ''
        
        # Convert to string
        text = str(text)
        
        # Try different separators
        if ';' in text:
            names = text.split(';')
        elif '|' in text:
            names = text.split('|')
        elif ',' in text and text.count(',') > 2:  # Multiple commas suggest separation
            names = text.split(',')
        else:
            return text.strip()
        
        # Clean each name
        names = [name.strip() for name in names if name.strip()]
        
        # Join with semicolon for consistency
        return '; '.join(names)
    
    return series.apply(clean_names)


def extract_keywords_from_text(df: pd.DataFrame, text_columns: List[str], 
                                max_keywords: int = 50) -> pd.Series:
    """
    Extract keywords from text columns when no keyword field exists
    Uses simple frequency-based extraction
    """
    from collections import Counter
    import re
    
    # Common stop words to exclude
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
        'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'only'
    }
    
    keywords_list = []
    
    for idx, row in df.iterrows():
        word_counts = Counter()
        
        # Collect text from all specified columns
        for col in text_columns:
            if col in df.columns and pd.notna(row[col]):
                text = str(row[col]).lower()
                # Extract words (alphanumeric, length >= 3)
                words = re.findall(r'\b[a-z]{3,}\b', text)
                # Filter stop words
                words = [w for w in words if w not in stop_words]
                word_counts.update(words)
        
        # Get top keywords
        top_keywords = [word for word, count in word_counts.most_common(10)]
        keywords_list.append('; '.join(top_keywords) if top_keywords else '')
    
    return pd.Series(keywords_list, index=df.index)


def preprocess_lens_data(df: pd.DataFrame, data_type: str = None) -> Tuple[pd.DataFrame, Dict]:
    """
    Preprocess lens.org data with intelligent column mapping
    
    Args:
        df: Raw dataframe from lens.org
        data_type: 'publication' or 'patent' (auto-detected if None)
    
    Returns:
        Tuple of (processed_df, metadata_dict)
    """
    # Auto-detect if not specified
    if data_type is None:
        data_type, confidence = detect_data_type(df)
    else:
        confidence = 1.0
    
    # Select appropriate column map
    column_map = PUBLICATION_COLUMN_MAP if data_type == 'publication' else PATENT_COLUMN_MAP
    
    # Create standardized dataframe
    processed_df = df.copy()
    metadata = {
        'data_type': data_type,
        'detection_confidence': confidence,
        'original_columns': list(df.columns),
        'mapped_columns': {},
        'generated_columns': []
    }
    
    # Map standard columns
    for standard_name, possible_names in column_map.items():
        found_col = find_column(df, possible_names)
        if found_col:
            # Create standardized column name
            if standard_name == 'inventors' and data_type == 'patent':
                processed_df['Authors'] = parse_authors_inventors(df[found_col])
                metadata['mapped_columns']['Authors'] = found_col
            elif standard_name == 'applicants' and data_type == 'patent':
                processed_df['Applicants'] = parse_authors_inventors(df[found_col])
                metadata['mapped_columns']['Applicants'] = found_col
            elif standard_name == 'authors' and data_type == 'publication':
                processed_df['Authors'] = parse_authors_inventors(df[found_col])
                metadata['mapped_columns']['Authors'] = found_col
            elif standard_name == 'title':
                processed_df['Title'] = df[found_col]
                metadata['mapped_columns']['Title'] = found_col
            elif standard_name == 'year':
                # Handle various date formats
                processed_df['Year'] = pd.to_datetime(df[found_col], errors='coerce').dt.year
                metadata['mapped_columns']['Year'] = found_col
            elif standard_name == 'citations':
                # Convert to numeric
                processed_df['Citations'] = pd.to_numeric(df[found_col], errors='coerce').fillna(0)
                metadata['mapped_columns']['Citations'] = found_col
            elif standard_name == 'keywords':
                processed_df['Keywords'] = df[found_col]
                metadata['mapped_columns']['Keywords'] = found_col
            elif standard_name == 'abstract':
                processed_df['Abstract'] = df[found_col]
                metadata['mapped_columns']['Abstract'] = found_col
    
    # Generate Authors column for patents if inventors were found
    if data_type == 'patent' and 'Authors' not in processed_df.columns:
        # Try to use inventors as authors
        inventor_col = find_column(df, PATENT_COLUMN_MAP['inventors'])
        if inventor_col:
            processed_df['Authors'] = parse_authors_inventors(df[inventor_col])
            metadata['generated_columns'].append('Authors (from Inventors)')
    
    # Generate Keywords if not present
    if 'Keywords' not in processed_df.columns:
        # Try to extract from title and abstract
        text_cols = []
        if 'Title' in processed_df.columns:
            text_cols.append('Title')
        if 'Abstract' in processed_df.columns:
            text_cols.append('Abstract')
        
        if text_cols:
            processed_df['Keywords'] = extract_keywords_from_text(df, text_cols)
            metadata['generated_columns'].append('Keywords (extracted from text)')
    
    # Add data type column
    processed_df['Data_Type'] = data_type
    
    return processed_df, metadata


def validate_lens_format(df: pd.DataFrame) -> Tuple[bool, str, float]:
    """
    Validate if dataframe is from lens.org
    
    Returns:
        Tuple of (is_valid, data_type, confidence)
    """
    if len(df) == 0:
        return False, None, 0.0
    
    # Check for lens.org specific indicators
    columns_lower = [col.lower() for col in df.columns]
    
    # Strong indicators
    has_lens_id = any('lens' in col and 'id' in col for col in columns_lower)
    
    # Detect data type
    data_type, confidence = detect_data_type(df)
    
    # Validation rules
    min_columns = 5  # Lens.org exports typically have many columns
    min_confidence = 0.3  # At least 30% match
    
    is_valid = (
        len(df.columns) >= min_columns and
        (confidence >= min_confidence or has_lens_id)
    )
    
    return is_valid, data_type, confidence


def get_available_fields(df: pd.DataFrame, data_type: str) -> Dict[str, bool]:
    """
    Check which standard fields are available in the dataset
    
    Returns:
        Dictionary with field names and availability status
    """
    column_map = PUBLICATION_COLUMN_MAP if data_type == 'publication' else PATENT_COLUMN_MAP
    
    available = {}
    for field, possible_names in column_map.items():
        found = find_column(df, possible_names)
        available[field] = found is not None
    
    return available
