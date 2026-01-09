# Patent & Publication Analytics Platform

A **100% FREE** comprehensive web-based analytics platform for researchers to analyze patent and publication data from lens.org.

## Copyright & Author

**© 2024-2026 Prof. Dr. Serhat Burmaoglu - All Rights Reserved**

- 📚 [Google Scholar](https://scholar.google.com/citations?user=HTleNI8AAAAJ&hl=en&oi=ao)
- 📊 [Scopus Profile](https://www.scopus.com/authid/detail.uri?authorId=53163130500)

## Citation Requirement

**IMPORTANT**: If you use this platform in your research, you **must** cite it:

```
Burmaoglu, S. (2024). Patent & Publication Analytics Platform: A Comprehensive 
Free Tool for Research Analysis. Retrieved from https://scholar.google.com/citations?user=HTleNI8AAAAJ
```

See `LICENSE.md` for complete citation formats (BibTeX, APA, IEEE, etc.)

---

## 🌟 Key Features

### 📊 Descriptive Analytics (FREE)
- Comprehensive statistical overview
- Publication/patent trends over time
- Citation analysis and distributions
- Author productivity analysis
- Keyword frequency analysis
- Temporal patterns and growth rates

### 🌐 Network Analysis (FREE)
- **Author Collaboration Networks**: Visualize co-authorship patterns
- **Keyword Co-occurrence Networks**: Discover research themes and connections
- **Network Metrics**: Density, centrality, community detection
- **Interactive Visualizations**: Explore networks with different layouts
- Citation networks (coming soon)

### 💡 Semantic Analysis (FREE)
- **Keyword Analysis**: Frequency, distribution, and trends
- **Topic Evolution**: Track how keywords change over time
- **Word Clouds**: Visual representation of key terms
- **N-gram Analysis**: Extract meaningful phrases (bigrams, trigrams)
- **Semantic Patterns**: Co-occurrence analysis
- Topic modeling (coming soon)

### 📈 TRL Analysis (FREE)
- **Technology Readiness Level Assessment**: Automated TRL classification
- **Portfolio Maturity Analysis**: Early/Mid/Late stage distribution
- **Temporal Evolution**: Track TRL changes over time
- **Strategic Insights**: Understand your technology portfolio

### 🔬 Advanced Analytics (FREE)
- **Comparative Analysis**: Compare time periods, authors, or groups
- **Predictive Models**: Forecast publication volumes and trends
- **Impact Analysis**: h-index, i10-index, citation percentiles
- **Statistical Tests**: Correlation, outlier detection, significance testing

## 🎯 Target Users

- Academic researchers
- R&D managers
- Technology analysts
- Patent attorneys
- Innovation scouts
- Policy makers

## 📦 What's Included

```
patent_analytics/
├── app.py                                  # Main application
├── config.py                               # Configuration
├── requirements.txt                        # Dependencies
│
├── pages/
│   ├── 1_📊_Descriptive_Analytics.py      # Basic statistics & trends
│   ├── 2_🌐_Network_Analysis.py           # Collaboration & keyword networks
│   ├── 3_💡_Semantic_Analysis.py          # Topic modeling & keywords
│   ├── 4_📈_TRL_Analysis.py               # Technology readiness levels
│   └── 5_🔬_Advanced_Analytics.py         # Predictions & comparisons
│
├── utils/                                  # Utility modules
├── analytics/                              # Analytics modules
└── visualizations/                         # Visualization modules
```

## 🚀 Quick Start

### Installation

```bash
# 1. Extract files
cd patent_analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run app.py
```

### First Use

1. Export your data from **lens.org** as CSV
2. Upload the file in the application
3. System automatically detects data type (publications or patents)
4. Explore different analytics modules!

## ⚠️ Important: Data Source

**This platform ONLY supports lens.org data exports.**

✅ **Supported:**
- Publications from lens.org
- Patents from lens.org
- Standard lens.org CSV format

❌ **Not Supported:**
- Scopus, Web of Science, PubMed
- Custom CSV formats
- Modified lens.org exports

## 🎓 Analytics Capabilities

### Network Analysis
- Identify key collaborators and research communities
- Discover interdisciplinary connections
- Visualize knowledge networks
- Detect research clusters

### Semantic Analysis  
- Track emerging research topics
- Identify keyword trends over time
- Generate publication word clouds
- Extract meaningful phrases

### TRL Assessment
- Estimate technology maturity (TRL 1-9)
- Portfolio gap analysis
- Track technology evolution
- Strategic technology planning

### Impact Metrics
- Citation impact assessment
- h-index calculation
- Identify influential papers
- Publication age analysis

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Network Analysis**: NetworkX
- **Statistics**: SciPy, Scikit-learn
- **Text Analysis**: WordCloud

## 📊 Example Analyses

- **Research Portfolio Review**: Understand your lab's output and impact
- **Technology Scouting**: Identify emerging technologies and trends
- **Collaboration Mapping**: Find potential research partners
- **Grant Applications**: Generate metrics and visualizations
- **Patent Landscaping**: Analyze patent technology clusters

## 🆓 Completely Free

This platform is 100% free to use:
- No subscription fees
- No hidden costs
- No data limits
- All features included
- Open source friendly

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Free Cloud Hosting (Recommended)
Deploy to Streamlit Community Cloud:
1. Push code to GitHub
2. Connect to share.streamlit.io
3. Deploy for free!

See `DEPLOYMENT.md` for detailed instructions.

## 📚 Documentation

- **QUICKSTART.md**: 5-minute setup guide
- **DEPLOYMENT.md**: Comprehensive deployment options
- **Config.py**: Customization settings

## 🤝 Contributing

Contributions welcome! This is a free, open platform for the research community.

## 📄 License

Free to use for research and educational purposes.

## 🆘 Support

- Check documentation files
- Review example analyses
- Submit issues on GitHub

## 🔮 Roadmap

**Coming Soon:**
- Citation network visualization
- Institution collaboration maps
- Advanced topic modeling (LDA/NMF)
- PDF export of analyses
- API access
- More data source support

## 🙏 Acknowledgments

Built for researchers, by researchers. 
Special thanks to lens.org for providing open access to scholarly data.

---

Made with ❤️ for the research community | 100% Free Forever

## 📖 Citation & License

This work is free for research and educational use but **requires citation**.

**Developed by:** Prof. Dr. Serhat Burmaoglu  
**Google Scholar:** https://scholar.google.com/citations?user=HTleNI8AAAAJ&hl=en&oi=ao  
**Scopus:** https://www.scopus.com/authid/detail.uri?authorId=53163130500  

See `LICENSE.md` for:
- Complete citation formats (Journal, BibTeX, APA, IEEE, etc.)
- Terms of use
- Commercial licensing information

**© 2024-2026 Prof. Dr. Serhat Burmaoglu - All Rights Reserved**
