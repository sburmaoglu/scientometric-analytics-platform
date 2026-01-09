import streamlit as st
import pandas as pd
from pathlib import Path

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="Patent & Publication Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-container {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'data_uploaded' not in st.session_state:
        st.session_state.data_uploaded = False
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'file_name' not in st.session_state:
        st.session_state.file_name = None
    if 'data_source' not in st.session_state:
        st.session_state.data_source = None  # 'lens.org' or None
    if 'data_type' not in st.session_state:
        st.session_state.data_type = None  # 'publication' or 'patent'

def main():
    load_css()
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">📊 Patent & Publication Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Transform your research data into actionable insights</div>', unsafe_allow_html=True)
    
    # Copyright and attribution
    st.markdown("""
    <div style='text-align: center; padding: 0.5rem; font-size: 0.85rem; color: #666;'>
        © 2024-2026 <strong>Prof. Dr. Serhat Burmaoglu</strong> | 
        <a href='https://scholar.google.com/citations?user=HTleNI8AAAAJ&hl=en&oi=ao' target='_blank'>Google Scholar</a> | 
        <a href='https://www.scopus.com/authid/detail.uri?authorId=53163130500' target='_blank'>Scopus</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/1f77b4/ffffff?text=Patent+Analytics", use_container_width=True)
        
        # Copyright info
        st.markdown("""
        <div style='text-align: center; font-size: 0.75rem; padding: 0.5rem; background-color: #f0f2f6; border-radius: 5px; margin-bottom: 1rem;'>
            <strong>Developed by</strong><br/>
            <a href='https://scholar.google.com/citations?user=HTleNI8AAAAJ&hl=en&oi=ao' target='_blank'>
            Prof. Dr. Serhat Burmaoglu</a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.success("🆓 100% Free Platform")
        st.caption("Advanced patent & publication analytics for researchers")
        
        # Citation reminder
        with st.expander("📖 How to Cite"):
            st.markdown("""
            **If you use this platform in your research, please cite:**
            
            Burmaoglu, S. (2024). Patent & Publication Analytics Platform. 
            
            [BibTeX and other formats available in LICENSE.md]
            """)
        
        st.markdown("---")
        
        # Navigation info
        st.markdown("### 📍 Navigation")
        st.markdown("""
        - **Home**: Upload data and overview
        - **📊 Descriptive Analytics**: Basic statistics
        - **🌐 Network Analysis**: Collaboration & citation networks
        - **💡 Semantic Analysis**: Topic modeling & trends
        - **📈 TRL Analysis**: Technology readiness levels
        - **🔬 Advanced Analytics**: Predictive & comparative
        - **ℹ️ About & Citation**: How to cite this work
        """)
        
        st.markdown("---")
        
        # Data status
        if st.session_state.data_uploaded:
            st.success(f"✅ Data loaded")
            st.info(f"📁 **File:** {st.session_state.file_name}")
            if st.session_state.data_source:
                st.info(f"🌐 **Source:** {st.session_state.data_source}")
            if st.session_state.data_type:
                st.info(f"📑 **Type:** {st.session_state.data_type.title()}")
            
            if st.button("🗑️ Clear Data"):
                st.session_state.data_uploaded = False
                st.session_state.df = None
                st.session_state.file_name = None
                st.session_state.data_source = None
                st.session_state.data_type = None
                st.rerun()
        else:
            st.warning("⚠️ No data uploaded")
    
    # Main content
    if not st.session_state.data_uploaded:
        show_upload_section()
    else:
        show_data_overview()

def show_upload_section():
    """Display file upload interface"""
    st.markdown("## 📤 Upload Your Data")
    
    # Important warning box
    st.warning("""
    ⚠️ **IMPORTANT: Data Source Requirements**
    
    This platform is **specifically designed for lens.org data exports**. 
    
    ✅ **Supported:**
    - CSV files exported from **lens.org** (Publications OR Patents)
    - Standard lens.org export format
    
    ❌ **Not Supported (Yet):**
    - Scopus, Web of Science, PubMed, or other databases
    - Custom CSV formats
    - Excel files (.xlsx)
    
    📚 **How to Export from lens.org:**
    1. Go to [lens.org](https://lens.org)
    2. Perform your search
    3. Click "Export" → "CSV"
    4. Upload the downloaded CSV file here
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Getting Started
        
        1. Export your data from **lens.org** in CSV format
        2. Upload the file using the uploader below
        3. System will automatically detect if it's Publications or Patents
        4. Data will be preprocessed and standardized
        5. Start analyzing with powerful analytics tools!
        
        **What You Can Analyze:**
        - 📊 Descriptive statistics
        - 🌐 Collaboration networks
        - 🔬 Citation networks
        - 💡 Semantic analysis & topic modeling
        - 📈 Technology Readiness Level (TRL) analysis
        - 🏷️ Keyword co-occurrence networks
        - 📅 Temporal trends and patterns
        """)
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a CSV file from lens.org",
            type=['csv'],
            help="Upload your lens.org export file in CSV format"
        )
        
        if uploaded_file is not None:
            try:
                with st.spinner("🔍 Analyzing and preprocessing file..."):
                    # Import parser
                    from utils.lens_parser import (
                        validate_lens_format, 
                        preprocess_lens_data,
                        get_available_fields
                    )
                    
                    # Read CSV
                    df_raw = pd.read_csv(uploaded_file)
                    
                    # Validate format - NOW RETURNS DICT
                    validation = validate_lens_format(df_raw)
                    
                    if not validation['is_valid']:
                        st.error("""
                        ❌ **This doesn't appear to be a lens.org file!**
                        
                        The uploaded file doesn't match the expected lens.org format.
                        
                        **Please ensure:**
                        - File is exported directly from lens.org
                        - Export format is CSV (not Excel or other)
                        - File hasn't been modified after export
                        - File contains at least 5 columns
                        
                        **Detection confidence:** {:.0%}
                        
                        **Need help?** Check the lens.org export guide above.
                        """.format(validation.get('confidence', 0)))
                        st.stop()
                    
                    # Extract values from validation dict
                    data_type = validation['data_type']
                    confidence = validation['confidence']
                    
                    # Preprocess data
                    df_processed, metadata = preprocess_lens_data(df_raw, data_type)
                    
                    # Check available fields
                    available_fields = get_available_fields(df_raw, data_type)
                    
                    # Store in session state
                    st.session_state.df = df_processed
                    st.session_state.df_raw = df_raw  # Keep original
                    st.session_state.file_name = uploaded_file.name
                    st.session_state.data_uploaded = True
                    st.session_state.data_source = validation.get('source', 'lens.org')
                    st.session_state.data_type = data_type
                    st.session_state.metadata = metadata
                    st.session_state.available_fields = available_fields
                    
                    # Success messages
                    st.success(f"✅ Successfully loaded: {uploaded_file.name}")
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.info(f"📑 **Type:** {data_type.title()}")
                    with col_b:
                        st.info(f"🎯 **Confidence:** {confidence:.0%}")
                    with col_c:
                        st.info(f"📊 **Records:** {len(df_processed):,}")

                    with st.expander("🔍 DEBUG: Column Mapping"):
                        st.write("**Original Columns:**")
                        st.write(list(df_raw.columns))
    
                        st.write("**Processed Columns:**")
                        st.write(list(processed_df.columns))
    
                        st.write("**Metadata:**")
                        st.json(metadata)
    
                    # Check specific columns
                        st.write("**Column Checks:**")
                        checks = {
                            'Has Title': 'Title' in processed_df.columns,
                            'Has Year': 'Year' in processed_df.columns,
                            'Has Citations': 'Citations' in processed_df.columns,
                            'Has Authors': 'Authors' in processed_df.columns,
                            'Has Keywords': 'Keywords' in processed_df.columns
                                }
                    for check, result in checks.items():
                        st.write(f"{check}: {'✅' if result else '❌'}")
    
                    # Show sample data from key columns
                    if 'Keywords' in processed_df.columns:
                        st.write("**Sample Keywords:**")
                        st.write(processed_df['Keywords'].head(3))
    
                    if 'Citations' in processed_df.columns:
                        st.write("**Sample Citations:**")
                        st.write(processed_df['Citations'].head(3))
                    # Show preprocessing info
                    with st.expander("🔧 Preprocessing Details"):
                        st.markdown("### Mapped Columns")
                        if metadata['mapped_columns']:
                            for std_name, orig_name in metadata['mapped_columns'].items():
                                st.write(f"✅ **{std_name}** ← `{orig_name}`")
                        else:
                            st.warning("No columns were mapped")
                        
                        if metadata['generated_columns']:
                            st.markdown("### Generated Columns")
                            for gen_col in metadata['generated_columns']:
                                st.write(f"🔧 {gen_col}")
                        
                        st.markdown("### Available Fields")
                        available_count = sum(available_fields.values())
                        total_count = len(available_fields)
                        st.write(f"**{available_count}/{total_count}** standard fields found")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**✅ Available:**")
                            for field, available in available_fields.items():
                                if available:
                                    st.write(f"  • {field.title()}")
                        
                        with col2:
                            st.markdown("**❌ Missing:**")
                            for field, available in available_fields.items():
                                if not available:
                                    st.write(f"  • {field.title()}")
                    
                    # Auto-refresh to show overview
                    st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                st.exception(e)  # Show full traceback for debugging
                st.info("Please ensure your file is a valid lens.org CSV export.")
    
    with col2:
        st.markdown("### 💡 Tips")
        st.markdown("""
        **File Requirements:**
        - Format: CSV only
        - Source: lens.org only
        - Size: Up to 200MB
        - Encoding: UTF-8
        
        **Data Quality:**
        - Check for complete exports
        - Verify date ranges
        - Review field completeness
        
        **First Time?**
        - Start with a small dataset (100-1000 records)
        - Test all analytics features
        - Then upload your full dataset
        
        **For Patents:**
        - System will use "Inventors" as "Authors"
        - Keywords extracted from title/abstract if needed
        
        **For Publications:**
        - Standard author fields detected
        - Keywords from various sources
        """)
        
        st.markdown("### 📖 Resources")
        st.markdown("""
        - [Lens.org Guide](https://lens.org)
        - [Export Tutorial](https://docs.lens.org)
        - [Sample Datasets](https://lens.org/lens/search/scholar)
        """)


