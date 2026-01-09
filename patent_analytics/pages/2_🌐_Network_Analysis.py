import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import numpy as np

st.set_page_config(page_title="Network Analysis", page_icon="🌐", layout="wide")

st.title("🌐 Network Analysis")
st.markdown("Visualize and analyze collaboration, citation, and keyword networks")

# Check if data is uploaded
if not st.session_state.get('data_uploaded', False):
    st.warning("⚠️ Please upload data first from the Home page")
    if st.button("← Go to Home"):
        st.switch_page("app.py")
    st.stop()

df = st.session_state.df
data_type = st.session_state.get('data_type', 'publication')

# Helper functions for network analysis
def create_coauthor_network(df, author_col, min_collaborations=2):
    """Create co-authorship network"""
    edges = []
    
    for _, row in df.iterrows():
        if pd.notna(row[author_col]):
            # Split authors (assuming semicolon or comma separated)
            authors = [a.strip() for a in str(row[author_col]).replace(';', ',').split(',')]
            authors = [a for a in authors if a]  # Remove empty
            
            # Create edges between all pairs
            for i, author1 in enumerate(authors):
                for author2 in authors[i+1:]:
                    edges.append((author1, author2))
    
    # Count collaborations
    edge_counts = Counter(edges)
    
    # Filter by minimum collaborations
    filtered_edges = [(a1, a2, count) for (a1, a2), count in edge_counts.items() 
                      if count >= min_collaborations]
    
    # Create network
    G = nx.Graph()
    for author1, author2, weight in filtered_edges:
        G.add_edge(author1, author2, weight=weight)
    
    return G

def create_keyword_network(df, keyword_col, min_cooccurrence=2):
    """Create keyword co-occurrence network"""
    edges = []
    
    for _, row in df.iterrows():
        if pd.notna(row[keyword_col]):
            keywords = [k.strip().lower() for k in str(row[keyword_col]).replace(';', ',').split(',')]
            keywords = [k for k in keywords if k]
            
            # Create edges between all pairs
            for i, kw1 in enumerate(keywords):
                for kw2 in keywords[i+1:]:
                    if kw1 != kw2:
                        edges.append(tuple(sorted([kw1, kw2])))
    
    edge_counts = Counter(edges)
    filtered_edges = [(k1, k2, count) for (k1, k2), count in edge_counts.items() 
                      if count >= min_cooccurrence]
    
    G = nx.Graph()
    for kw1, kw2, weight in filtered_edges:
        G.add_edge(kw1, kw2, weight=weight)
    
    return G

def network_to_plotly(G, title, layout='spring'):
    """Convert NetworkX graph to Plotly figure - FIXED VERSION"""
    
    if len(G.nodes()) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No network data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    try:
        # Calculate layout
        if layout == 'spring':
            pos = nx.spring_layout(G, k=0.5, iterations=50)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        elif layout == 'kamada_kawai':
            try:
                pos = nx.kamada_kawai_layout(G)
            except:
                pos = nx.spring_layout(G)
        else:
            pos = nx.spring_layout(G)
        
        # Edge trace
        edge_trace = go.Scatter(
            x=[], y=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])
        
        # Build node properties
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        node_color = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            degree = G.degree(node)
            node_size.append(10 + degree * 2)
            node_color.append(degree)
            node_text.append(f"{node}<br>Connections: {degree}")
        
        # Node trace - FIXED
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[str(node)[:20] for node in G.nodes()],
            hovertext=node_text,
            textposition="top center",
            textfont=dict(size=8),
            marker=dict(
                size=node_size,
                color=node_color,
                colorscale='YlOrRd',
                showscale=True,
                colorbar=dict(
                    title="Connections",
                    thickness=15,
                    xanchor='left'
                ),
                line=dict(width=1, color='white')
            )
        )
        
        # Create figure
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title=title,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=0, l=0, r=0, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=600
            )
        )
        
        return fig
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error: {str(e)[:100]}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color='red')
        )
        return fig

def calculate_network_metrics(G):
    """Calculate key network metrics"""
    if len(G.nodes()) == 0:
        return {}
    
    metrics = {
        'nodes': G.number_of_nodes(),
        'edges': G.number_of_edges(),
        'density': nx.density(G),
        'avg_degree': sum(dict(G.degree()).values()) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0,
    }
    
    # Calculate centrality measures for top nodes
    if len(G.nodes()) > 0:
        degree_cent = nx.degree_centrality(G)
        metrics['top_nodes'] = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:10]
        
        if nx.is_connected(G):
            metrics['diameter'] = nx.diameter(G)
            metrics['avg_path_length'] = nx.average_shortest_path_length(G)
        else:
            metrics['components'] = nx.number_connected_components(G)
            largest_cc = max(nx.connected_components(G), key=len)
            metrics['largest_component'] = len(largest_cc)
    
    return metrics

