"""
ENHANCED MAIN PAGE (app.py)
Beautiful, informative landing page with patent/publication explanations
Replace your current app.py content with this
"""

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

# Enhanced CSS with modern styling
def load_css():
    st.markdown("""
    <style>
    /* Main header styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(120deg, #1f77b4 0%, #ff7f0e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #555;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 300;
    }
    
    /* Feature boxes */
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .feature-box:hover {
        transform: translateY(-5px);
    }
    
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stats-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .module-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .module-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 5px 20px rgba(31, 119, 180, 0.3);
        transform: translateY(-3px);
    }
    
    .upload-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 2rem 0;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Info boxes */
    .highlight-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Animated gradient background */
    .gradient-bg {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        padding: 2rem;
        border-radius: 15px;
        color: white;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Copyright styling */
    .copyright-box {
        text-align: center;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #e0e0e0;
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
        st.session_state.data_source = None
    if 'data_type' not in st.session_state:
        st.session_state.data_type = None

def show_welcome_section():
    """Beautiful welcome section with explanations"""
    
    # Hero section
    st.markdown("""
    <div class="gradient-bg" style="margin: 2rem 0;">
        <h2 style="color: white; text-align: center; margin-bottom: 1rem;">
            🚀 Welcome to Advanced Research Analytics
        </h2>
        <p style="color: white; text-align: center; font-size: 1.2rem; margin-bottom: 0;">
            Transform your patent and publication data into actionable research insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # What is this platform?
    st.markdown("## 🎯 What is This Platform?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>📜 Patent Analysis</h3>
            <p><strong>Patents</strong> are legal documents that grant exclusive rights to inventions. 
            Analyzing patents helps researchers:</p>
            <ul>
                <li>🔍 <strong>Track technological trends</strong> in specific fields</li>
                <li>🏢 <strong>Identify key inventors</strong> and organizations</li>
                <li>💡 <strong>Discover innovation patterns</strong> across industries</li>
                <li>🌍 <strong>Map technological landscapes</strong> globally</li>
                <li>🔗 <strong>Find collaboration opportunities</strong></li>
            </ul>
            <p><em>Example: Analyzing AI patents to identify emerging technologies</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>📚 Publication Analysis</h3>
            <p><strong>Scientific publications</strong> (journal articles, conference papers) represent 
            research outputs. Analyzing publications helps:</p>
            <ul>
                <li>📊 <strong>Measure research impact</strong> through citations</li>
                <li>🎓 <strong>Identify influential researchers</strong> and institutions</li>
                <li>🔬 <strong>Discover research trends</strong> and hot topics</li>
                <li>🤝 <strong>Map collaboration networks</strong> in academia</li>
                <li>📈 <strong>Track knowledge evolution</strong> over time</li>
            </ul>
            <p><em>Example: Analyzing climate change research to find key themes</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Why use this platform?
    st.markdown("## 💎 Why Use This Platform?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stats-box">
            <h2 style="color: white;">🆓</h2>
            <h3 style="color: white;">100% FREE</h3>
            <p style="color: white; margin: 0;">No subscriptions, no hidden fees. 
            Professional analytics accessible to all researchers.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h2 style="color: white;">🎓</h2>
            <h3 style="color: white;">ACADEMIC-GRADE</h3>
            <p style="color: white; margin: 0;">Statistical methods with proper citations. 
            Publication-ready results.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-box" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <h2 style="color: white;">⚡</h2>
            <h3 style="color: white;">EASY TO USE</h3>
            <p style="color: white; margin: 0;">Upload your data, click analyze. 
            No coding required.</p>
        </div>
        """, unsafe_allow_html=True)

def show_analytics_modules():
    """Show available analytics modules with descriptions"""
    
    st.markdown("## 🛠️ Analytics Modules")
    st.markdown("### Comprehensive tools for deep research insights")
    
    modules = [
        {
            "icon": "📊",
            "name": "Descriptive Analytics",
            "description": "Get comprehensive statistics, trends, and distributions",
            "features": [
                "Publication/Patent counts over time",
                "Citation statistics and rankings",
                "Author/Inventor analysis",
                "Keyword frequency analysis",
                "Top cited works identification"
            ]
        },
        {
            "icon": "🌐",
            "name": "Network Analysis",
            "description": "Visualize collaboration patterns and relationships",
            "features": [
                "Author collaboration networks",
                "Keyword co-occurrence networks",
                "Community detection",
                "Centrality analysis",
                "Network metrics (density, clustering)"
            ]
        },
        {
            "icon": "💡",
            "name": "Semantic Analysis",
            "description": "Advanced text mining and topic discovery",
            "features": [
                "N-gram extraction (unigrams, bigrams, trigrams)",
                "Topic modeling (LDA-style)",
                "Keyword emergence analysis",
                "Word clouds and visualizations",
                "Trend tracking over time"
            ]
        },
        {
            "icon": "📈",
            "name": "TRL Assessment",
            "description": "Technology Readiness Level evaluation",
            "features": [
                "Automatic TRL classification (1-9)",
                "Patent maturity assessment",
                "Technology portfolio analysis",
                "Development stage identification",
                "Investment readiness scoring"
            ]
        },
        {
            "icon": "🔬",
            "name": "Advanced Analytics",
            "description": "Statistical testing and predictive modeling",
            "features": [
                "Impact metrics (h-index, i10, i100)",
                "K-Means clustering with elbow method",
                "Comparative analysis",
                "Statistical hypothesis testing",
                "Citation prediction models"
            ]
        }
    ]
    
    # Display modules in grid
    cols = st.columns(2)
    for idx, module in enumerate(modules):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="module-card">
                <h3>{module['icon']} {module['name']}</h3>
                <p style="color: #666; margin-bottom: 1rem;">{module['description']}</p>
                <p style="margin: 0;"><strong>Key Features:</strong></p>
                <ul style="margin-top: 0.5rem; margin-bottom: 0;">
                    {''.join([f'<li>{feature}</li>' for feature in module['features'][:3]])}
                </ul>
            </div>
            """, unsafe_allow_html=True)

def show_data_sources():
    """Show supported data sources"""
    
    st.markdown("## 📁 Supported Data Sources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h3>✅ Lens.org (Recommended)</h3>
            <p>Free, comprehensive patent and scholarly database</p>
            <ul>
                <li><strong>Patents:</strong> 130M+ global patents</li>
                <li><strong>Publications:</strong> 260M+ scholarly works</li>
                <li><strong>Export:</strong> CSV format with rich metadata</li>
            </ul>
            <p><strong>How to get data:</strong></p>
            <ol>
                <li>Visit <a href="https://www.lens.org" target="_blank">lens.org</a></li>
                <li>Search for your topic (e.g., "artificial intelligence patents")</li>
                <li>Filter results (by year, country, etc.)</li>
                <li>Click "Export" → Select CSV format</li>
                <li>Download and upload here!</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="highlight-box">
            <h3>⚠️ Data Requirements</h3>
            <p><strong>Your CSV file should contain:</strong></p>
            <ul>
                <li><strong>Essential:</strong> Title, Year, Citations</li>
                <li><strong>Recommended:</strong> Authors/Inventors, Keywords</li>
                <li><strong>Optional:</strong> Abstract, DOI, Classifications</li>
            </ul>
            <p><strong>Platform automatically:</strong></p>
            <ul>
                <li>✅ Detects publication vs. patent data</li>
                <li>✅ Maps column names to standard format</li>
                <li>✅ Generates missing fields when possible</li>
                <li>✅ Validates data quality</li>
            </ul>
            <p style="margin: 0;"><em>Don't worry about exact column names - our intelligent parser handles variations!</em></p>
        </div>
        """, unsafe_allow_html=True)

def show_workflow():
    """Show typical workflow"""
    
    st.markdown("## 🔄 How It Works")
    
    st.markdown("""
    <div style="display: flex; justify-content: space-around; margin: 2rem 0;">
        <div style="text-align: center; flex: 1;">
            <div style="background: #1f77b4; color: white; width: 60px; height: 60px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; 
                        font-size: 1.5rem; font-weight: bold;">1</div>
            <h4>📤 Upload Data</h4>
            <p>Upload your CSV file from Lens.org or compatible source</p>
        </div>
        <div style="text-align: center; flex: 1;">
            <div style="background: #ff7f0e; color: white; width: 60px; height: 60px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; 
                        font-size: 1.5rem; font-weight: bold;">2</div>
            <h4>🔍 Preprocess</h4>
            <p>Platform automatically validates and prepares your data</p>
        </div>
        <div style="text-align: center; flex: 1;">
            <div style="background: #2ca02c; color: white; width: 60px; height: 60px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; 
                        font-size: 1.5rem; font-weight: bold;">3</div>
            <h4>📊 Analyze</h4>
            <p>Explore 5 powerful analytics modules with visualizations</p>
        </div>
        <div style="text-align: center; flex: 1;">
            <div style="background: #d62728; color: white; width: 60px; height: 60px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; 
                        font-size: 1.5rem; font-weight: bold;">4</div>
            <h4>💾 Export</h4>
            <p>Download reports, charts, and statistics for your research</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_use_cases():
    """Show typical use cases"""
    
    st.markdown("## 🎯 Who Uses This Platform?")
    
    use_cases = {
        "🎓 PhD Researchers": [
            "Literature review and gap analysis",
            "Identifying research trends in their field",
            "Finding potential collaborators",
            "Preparing systematic reviews"
        ],
        "🏢 R&D Managers": [
            "Technology landscape mapping",
            "Competitor patent analysis",
            "Innovation trend tracking",
            "Investment decision support"
        ],
        "📚 University Libraries": [
            "Research output assessment",
            "Bibliometric analysis",
            "Institutional benchmarking",
            "Identifying emerging topics"
        ],
        "💼 Policy Makers": [
            "Science & technology policy analysis",
            "Regional innovation assessment",
            "Funding impact evaluation",
            "Strategic planning"
        ]
    }
    
    cols = st.columns(2)
    for idx, (user_type, uses) in enumerate(use_cases.items()):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="info-card">
                <h3>{user_type}</h3>
                <ul>
                    {''.join([f'<li>{use}</li>' for use in uses])}
                </ul>
            </div>
            """, unsafe_allow_html=True)

def main():
    load_css()
    initialize_session_state()
    
    # Main header
    st.markdown('<div class="main-header">📊 Patent & Publication Analytics Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">🚀 Transform Research Data into Actionable Insights</div>', unsafe_allow_html=True)
    
    # Copyright section
    st.markdown("""
    <div class="copyright-box">
        <p style="margin: 0; color: #666;">
            © 2024-2026 <strong>Prof. Dr. Serhat Burmaoglu</strong> | 
            <a href='https://scholar.google.com/citations?user=HTleNI8AAAAJ&hl=en&oi=ao' target='_blank'>Google Scholar</a> | 
            <a href='https://www.scopus.com/authid/detail.uri?authorId=53163130500' target='_blank'>Scopus</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show informational sections if no data uploaded
    if not st.session_state.data_uploaded:
        # Welcome and explanations
        show_welcome_section()
        
        st.markdown("---")
        
        # Analytics modules
        show_analytics_modules()
        
        st.markdown("---")
        
        # Data sources
        show_data_sources()
        
        st.markdown("---")
        
        # Workflow
        show_workflow()
        
        st.markdown("---")
        
        # Use cases
        show_use_cases()
        
        st.markdown("---")
    
    # Upload section (always visible)
    st.markdown("""
    <div class="upload-section">
        <h2 style="color: white; text-align: center; margin-bottom: 1rem;">
            📤 Upload Your Data to Get Started
        </h2>
        <p style="color: white; text-align: center; font-size: 1.1rem; margin-bottom: 0;">
            Upload a CSV file from Lens.org or compatible source
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        uploaded_file = st.file_uploader(
            "Choose your CSV file",
            type=['csv'],
            help="Upload a CSV file exported from Lens.org or similar source"
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
            
            # Validate format - RETURNS DICT NOW
            validation = validate_lens_format(df_raw)
            
            if not validation['is_valid']:
                st.error(f"""
                ❌ **Data validation failed!**
                
                {validation.get('message', 'Unknown error')}
                
                **Details:**
                - Detection confidence: {validation.get('confidence', 0):.0%}
                - Data type detected: {validation.get('data_type', 'Unknown')}
                - Columns found: {len(df_raw.columns)}
                
                **Requirements:**
                - Minimum 5 columns required
                - Must contain: Title, Year, Citations (or similar)
                - Recommended: Use lens.org export format
                """)
                
                with st.expander("📋 Show Your File's Columns"):
                    st.write(list(df_raw.columns))
                
                st.info("""
                **💡 Tips:**
                - Visit [lens.org](https://lens.org) and export data as CSV
                - Make sure the file hasn't been modified
                - Check that required columns exist
                """)
                
            else:
                # SUCCESS - Process the data
                st.success(f"✅ {validation.get('message', 'Data loaded successfully!')}")
                
                with st.spinner("⚙️ Preprocessing data..."):
                    # Preprocess with detected type
                    processed_df, report = preprocess_lens_data(
                        df_raw, 
                        data_type=validation['data_type']
                    )
                
                # Save to session state - USE DICT VALUES
                st.session_state.df = processed_df
                st.session_state.data_uploaded = True
                st.session_state.file_name = uploaded_file.name
                st.session_state.data_source = validation.get('source', 'unknown')
                st.session_state.data_type = validation.get('data_type', 'unknown')
                
                # Show preprocessing report
                with st.expander("📊 View Preprocessing Report"):
                    st.markdown("### Detected Information")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Data Type", validation['data_type'].title())
                    with col2:
                        st.metric("Confidence", f"{validation['confidence']:.0%}")
                    with col3:
                        st.metric("Source", validation['source'])
                    
                    st.markdown("### Mapped Columns")
                    for std_col, orig_col in report.get('mapped_columns', {}).items():
                        st.write(f"✅ **{std_col}** ← `{orig_col}`")
                    
                    if report.get('generated_columns'):
                        st.markdown("### Generated Columns")
                        for col in report['generated_columns']:
                            st.write(f"🔧 **{col}** (auto-generated)")
                
                # Show data preview
                st.markdown("### 👀 Data Preview")
                st.dataframe(processed_df.head(10), use_container_width=True)
                
                # Quick stats
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Records", f"{len(processed_df):,}")
                
                with col2:
                    if 'Year' in processed_df.columns:
                        years = processed_df['Year'].dropna()
                        if len(years) > 0:
                            st.metric("Year Range", f"{int(years.min())}-{int(years.max())}")
                
                with col3:
                    if 'Citations' in processed_df.columns:
                        total_cites = int(processed_df['Citations'].sum())
                        st.metric("Total Citations", f"{total_cites:,}")
                
                with col4:
                    st.metric("Data Type", validation['data_type'].title())
                
                # Navigation to analytics
                st.markdown("---")
                st.success("🎉 **Ready to Analyze!** Choose a module below or use the sidebar.")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    if st.button("📊 Descriptive", use_container_width=True, type="primary"):
                        st.switch_page("pages/1_📊_Descriptive_Analytics.py")
                
                with col2:
                    if st.button("🌐 Network", use_container_width=True):
                        st.switch_page("pages/2_🌐_Network_Analysis.py")
                
                with col3:
                    if st.button("💡 Semantic", use_container_width=True):
                        st.switch_page("pages/3_💡_Semantic_Analysis.py")
                
                with col4:
                    if st.button("📈 TRL", use_container_width=True):
                        st.switch_page("pages/4_📈_TRL_Analysis.py")
                
                with col5:
                    if st.button("🔬 Advanced", use_container_width=True):
                        st.switch_page("pages/5_🔬_Advanced_Analytics.py")
                
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        
        with st.expander("🔍 Technical Details"):
            st.code(str(e))
            
            import traceback
            st.code(traceback.format_exc())
        
        st.info("""
        **Common Issues:**
        - File encoding: Try saving as UTF-8 CSV
        - Column names: Check for special characters
        - File size: Very large files may timeout
        - Format: Ensure it's a valid CSV file
        """)    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Quick Start Guide")
        
        st.markdown("""
        1. **Get Your Data**
           - Visit [Lens.org](https://lens.org)
           - Search your topic
           - Export as CSV
        
        2. **Upload Here**
           - Use the upload button
           - Wait for processing
        
        3. **Explore Analytics**
           - 5 powerful modules
           - Interactive visualizations
           - Downloadable reports
        """)
        
        st.markdown("---")
        
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [User Guide](https://github.com/yourusername/patent-analytics)
        - [Video Tutorial](https://youtube.com)
        - [Example Datasets](https://lens.org)
        - [FAQ](https://github.com)
        """)
        
        st.markdown("---")
        
        st.markdown("""
        <div style='text-align: center; font-size: 0.75rem; padding: 1rem; background-color: #f0f2f6; border-radius: 10px;'>
            <strong>Developed by</strong><br/>
            <a href='https://scholar.google.com/citations?user=HTleNI8AAAAJ&hl=en&oi=ao' target='_blank'>
            Prof. Dr. Serhat Burmaoglu</a>
            <br/><br/>
            <strong>Version:</strong> 3.0<br/>
            <strong>License:</strong> Free for Research
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📖 How to Cite"):
            st.markdown("""
            **If you use this platform in your research, please cite:**
            
            Burmaoglu, S. (2024). Patent & Publication Analytics Platform. 
            Available at: https://your-app-url.streamlit.app
            """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.85rem; padding: 2rem 0;'>
        <p><strong>© 2024-2026 Prof. Dr. Serhat Burmaoglu</strong></p>
        <p>
            Patent & Publication Analytics Platform v3.0 | 
            Free for Research & Education | 
            Citation Required for Publications
        </p>
        <p style='margin-top: 1rem;'>
            Built with ❤️ using Streamlit | 
            <a href='https://github.com' target='_blank'>Source Code</a> | 
            <a href='mailto:contact@example.com'>Contact</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
