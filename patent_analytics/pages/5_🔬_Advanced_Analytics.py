import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats

st.set_page_config(page_title="Advanced Analytics", page_icon="🔬", layout="wide")
# Add this after imports, before title
def add_navigation():
    """Back and Home buttons"""
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("← Back", key="nav_back", use_container_width=True):
            st.switch_page("app.py")
    
    with col2:
        if st.button("🏠 Home", key="nav_home", use_container_width=True, type="primary"):
            st.switch_page("app.py")
    
    st.markdown("---")

st.title("🔬 Advanced Analytics")
add_navigation()  # ← ADD THIS LINE RIGHT AFTER TITLE
st.markdown("Comparative analysis, predictions, and advanced statistical insights")

# Check if data is uploaded
if not st.session_state.get('data_uploaded', False):
    st.warning("⚠️ Please upload data first from the Home page")
    if st.button("← Go to Home"):
        st.switch_page("app.py")
    st.stop()

df = st.session_state.df

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Comparative Analysis",
    "📈 Predictive Models",
    "🎯 Impact Analysis",
    "📉 Statistical Tests"
])

with tab1:
    st.markdown("## 📊 Comparative Analysis")
    st.info("Compare different segments of your dataset to identify patterns and differences")
    
    # Find grouping columns
    year_cols = [col for col in df.columns if 'year' in col.lower()]
    author_cols = [col for col in df.columns if 'author' in col.lower()]
    citation_cols = [col for col in df.columns if 'citation' in col.lower() or 'cited' in col.lower()]
    
    comparison_type = st.selectbox(
        "Select Comparison Type",
        [
            "Time Period Comparison",
            "Top Authors Comparison",
            "High vs Low Citation Groups",
            "Custom Group Comparison"
        ]
    )
    
    if comparison_type == "Time Period Comparison" and year_cols:
        year_col = year_cols[0]
        
        st.markdown("### 📅 Compare Different Time Periods")
        
        col1, col2 = st.columns(2)
        
        with col1:
            years = sorted(df[year_col].dropna().unique())
            mid_point = len(years) // 2
            
            period1_years = st.multiselect(
                "Period 1 (Earlier)",
                options=years,
                default=list(years[:mid_point])
            )
        
        with col2:
            period2_years = st.multiselect(
                "Period 2 (Later)",
                options=years,
                default=list(years[mid_point:])
            )
        
        if period1_years and period2_years:
            period1_df = df[df[year_col].isin(period1_years)]
            period2_df = df[df[year_col].isin(period2_years)]
            
            st.markdown("### 📊 Comparison Results")
            
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Period 1 Publications",
                    f"{len(period1_df):,}",
                    help=f"Years: {min(period1_years)}-{max(period1_years)}"
                )
            
            with col2:
                st.metric(
                    "Period 2 Publications",
                    f"{len(period2_df):,}",
                    delta=f"{len(period2_df) - len(period1_df):+,}",
                    help=f"Years: {min(period2_years)}-{max(period2_years)}"
                )
            
            with col3:
                growth = ((len(period2_df) - len(period1_df)) / len(period1_df) * 100) if len(period1_df) > 0 else 0
                st.metric(
                    "Growth Rate",
                    f"{growth:+.1f}%"
                )
            
            # Citation comparison
            if citation_cols:
                citation_col = citation_cols[0]
                
                st.markdown("### 📚 Citation Comparison")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    avg_cit_p1 = period1_df[citation_col].mean()
                    st.metric("Period 1 Avg Citations", f"{avg_cit_p1:.1f}")
                
                with col2:
                    avg_cit_p2 = period2_df[citation_col].mean()
                    delta = avg_cit_p2 - avg_cit_p1
                    st.metric("Period 2 Avg Citations", f"{avg_cit_p2:.1f}", delta=f"{delta:+.1f}")
                
                # Distribution comparison
                fig = go.Figure()
                
                fig.add_trace(go.Box(
                    y=period1_df[citation_col],
                    name=f"Period 1 ({min(period1_years)}-{max(period1_years)})",
                    marker_color='#3498db'
                ))
                
                fig.add_trace(go.Box(
                    y=period2_df[citation_col],
                    name=f"Period 2 ({min(period2_years)}-{max(period2_years)})",
                    marker_color='#e74c3c'
                ))
                
                fig.update_layout(
                    title='Citation Distribution Comparison',
                    yaxis_title='Citations',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistical test
                if len(period1_df[citation_col].dropna()) > 0 and len(period2_df[citation_col].dropna()) > 0:
                    t_stat, p_value = stats.ttest_ind(
                        period1_df[citation_col].dropna(),
                        period2_df[citation_col].dropna()
                    )
                    
                    if p_value < 0.05:
                        st.success(f"✅ **Statistically Significant Difference** (p={p_value:.4f})")
                        st.caption("The two periods show significantly different citation patterns")
                    else:
                        st.info(f"ℹ️ **No Significant Difference** (p={p_value:.4f})")
                        st.caption("The two periods show similar citation patterns")
    
    elif comparison_type == "Top Authors Comparison" and author_cols and citation_cols:
        st.markdown("### 👥 Compare Performance of Top Authors")
        
        author_col = author_cols[0]
        citation_col = citation_cols[0]
        
        # Get top authors (simplified - assumes single author per record)
        author_stats = df.groupby(author_col).agg({
            citation_col: ['count', 'sum', 'mean']
        }).reset_index()
        author_stats.columns = ['Author', 'Publications', 'Total_Citations', 'Avg_Citations']
        author_stats = author_stats.nlargest(20, 'Publications')
        
        selected_authors = st.multiselect(
            "Select authors to compare (max 5)",
            options=author_stats['Author'].tolist(),
            default=author_stats['Author'].tolist()[:3],
            max_selections=5
        )
        
        if selected_authors:
            # Create comparison chart
            comparison_data = author_stats[author_stats['Author'].isin(selected_authors)]
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    comparison_data,
                    x='Author',
                    y='Publications',
                    title='Publications Comparison',
                    text='Publications'
                )
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    comparison_data,
                    x='Author',
                    y='Avg_Citations',
                    title='Average Citations Comparison',
                    text='Avg_Citations'
                )
                fig.update_traces(textposition='outside', texttemplate='%{text:.1f}')
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            st.dataframe(
                comparison_data,
                use_container_width=True,
                hide_index=True
            )
    
    else:
        st.info("💡 Select a comparison type and ensure required data fields are available")