# Main interface
st.markdown("## 🌐 Network Visualization & Analysis")

# Network type selector
network_type = st.selectbox(
    "Select Network Type",
    [
        "👥 Author Collaboration Network",
        "🏷️ Keyword Co-occurrence Network",
        "🔗 Citation Network (Coming Soon)",
        "🏢 Institution Collaboration (Coming Soon)"
    ],
    help="Choose the type of network to visualize"
)

st.markdown("---")

if "Author Collaboration" in network_type:
    st.markdown("### 👥 Author Collaboration Network")
    
    if st.session_state.get('data_type') == 'patent':
        st.info("Visualizes inventor collaboration patterns. Nodes are inventors, edges represent joint patents.")
    else:
        st.info("Visualizes co-authorship patterns. Nodes are authors, edges represent collaborations.")
    
    # Use standardized Authors column
    if 'Authors' not in df.columns:
        st.error("❌ No author/inventor data found in the dataset. The preprocessing step should have created an 'Authors' column.")
        st.info("💡 **Tip:** For patent data, inventors are mapped to the Authors column during preprocessing.")
        st.stop()
    
    author_col = 'Authors'
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_collab = st.slider(
            "Minimum Collaborations",
            min_value=1,
            max_value=10,
            value=2,
            help="Filter edges by minimum number of joint publications"
        )
    
    with col2:
        layout_type = st.selectbox(
            "Layout Algorithm",
            ["spring", "circular", "kamada"],
            help="Algorithm for node positioning"
        )
    
    with col3:
        max_nodes = st.slider(
            "Maximum Nodes",
            min_value=10,
            max_value=200,
            value=50,
            help="Limit network size for better visualization"
        )
    
    if st.button("🔨 Generate Network", type="primary"):
        with st.spinner("Building collaboration network..."):
            # Create network
            G = create_coauthor_network(df, author_col, min_collab)
            
            if len(G.nodes()) == 0:
                st.warning("⚠️ No collaborations found with current filters. Try reducing minimum collaborations.")
            else:
                # Limit to largest component if too many nodes
                if len(G.nodes()) > max_nodes:
                    # Get largest connected component
                    components = sorted(nx.connected_components(G), key=len, reverse=True)
                    largest = components[0]
                    G = G.subgraph(largest).copy()
                    st.info(f"ℹ️ Showing largest connected component ({len(G.nodes())} nodes)")
                
                # Visualize
                fig = network_to_plotly(G, f"Author Collaboration Network ({len(G.nodes())} authors)", layout_type)
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Calculate metrics
                    st.markdown("### 📊 Network Metrics")
                    
                    metrics = calculate_network_metrics(G)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Authors (Nodes)", metrics['nodes'])
                    with col2:
                        st.metric("Collaborations (Edges)", metrics['edges'])
                    with col3:
                        st.metric("Network Density", f"{metrics['density']:.3f}")
                    with col4:
                        st.metric("Avg Connections", f"{metrics['avg_degree']:.1f}")
                    
                    # Top collaborators
                    if 'top_nodes' in metrics:
                        st.markdown("### 🏆 Most Connected Authors")
                        
                        top_df = pd.DataFrame(
                            [(node, f"{cent:.3f}") for node, cent in metrics['top_nodes']],
                            columns=['Author', 'Centrality Score']
                        )
                        
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.dataframe(top_df, use_container_width=True, hide_index=True)
                        
                        with col2:
                            st.markdown("""
                            **Centrality Score** measures how well-connected an author is.
                            
                            Higher scores indicate:
                            - More collaborators
                            - Central position in network
                            - Key connector role
                            """)
                    
                    # Community detection
                    if len(G.nodes()) >= 5:
                        st.markdown("### 👥 Research Communities")
                        
                        try:
                            communities = nx.community.greedy_modularity_communities(G)
                            
                            st.info(f"🔍 Detected {len(communities)} research communities/clusters")
                            
                            # Show largest communities
                            sorted_communities = sorted(communities, key=len, reverse=True)[:5]
                            
                            for i, community in enumerate(sorted_communities, 1):
                                with st.expander(f"Community {i} ({len(community)} members)"):
                                    members = list(community)[:20]  # Show first 20
                                    st.write(", ".join(members))
                                    if len(community) > 20:
                                        st.caption(f"... and {len(community) - 20} more")
                        except:
                            st.warning("Unable to detect communities with current network structure")

