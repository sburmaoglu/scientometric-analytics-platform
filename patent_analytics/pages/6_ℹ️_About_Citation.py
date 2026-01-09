import streamlit as st

st.set_page_config(page_title="About & Citation", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About & Citation")

# Author information
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://via.placeholder.com/200x200/1f77b4/ffffff?text=SB", width=200)

with col2:
    st.markdown("""
    ## Prof. Dr. Serhat Burmaoglu
    
    **Developer & Project Lead**
    
    📚 [Google Scholar Profile](https://scholar.google.com/citations?user=HTleNI8AAAAJ&hl=en&oi=ao)
    
    📊 [Scopus Profile](https://www.scopus.com/authid/detail.uri?authorId=53163130500)
    
    💼 Research interests in innovation, technology assessment, and bibliometrics
    """)

st.markdown("---")

# About the platform
st.markdown("""
## 📊 About the Platform

The **Patent & Publication Analytics Platform** is a comprehensive, free web-based tool designed to help 
researchers, analysts, and innovation professionals analyze patent and publication data from lens.org.

### 🎯 Mission

To democratize access to advanced research analytics by providing professional-grade tools **completely free** 
to the academic and research community.

### ⭐ Key Features

- **Descriptive Analytics**: Comprehensive statistical analysis
- **Network Analysis**: Collaboration and keyword co-occurrence networks
- **Semantic Analysis**: Topic evolution and keyword trends
- **TRL Assessment**: Technology Readiness Level classification
- **Advanced Analytics**: Predictive modeling and comparative analysis

### 💡 Philosophy

Research should be open, accessible, and collaborative. This platform embodies these principles by:
- Being 100% free for academic and research use
- Supporting open data sources (lens.org)
- Providing transparent, reproducible analysis methods
- Encouraging proper attribution through citation
""")

st.markdown("---")

# Citation section
st.markdown("## 📖 How to Cite This Work")

st.warning("""
**IMPORTANT FOR RESEARCHERS**: If you use this platform in your research, you **must** cite it in your 
publications. Academic citation supports continued development and helps others discover these free tools.
""")

tab1, tab2, tab3, tab4 = st.tabs(["📄 Journal Articles", "📊 BibTeX", "📑 Other Formats", "📋 Copy & Use"])

with tab1:
    st.markdown("### Recommended Citation for Journal Articles")
    
    citation_journal = """Burmaoglu, S. (2026). Patent & Publication Analytics Platform: A Comprehensive 
Free Tool for Research Analysis. Retrieved from https://scholar.google.com/citations?user=HTleNI8AAAAJ"""
    
    st.code(citation_journal, language="text")
    
    if st.button("📋 Copy Journal Citation", key="copy_journal"):
        st.success("✅ Citation copied! (paste from clipboard)")
    
    st.markdown("### For Specific Features")
    
    st.markdown("""
    If you specifically use certain modules, you can reference them:
    
    - **TRL Analysis**: "Technology Readiness Level assessment performed using Burmaoglu (2026)"
    - **Network Analysis**: "Network visualization conducted using the Patent & Publication Analytics Platform (Burmaoglu, 2026)"
    - **Semantic Analysis**: "Topic evolution analysis performed using Burmaoglu (2026)"
    """)

with tab2:
    st.markdown("### BibTeX Format")
    
    bibtex = """@software{burmaoglu2026patent,
  author = {Burmaoglu, Serhat},
  title = {Patent & Publication Analytics Platform: A Comprehensive 
           Free Tool for Research Analysis},
  year = {2026},
  url = {https://scholar.google.com/citations?user=HTleNI8AAAAJ&hl=en&oi=ao},
  note = {Free research analytics platform for lens.org data}
}"""
    
    st.code(bibtex, language="bibtex")
    
    if st.button("📋 Copy BibTeX", key="copy_bibtex"):
        st.success("✅ BibTeX copied! (paste from clipboard)")
    
    st.markdown("""
    **Usage in LaTeX:**
    ```latex
    \\cite{burmaoglu2026patent}
    ```
    """)

with tab3:
    st.markdown("### APA Format (7th Edition)")
    st.code("""Burmaoglu, S. (2026). Patent & Publication Analytics Platform [Computer software]. 
Retrieved from https://scholar.google.com/citations?user=HTleNI8AAAAJ&hl=en&oi=ao""", language="text")
    
    st.markdown("### IEEE Format")
    st.code("""S. Burmaoglu, "Patent & Publication Analytics Platform," 2026. 
[Online]. Available: https://scholar.google.com/citations?user=HTleNI8AAAAJ""", language="text")
    
    st.markdown("### Chicago Format")
    st.code("""Burmaoglu, Serhat. 2026. "Patent & Publication Analytics Platform." Computer Software. 
https://scholar.google.com/citations?user=HTleNI8AAAAJ&hl=en&oi=ao.""", language="text")
    
    st.markdown("### Harvard Format")
    st.code("""Burmaoglu, S. (2026) Patent & Publication Analytics Platform. Available at: 
https://scholar.google.com/citations?user=HTleNI8AAAAJ (Accessed: [date]).""", language="text")

with tab4:
    st.markdown("### Ready-to-Use Acknowledgment")
    
    st.markdown("**For Methods Section:**")
    acknowledgment_methods = """Data analysis was performed using the Patent & Publication Analytics Platform 
(Burmaoglu, 2026), a free comprehensive tool for research analytics."""
    
    st.code(acknowledgment_methods, language="text")
    
    st.markdown("**For Acknowledgments Section:**")
    acknowledgment_ack = """The authors thank Prof. Dr. Serhat Burmaoglu for developing and freely 
providing the Patent & Publication Analytics Platform used in this research."""
    
    st.code(acknowledgment_ack, language="text")
    
    st.markdown("**For Figure Captions:**")
    acknowledgment_fig = """Figure X: [Your caption]. Analysis performed using the Patent & 
Publication Analytics Platform (Burmaoglu, 2026)."""
    
    st.code(acknowledgment_fig, language="text")

st.markdown("---")

# License and terms
st.markdown("## 📜 License & Terms of Use")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ✅ Permitted Uses")
    st.markdown("""
    - ✅ Academic research
    - ✅ Educational purposes
    - ✅ Personal analysis
    - ✅ Non-profit organizations
    - ✅ Thesis and dissertation work
    - ✅ Conference presentations
    - ✅ Teaching and training
    """)

with col2:
    st.markdown("### ❌ Restrictions")
    st.markdown("""
    - ❌ Commercial use without permission
    - ❌ Redistribution of modified versions
    - ❌ Removal of attribution
    - ❌ Claiming as your own work
    - ❌ Use without citation
    """)

st.info("""
**Commercial Licensing**: For commercial use, custom development, or enterprise deployment, 
please contact Prof. Dr. Serhat Burmaoglu through his Google Scholar or Scopus profile.
""")

st.markdown("---")

# Platform statistics
st.markdown("## 📊 Platform Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Version", "3.0")
    st.caption("Latest release")

with col2:
    st.metric("Code Lines", "3,000+")
    st.caption("Python code")

with col3:
    st.metric("Features", "5")
    st.caption("Analytics modules")

with col4:
    st.metric("Cost", "$0")
    st.caption("Completely free")

st.markdown("---")

# Development info
st.markdown("## 🛠️ Development")

st.markdown("""
### Technology Stack

**Frontend:** Streamlit  
**Data Processing:** Pandas, NumPy  
**Visualization:** Plotly, Matplotlib, Seaborn  
**Network Analysis:** NetworkX  
**Statistics:** SciPy, Scikit-learn  
**Text Analysis:** NLTK, WordCloud  

### Version History

- **v3.0** (2024): Intelligent lens.org parser with smart column detection
- **v2.0** (2024): Added network analysis, TRL assessment, semantic analysis
- **v1.0** (2024): Initial release with descriptive analytics

### Roadmap

Planned future features:
- Additional data source support (Scopus, Web of Science)
- Advanced machine learning models
- API access for automation
- Collaborative features
- Custom report generation
""")

st.markdown("---")

# Contact and support
st.markdown("## 📬 Contact & Support")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Get in Touch
    
    **For questions about the platform:**
    - View documentation (README.md, QUICKSTART.md)
    - Check LICENSE.md for citation formats
    - Review example analyses
    
    **For research collaboration:**
    - Contact via Google Scholar
    - Connect on Scopus
    """)

with col2:
    st.markdown("""
    ### Contributing
    
    **Feedback Welcome:**
    - Report bugs or issues
    - Suggest new features
    - Share use cases
    - Contribute improvements
    
    **Academic Collaboration:**
    - Joint research projects
    - Method development
    - Tool validation studies
    """)

st.markdown("---")

# Disclaimer
st.markdown("## ⚠️ Disclaimer")

st.warning("""
**Important Notice:**

This software is provided "as is" for research and educational purposes. While every effort has been 
made to ensure accuracy:

- The author makes no warranties about analysis results
- Users are responsible for validating outputs
- Appropriate statistical methods should be verified
- Domain expertise is required for interpretation
- Results should be cross-checked with other sources

**Recommended Practice:** Always validate critical findings using multiple methods and consult with 
domain experts before making important decisions based on these analyses.
""")

st.markdown("---")

# Thank you message
st.success("""
### 🙏 Thank You!

Thank you for using the Patent & Publication Analytics Platform. Your proper citation of this work 
helps support continued development and makes these tools available to the broader research community.

**If this platform has been useful for your research, please:**
1. ✅ Cite it in your publications
2. ✅ Share it with colleagues
3. ✅ Provide feedback for improvements
4. ✅ Acknowledge it in presentations

Together, we can make research analytics more accessible to everyone!

— Prof. Dr. Serhat Burmaoglu
""")

# Final footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem; color: #666; font-size: 0.85rem;'>
    © 2026 Prof. Dr. Serhat Burmaoglu - All Rights Reserved<br/>
    <a href='https://scholar.google.com/citations?user=HTleNI8AAAAJ&hl=en&oi=ao' target='_blank'>Google Scholar</a> | 
    <a href='https://www.scopus.com/authid/detail.uri?authorId=53163130500' target='_blank'>Scopus</a><br/>
    Patent & Publication Analytics Platform v3.0
</div>
""", unsafe_allow_html=True)