with tab2:
    st.markdown("## 📈 Predictive Models")
    st.info("Forecast future trends based on historical patterns")
    
    year_cols = [col for col in df.columns if 'year' in col.lower()]
    citation_cols = [col for col in df.columns if 'citation' in col.lower()]
    
    if not year_cols:
        st.error("❌ Year column required for predictions")
    else:
        year_col = year_cols[0]
        
        prediction_type = st.selectbox(
            "Select Prediction Type",
            [
                "Publication Volume Forecast",
                "Citation Growth Prediction",
                "Keyword Trend Forecast"
            ]
        )
        
        if prediction_type == "Publication Volume Forecast":
            st.markdown("### 📊 Forecast Future Publication Volume")
            
            # Historical data
            yearly_counts = df[year_col].value_counts().sort_index()
            
            if len(yearly_counts) < 3:
                st.warning("⚠️ Need at least 3 years of data for forecasting")
            else:
                # Simple linear regression
                years = yearly_counts.index.values
                counts = yearly_counts.values
                
                # Fit model
                z = np.polyfit(years, counts, 1)
                p = np.poly1d(z)
                
                # Forecast
                forecast_years = st.slider(
                    "Forecast horizon (years)",
                    min_value=1,
                    max_value=10,
                    value=5
                )
                
                future_years = np.arange(years[-1] + 1, years[-1] + forecast_years + 1)
                future_predictions = p(future_years)
                
                # Visualize
                fig = go.Figure()
                
                # Historical data
                fig.add_trace(go.Scatter(
                    x=years,
                    y=counts,
                    mode='lines+markers',
                    name='Historical',
                    line=dict(color='#3498db', width=3)
                ))
                
                # Predictions
                fig.add_trace(go.Scatter(
                    x=future_years,
                    y=future_predictions,
                    mode='lines+markers',
                    name='Forecast',
                    line=dict(color='#e74c3c', width=3, dash='dash')
                ))
                
                fig.update_layout(
                    title='Publication Volume Forecast',
                    xaxis_title='Year',
                    yaxis_title='Number of Publications',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Forecast table
                st.markdown("### 📊 Forecast Details")
                
                forecast_df = pd.DataFrame({
                    'Year': future_years,
                    'Predicted Publications': [int(max(0, p)) for p in future_predictions]
                })
                
                st.dataframe(forecast_df, use_container_width=True, hide_index=True)
                
                # Growth rate
                avg_growth = (counts[-1] - counts[0]) / len(counts)
                st.info(f"📈 Average annual growth: {avg_growth:+.1f} publications/year")
                
                st.warning("""
                ⚠️ **Disclaimer**: This is a simple linear forecast based on historical trends.
                Actual results may vary significantly due to external factors not captured in the model.
                """)
        
        elif prediction_type == "Citation Growth Prediction":
            if not citation_cols:
                st.error("""❌ Citation data required for this analysis""")
            else:
                st.info("🚧 Advanced citation prediction models coming soon!")
                st.markdown("""
                **Planned Features:**
                - Citation trajectory prediction for recent papers
                - Half-life estimation
                - Impact factor forecasting
                - Sleeping beauty detection (late-blooming papers)
                """)
        
        else:
            st.info("🚧 Keyword trend forecasting coming soon!")

with tab3:
    st.markdown("## 🎯 Impact Analysis")
    
    # Check required columns
    if 'Citations' not in df.columns:
        st.warning("⚠️ Citation data required for impact analysis")
        st.stop()
    
    if 'Title' not in df.columns:
        st.warning("⚠️ Title data required for display")
        st.stop()
    
    col1, col2, col3 = st.columns(3)
    
    # Calculate impact metrics
    try:
        with col1:
            st.markdown("### 📊 Core Metrics")
            
            # H-index calculation
            citations = sorted(df['Citations'].dropna().tolist(), reverse=True)
            h_index = 0
            for i, c in enumerate(citations, 1):
                if c >= i:
                    h_index = i
                else:
                    break
            
            st.metric("h-index", h_index)
            st.caption("Papers with ≥h citations")
            
            # i10-index
            i10 = len([c for c in citations if c >= 10])
            st.metric("i10-index", i10)
            st.caption("Papers with ≥10 citations")
        
        with col2:
            st.markdown("### 📈 Citation Statistics")
            
            total_cites = int(df['Citations'].sum())
            avg_cites = df['Citations'].mean()
            median_cites = df['Citations'].median()
            
            st.metric("Total Citations", f"{total_cites:,}")
            st.metric("Mean Citations", f"{avg_cites:.2f}")
            st.metric("Median Citations", f"{median_cites:.1f}")
        
        with col3:
            st.markdown("### 📍 Percentiles")
            
            percentiles = df['Citations'].quantile([0.75, 0.9, 0.95])
            st.write(f"**75th:** {percentiles[0.75]:.0f}")
            st.write(f"**90th:** {percentiles[0.9]:.0f}")
            st.write(f"**95th:** {percentiles[0.95]:.0f}")
        
        st.markdown("---")
        
        # Most cited - FIXED VERSION
        st.markdown("### 🌟 Most Cited")
        
        # Build columns safely
        cols_to_show = ['Title', 'Citations']
        if 'Year' in df.columns:
            cols_to_show.append('Year')
        
        # Get top cited
        top_cited = df.nlargest(10, 'Citations')[cols_to_show].copy()
        
        # Display directly - no renaming needed
        st.dataframe(top_cited, use_container_width=True, hide_index=True)
        
        # Methodology
        with st.expander("📚 Methodology & Citations"):
            st.markdown("""
            ### Impact Metrics
            
            **h-index:**
            - Reference: Hirsch, J. E. (2005). An index to quantify an individual's 
              scientific research output. PNAS, 102(46), 16569-16572.
            Impact analysis performed using Patent & Publication Analytics Platform 
        (Burmaoglu, 2024). H-index calculated following Hirsch (2005).
            **How to Cite:**
            """)
        except Exception as e:
        st.error(f"❌ Error: {str(e)}")
with tab4:
    st.markdown("## 📉 Statistical Tests & Analysis")
    st.info("Perform statistical tests to validate hypotheses about your data")
    
    st.markdown("### 🔬 Available Tests")
    
    test_type = st.selectbox(
        "Select Statistical Test",
        [
            "Correlation Analysis",
            "Distribution Tests",
            "Trend Analysis",
            "Outlier Detection"
        ]
    )
    
    if test_type == "Correlation Analysis":
        st.markdown("### 📊 Correlation Between Variables")
        
        # Find numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) < 2:
            st.warning("⚠️ Need at least 2 numeric columns for correlation analysis")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                var1 = st.selectbox("Variable 1", numeric_cols, index=0)
            
            with col2:
                var2 = st.selectbox("Variable 2", numeric_cols, index=min(1, len(numeric_cols)-1))
            
            if var1 != var2:
                # Calculate correlation
                valid_data = df[[var1, var2]].dropna()
                
                if len(valid_data) > 2:
                    correlation, p_value = stats.pearsonr(valid_data[var1], valid_data[var2])
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Correlation Coefficient", f"{correlation:.3f}")
                    
                    with col2:
                        st.metric("P-value", f"{p_value:.4f}")
                    
                    with col3:
                        if abs(correlation) > 0.7:
                            strength = "Strong"
                        elif abs(correlation) > 0.4:
                            strength = "Moderate"
                        else:
                            strength = "Weak"
                        st.metric("Correlation Strength", strength)
                    
                    # Scatter plot
                    fig = px.scatter(
                        valid_data,
                        x=var1,
                        y=var2,
                        title=f'Correlation: {var1} vs {var2}',
                        trendline="ols"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Interpretation
                    if p_value < 0.05:
                        st.success(f"✅ **Statistically Significant** correlation (p < 0.05)")
                    else:
                        st.info(f"ℹ️ **Not Significant** (p = {p_value:.4f})")
    
    elif test_type == "Outlier Detection":
        st.markdown("### 🎯 Detect Statistical Outliers")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            st.warning("No numeric columns available")
        else:
            selected_col = st.selectbox("Select variable to analyze", numeric_cols)
            
            method = st.radio(
                "Detection Method",
                ["IQR Method (Standard)", "Z-Score Method", "Modified Z-Score"]
            )
            
            data = df[selected_col].dropna()
            
            if "IQR" in method:
                Q1 = data.quantile(0.25)
                Q3 = data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = data[(data < lower_bound) | (data > upper_bound)]
            else:
                z_scores = np.abs(stats.zscore(data))
                outliers = data[z_scores > 3]
            
            st.metric("Outliers Detected", f"{len(outliers)} ({len(outliers)/len(data)*100:.1f}%)")
            
            # Visualization
            fig = go.Figure()
            
            fig.add_trace(go.Box(
                y=data,
                name=selected_col,
                boxmean='sd'
            ))
            
            fig.update_layout(
                title=f'Distribution with Outliers: {selected_col}',
                yaxis_title=selected_col,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            if len(outliers) > 0:
                with st.expander(f"View Outlier Values ({len(outliers)})"):
                    st.write(sorted(outliers.values, reverse=True))
    
    else:
        st.info(f"🚧 {test_type} coming soon!")

# Export options
# Add at very end of file, before any closing
st.markdown("---")
st.markdown("### 🔄 Quick Navigation")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📊 Descriptive", key="footer_1", use_container_width=True):
        st.switch_page("pages/1_📊_Descriptive_Analytics.py")

with col2:
    if st.button("🌐 Network", key="footer_2", use_container_width=True):
        st.switch_page("pages/2_🌐_Network_Analysis.py")

with col3:
    if st.button("💡 Semantic", key="footer_3", use_container_width=True):
        st.switch_page("pages/3_💡_Semantic_Analysis.py")

with col4:
    if st.button("📈 TRL", key="footer_4", use_container_width=True):
        st.switch_page("pages/4_📈_TRL_Analysis.py")

with col5:
    if st.button("🔬 Advanced", key="footer_5", use_container_width=True):
        st.switch_page("pages/5_🔬_Advanced_Analytics.py")
st.button("📥 Download Statistical Report (PDF)", disabled=True, use_container_width=False)
st.caption("Comprehensive statistical report of all analyses")