elif "Keyword Co-occurrence" in network_type:
    st.markdown("### 🏷️ Keyword Co-occurrence Network")
    st.info("Shows relationships between keywords. Nodes are keywords, edges show co-occurrence in publications.")
    
    # Use standardized Keywords column
    if 'Keywords' not in df.columns:
        st.error("❌ No keyword data found in the dataset")
        st.info("💡 **Note:** Keywords should have been generated during preprocessing from title/abstract if not present in original data.")
        st.stop()
    
    keyword_col = 'Keywords'
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_cooccur = st.slider(
            "Minimum Co-occurrences",
            min_value=2,
            max_value=20,
            value=3,
            help="Filter edges by minimum number of joint appearances"
        )
    
    with col2:
        layout_type = st.selectbox(
            "Layout Algorithm",
            ["spring", "circular", "kamada"]
        )
    
    with col3:
        max_nodes = st.slider(
            "Maximum Keywords",
            min_value=20,
            max_value=150,
            value=50
        )
    
    if st.button("🔨 Generate Network", type="primary"):
        with st.spinner("Building keyword network..."):
            G = create_keyword_network(df, keyword_col, min_cooccur)
            
            if len(G.nodes()) == 0:
                st.warning("⚠️ No keyword co-occurrences found. Try reducing minimum co-occurrences.")
            else:
                # Limit size
                if len(G.nodes()) > max_nodes:
                    # Keep most connected nodes
                    degrees = dict(G.degree())
                    top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:max_nodes]
                    keep_nodes = [node for node, _ in top_nodes]
                    G = G.subgraph(keep_nodes).copy()
                    st.info(f"ℹ️ Showing top {len(G.nodes())} most connected keywords")
                
                fig = network_to_plotly(G, f"Keyword Co-occurrence Network ({len(G.nodes())} keywords)", layout_type)
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("### 📊 Network Metrics")
                    
                    metrics = calculate_network_metrics(G)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Keywords (Nodes)", metrics['nodes'])
                    with col2:
                        st.metric("Co-occurrences (Edges)", metrics['edges'])
                    with col3:
                        st.metric("Network Density", f"{metrics['density']:.3f}")
                    with col4:
                        st.metric("Avg Connections", f"{metrics['avg_degree']:.1f}")
                    
                    # Top keywords
                    if 'top_nodes' in metrics:
                        st.markdown("### 🏆 Most Central Keywords")
                        
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            top_df = pd.DataFrame(
                                [(node.title(), f"{cent:.3f}") for node, cent in metrics['top_nodes']],
                                columns=['Keyword', 'Centrality Score']
                            )
                            st.dataframe(top_df, use_container_width=True, hide_index=True)
                        
                        with col2:
                            st.markdown("""
                            **Central keywords** connect multiple research topics.
                            
                            These are often:
                            - Interdisciplinary terms
                            - Foundational concepts
                            - Bridge topics
                            """)
                    
                    # Keyword clusters
                    if len(G.nodes()) >= 5:
                        st.markdown("### 🎯 Topic Clusters")
                        
                        try:
                            communities = nx.community.greedy_modularity_communities(G)
                            st.info(f"🔍 Detected {len(communities)} topic clusters")
                            
                            sorted_communities = sorted(communities, key=len, reverse=True)[:5]
                            
                            for i, community in enumerate(sorted_communities, 1):
                                with st.expander(f"Cluster {i}: {len(community)} keywords"):
                                    keywords = [kw.title() for kw in list(community)[:30]]
                                    st.write(", ".join(keywords))
                        except:
                            st.warning("Unable to detect clusters with current network structure")

else:
    st.info("🚧 This network type is coming soon!")
    st.markdown("""
    **Planned Features:**
    
    **Citation Network:**
    - Visualize citation relationships between publications
    - Identify influential papers
    - Track knowledge flow
    
    **Institution Collaboration:**
    - Map inter-institutional research networks
    - Identify collaboration hubs
    - Geographic distribution of partnerships
    """)

# Export options
st.markdown("---")
st.markdown("### 💾 Export Network Data")

col1, col2 = st.columns(2)

with col1:
    st.button("📥 Download Network (GraphML)", disabled=True, use_container_width=True)
    st.caption("Export network for analysis in Gephi, Cytoscape, etc.")

with col2:
    st.button("📊 Download Metrics (CSV)", disabled=True, use_container_width=True)
    st.caption("Export network statistics and centrality scores")
