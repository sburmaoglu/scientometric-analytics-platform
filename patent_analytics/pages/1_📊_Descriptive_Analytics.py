import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

st.set_page_config(page_title="Descriptive Analytics", page_icon="📊", layout="wide")

st.title("📊 Descriptive Analytics")
st.markdown("Comprehensive statistical overview and trend analysis")

# Check if data is uploaded
if not st.session_state.get('data_uploaded', False):
    st.warning("⚠️ Please upload data first from the Home page")
    if st.button("← Go to Home"):
        st.switch_page("app.py")
    st.stop()

df = st.session_state.df

# Sidebar filters
with st.sidebar:
    st.markdown("### 🔍 Filters")
    
    # Year filter
    year_cols = [col for col in df.columns if 'year' in col.lower()]
    if year_cols:
        year_col = year_cols[0]
        years = sorted(df[year_col].dropna().unique())
        if len(years) > 0:
            year_range = st.slider(
                "Year Range",
                min_value=int(min(years)),
                max_value=int(max(years)),
                value=(int(min(years)), int(max(years)))
            )
            df = df[(df[year_col] >= year_range[0]) & (df[year_col] <= year_range[1])]
    
    st.markdown("---")
    st.info(f"📊 Showing {len(df)} records")

# Main analytics sections
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview", 
    "📚 Publications", 
    "👥 Authors", 
    "🏷️ Keywords",
    "📊 Citations"
])

