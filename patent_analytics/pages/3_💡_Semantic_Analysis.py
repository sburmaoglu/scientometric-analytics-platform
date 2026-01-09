import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Semantic Analysis", page_icon="💡", layout="wide")

st.title("💡 Semantic Analysis")
st.markdown("Topic modeling, keyword trends, and semantic patterns in your research data")

# Check if data is uploaded
if not st.session_state.get('data_uploaded', False):
    st.warning("⚠️ Please upload data first from the Home page")
    if st.button("← Go to Home"):
        st.switch_page("app.py")
    st.stop()

df = st.session_state.df

# Helper functions
def extract_all_keywords(df, keyword_col):
    """Extract and count all keywords"""
    all_keywords = []
    for keywords in df[keyword_col].dropna():
        if isinstance(keywords, str):
            kw_list = [k.strip().lower() for k in keywords.replace(';', ',').split(',')]
            all_keywords.extend([k for k in kw_list if k])
    return Counter(all_keywords)

def extract_ngrams(text_series, n=2):
    """Extract n-grams from text"""
    from collections import defaultdict
    ngrams = defaultdict(int)
    
    for text in text_series.dropna():
        if isinstance(text, str):
            words = text.lower().split()
            for i in range(len(words) - n + 1):
                ngram = ' '.join(words[i:i+n])
                ngrams[ngram] += 1
    
    return dict(sorted(ngrams.items(), key=lambda x: x[1], reverse=True))

def calculate_keyword_growth(df, keyword_col, year_col, keywords_to_track):
    """Calculate keyword frequency over time"""
    data = []
    
    for year in sorted(df[year_col].dropna().unique()):
        year_df = df[df[year_col] == year]
        
        for keyword in keywords_to_track:
            count = sum(
                keyword.lower() in str(kws).lower()
                for kws in year_df[keyword_col].dropna()
            )
            
            data.append({
                'Year': int(year),
                'Keyword': keyword,
                'Count': count,
                'Publications': len(year_df)
            })
    
    result_df = pd.DataFrame(data)
    result_df['Percentage'] = (result_df['Count'] / result_df['Publications'] * 100).round(2)
    
    return result_df

# Main interface
tab1, tab2, tab3, tab4 = st.tabs([
    "🔤 Keyword Analysis",
    "📊 Topic Evolution", 
    "☁️ Word Clouds",
    "🎯 Semantic Patterns"
])

