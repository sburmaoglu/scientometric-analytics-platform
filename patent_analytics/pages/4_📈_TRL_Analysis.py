import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from collections import Counter

st.set_page_config(page_title="TRL Analysis", page_icon="📈", layout="wide")

st.title("📈 Technology Readiness Level (TRL) Analysis")
st.markdown("Assess and visualize the maturity of technologies in your patent/publication portfolio")

# Check if data is uploaded
if not st.session_state.get('data_uploaded', False):
    st.warning("⚠️ Please upload data first from the Home page")
    if st.button("← Go to Home"):
        st.switch_page("app.py")
    st.stop()

df = st.session_state.df
data_type = st.session_state.get('data_type', 'publication')

# TRL Definitions
TRL_DEFINITIONS = {
    1: {
        'name': 'Basic Principles Observed',
        'description': 'Scientific research begins and results are translated into future applications',
        'keywords': ['basic research', 'fundamental', 'theoretical', 'principle', 'observation', 'hypothesis']
    },
    2: {
        'name': 'Technology Concept Formulated',
        'description': 'Invention begins and practical applications are identified',
        'keywords': ['concept', 'formulation', 'application', 'potential', 'feasibility', 'initial']
    },
    3: {
        'name': 'Experimental Proof of Concept',
        'description': 'Active R&D with analytical/laboratory studies to validate predictions',
        'keywords': ['proof of concept', 'experimental', 'laboratory', 'validation', 'demonstration', 'analytical']
    },
    4: {
        'name': 'Technology Validated in Lab',
        'description': 'Component validation in laboratory environment',
        'keywords': ['component', 'validation', 'prototype', 'laboratory', 'testing', 'integration']
    },
    5: {
        'name': 'Technology Validated in Relevant Environment',
        'description': 'Component/subsystem validation in relevant environment',
        'keywords': ['relevant environment', 'simulated', 'realistic', 'subsystem', 'industrial', 'scale-up']
    },
    6: {
        'name': 'Technology Demonstrated in Relevant Environment',
        'description': 'System/subsystem model demonstration in relevant environment',
        'keywords': ['demonstration', 'pilot', 'system model', 'engineering', 'relevant environment', 'scale']
    },
    7: {
        'name': 'System Prototype Demonstrated',
        'description': 'System prototype demonstration in operational environment',
        'keywords': ['prototype', 'operational', 'full-scale', 'field test', 'pre-commercial', 'demonstration']
    },
    8: {
        'name': 'System Complete and Qualified',
        'description': 'Actual system completed and qualified through test and demonstration',
        'keywords': ['qualified', 'complete system', 'actual', 'commercial', 'manufacturing', 'production']
    },
    9: {
        'name': 'Actual System Proven',
        'description': 'Actual system proven through successful mission operations',
        'keywords': ['proven', 'operational', 'deployed', 'market', 'successful', 'established']
    }
}

def estimate_trl_from_text(text, title='', abstract=''):
    """
    Estimate TRL based on keywords in text, title, and abstract
    Returns TRL level (1-9) and confidence score (0-1)
    """
    if pd.isna(text):
        text = ''
    if pd.isna(title):
        title = ''
    if pd.isna(abstract):
        abstract = ''
    
    combined_text = f"{text} {title} {abstract}".lower()
    
    if not combined_text.strip():
        return None, 0.0
    
    # Score each TRL level
    scores = {}
    for trl, info in TRL_DEFINITIONS.items():
        score = sum(1 for keyword in info['keywords'] if keyword in combined_text)
        scores[trl] = score
    
    # Find TRL with highest score
    if max(scores.values()) == 0:
        # No matches - use heuristics
        if any(word in combined_text for word in ['theoretical', 'basic', 'fundamental']):
            return 1, 0.3
        elif any(word in combined_text for word in ['experimental', 'laboratory', 'test']):
            return 3, 0.3
        else:
            return 5, 0.2  # Default to mid-range
    
    best_trl = max(scores.items(), key=lambda x: x[1])
    trl_level = best_trl[0]
    
    # Calculate confidence based on score
    max_possible = len(TRL_DEFINITIONS[trl_level]['keywords'])
    confidence = min(best_trl[1] / max_possible, 1.0)
    
    return trl_level, confidence

def analyze_trl_distribution(df):
    """Analyze TRL distribution across dataset"""
    
    # Find relevant columns
    title_cols = [col for col in df.columns if 'title' in col.lower()]
    abstract_cols = [col for col in df.columns if 'abstract' in col.lower()]
    keyword_cols = [col for col in df.columns if 'keyword' in col.lower()]
    
    results = []
    
    for idx, row in df.iterrows():
        title = row[title_cols[0]] if title_cols else ''
        abstract = row[abstract_cols[0]] if abstract_cols else ''
        keywords = row[keyword_cols[0]] if keyword_cols else ''
        
        trl, confidence = estimate_trl_from_text(keywords, title, abstract)
        
        if trl:
            results.append({
                'index': idx,
                'trl': trl,
                'confidence': confidence,
                'trl_name': TRL_DEFINITIONS[trl]['name']
            })
    
    return pd.DataFrame(results)