with tab1:
    st.markdown("## 📈 Quick Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    
    with col2:
        # Try to find unique authors
        author_cols = [col for col in df.columns if 'author' in col.lower()]
        if author_cols:
            # This is a simplified count - real implementation would parse author lists
            unique_authors = df[author_cols[0]].nunique()
            st.metric("Unique Authors", f"{unique_authors:,}")
        else:
            st.metric("Unique Authors", "N/A")
    
    with col3:
        # Try to find citations
        citation_cols = [col for col in df.columns if 'citation' in col.lower() or 'cited' in col.lower()]
        if citation_cols:
            total_citations = df[citation_cols[0]].sum()
            st.metric("Total Citations", f"{int(total_citations):,}")
        else:
            st.metric("Total Citations", "N/A")
    
    with col4:
        if citation_cols and len(df) > 0:
            avg_citations = df[citation_cols[0]].mean()
            st.metric("Avg Citations", f"{avg_citations:.1f}")
        else:
            st.metric("Avg Citations", "N/A")
    
    st.markdown("---")
    
    # Year distribution
    if year_cols:
        st.markdown("### 📅 Publications Over Time")
        
        yearly_counts = df[year_col].value_counts().sort_index()
        
        fig = px.line(
            x=yearly_counts.index, 
            y=yearly_counts.values,
            labels={'x': 'Year', 'y': 'Number of Publications'},
            title='Publication Trend'
        )
        fig.update_traces(mode='lines+markers')
        st.plotly_chart(fig, use_container_width=True)
        
        # Year-over-year growth
        if len(yearly_counts) > 1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Growth Analysis")
                growth_rate = ((yearly_counts.iloc[-1] - yearly_counts.iloc[0]) / yearly_counts.iloc[0] * 100)
                st.metric(
                    "Overall Growth", 
                    f"{growth_rate:+.1f}%",
                    delta=f"{yearly_counts.iloc[-1] - yearly_counts.iloc[0]} publications"
                )
            
            with col2:
                st.markdown("#### 🏆 Peak Year")
                peak_year = yearly_counts.idxmax()
                peak_count = yearly_counts.max()
                st.metric("Most Productive Year", f"{peak_year}", f"{peak_count} publications")

with tab2:
    st.markdown("## 📚 Publication Analysis")
    
    # Check what we have
    has_title = 'Title' in df.columns
    has_citations = 'Citations' in df.columns
    has_year = 'Year' in df.columns
    
    # Show warnings for missing data
    if not has_citations:
        st.warning("⚠️ Citation data not found in dataset")
        st.info("Unable to display publication rankings without citation information.")
    elif not has_title:
        st.warning("⚠️ Title data not found in dataset")
        st.info("Unable to display publications without titles.")
    else:
        # We have what we need!
        st.markdown("### 🌟 Most Cited Publications")
        
        try:
            # Build column list carefully
            cols = ['Title', 'Citations']
            if has_year:
                cols.append('Year')
            
            # Get top 10
            top_pubs = df.nlargest(10, 'Citations')[cols].copy()
            
            # Show table
            st.dataframe(top_pubs, use_container_width=True, hide_index=True)
            
            # Show chart
            fig = px.bar(
                top_pubs,
                x='Citations',
                y='Title',
                orientation='h',
                title='Top 10 Most Cited'
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error("❌ Error displaying data")
            st.caption(str(e))
    
    # Year trends (if available)
    if has_year and 'Year' in df.columns:
        st.markdown("### 📅 Publications Over Time")
        try:
            yearly = df.groupby('Year').size().reset_index(name='Count')
            fig = px.line(yearly, x='Year', y='Count', markers=True)
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.info("Unable to show trends")
with tab3:
    st.markdown("## 👥 Author Analysis")
    
    author_cols = [col for col in df.columns if 'author' in col.lower()]
    
    if author_cols:
        st.info("ℹ️ This is a simplified author analysis. Advanced author network analysis is available in Premium tier.")
        
        # Most productive authors (simplified - assumes single author per record)
        st.markdown("### 🏆 Most Productive Authors")
        
        author_counts = df[author_cols[0]].value_counts().head(20)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(
                x=author_counts.values,
                y=author_counts.index,
                orientation='h',
                title='Top 20 Authors by Publication Count',
                labels={'x': 'Number of Publications', 'y': 'Author'}
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(
                pd.DataFrame({
                    'Author': author_counts.index,
                    'Publications': author_counts.values
                }),
                use_container_width=True,
                hide_index=True
            )
    else:
        st.warning("No author information found in the dataset")

with tab4:
    st.markdown("## 🏷️ Keyword Analysis")
    
    keyword_cols = [col for col in df.columns if 'keyword' in col.lower()]
    
    if keyword_cols:
        st.markdown("### 🔤 Most Common Keywords")
        
        # Extract all keywords (simplified - assumes comma-separated)
        all_keywords = []
        for keywords in df[keyword_cols[0]].dropna():
            if isinstance(keywords, str):
                all_keywords.extend([k.strip() for k in keywords.split(';')])
        
        if all_keywords:
            keyword_counts = Counter(all_keywords).most_common(30)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Bar chart
                fig = px.bar(
                    x=[count for _, count in keyword_counts[:20]],
                    y=[keyword for keyword, _ in keyword_counts[:20]],
                    orientation='h',
                    title='Top 20 Keywords',
                    labels={'x': 'Frequency', 'y': 'Keyword'}
                )
                fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(
                    pd.DataFrame(keyword_counts[:20], columns=['Keyword', 'Count']),
                    use_container_width=True,
                    hide_index=True
                )
            
            # Word frequency over time
            if year_cols:
                st.markdown("### 📈 Keyword Trends")
                
                selected_keywords = st.multiselect(
                    "Select keywords to track",
                    options=[k for k, _ in keyword_counts[:20]],
                    default=[k for k, _ in keyword_counts[:5]]
                )
                
                if selected_keywords:
                    # Create trend data
                    trend_data = []
                    for year in sorted(df[year_col].dropna().unique()):
                        year_df = df[df[year_col] == year]
                        for keyword in selected_keywords:
                            count = sum(
                                keyword.lower() in str(keywords).lower() 
                                for keywords in year_df[keyword_cols[0]].dropna()
                            )
                            trend_data.append({
                                'Year': year,
                                'Keyword': keyword,
                                'Count': count
                            })
                    
                    trend_df = pd.DataFrame(trend_data)
                    
                    fig = px.line(
                        trend_df,
                        x='Year',
                        y='Count',
                        color='Keyword',
                        title='Keyword Trends Over Time',
                        markers=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No keywords found in the dataset")
    else:
        st.warning("No keyword column found in the dataset")

with tab5:
    st.markdown("## 📊 Citation Analysis")
    
    if citation_cols:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Citations", f"{int(df[citation_cols[0]].sum()):,}")
        
        with col2:
            st.metric("Average Citations", f"{df[citation_cols[0]].mean():.2f}")
        
        with col3:
            st.metric("Median Citations", f"{df[citation_cols[0]].median():.1f}")
        
        st.markdown("---")
        
        # Citations by year
        if year_cols:
            st.markdown("### 📈 Citations by Publication Year")
            
            citations_by_year = df.groupby(year_col)[citation_cols[0]].agg(['sum', 'mean', 'count'])
            citations_by_year.columns = ['Total Citations', 'Avg Citations', 'Publications']
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    citations_by_year,
                    y='Total Citations',
                    title='Total Citations by Year'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.line(
                    citations_by_year,
                    y='Avg Citations',
                    title='Average Citations by Year',
                    markers=True
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # h-index calculation
        st.markdown("### 📊 Impact Metrics")
        
        citations_sorted = sorted(df[citation_cols[0]].values, reverse=True)
        h_index = 0
        for i, citations in enumerate(citations_sorted, 1):
            if citations >= i:
                h_index = i
            else:
                break
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("h-index", h_index)
            st.caption("Number of papers (h) with at least h citations each")
        
        with col2:
            # i10-index
            i10_index = len([c for c in citations_sorted if c >= 10])
            st.metric("i10-index", i10_index)
            st.caption("Number of publications with at least 10 citations")
    else:
        st.warning("No citation data found in the dataset")

# Export section
st.markdown("---")
st.markdown("### 💾 Export Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 Download Filtered Data", use_container_width=True):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv",
            use_container_width=True
        )

with col2:
    st.button("📊 Generate Report (Premium)", disabled=True, use_container_width=True)

with col3:
    st.button("🔬 Advanced Analytics →", type="primary", use_container_width=True, disabled=True)