with tab1:
    st.markdown("## 🔤 Comprehensive Keyword Analysis")
    
    # Find keyword column
    keyword_cols = [col for col in df.columns if 'keyword' in col.lower() or 'subject' in col.lower()]
    
    if not keyword_cols:
        st.error("❌ No keyword column found in the dataset")
    else:
        keyword_col = keyword_cols[0]
        
        st.info(f"📊 Analyzing keywords from column: **{keyword_col}**")
        
        # Extract all keywords
        keyword_counts = extract_all_keywords(df, keyword_col)
        
        if not keyword_counts:
            st.warning("No keywords found in the dataset")
        else:
            st.success(f"✅ Found **{len(keyword_counts):,}** unique keywords")
            
            # Top keywords
            st.markdown("### 🏆 Most Frequent Keywords")
            
            top_n = st.slider("Number of keywords to display", 10, 100, 30)
            
            top_keywords = keyword_counts.most_common(top_n)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Bar chart
                fig = px.bar(
                    x=[count for _, count in top_keywords],
                    y=[kw.title() for kw, _ in top_keywords],
                    orientation='h',
                    title=f'Top {top_n} Keywords by Frequency',
                    labels={'x': 'Frequency', 'y': 'Keyword'}
                )
                fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=600)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 📊 Keyword Statistics")
                st.dataframe(
                    pd.DataFrame(top_keywords[:20], columns=['Keyword', 'Count']),
                    use_container_width=True,
                    hide_index=True,
                    height=600
                )
            
            # Keyword distribution analysis
            st.markdown("### 📈 Keyword Distribution Analysis")
            
            counts_only = [count for _, count in keyword_counts.items()]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Keywords", f"{len(keyword_counts):,}")
                st.metric("Total Occurrences", f"{sum(counts_only):,}")
            
            with col2:
                st.metric("Mean Frequency", f"{np.mean(counts_only):.1f}")
                st.metric("Median Frequency", f"{np.median(counts_only):.0f}")
            
            with col3:
                single_use = sum(1 for c in counts_only if c == 1)
                st.metric("Single-use Keywords", f"{single_use:,}")
                st.metric("% Single-use", f"{single_use/len(keyword_counts)*100:.1f}%")
            
            # Distribution histogram
            fig = px.histogram(
                x=counts_only,
                nbins=50,
                title='Keyword Frequency Distribution',
                labels={'x': 'Frequency', 'y': 'Number of Keywords'}
            )
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("## 📊 Topic Evolution Over Time")
    
    keyword_cols = [col for col in df.columns if 'keyword' in col.lower()]
    year_cols = [col for col in df.columns if 'year' in col.lower()]
    
    if not keyword_cols or not year_cols:
        st.error("❌ Need both keyword and year columns for temporal analysis")
    else:
        keyword_col = keyword_cols[0]
        year_col = year_cols[0]
        
        st.info("🔍 Track how specific keywords evolve over time")
        
        # Get all keywords for selection
        all_keywords = extract_all_keywords(df, keyword_col)
        top_keywords_list = [kw for kw, _ in all_keywords.most_common(100)]
        
        # Keyword selection
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_keywords = st.multiselect(
                "Select keywords to track (max 10)",
                options=top_keywords_list,
                default=top_keywords_list[:5],
                max_selections=10
            )
        
        with col2:
            metric_type = st.radio(
                "Metric",
                ["Absolute Count", "Percentage"]
            )
        
        if selected_keywords:
            with st.spinner("Calculating keyword trends..."):
                trend_df = calculate_keyword_growth(df, keyword_col, year_col, selected_keywords)
                
                # Line chart
                if metric_type == "Absolute Count":
                    fig = px.line(
                        trend_df,
                        x='Year',
                        y='Count',
                        color='Keyword',
                        title='Keyword Trends Over Time (Absolute Count)',
                        markers=True
                    )
                else:
                    fig = px.line(
                        trend_df,
                        x='Year',
                        y='Percentage',
                        color='Keyword',
                        title='Keyword Trends Over Time (% of Publications)',
                        markers=True
                    )
                    fig.update_yaxes(title='Percentage (%)')
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Growth analysis
                st.markdown("### 📈 Growth Analysis")
                
                growth_data = []
                for keyword in selected_keywords:
                    kw_data = trend_df[trend_df['Keyword'] == keyword].sort_values('Year')
                    if len(kw_data) >= 2:
                        first_count = kw_data.iloc[0]['Count']
                        last_count = kw_data.iloc[-1]['Count']
                        
                        if first_count > 0:
                            growth = ((last_count - first_count) / first_count) * 100
                        else:
                            growth = 0
                        
                        growth_data.append({
                            'Keyword': keyword,
                            'First Year': kw_data.iloc[0]['Year'],
                            'Last Year': kw_data.iloc[-1]['Year'],
                            'Initial Count': first_count,
                            'Final Count': last_count,
                            'Growth %': f"{growth:+.1f}%"
                        })
                
                if growth_data:
                    growth_df = pd.DataFrame(growth_data)
                    st.dataframe(growth_df, use_container_width=True, hide_index=True)
                
                # Emerging vs declining keywords
                st.markdown("### 🎯 Keyword Momentum")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🚀 Rising Keywords")
                    rising = [item for item in growth_data if '+' in item['Growth %']]
                    if rising:
                        rising_sorted = sorted(rising, key=lambda x: float(x['Growth %'].replace('%', '').replace('+', '')), reverse=True)
                        for item in rising_sorted[:5]:
                            st.success(f"**{item['Keyword']}**: {item['Growth %']}")
                    else:
                        st.info("No rising keywords in selection")
                
                with col2:
                    st.markdown("#### 📉 Declining Keywords")
                    declining = [item for item in growth_data if '-' in item['Growth %']]
                    if declining:
                        declining_sorted = sorted(declining, key=lambda x: float(x['Growth %'].replace('%', '').replace('+', '').replace('-', '')), reverse=True)
                        for item in declining_sorted[:5]:
                            st.warning(f"**{item['Keyword']}**: {item['Growth %']}")
                    else:
                        st.info("No declining keywords in selection")

