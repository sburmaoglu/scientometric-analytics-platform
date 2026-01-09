# app.py - Main Application Entry Point

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from config.settings import PAGE_CONFIG, THEME_CONFIG
from utils.session_state import initialize_session_state
from pages import (
    home,
    data_upload,
    publications_analysis,
    patents_analysis,
    comparative_analysis,
    network_analysis,
    temporal_analysis,
    geospatial_analysis,
    topic_modeling,
    ai_insights,
    custom_reports
)

# Page configuration
st.set_page_config(
    page_title="Advanced Scientometric Analysis Platform",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Apply custom theme
st.markdown(THEME_CONFIG, unsafe_allow_html=True)

def main():
    """Main application controller"""
    
    # Sidebar navigation
    with st.sidebar:
        st.image("assets/logo.png", width=200) if Path("assets/logo.png").exists() else st.title("🔬 Scientometrics")
        st.markdown("---")
        
        # Navigation menu
        page = st.radio(
            "Navigation",
            [
                "🏠 Home",
                "📤 Data Upload",
                "📚 Publications Analysis",
                "💡 Patents Analysis",
                "🔄 Comparative Analysis",
                "🕸️ Network Analysis",
                "📈 Temporal Analysis",
                "🌐 Geospatial Analysis",
                "🏷️ Topic Modeling",
                "🤖 AI Insights",
                "📊 Custom Reports"
            ],
            key="navigation"
        )
        
        st.markdown("---")
        
        # Data status indicator
        if st.session_state.get('publications_data') is not None:
            st.success(f"✅ Publications loaded: {len(st.session_state.publications_data)} records")
        else:
            st.info("📚 No publications data loaded")
            
        if st.session_state.get('patents_data') is not None:
            st.success(f"✅ Patents loaded: {len(st.session_state.patents_data)} records")
        else:
            st.info("💡 No patents data loaded")
        
        st.markdown("---")
        
        # Settings
        with st.expander("⚙️ Settings"):
            st.session_state.theme = st.selectbox(
                "Theme",
                ["Light", "Dark"],
                index=0 if st.session_state.get('theme', 'Light') == 'Light' else 1
            )
            
            st.session_state.chart_style = st.selectbox(
                "Chart Style",
                ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn"],
                index=0
            )
            
            st.session_state.animation_speed = st.slider(
                "Animation Speed (ms)",
                100, 2000, 500, 100
            )
        
        # Help & Info
        with st.expander("ℹ️ Help & Info"):
            st.markdown("""
            **Quick Start:**
            1. Upload your data (Publications & Patents)
            2. Explore individual analyses
            3. Compare and integrate insights
            4. Generate custom reports
            
            **Supported Formats:**
            - CSV, Excel, JSON
            - BibTeX, RIS (publications)
            - Patent XML, JSON
            """)
    
    # Main content area - Route to appropriate page
    page_mapping = {
        "🏠 Home": home,
        "📤 Data Upload": data_upload,
        "📚 Publications Analysis": publications_analysis,
        "💡 Patents Analysis": patents_analysis,
        "🔄 Comparative Analysis": comparative_analysis,
        "🕸️ Network Analysis": network_analysis,
        "📈 Temporal Analysis": temporal_analysis,
        "🌐 Geospatial Analysis": geospatial_analysis,
        "🏷️ Topic Modeling": topic_modeling,
        "🤖 AI Insights": ai_insights,
        "📊 Custom Reports": custom_reports
    }
    
    # Render selected page
    page_mapping[page].render()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        Advanced Scientometric Analysis Platform v1.0 | 
        Built with Streamlit | 
        <a href='https://github.com/yourusername/scientometrics' target='_blank'>GitHub</a>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