def show_data_overview():
    """Display overview of uploaded data"""
    df = st.session_state.df
    metadata = st.session_state.get('metadata', {})
    data_type = st.session_state.get('data_type', 'unknown')
    
    st.markdown("## 📊 Data Overview")
    
    # Show data type badge
    if data_type == 'patent':
        st.info("📜 **Data Type:** Patents")
    else:
        st.info("📚 **Data Type:** Publications")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    
    with col2:
        st.metric("Columns", len(df.columns))
    
    with col3:
        # Try to find year column (standardized)
        if 'Year' in df.columns:
            year_range = f"{int(df['Year'].min())}-{int(df['Year'].max())}"
            st.metric("Year Range", year_range)
        else:
            st.metric("Year Range", "N/A")
    
    with col4:
        # Calculate completeness
        completeness = (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        st.metric("Data Completeness", f"{completeness:.1f}%")
    
    st.markdown("---")
    
    # Show standardized columns info
    if metadata:
        with st.expander("🔧 Data Preprocessing Summary", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ✅ Standardized Columns")
                if 'mapped_columns' in metadata and metadata['mapped_columns']:
                    for std_col in metadata['mapped_columns'].keys():
                        st.write(f"• {std_col}")
                else:
                    st.write("None")
            
            with col2:
                st.markdown("### 🔧 Generated Columns")
                if 'generated_columns' in metadata and metadata['generated_columns']:
                    for gen_col in metadata['generated_columns']:
                        st.write(f"• {gen_col}")
                else:
                    st.write("None")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Data Preview", "📊 Column Info", "🔍 Data Quality"])
    
    with tab1:
        st.markdown("### First 10 Rows (Standardized View)")
        
        # Show standardized columns first
        standard_cols = ['Title', 'Authors', 'Year', 'Citations', 'Keywords', 'Abstract']
        available_standard = [col for col in standard_cols if col in df.columns]
        
        if available_standard:
            st.dataframe(df[available_standard].head(10), use_container_width=True)
        else:
            st.dataframe(df.head(10), use_container_width=True)
        
        with st.expander("View All Columns"):
            st.write(f"**Standardized columns ({len(available_standard)}):**")
            st.write(available_standard)
            st.write(f"**All columns ({len(df.columns)}):**")
            st.write(list(df.columns))
    
    with tab2:
        st.markdown("### Column Information")
        
        # Focus on standardized columns
        if available_standard:
            col_info = pd.DataFrame({
                'Column': available_standard,
                'Type': [df[col].dtype for col in available_standard],
                'Non-Null Count': [df[col].count() for col in available_standard],
                'Null Count': [df[col].isnull().sum() for col in available_standard],
                'Unique Values': [df[col].nunique() for col in available_standard]
            })
            
            st.dataframe(col_info, use_container_width=True)
        
        with st.expander("All Columns Details"):
            col_info_all = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.values,
                'Non-Null Count': df.count().values,
                'Null Count': df.isnull().sum().values,
                'Unique Values': df.nunique().values
            })
            st.dataframe(col_info_all, use_container_width=True)
    
    with tab3:
        st.markdown("### Data Quality Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Missing Values (Standardized Columns)")
            if available_standard:
                missing = df[available_standard].isnull().sum()
                missing = missing[missing > 0].sort_values(ascending=False)
                
                if len(missing) > 0:
                    st.dataframe(pd.DataFrame({
                        'Column': missing.index,
                        'Missing': missing.values,
                        'Percentage': (missing.values / len(df) * 100).round(2)
                    }), use_container_width=True, hide_index=True)
                else:
                    st.success("✅ No missing values in standardized columns!")
            else:
                st.info("No standardized columns available")
        
        with col2:
            st.markdown("#### Duplicate Records")
            duplicates = df.duplicated().sum()
            st.metric("Duplicate Rows", duplicates)
            
            if duplicates > 0:
                st.warning(f"⚠️ Found {duplicates} duplicate records")
                if st.button("Remove Duplicates"):
                    st.session_state.df = df.drop_duplicates()
                    st.success("✅ Duplicates removed!")
                    st.rerun()
            else:
                st.success("✅ No duplicates found")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### 🚀 Available Analytics Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📊 Descriptive")
        if st.button("Basic Statistics", type="primary", use_container_width=True):
            st.switch_page("pages/1_📊_Descriptive_Analytics.py")
        st.caption("Overview, trends, distributions")
    
    with col2:
        st.markdown("#### 🌐 Networks")
        if st.button("Network Analysis", use_container_width=True):
            st.switch_page("pages/2_🌐_Network_Analysis.py")
        st.caption("Collaboration & citation networks")
    
    with col3:
        st.markdown("#### 💡 Semantic")
        if st.button("Topic Modeling", use_container_width=True):
            st.switch_page("pages/3_💡_Semantic_Analysis.py")
        st.caption("Keywords, topics, trends")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("#### 📈 TRL")
        if st.button("TRL Analysis", use_container_width=True):
            st.switch_page("pages/4_📈_TRL_Analysis.py")
        st.caption("Technology readiness levels")
    
    with col5:
        st.markdown("#### 🎯 Advanced")
        if st.button("Advanced Analytics", use_container_width=True):
            st.switch_page("pages/5_🔬_Advanced_Analytics.py")
        st.caption("Predictive & comparative analysis")
    
    with col6:
        st.markdown("#### 💾 Export")
        if st.button("Download Data", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"cleaned_{st.session_state.file_name}",
                mime="text/csv",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1rem; color: #666; font-size: 0.85rem;'>
        <strong>Patent & Publication Analytics Platform</strong> v3.0<br/>
        © 2024-2026 Prof. Dr. Serhat Burmaoglu - All Rights Reserved<br/>
        <a href='https://scholar.google.com/citations?user=HTleNI8AAAAJ&hl=en&oi=ao' target='_blank'>Google Scholar</a> | 
        <a href='https://www.scopus.com/authid/detail.uri?authorId=53163130500' target='_blank'>Scopus</a><br/>
        <br/>
        <em>Free for research and educational use • Citation required for publications</em><br/>
        See LICENSE.md for citation formats
    </div>
    """, unsafe_allow_html=True)