with tab3:
    st.markdown("## ☁️ Word Cloud Visualizations")
    
    keyword_cols = [col for col in df.columns if 'keyword' in col.lower()]
    title_cols = [col for col in df.columns if 'title' in col.lower()]
    abstract_cols = [col for col in df.columns if 'abstract' in col.lower()]
    
    text_source = st.selectbox(
        "Select text source for word cloud",
        ["Keywords"] + (["Titles"] if title_cols else []) + (["Abstracts"] if abstract_cols else [])
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        max_words = st.slider("Maximum words", 50, 300, 100)
    
    with col2:
        width = st.slider("Width", 400, 1200, 800)
    
    with col3:
        height = st.slider("Height", 300, 800, 400)
    
    if st.button("🎨 Generate Word Cloud", type="primary"):
        with st.spinner("Creating word cloud..."):
            
            # Collect text
            if text_source == "Keywords" and keyword_cols:
                text = ' '.join(df[keyword_cols[0]].dropna().astype(str))
            elif text_source == "Titles" and title_cols:
                text = ' '.join(df[title_cols[0]].dropna().astype(str))
            elif text_source == "Abstracts" and abstract_cols:
                text = ' '.join(df[abstract_cols[0]].dropna().astype(str))
            else:
                st.error("Selected text source not available")
                st.stop()
            
            if not text.strip():
                st.warning("No text data available for word cloud")
            else:
                # Create word cloud
                wordcloud = WordCloud(
                    width=width,
                    height=height,
                    max_words=max_words,
                    background_color='white',
                    colormap='viridis',
                    relative_scaling=0.5,
                    min_font_size=10
                ).generate(text)
                
                # Display
                fig, ax = plt.subplots(figsize=(width/100, height/100))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
                
                st.success(f"✅ Word cloud generated from {len(text.split())} words")

with tab4:
    st.markdown("## 🎯 Semantic Patterns & Insights")
    
    st.info("🔍 Advanced semantic analysis of your research corpus")
    
    # Find text columns
    keyword_cols = [col for col in df.columns if 'keyword' in col.lower()]
    title_cols = [col for col in df.columns if 'title' in col.lower()]
    abstract_cols = [col for col in df.columns if 'abstract' in col.lower()]
    
    analysis_type = st.selectbox(
        "Select Analysis Type",
        [
            "Bigram Analysis (2-word phrases)",
            "Trigram Analysis (3-word phrases)",
            "Keyword Co-occurrence Patterns",
            "Emerging Topics Detection"
        ]
    )
    
    if "Bigram" in analysis_type or "Trigram" in analysis_type:
        n = 2 if "Bigram" in analysis_type else 3
        
        text_source = st.radio(
            "Analyze from",
            ["Titles"] if title_cols else [] + ["Abstracts"] if abstract_cols else []
        )
        
        if st.button("🔍 Analyze", type="primary"):
            with st.spinner(f"Extracting {n}-grams..."):
                
                if text_source == "Titles" and title_cols:
                    text_series = df[title_cols[0]]
                elif text_source == "Abstracts" and abstract_cols:
                    text_series = df[abstract_cols[0]]
                else:
                    st.error("Selected source not available")
                    st.stop()
                
                ngrams = extract_ngrams(text_series, n)
                
                if not ngrams:
                    st.warning(f"No {n}-grams found")
                else:
                    top_ngrams = list(ngrams.items())[:50]
                    
                    st.success(f"✅ Found {len(ngrams):,} unique {n}-grams")
                    
                    # Visualization
                    fig = px.bar(
                        x=[count for _, count in top_ngrams[:30]],
                        y=[ngram.title() for ngram, _ in top_ngrams[:30]],
                        orientation='h',
                        title=f'Top 30 {n}-grams',
                        labels={'x': 'Frequency', 'y': f'{n}-gram'}
                    )
                    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=700)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Table
                    st.dataframe(
                        pd.DataFrame(top_ngrams[:50], columns=[f'{n}-gram', 'Frequency']),
                        use_container_width=True,
                        hide_index=True
                    )
    
    elif "Co-occurrence" in analysis_type:
        if not keyword_cols:
            st.error("❌ No keyword column found")
        else:
            st.info("Shows which keywords frequently appear together")
            
            keyword_col = keyword_cols[0]
            
            if st.button("🔍 Analyze Patterns", type="primary"):
                with st.spinner("Analyzing co-occurrence patterns..."):
                    
                    # Build co-occurrence matrix
                    cooccur = {}
                    
                    for keywords in df[keyword_col].dropna():
                        if isinstance(keywords, str):
                            kw_list = [k.strip().lower() for k in keywords.replace(';', ',').split(',')]
                            kw_list = [k for k in kw_list if k]
                            
                            for i, kw1 in enumerate(kw_list):
                                for kw2 in kw_list[i+1:]:
                                    pair = tuple(sorted([kw1, kw2]))
                                    cooccur[pair] = cooccur.get(pair, 0) + 1
                    
                    # Get top pairs
                    top_pairs = sorted(cooccur.items(), key=lambda x: x[1], reverse=True)[:30]
                    
                    if not top_pairs:
                        st.warning("No co-occurring keyword pairs found")
                    else:
                        st.success(f"✅ Found {len(cooccur):,} keyword pairs")
                        
                        # Visualization
                        pair_labels = [f"{kw1.title()} ↔ {kw2.title()}" for (kw1, kw2), _ in top_pairs]
                        pair_counts = [count for _, count in top_pairs]
                        
                        fig = px.bar(
                            x=pair_counts,
                            y=pair_labels,
                            orientation='h',
                            title='Top 30 Keyword Co-occurrences',
                            labels={'x': 'Co-occurrence Count', 'y': 'Keyword Pair'}
                        )
                        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=700)
                        st.plotly_chart(fig, use_container_width=True)
    
    else:  # Emerging topics
        st.info("🚧 Advanced topic modeling coming soon!")
        st.markdown("""
        **Planned Features:**
        - LDA (Latent Dirichlet Allocation) topic modeling
        - Dynamic topic evolution tracking
        - Topic-document relationships
        - Automated topic labeling
        - Topic similarity analysis
        """)

# Export options
st.markdown("---")
st.markdown("### 💾 Export Analysis Results")

col1, col2 = st.columns(2)

with col1:
    st.button("📥 Download Keyword Data (CSV)", disabled=True, use_container_width=True)

with col2:
    st.button("📊 Download Trend Analysis (Excel)", disabled=True, use_container_width=True)