# Main interface
st.markdown("""
## 🎯 What is TRL?

**Technology Readiness Level (TRL)** is a systematic metric/measurement system that assesses the maturity level of a technology.

The scale ranges from **TRL 1** (basic research) to **TRL 9** (proven system in operation).
""")

with st.expander("📖 View TRL Definitions"):
    for trl, info in TRL_DEFINITIONS.items():
        st.markdown(f"**TRL {trl}: {info['name']}**")
        st.caption(info['description'])
        st.markdown("---")

st.markdown("## 🔍 TRL Assessment")

st.info("""
⚙️ **How it works:**
This tool analyzes keywords, titles, and abstracts to estimate the TRL of each publication/patent.
The classification is based on keyword matching and may not be 100% accurate.

**Note:** Manual review is recommended for critical decisions.
""")

if st.button("🚀 Analyze TRL Distribution", type="primary"):
    with st.spinner("Analyzing TRL across your dataset... This may take a moment."):
        
        trl_df = analyze_trl_distribution(df)
        
        if len(trl_df) == 0:
            st.warning("⚠️ Unable to estimate TRL for any records. The dataset may lack sufficient textual information.")
        else:
            st.success(f"✅ Successfully estimated TRL for **{len(trl_df):,}** records ({len(trl_df)/len(df)*100:.1f}% of dataset)")
            
            # Store in session state
            st.session_state.trl_analysis = trl_df
            
            # Overall statistics
            st.markdown("### 📊 TRL Distribution Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_trl = trl_df['trl'].mean()
                st.metric("Average TRL", f"{avg_trl:.1f}")
            
            with col2:
                median_trl = trl_df['trl'].median()
                st.metric("Median TRL", f"{median_trl:.0f}")
            
            with col3:
                most_common_trl = trl_df['trl'].mode()[0]
                st.metric("Most Common TRL", f"{most_common_trl}")
            
            with col4:
                avg_confidence = trl_df['confidence'].mean()
                st.metric("Avg Confidence", f"{avg_confidence:.0%}")
            
            st.markdown("---")
            
            # Distribution chart
            col1, col2 = st.columns([2, 1])
            
            with col1:
                trl_counts = trl_df['trl'].value_counts().sort_index()
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=[f"TRL {trl}" for trl in trl_counts.index],
                    y=trl_counts.values,
                    text=trl_counts.values,
                    textposition='auto',
                    marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                                 '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22'][:len(trl_counts)]
                ))
                
                fig.update_layout(
                    title='TRL Distribution Across Portfolio',
                    xaxis_title='Technology Readiness Level',
                    yaxis_title='Number of Records',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 📋 TRL Summary")
                
                summary_data = []
                for trl in sorted(trl_counts.index):
                    count = trl_counts[trl]
                    percentage = (count / len(trl_df)) * 100
                    summary_data.append({
                        'TRL': f"TRL {trl}",
                        'Count': count,
                        'Percentage': f"{percentage:.1f}%"
                    })
                
                st.dataframe(
                    pd.DataFrame(summary_data),
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
            
            # Maturity analysis
            st.markdown("### 🎯 Technology Maturity Analysis")
            
            early_stage = trl_df[trl_df['trl'] <= 3]['trl'].count()
            mid_stage = trl_df[(trl_df['trl'] >= 4) & (trl_df['trl'] <= 6)]['trl'].count()
            late_stage = trl_df[trl_df['trl'] >= 7]['trl'].count()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info(f"""
                **🔬 Early Stage (TRL 1-3)**
                
                Research & Development
                
                **{early_stage}** records ({early_stage/len(trl_df)*100:.1f}%)
                """)
            
            with col2:
                st.warning(f"""
                **⚙️ Mid Stage (TRL 4-6)**
                
                Technology Validation
                
                **{mid_stage}** records ({mid_stage/len(trl_df)*100:.1f}%)
                """)
            
            with col3:
                st.success(f"""
                **🚀 Late Stage (TRL 7-9)**
                
                System Deployment
                
                **{late_stage}** records ({late_stage/len(trl_df)*100:.1f}%)
                """)
            
            # Pie chart of stages
            stages_df = pd.DataFrame({
                'Stage': ['Early Stage (1-3)', 'Mid Stage (4-6)', 'Late Stage (7-9)'],
                'Count': [early_stage, mid_stage, late_stage]
            })
            
            fig = px.pie(
                stages_df,
                values='Count',
                names='Stage',
                title='Technology Maturity Stages',
                color_discrete_sequence=['#3498db', '#f39c12', '#2ecc71']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Temporal analysis if year column exists
            year_cols = [col for col in df.columns if 'year' in col.lower()]
            
            if year_cols:
                st.markdown("### 📅 TRL Evolution Over Time")
                
                year_col = year_cols[0]
                
                # Merge TRL data with original df
                df_with_trl = df.copy()
                df_with_trl['trl'] = None
                df_with_trl.loc[trl_df['index'], 'trl'] = trl_df['trl'].values
                
                # Calculate average TRL by year
                trl_by_year = df_with_trl.dropna(subset=['trl']).groupby(year_col)['trl'].agg(['mean', 'count'])
                trl_by_year = trl_by_year[trl_by_year['count'] >= 3]  # At least 3 records per year
                
                if len(trl_by_year) > 0:
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=trl_by_year.index,
                        y=trl_by_year['mean'],
                        mode='lines+markers',
                        name='Average TRL',
                        line=dict(width=3)
                    ))
                    
                    fig.update_layout(
                        title='Average TRL Evolution Over Time',
                        xaxis_title='Year',
                        yaxis_title='Average TRL',
                        yaxis=dict(range=[0, 10]),
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Trend interpretation
                    if len(trl_by_year) >= 3:
                        first_avg = trl_by_year['mean'].iloc[0]
                        last_avg = trl_by_year['mean'].iloc[-1]
                        change = last_avg - first_avg
                        
                        if change > 0.5:
                            st.success(f"📈 **Upward Trend**: Average TRL increased by {change:.1f} levels, indicating technology maturation")
                        elif change < -0.5:
                            st.info(f"📉 **Downward Trend**: Average TRL decreased by {abs(change):.1f} levels, possibly indicating renewed focus on early-stage research")
                        else:
                            st.info("➡️ **Stable**: TRL levels remain relatively consistent over time")
            
            # Download options
            st.markdown("---")
            st.markdown("### 💾 Export TRL Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Prepare export data
                export_df = df.copy()
                export_df['Estimated_TRL'] = None
                export_df['TRL_Confidence'] = None
                export_df['TRL_Name'] = None
                
                export_df.loc[trl_df['index'], 'Estimated_TRL'] = trl_df['trl'].values
                export_df.loc[trl_df['index'], 'TRL_Confidence'] = trl_df['confidence'].values
                export_df.loc[trl_df['index'], 'TRL_Name'] = trl_df['trl_name'].values
                
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Full Dataset with TRL",
                    data=csv,
                    file_name="dataset_with_trl_analysis.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                summary_csv = trl_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download TRL Summary",
                    data=summary_csv,
                    file_name="trl_summary.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# Additional insights
st.markdown("---")
st.markdown("## 💡 Understanding Your TRL Profile")

with st.expander("📖 Interpretation Guide"):
    st.markdown("""
    ### What does your TRL distribution tell you?
    
    **High concentration in TRL 1-3:**
    - Focus on fundamental research
    - Early stage technology development
    - Higher risk but potentially transformative innovations
    
    **High concentration in TRL 4-6:**
    - Active technology validation phase
    - Moving toward commercialization
    - Balance of innovation and practicality
    
    **High concentration in TRL 7-9:**
    - Mature technology portfolio
    - Near-market or deployed technologies
    - Lower risk but potentially less disruptive
    
    **Broad distribution:**
    - Diversified portfolio across all stages
    - Balanced risk management
    - Pipeline from research to deployment
    
    ### Strategic Implications
    
    - **For Investors**: Higher TRL = Lower technical risk, closer to market
    - **For Researchers**: Track your portfolio's maturation trajectory
    - **For Policy**: Identify gaps in technology development pipeline
    - **For R&D Management**: Balance early-stage research with commercialization
    """)

with st.expander("⚠️ Limitations & Disclaimers"):
    st.markdown("""
    ### Important Limitations
    
    1. **Automated Assessment**: TRL estimation is based on keyword matching and may not capture nuanced technical details
    
    2. **Context Matters**: TRL definitions vary by industry and application domain
    
    3. **Manual Review Recommended**: Use this analysis as a starting point, not definitive classification
    
    4. **Data Quality**: Accuracy depends on quality of titles, abstracts, and keywords
    
    5. **False Positives/Negatives**: Some records may be misclassified due to ambiguous language
    
    ### Best Practices
    
    - Use TRL analysis for portfolio-level insights
    - Validate critical classifications manually
    - Consider domain-specific TRL frameworks when available
    - Combine with expert judgment for decision-making
    """)
