"""
Enhanced Semantic Analysis with NLP Features
Replace pages/3_💡_Semantic_Analysis.py with this improved version
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Semantic Analysis", page_icon="💡", layout="wide")
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

st.title("💡 Semantic Analysis")
add_navigation()  # ← ADD THIS LINE RIGHT AFTER TITLE
st.markdown("Advanced text mining and topic modeling")

# Check if data is uploaded
if not st.session_state.get('data_uploaded', False):
    st.warning("⚠️ Please upload data first from the Home page")
    if st.button("← Go to Home"):
        st.switch_page("app.py")
    st.stop()

df = st.session_state.df

# Check for required columns
if 'Title' not in df.columns and 'Abstract' not in df.columns and 'Keywords' not in df.columns:
    st.error("❌ No text data available for semantic analysis")
    st.info("This module requires at least one of: Title, Abstract, or Keywords")
    st.stop()

# ============= TEXT PREPROCESSING =============
def preprocess_text(text):
    """Clean and preprocess text"""
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def remove_stopwords(text, custom_stopwords=None):
    """Remove common stopwords"""
    default_stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
        'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
        'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
        'very', 'can', 'just', 'should', 'now', 'use', 'used', 'using',
        'based', 'new', 'study', 'research', 'paper', 'article', 'analysis'
    }
    
    if custom_stopwords:
        default_stopwords.update(custom_stopwords)
    
    words = text.split()
    filtered = [w for w in words if w not in default_stopwords and len(w) > 2]
    return ' '.join(filtered)

# ============= N-GRAM EXTRACTION =============
def extract_ngrams(text, n=2):
    """Extract n-grams from text"""
    words = text.split()
    ngrams = []
    
    for i in range(len(words) - n + 1):
        ngram = ' '.join(words[i:i+n])
        ngrams.append(ngram)
    
    return ngrams

def get_ngram_frequencies(texts, n=2, top_k=30, preprocess=True, remove_stops=True):
    """Get most frequent n-grams from texts"""
    all_ngrams = []
    
    for text in texts:
        if pd.isna(text):
            continue
        
        text = str(text)
        
        if preprocess:
            text = preprocess_text(text)
        
        if remove_stops:
            text = remove_stopwords(text)
        
        ngrams = extract_ngrams(text, n)
        all_ngrams.extend(ngrams)
    
    counter = Counter(all_ngrams)
    return counter.most_common(top_k)

# ============= LDA TOPIC MODELING =============
def simple_lda_analysis(texts, num_topics=5, top_words=10):
    """
    Simplified topic modeling using word co-occurrence
    (Full LDA would require sklearn)
    """
    # Build word co-occurrence matrix
    word_doc_freq = Counter()
    word_cooccurrence = {}
    
    for text in texts:
        if pd.isna(text):
            continue
        
        text = preprocess_text(str(text))
        text = remove_stopwords(text)
        words = list(set(text.split()))  # Unique words in doc
        
        for word in words:
            if len(word) > 3:
                word_doc_freq[word] += 1
                
                # Build co-occurrence
                if word not in word_cooccurrence:
                    word_cooccurrence[word] = Counter()
                
                for other_word in words:
                    if other_word != word and len(other_word) > 3:
                        word_cooccurrence[word][other_word] += 1
    
    # Find most common words
    top_words_list = [w for w, c in word_doc_freq.most_common(100)]
    
    # Create topics based on co-occurrence clusters
    topics = []
    used_words = set()
    
    for i in range(num_topics):
        if not top_words_list:
            break
        
        # Start with an unused top word
        seed_word = None
        for word in top_words_list:
            if word not in used_words:
                seed_word = word
                break
        
        if not seed_word:
            break
        
        # Get words that co-occur most with seed
        related = word_cooccurrence.get(seed_word, Counter())
        topic_words = [seed_word]
        used_words.add(seed_word)
        
        for word, count in related.most_common(top_words - 1):
            if word not in used_words and len(word) > 3:
                topic_words.append(word)
                used_words.add(word)
        
        if len(topic_words) < top_words:
            # Fill with remaining top words
            for word in top_words_list:
                if word not in used_words and len(topic_words) < top_words:
                    topic_words.append(word)
                    used_words.add(word)
        
        topics.append(topic_words)
    
    return topics

# ============= KEYWORD EMERGENCE ANALYSIS =============
def analyze_keyword_emergence(df, text_column, year_column='Year', min_docs=5):
    """
    Analyze emerging keywords over time
    """
    if year_column not in df.columns:
        return None
    
    # Get keywords by year
    year_keywords = {}
    
    for idx, row in df.iterrows():
        year = row.get(year_column)
        text = row.get(text_column)
        
        if pd.isna(year) or pd.isna(text):
            continue
        
        year = int(year)
        text = preprocess_text(str(text))
        text = remove_stopwords(text)
        words = text.split()
        
        if year not in year_keywords:
            year_keywords[year] = Counter()
        
        year_keywords[year].update(words)
    
    # Calculate emergence scores
    years = sorted(year_keywords.keys())
    
    if len(years) < 2:
        return None
    
    # Get recent vs historical keywords
    recent_years = years[-2:]  # Last 2 years
    historical_years = years[:-2] if len(years) > 2 else years[:1]
    
    recent_keywords = Counter()
    for year in recent_years:
        recent_keywords.update(year_keywords[year])
    
    historical_keywords = Counter()
    for year in historical_years:
        historical_keywords.update(year_keywords[year])
    
    # Calculate emergence score (new frequency / historical frequency)
    emerging = []
    
    for word, recent_count in recent_keywords.most_common(100):
        if len(word) <= 3:
            continue
        
        historical_count = historical_keywords.get(word, 0)
        
        if recent_count >= min_docs:
            if historical_count == 0:
                # New keyword
                emergence_score = recent_count * 10
            else:
                # Growing keyword
                emergence_score = (recent_count / historical_count) * recent_count
            
            emerging.append({
                'keyword': word,
                'recent_count': recent_count,
                'historical_count': historical_count,
                'emergence_score': emergence_score,
                'status': 'New' if historical_count == 0 else 'Growing'
            })
    
    # Sort by emergence score
    emerging.sort(key=lambda x: x['emergence_score'], reverse=True)
    
    return pd.DataFrame(emerging[:30])


# ============= MAIN UI =============

# Sidebar settings
with st.sidebar:
    st.markdown("### ⚙️ Analysis Settings")
    
    # Text source selection
    text_sources = []
    if 'Title' in df.columns:
        text_sources.append('Title')
    if 'Abstract' in df.columns:
        text_sources.append('Abstract')
    if 'Keywords' in df.columns:
        text_sources.append('Keywords')
    
    if text_sources:
        selected_source = st.selectbox(
            "Text Source",
            text_sources,
            help="Choose which field to analyze"
        )
    else:
        st.error("No text fields available")
        st.stop()
    
    st.markdown("---")
    
    # Preprocessing options
    st.markdown("#### Text Preprocessing")
    apply_preprocessing = st.checkbox("Apply preprocessing", value=True)
    remove_stops = st.checkbox("Remove stopwords", value=True)
    
    # Custom stopwords
    custom_stops = st.text_area(
        "Additional stopwords (comma-separated)",
        help="Add domain-specific words to exclude"
    )
    custom_stopwords = set([w.strip().lower() for w in custom_stops.split(',') if w.strip()])

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔤 N-Grams",
    "📊 Topic Modeling (LDA)",
    "🚀 Emergence Analysis",
    "☁️ Word Clouds",
    "📈 Keyword Trends"
])

# ============= TAB 1: N-GRAMS =============
with tab1:
    st.markdown("## 🔤 N-Gram Analysis")
    st.info("Extract frequent word sequences (unigrams, bigrams, trigrams)")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        ngram_type = st.radio(
            "N-gram Type",
            ["Unigrams (1-word)", "Bigrams (2-word)", "Trigrams (3-word)"],
            help="Select sequence length"
        )
        
        n = 1 if "Unigrams" in ngram_type else (2 if "Bigrams" in ngram_type else 3)
        
        top_k = st.slider("Number of n-grams", 10, 100, 30)
    
    with col2:
        if selected_source in df.columns:
            try:
                with st.spinner(f"Extracting {ngram_type.lower()}..."):
                    texts = df[selected_source].dropna()
                    
                    ngrams = get_ngram_frequencies(
                        texts,
                        n=n,
                        top_k=top_k,
                        preprocess=apply_preprocessing,
                        remove_stops=remove_stops
                    )
                    
                    if ngrams:
                        # Create dataframe
                        ngram_df = pd.DataFrame(ngrams, columns=['N-gram', 'Frequency'])
                        
                        # Visualization
                        fig = px.bar(
                            ngram_df.head(20),
                            x='Frequency',
                            y='N-gram',
                            orientation='h',
                            title=f'Top 20 {ngram_type}'
                        )
                        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Data table
                        st.markdown("#### Full Results")
                        st.dataframe(ngram_df, use_container_width=True, hide_index=True)
                        
                    else:
                        st.warning("⚠️ No n-grams found. Try adjusting preprocessing settings.")
                        
            except Exception as e:
                st.error(f"❌ Error extracting n-grams: {str(e)}")

# ============= TAB 2: TOPIC MODELING =============
with tab2:
    st.markdown("## 📊 Topic Modeling (LDA-style)")
    st.info("Discover latent topics in your documents using co-occurrence analysis")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        num_topics = st.slider("Number of Topics", 3, 10, 5)
        words_per_topic = st.slider("Words per Topic", 5, 15, 10)
    
    with col2:
        if selected_source in df.columns:
            try:
                with st.spinner("Discovering topics..."):
                    texts = df[selected_source].dropna()
                    
                    topics = simple_lda_analysis(
                        texts,
                        num_topics=num_topics,
                        top_words=words_per_topic
                    )
                    
                    if topics:
                        st.markdown("### 🎯 Discovered Topics")
                        
                        for i, topic_words in enumerate(topics, 1):
                            with st.expander(f"**Topic {i}**: {' • '.join(topic_words[:5])}", expanded=True):
                                st.markdown(f"**Top words:** {', '.join(topic_words)}")
                                
                                # Simple visualization
                                topic_df = pd.DataFrame({
                                    'Word': topic_words,
                                    'Relevance': list(range(len(topic_words), 0, -1))
                                })
                                
                                fig = px.bar(
                                    topic_df,
                                    x='Relevance',
                                    y='Word',
                                    orientation='h',
                                    title=f'Topic {i} Word Weights'
                                )
                                fig.update_layout(showlegend=False, height=300)
                                st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("⚠️ Unable to extract topics. Try different settings.")
                        
            except Exception as e:
                st.error(f"❌ Error in topic modeling: {str(e)}")

# ============= TAB 3: EMERGENCE ANALYSIS =============
with tab3:
    st.markdown("## 🚀 Keyword Emergence Analysis")
    st.info("Identify new and rapidly growing keywords in recent years")
    
    if 'Year' not in df.columns:
        st.warning("⚠️ Year information required for emergence analysis")
    else:
        try:
            with st.spinner("Analyzing keyword emergence..."):
                min_docs = st.slider("Minimum recent documents", 1, 20, 5)
                
                emerging_df = analyze_keyword_emergence(
                    df,
                    selected_source,
                    year_column='Year',
                    min_docs=min_docs
                )
                
                if emerging_df is not None and len(emerging_df) > 0:
                    # Split by status
                    new_keywords = emerging_df[emerging_df['status'] == 'New']
                    growing_keywords = emerging_df[emerging_df['status'] == 'Growing']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 🆕 New Keywords")
                        st.caption("Keywords appearing only in recent years")
                        
                        if len(new_keywords) > 0:
                            fig = px.bar(
                                new_keywords.head(15),
                                x='recent_count',
                                y='keyword',
                                orientation='h',
                                title='Frequency of New Keywords'
                            )
                            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No new keywords found")
                    
                    with col2:
                        st.markdown("### 📈 Growing Keywords")
                        st.caption("Keywords with increasing frequency")
                        
                        if len(growing_keywords) > 0:
                            fig = px.bar(
                                growing_keywords.head(15),
                                x='emergence_score',
                                y='keyword',
                                orientation='h',
                                title='Emergence Score (Growth Rate × Frequency)',
                                color='emergence_score',
                                color_continuous_scale='Viridis'
                            )
                            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No growing keywords found")
                    
                    # Full table
                    st.markdown("### 📋 Complete Emergence Report")
                    st.dataframe(emerging_df, use_container_width=True, hide_index=True)
                    
                else:
                    st.warning("⚠️ Insufficient data for emergence analysis")
                    
        except Exception as e:
            st.error(f"❌ Error in emergence analysis: {str(e)}")

# ============= TAB 4: WORD CLOUDS =============
with tab4:
    st.markdown("## ☁️ Word Cloud Visualization")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        max_words = st.slider("Maximum words", 50, 300, 100)
        width = st.slider("Width (px)", 400, 1200, 800)
        height = st.slider("Height (px)", 300, 800, 400)
    
    with col2:
        if selected_source in df.columns:
            try:
                with st.spinner("Generating word cloud..."):
                    # Combine all text
                    texts = df[selected_source].dropna()
                    combined_text = ' '.join([preprocess_text(str(t)) for t in texts])
                    
                    if remove_stops:
                        combined_text = remove_stopwords(combined_text, custom_stopwords)
                    
                    if combined_text:
                        # Generate word cloud
                        wordcloud = WordCloud(
                            width=width,
                            height=height,
                            max_words=max_words,
                            background_color='white',
                            colormap='viridis',
                            relative_scaling=0.5
                        ).generate(combined_text)
                        
                        # Display
                        fig, ax = plt.subplots(figsize=(12, 6))
                        ax.imshow(wordcloud, interpolation='bilinear')
                        ax.axis('off')
                        st.pyplot(fig)
                        
                    else:
                        st.warning("⚠️ No text available for word cloud")
                        
            except Exception as e:
                st.error(f"❌ Error generating word cloud: {str(e)}")

# ============= TAB 5: KEYWORD TRENDS =============
with tab5:
    st.markdown("## 📈 Keyword Trends Over Time")
    
    if 'Year' not in df.columns:
        st.warning("⚠️ Year information required for trend analysis")
    else:
        # Get top keywords
        texts = df[selected_source].dropna()
        
        all_words = []
        for text in texts:
            text = preprocess_text(str(text))
            text = remove_stopwords(text, custom_stopwords)
            all_words.extend(text.split())
        
        word_freq = Counter(all_words)
        top_words = [w for w, c in word_freq.most_common(50) if len(w) > 3]
        
        # Select keywords
        selected_keywords = st.multiselect(
            "Select keywords to track",
            top_words[:30],
            default=top_words[:5],
            max_selections=10
        )
        
        if selected_keywords:
            # Calculate trends
            trend_data = []
            
            for year in sorted(df['Year'].dropna().unique()):
                year_df = df[df['Year'] == year]
                year_texts = year_df[selected_source].dropna()
                
                year_combined = ' '.join([preprocess_text(str(t)) for t in year_texts])
                year_combined = remove_stopwords(year_combined, custom_stopwords)
                year_words = year_combined.split()
                year_counter = Counter(year_words)
                
                for keyword in selected_keywords:
                    count = year_counter.get(keyword, 0)
                    trend_data.append({
                        'Year': int(year),
                        'Keyword': keyword,
                        'Frequency': count
                    })
            
            trend_df = pd.DataFrame(trend_data)
            
            # Visualization
            fig = px.line(
                trend_df,
                x='Year',
                y='Frequency',
                color='Keyword',
                title='Keyword Frequency Over Time',
                markers=True
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Growth analysis
            st.markdown("### 📊 Growth Analysis")
            
            growth_data = []
            for keyword in selected_keywords:
                keyword_df = trend_df[trend_df['Keyword'] == keyword]
                
                if len(keyword_df) >= 2:
                    first_count = keyword_df.iloc[0]['Frequency']
                    last_count = keyword_df.iloc[-1]['Frequency']
                    
                    if first_count > 0:
                        growth_pct = ((last_count - first_count) / first_count) * 100
                    else:
                        growth_pct = 100 if last_count > 0 else 0
                    
                    growth_data.append({
                        'Keyword': keyword,
                        'First Year': int(keyword_df.iloc[0]['Year']),
                        'First Count': first_count,
                        'Last Year': int(keyword_df.iloc[-1]['Year']),
                        'Last Count': last_count,
                        'Growth %': growth_pct
                    })
            
            if growth_data:
                growth_df = pd.DataFrame(growth_data)
                st.dataframe(growth_df, use_container_width=True, hide_index=True)
        else:
            st.info("👆 Select keywords to analyze trends")

# Footer
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
