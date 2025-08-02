import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
import numpy as np

# Configure page
st.set_page_config(
    page_title="Malaysia Agricultural Land Use Dashboard",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Times New Roman and clean styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');
    
    .main {
        font-family: 'Times New Roman', serif;
        background-color: white;
    }
    
    .stTitle {
        font-family: 'Times New Roman', serif;
        color: #2E4057;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Times New Roman', serif;
    }
    
    .timeline-item {
        background-color: #f8f9fa;
        border-left: 4px solid #2E4057;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        font-family: 'Times New Roman', serif;
    }
    
    .felda-card {
        background-color: #e8f4fd;
        border: 2px solid #2E4057;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-family: 'Times New Roman', serif;
    }
    
    .insight-box {
        background-color: #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: 'Times New Roman', serif;
    }
    
    .trade-box {
        background-color: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Times New Roman', serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Times New Roman', serif;
        color: #2E4057;
    }
</style>
""", unsafe_allow_html=True)

# Title and Introduction
st.markdown('<h1 class="stTitle">🇲🇾 Malaysia Agricultural Land Use Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #6c757d; font-family: Times New Roman, serif;">Historical Evolution from Colonial Times to Present (1900-2024)</p>', unsafe_allow_html=True)

# Create comprehensive data
@st.cache_data
def load_data():
    # Historical ownership data
    ownership_data = pd.DataFrame({
        'Year': [1920, 1940, 1957, 1980, 2000, 2024],
        'European_Corporate': [73, 70, 65, 55, 49, 45],
        'FELDA_Schemes': [0, 0, 5, 15, 25, 33],
        'Independent_Smallholders': [25, 28, 25, 25, 20, 15],
        'State_Schemes': [2, 2, 5, 5, 6, 7]
    })
    
    # Enhanced crop data with import/export values
    crop_data = pd.DataFrame({
        'Crop': ['Oil Palm', 'Rubber', 'Rice', 'Coconut', 'Durian', 'Cocoa', 'Pepper'],
        'Area_Million_Ha': [5.67, 1.2, 0.68, 0.4, 0.15, 0.05, 0.02],
        'Export_Value_Billion_USD': [22.3, 3.2, 0.1, 0.5, 1.2, 0.3, 0.15],
        'Import_Value_Billion_USD': [0.2, 0.1, 2.8, 0.05, 0.02, 0.4, 0.01],
        'Net_Trade_Billion_USD': [22.1, 3.1, -2.7, 0.45, 1.18, -0.1, 0.14],
        'Smallholder_Percentage': [45, 94, 85, 78, 60, 96, 75],
        'Production_Million_Tonnes': [19.3, 0.35, 2.8, 0.6, 0.4, 0.02, 0.025]
    })
    
    # Enhanced state data with FELDA details and corporate presence
    state_data = pd.DataFrame({
        'State': ['Johor', 'Pahang', 'Perak', 'Selangor', 'Negeri Sembilan', 
                 'Kedah', 'Kelantan', 'Terengganu', 'Sabah', 'Sarawak'],
        'Oil_Palm_Ha': [750000, 680000, 380000, 280000, 180000, 
                       120000, 140000, 160000, 1500000, 1200000],
        'Rubber_Ha': [150000, 120000, 200000, 80000, 60000,
                     100000, 80000, 70000, 200000, 180000],
        'FELDA_Schemes': [45, 89, 12, 8, 6, 15, 22, 18, 35, 25],
        'FELDA_Settlers': [112000, 186000, 28000, 18000, 14000, 
                          35000, 52000, 42000, 89000, 64000],
        'Corporate_Estates_Ha': [400000, 300000, 180000, 150000, 100000,
                               60000, 70000, 80000, 900000, 750000],
        'Smallholder_Ha': [500000, 500000, 400000, 210000, 140000,
                          175000, 150000, 150000, 835000, 630000],
        'Major_Companies': ['IOI Corp, KLK', 'Felda Global, Genting Plant', 'Kuala Lumpur Kepong', 
                          'Sime Darby', 'IOI Corp', 'Guthrie, TH Plant', 'Felda Global', 
                          'TDM Berhad', 'Wilmar, Sabah Softwoods', 'Shin Yang, Rimbunan Hijau'],
        'Latitude': [1.4854, 3.8126, 4.5921, 3.0738, 2.7297,
                    6.1184, 6.1254, 5.3117, 5.9804, 1.5533],
        'Longitude': [103.7618, 103.3256, 101.0901, 101.5183, 101.9424,
                     100.3681, 102.2386, 103.1324, 116.0735, 110.3592]
    })
    
    # Export growth data
    export_data = pd.DataFrame({
        'Year': [1960, 1970, 1980, 1990, 2000, 2010, 2020, 2024],
        'Palm_Oil_Million_Tonnes': [0.1, 0.8, 4.5, 8.9, 13.2, 17.1, 18.0, 19.3],
        'Rubber_Million_Tonnes': [1.2, 1.5, 1.8, 1.2, 0.9, 0.8, 0.6, 0.35],
        'Palm_Oil_Value_Billion_USD': [0.05, 0.4, 2.8, 6.2, 10.8, 16.5, 19.2, 22.3],
        'Rubber_Value_Billion_USD': [2.1, 2.8, 4.2, 3.8, 2.9, 3.1, 2.8, 3.2]
    })
    
    # FELDA historical data
    felda_data = pd.DataFrame({
        'Year': [1956, 1960, 1970, 1980, 1990, 2000, 2010, 2024],
        'Schemes_Opened': [0, 12, 78, 156, 234, 289, 312, 317],
        'Settlers_Families': [0, 8500, 52000, 89000, 112000, 118000, 112500, 123000],
        'Land_Developed_Ha': [0, 48000, 312000, 624000, 936000, 1156000, 1248000, 1268000],
        'Oil_Palm_Ha': [0, 15000, 180000, 450000, 680000, 820000, 860000, 875000]
    })
    
    return ownership_data, crop_data, state_data, export_data, felda_data

ownership_data, crop_data, state_data, export_data, felda_data = load_data()

# Sidebar for navigation
st.sidebar.markdown("## Navigation")
section = st.sidebar.selectbox(
    "Choose Section:",
    ["Overview", "FELDA Vision & History", "Interactive Plantation Map", "Trade Analysis", "Historical Timeline", "Economic Analysis", "Insights"]
)

if section == "Overview":
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2E4057; margin: 0;">5.67M</h3>
            <p style="margin: 0; color: #6c757d;">Hectares Oil Palm (2024)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2E4057; margin: 0;">$22.3B</h3>
            <p style="margin: 0; color: #6c757d;">Palm Oil Export Value</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2E4057; margin: 0;">317</h3>
            <p style="margin: 0; color: #6c757d;">FELDA Schemes Active</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2E4057; margin: 0;">123K</h3>
            <p style="margin: 0; color: #6c757d;">FELDA Settler Families</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Current crop distribution
    st.subheader("Current Agricultural Land Distribution (2024)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie = px.pie(
            crop_data, 
            values='Area_Million_Ha', 
            names='Crop',
            title="Land Distribution by Crop (Million Hectares)",
            color_discrete_sequence=['#2E4057', '#548CA8', '#334257', '#476072', '#8B9DC3', '#A8DADC', '#B8B8B8']
        )
        fig_pie.update_layout(
            font_family="Times New Roman",
            title_font_family="Times New Roman",
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Net trade balance
        fig_trade = px.bar(
            crop_data,
            x='Crop',
            y='Net_Trade_Billion_USD',
            title="Net Trade Balance by Crop (Billion USD)",
            color='Net_Trade_Billion_USD',
            color_continuous_scale=['#dc3545', '#ffffff', '#28a745']
        )
        fig_trade.update_layout(
            font_family="Times New Roman",
            title_font_family="Times New Roman",
            paper_bgcolor='white',
            plot_bgcolor='white',
            showlegend=False
        )
        fig_trade.add_hline(y=0, line_dash="dash", line_color="black")
        st.plotly_chart(fig_trade, use_container_width=True)

elif section == "FELDA Vision & History":
    st.markdown("""
    <div class="felda-card">
        <h2 style="color: #2E4057; text-align: center;">🏛️ FELDA: Transforming Rural Malaysia Since 1956</h2>
        <p style="text-align: center; font-size: 1.1rem; margin: 0;">Federal Land Development Authority - A Vision of Rural Prosperity</p>
    </div>
    """, unsafe_allow_html=True)
    
    # FELDA Vision and Mission
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🎯 FELDA Vision
        **"To be a world-class organization in sustainable plantation development and agribusiness."**
        
        #### 📋 Original Mission (1956)
        - **Poverty Eradication**: Provide land to landless rural poor
        - **National Unity**: Integrate different ethnic communities
        - **Economic Development**: Develop plantation agriculture
        - **Rural Transformation**: Create modern rural communities
        """)
    
    with col2:
        st.markdown("""
        #### 🏗️ FELDA Model Components
        - **Land Allocation**: 4 hectares per settler family
        - **Infrastructure**: Houses, schools, clinics, mosques
        - **Technical Support**: Agricultural extension services
        - **Financial Aid**: Loans and subsidies during establishment
        - **Community Development**: Cooperative societies and associations
        """)
    
    # FELDA Growth Timeline
    st.subheader("📈 FELDA Development Timeline (1956-2024)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_schemes = go.Figure()
        fig_schemes.add_trace(go.Scatter(
            x=felda_data['Year'],
            y=felda_data['Schemes_Opened'],
            mode='lines+markers',
            name='FELDA Schemes',
            line=dict(color='#2E4057', width=4),
            marker=dict(size=8)
        ))
        fig_schemes.update_layout(
            title="FELDA Schemes Development",
            xaxis_title="Year",
            yaxis_title="Number of Schemes",
            font_family="Times New Roman",
            title_font_family="Times New Roman",
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        st.plotly_chart(fig_schemes, use_container_width=True)
    
    with col2:
        fig_settlers = go.Figure()
        fig_settlers.add_trace(go.Scatter(
            x=felda_data['Year'],
            y=felda_data['Settlers_Families'],
            mode='lines+markers',
            name='Settler Families',
            line=dict(color='#548CA8', width=4),
            marker=dict(size=8),
            fill='tonexty'
        ))
        fig_settlers.update_layout(
            title="FELDA Settler Families Growth",
            xaxis_title="Year",
            yaxis_title="Number of Families",
            font_family="Times New Roman",
            title_font_family="Times New Roman",
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        st.plotly_chart(fig_settlers, use_container_width=True)
    
    # FELDA Corporate Evolution
    st.subheader("🏢 FELDA Corporate Structure Evolution")
    
    st.markdown("""
    <div class="timeline-item">
        <h4 style="color: #2E4057;">1956-1980: Government Agency Era</h4>
        <p>FELDA operated as a government development agency focusing purely on land settlement and smallholder development.</p>
    </div>
    
    <div class="timeline-item">
        <h4 style="color: #2E4057;">1980-2000: Commercialization Phase</h4>
        <p>Established FELDA Holdings to manage commercial plantations and processing facilities. Began vertical integration into palm oil milling and refining.</p>
    </div>
    
    <div class="timeline-item">
        <h4 style="color: #2E4057;">2000-2012: Corporate Expansion</h4>
        <p>Created multiple subsidiaries including FELDA Global Ventures (FGV), expanded into downstream industries, and developed global operations.</p>
    </div>
    
    <div class="timeline-item">
        <h4 style="color: #2E4057;">2012-Present: Public-Private Model</h4>
        <p>FGV became publicly listed (2012), creating hybrid model where FELDA maintains development role while FGV operates commercial businesses.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Current FELDA Structure
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
            <h4 style="color: #2E4057;">👥 FELDA (Development)</h4>
            <ul>
                <li>Land development authority</li>
                <li>Settler welfare & support</li>
                <li>Community development</li>
                <li>Social infrastructure</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
            <h4 style="color: #2E4057;">🏭 FGV Holdings (Commercial)</h4>
            <ul>
                <li>Plantation management</li>
                <li>Palm oil processing</li>
                <li>Global trading</li>
                <li>Downstream products</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="insight-box">
            <h4 style="color: #2E4057;">🤝 Settler Cooperatives</h4>
            <ul>
                <li>Individual land ownership</li>
                <li>Cooperative societies</li>
                <li>Profit sharing</li>
                <li>Community participation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif section == "Interactive Plantation Map":
    st.subheader("🗺️ Interactive Malaysian Plantation Map")
    st.markdown("**Click on states to see detailed breakdown of corporate estates, FELDA schemes, and smallholders**")
    
    # Map type selection
    map_type = st.selectbox(
        "Select Map View:",
        ["Ownership Structure", "FELDA Distribution", "Corporate Presence"]
    )
    
    # Create base map
    m = folium.Map(
        location=[4.2105, 101.9758],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Add state data based on selected view
    for idx, row in state_data.iterrows():
        if map_type == "Ownership Structure":
            # Pie chart-like visualization for ownership
            corporate_pct = (row['Corporate_Estates_Ha'] / (row['Oil_Palm_Ha'] + row['Rubber_Ha'])) * 100
            smallholder_pct = (row['Smallholder_Ha'] / (row['Oil_Palm_Ha'] + row['Rubber_Ha'])) * 100
            felda_pct = 100 - corporate_pct - smallholder_pct
            
            popup_content = f"""
            <div style="font-family: Times New Roman; width: 300px;">
                <h4 style="color: #2E4057; margin-bottom: 10px;">{row['State']} - Ownership Structure</h4>
                <p><strong>🏢 Corporate Estates:</strong> {row['Corporate_Estates_Ha']:,} ha ({corporate_pct:.1f}%)</p>
                <p><strong>🏛️ FELDA Schemes:</strong> {row['FELDA_Schemes']} schemes, {row['FELDA_Settlers']:,} families</p>
                <p><strong>👨‍🌾 Smallholders:</strong> {row['Smallholder_Ha']:,} ha ({smallholder_pct:.1f}%)</p>
                <p><strong>🌴 Total Oil Palm:</strong> {row['Oil_Palm_Ha']:,} ha</p>
                <p><strong>🔴 Total Rubber:</strong> {row['Rubber_Ha']:,} ha</p>
                <hr>
                <p><strong>Major Companies:</strong> {row['Major_Companies']}</p>
            </div>
            """
            color = '#2E4057'
            
        elif map_type == "FELDA Distribution":
            popup_content = f"""
            <div style="font-family: Times New Roman; width: 280px;">
                <h4 style="color: #548CA8; margin-bottom: 10px;">{row['State']} - FELDA Programs</h4>
                <p><strong>📊 FELDA Schemes:</strong> {row['FELDA_Schemes']}</p>
                <p><strong>👨‍👩‍👧‍👦 Settler Families:</strong> {row['FELDA_Settlers']:,}</p>
                <p><strong>💰 Est. Annual Income:</strong> ${(row['FELDA_Settlers'] * 12000):,}</p>
                <p><strong>🏠 Communities Established:</strong> {row['FELDA_Schemes'] * 3}</p>
                <p><strong>🎓 Schools Built:</strong> {row['FELDA_Schemes'] * 2}</p>
                <p><strong>🏥 Health Clinics:</strong> {row['FELDA_Schemes']}</p>
            </div>
            """
            color = '#548CA8'
            
        else:  # Corporate Presence
            popup_content = f"""
            <div style="font-family: Times New Roman; width: 280px;">
                <h4 style="color: #334257; margin-bottom: 10px;">{row['State']} - Corporate Plantations</h4>
                <p><strong>🏢 Estate Area:</strong> {row['Corporate_Estates_Ha']:,} hectares</p>
                <p><strong>📈 Est. Production:</strong> {(row['Corporate_Estates_Ha'] * 20):,} tonnes CPO/year</p>
                <p><strong>💼 Major Corporations:</strong></p>
                <p style="font-size: 0.9em;">{row['Major_Companies']}</p>
                <p><strong>👷 Est. Employment:</strong> {(row['Corporate_Estates_Ha'] // 10):,} workers</p>
                <p><strong>🏭 Processing Mills:</strong> {max(1, row['Corporate_Estates_Ha'] // 50000)} facilities</p>
            </div>
            """
            color = '#334257'
        
        # Circle size based on total plantation area
        radius = ((row['Oil_Palm_Ha'] + row['Rubber_Ha']) / 100000) + 8
        
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=radius,
            popup=folium.Popup(popup_content, max_width=350),
            color=color,
            fillColor=color,
            fillOpacity=0.6,
            weight=3
        ).add_to(m)
        
        # Add state labels
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            icon=folium.DivIcon(
                html=f'<div style="font-family: Times New Roman; font-size: 11px; color: {color}; font-weight: bold; text-shadow: 1px 1px 1px white;">{row["State"]}</div>',
                icon_size=(60, 20),
                icon_anchor=(30, 10)
            )
        ).add_to(m)
    
    # Add legend based on map type
    if map_type == "Ownership Structure":
        legend_html = '''
        <div style="position: fixed; bottom: 50px; left: 50px; width: 180px; height: 110px; 
                    background-color: white; border: 2px solid grey; z-index: 9999; 
                    font-size: 12px; font-family: Times New Roman; padding: 10px;">
        <h5 style="margin: 0 0 10px 0;">Ownership Structure</h5>
        <p style="margin: 2px;"><span style="color: #2E4057;">●</span> Corporate Estates</p>
        <p style="margin: 2px;"><span style="color: #548CA8;">●</span> FELDA Schemes</p>
        <p style="margin: 2px;"><span style="color: #334257;">●</span> Smallholders</p>
        <p style="margin: 5px 0 0 0; font-size: 10px;">Circle size = Total plantation area</p>
        </div>
        '''
    elif map_type == "FELDA Distribution":
        legend_html = '''
        <div style="position: fixed; bottom: 50px; left: 50px; width: 160px; height: 100px; 
                    background-color: white; border: 2px solid grey; z-index: 9999; 
                    font-size: 12px; font-family: Times New Roman; padding: 10px;">
        <h5 style="margin: 0 0 10px 0;">FELDA Programs</h5>
        <p style="margin: 2px;">🏛️ FELDA Schemes</p>
        <p style="margin: 2px;">👨‍👩‍👧‍👦 Settler Families</p>
        <p style="margin: 2px;">🏠 Community Infrastructure</p>
        <p style="margin: 5px 0 0 0; font-size: 10px;">Click for detailed info</p>
        </div>
        '''
    else:
        legend_html = '''
        <div style="position: fixed; bottom: 50px; left: 50px; width: 160px; height: 100px; 
                    background-color: white; border: 2px solid grey; z-index: 9999; 
                    font-size: 12px; font-family: Times New Roman; padding: 10px;">
        <h5 style="margin: 0 0 10px 0;">Corporate Presence</h5>
        <p style="margin: 2px;">🏢 Estate Areas</p>
        <p style="margin: 2px;">🏭 Processing Facilities</p>
        <p style="margin: 2px;">👷 Employment Impact</p>
        <p style="margin: 5px 0 0 0; font-size: 10px;">Major plantation companies</p>
        </div>
        '''
    
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Display map
    map_data = st_folium(m, width=700, height=500)
    
    st.markdown("---")
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_corporate = state_data['Corporate_Estates_Ha'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #2E4057; margin: 0;">🏢 Corporate Estates</h4>
            <p style="margin: 5px 0;"><strong>{total_corporate:,}</strong> hectares</p>
            <p style="margin: 0; font-size: 0.9em;">Major companies across {len(state_data)} states</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_felda_schemes = state_data['FELDA_Schemes'].sum()
        total_settlers = state_data['FELDA_Settlers'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #548CA8; margin: 0;">🏛️ FELDA Programs</h4>
            <p style="margin: 5px 0;"><strong>{total_felda_schemes}</strong> schemes</p>
            <p style="margin: 0; font-size: 0.9em;"><strong>{total_settlers:,}</strong> settler families</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_smallholder = state_data['Smallholder_Ha'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #334257; margin: 0;">👨‍🌾 Smallholders</h4>
            <p style="margin: 5px 0;"><strong>{total_smallholder:,}</strong> hectares</p>
            <p style="margin: 0; font-size: 0.9em;">Independent farmers nationwide</p>
        </div>
        """, unsafe_allow_html=True)

elif section == "Trade Analysis":
    st.subheader("📊 Import/Export Analysis by Crop")
    
    # Trade overview
    col1, col2 = st.columns(2)
    
    with col1:
        # Export vs Import comparison
        fig_trade_compare = go.Figure()
        
        fig_trade_compare.add_trace(go.Bar(
            name='Exports',
            x=crop_data['Crop'],
            y=crop_data['Export_Value_Billion_USD'],
            marker_color='#28a745',
            yaxis='y'
        ))
        
        fig_trade_compare.add_trace(go.Bar(
            name='Imports',
            x=crop_data['Crop'],
            y=crop_data['Import_Value_Billion_USD'],
            marker_color='#dc3545',
            yaxis='y'
        ))
        
        fig_trade_compare.update_layout(
            title='Export vs Import Values by Crop (2024)',
            xaxis_title='Crop',
            yaxis_title='Value (Billion USD)',
            font_family="Times New Roman",
            title_font_family="Times New Roman",
            paper_bgcolor='white',
            plot_bgcolor='white',
            barmode='group'
        )
        
        st.plotly_chart(fig_trade_compare, use_container_width=True)
    
    with col2:
        # Net trade balance
        fig_net_trade = px.bar(
            crop_data,
            x='Crop',
            y='Net_Trade_Billion_USD',
            title='Net Trade Balance by Crop (2024)',
            color='Net_Trade_Billion_USD',
            color_continuous_scale=['#dc3545', '#ffffff', '#28a745'],
            labels={'Net_Trade_Billion_USD': 'Net Trade (Billion USD)'}
        )
        
        fig_net_trade.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Trade Balance")
        
        fig_net_trade.update_layout(
            font_family="Times New Roman",
            title_font_family="Times New Roman",
            paper_bgcolor='white',
            plot_bgcolor='white',
            showlegend=False
        )
        
        st.plotly_chart(fig_net_trade, use_container_width=True)
    
    # Detailed trade data table
    st.subheader("📋 Detailed Trade Data (2024)")
    
    trade_display = crop_data[['Crop', 'Production_Million_Tonnes', 'Export_Value_Billion_USD', 
                              'Import_Value_Billion_USD', 'Net_Trade_Billion_USD']].copy()
    
    trade_display.columns = ['Crop', 'Production (Million Tonnes)', 'Exports (Billion USD)', 
                           'Imports (Billion USD)', 'Net Trade (Billion USD)']
    
    # Color coding for the dataframe
    def color_trade_balance(val):
        if isinstance(val, (int, float)):
            if val > 0:
                return 'background-color: #d4edda; color: #155724'  # Green for surplus
            elif val < 0:
                return 'background-color: #f8d7da; color: #721c24'  # Red for deficit
        return ''
    
    styled_df = trade_display.style.applymap(color_trade_balance, subset=['Net Trade (Billion USD)'])
    st.dataframe(styled_df, use_container_width=True)
    
    # Trade insights
    st.subheader("💡 Trade Analysis Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        surplus_crops = crop_data[crop_data['Net_Trade_Billion_USD'] > 0]
        st.markdown(f"""
        <div class="trade-box">
            <h4 style="color: #155724;">✅ Export Champions (Trade Surplus)</h4>
            <ul>
        """, unsafe_allow_html=True)
        
        for _, crop in surplus_crops.iterrows():
            st.markdown(f"<li><strong>{crop['Crop']}:</strong> +${crop['Net_Trade_Billion_USD']:.1f}B net export</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)
    
    with col2:
        deficit_crops = crop_data[crop_data['Net_Trade_Billion_USD'] < 0]
        st.markdown(f"""
        <div style="background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; font-family: Times New Roman, serif;">
            <h4 style="color: #721c24;">⚠️ Import Dependent (Trade Deficit)</h4>
            <ul>
        """, unsafe_allow_html=True)
        
        for _, crop in deficit_crops.iterrows():
            st.markdown(f"<li><strong>{crop['Crop']}:</strong> -${abs(crop['Net_Trade_Billion_USD']):.1f}B net import</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)
    
    # Export trends over time
    st.subheader("📈 Historical Export Value Trends")
    
    fig_export_trends = go.Figure()
    
    fig_export_trends.add_trace(go.Scatter(
        x=export_data['Year'],
        y=export_data['Palm_Oil_Value_Billion_USD'],
        mode='lines+markers',
        name='Palm Oil',
        line=dict(color='#2E4057', width=4),
        marker=dict(size=8)
    ))
    
    fig_export_trends.add_trace(go.Scatter(
        x=export_data['Year'],
        y=export_data['Rubber_Value_Billion_USD'],
        mode='lines+markers',
        name='Rubber',
        line=dict(color='#548CA8', width=4),
        marker=dict(size=8)
    ))
    
    fig_export_trends.update_layout(
        title='Historical Export Value Growth (1960-2024)',
        xaxis_title='Year',
        yaxis_title='Export Value (Billion USD)',
        font_family="Times New Roman",
        title_font_family="Times New Roman",
        paper_bgcolor='white',
        plot_bgcolor='white',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_export_trends, use_container_width=True)

elif section == "Historical Timeline":
    st.subheader("Historical Evolution of Malaysian Agriculture")
    
    timeline_data = [
        {
            'period': '1900s-1920s (Colonial Era)',
            'description': 'British Plantation System: Large rubber estates dominated by European companies (73% ownership). Tin mining and rubber exports formed economic backbone. Malays restricted to rice cultivation through land reservation laws.'
        },
        {
            'period': '1920s-1940s',
            'description': 'Rubber Boom: Malaysia became world\'s largest rubber exporter. 1.1M acres of rubber by 1924 - 55% on European estates, 25% Malay smallholders. First commercial oil palm estate established in 1917.'
        },
        {
            'period': '1956 - FELDA Establishment',
            'description': 'Federal Land Development Authority created to eradicate rural poverty. Revolutionary approach: provide 4 hectares of land per family, complete with housing, infrastructure, and technical support. Beginning of Malaysia\'s most successful rural development program.'
        },
        {
            'period': '1957-1960s (Independence)',
            'description': 'Diversification Policy: Government reduced dependency on rubber and tin. FELDA schemes expanded rapidly - 12 schemes by 1960, growing to 78 by 1970. Each settler received comprehensive support package including loans, housing, and agricultural training.'
        },
        {
            'period': '1980s-1990s',
            'description': 'Palm Oil Expansion: Major plantation companies nationalized (Guthrie, Golden Hope, Sime Darby). FELDA reached 156 schemes by 1980 with 89,000 settler families. Palm oil plantations expanded rapidly as rubber prices declined.'
        },
        {
            'period': '2000s-Present',
            'description': 'Sustainable Agriculture: Malaysia caps palm oil at 6.5M hectares, maintaining 50% forest cover. FELDA operates 317 schemes with 123,000 families. Smallholders now cultivate 45% of oil palm, 94% of rubber, 96% of cocoa.'
        }
    ]
    
    for item in timeline_data:
        st.markdown(f"""
        <div class="timeline-item">
            <h4 style="color: #2E4057; margin-bottom: 0.5rem;">{item['period']}</h4>
            <p style="margin: 0; line-height: 1.6;">{item['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Land ownership evolution chart
    st.subheader("📈 Land Ownership Evolution (1920-2024)")
    
    fig_ownership = go.Figure()
    
    fig_ownership.add_trace(go.Scatter(
        x=ownership_data['Year'],
        y=ownership_data['European_Corporate'],
        mode='lines+markers',
        name='European/Corporate Estates',
        line=dict(color='#2E4057', width=3),
        fill='tonexty'
    ))
    
    fig_ownership.add_trace(go.Scatter(
        x=ownership_data['Year'],
        y=ownership_data['FELDA_Schemes'],
        mode='lines+markers',
        name='FELDA Schemes',
        line=dict(color='#548CA8', width=3),
        fill='tonexty'
    ))
    
    fig_ownership.add_trace(go.Scatter(
        x=ownership_data['Year'],
        y=ownership_data['Independent_Smallholders'],
        mode='lines+markers',
        name='Independent Smallholders',
        line=dict(color='#334257', width=3),
        fill='tonexty'
    ))
    
    fig_ownership.add_trace(go.Scatter(
        x=ownership_data['Year'],
        y=ownership_data['State_Schemes'],
        mode='lines+markers',
        name='State Schemes',
        line=dict(color='#476072', width=3),
        fill='tonexty'
    ))
    
    fig_ownership.update_layout(
        title="Land Ownership Distribution Evolution (%)",
        xaxis_title="Year",
        yaxis_title="Percentage (%)",
        font_family="Times New Roman",
        title_font_family="Times New Roman",
        paper_bgcolor='white',
        plot_bgcolor='white',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_ownership, use_container_width=True)

elif section == "Economic Analysis":
    st.subheader("Economic Impact Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export growth over time
        fig_export = go.Figure()
        
        fig_export.add_trace(go.Scatter(
            x=export_data['Year'],
            y=export_data['Palm_Oil_Million_Tonnes'],
            mode='lines+markers',
            name='Palm Oil (Million Tonnes)',
            line=dict(color='#2E4057', width=3),
            yaxis='y'
        ))
        
        fig_export.add_trace(go.Scatter(
            x=export_data['Year'],
            y=export_data['Rubber_Million_Tonnes'],
            mode='lines+markers',
            name='Rubber (Million Tonnes)',
            line=dict(color='#548CA8', width=3),
            yaxis='y'
        ))
        
        fig_export.update_layout(
            title="Agricultural Export Growth (1960-2024)",
            xaxis_title="Year",
            yaxis_title="Million Tonnes",
            font_family="Times New Roman",
            title_font_family="Times New Roman",
            paper_bgcolor='white',
            plot_bgcolor='white',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_export, use_container_width=True)
    
    with col2:
        # Smallholder contribution
        fig_smallholder = px.bar(
            crop_data,
            x='Crop',
            y='Smallholder_Percentage',
            title="Smallholder Share by Crop (%)",
            color='Smallholder_Percentage',
            color_continuous_scale=['#E8F4FD', '#2E4057']
        )
        fig_smallholder.update_layout(
            font_family="Times New Roman",
            title_font_family="Times New Roman",
            paper_bgcolor='white',
            plot_bgcolor='white',
            showlegend=False
        )
        st.plotly_chart(fig_smallholder, use_container_width=True)
    
    # Economic indicators
    st.markdown("### Key Economic Indicators (2024)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
            <h4 style="color: #2E4057;">GDP Contribution</h4>
            <ul style="margin: 0;">
                <li>Agriculture: 5.3% of total GDP</li>
                <li>Palm oil: 2.0% of GDP</li>
                <li>Export share: 12.2% of total exports</li>
                <li>Total export value: $32.5B</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
            <h4 style="color: #2E4057;">Employment Impact</h4>
            <ul style="margin: 0;">
                <li>Agricultural workforce: ~10% of total</li>
                <li>FELDA settler families: 123,000</li>
                <li>Smallholder families: >1.2 million</li>
                <li>Plantation workers: ~650,000</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="insight-box">
            <h4 style="color: #2E4057;">Global Position</h4>
            <ul style="margin: 0;">
                <li>2nd largest palm oil producer</li>
                <li>Largest palm oil exporter</li>
                <li>26% of world palm oil production</li>
                <li>34% of world palm oil exports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif section == "Insights":
    st.subheader("Key Insights and Analysis")
    
    insights = [
        {
            'title': 'Colonial Legacy and Transformation',
            'content': 'British colonial policies created lasting inequality in land ownership, with Europeans controlling 73% of plantation agriculture in the 1920s. However, Malaysia\'s post-independence policies, particularly FELDA, successfully transformed this structure. Today, smallholders control 45% of oil palm and 94% of rubber production, demonstrating remarkable rural transformation.'
        },
        {
            'title': 'FELDA: World-Class Rural Development Model',
            'content': 'FELDA represents one of the world\'s most successful rural development programs. From its establishment in 1956 to today\'s 317 schemes serving 123,000 families, FELDA has lifted entire communities out of poverty. The model combines land allocation (4 hectares per family), infrastructure development, and technical support, creating sustainable rural economies.'
        },
        {
            'title': 'Trade Balance Success Story',
            'content': 'Malaysia maintains a strong agricultural trade surplus of $20.1 billion, led by palm oil exports ($22.3B) and rubber ($3.2B). However, the country remains import-dependent for rice ($2.8B deficit), highlighting food security challenges despite agricultural success in cash crops.'
        },
        {
            'title': 'Corporate-Smallholder Coexistence',
            'content': 'Malaysia has achieved a unique balance between large-scale corporate efficiency and smallholder inclusivity. Major corporations like IOI, Sime Darby, and FGV operate alongside 1.2 million smallholder families, creating a diversified agricultural ecosystem that benefits from both economies of scale and grassroots participation.'
        },
        {
            'title': 'Sustainability Challenge and Innovation',
            'content': 'With palm oil expansion capped at 6.5 million hectares and 50% forest cover maintained, Malaysia must focus on productivity improvements rather than area expansion. This constraint drives innovation in sustainable practices, precision agriculture, and value-added processing to maintain competitiveness.'
        },
        {
            'title': 'FELDA Corporate Evolution Impact',
            'content': 'FELDA\'s transformation from government agency to hybrid public-private model (with FGV Holdings) demonstrates institutional evolution. While this brought commercial efficiency and global reach, it also created tensions between development objectives and profit maximization, requiring careful balance to maintain settler welfare.'
        }
    ]
    
    for insight in insights:
        st.markdown(f"""
        <div class="insight-box">
            <h4 style="color: #2E4057; margin-bottom: 10px;">{insight['title']}</h4>
            <p style="line-height: 1.6; margin: 0;">{insight['content']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Future outlook
    st.subheader("Future Outlook and Strategic Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🌟 Strategic Opportunities
        - **Productivity Enhancement**: Focus on yield improvements through R&D and precision agriculture
        - **Value-Added Processing**: Develop downstream industries and specialty products
        - **Sustainable Certification**: Meet international sustainability standards (RSPO, MSPO)
        - **Digital Agriculture**: Adopt IoT, AI, and precision farming technologies
        - **Crop Diversification**: Expand high-value crops like durian and specialty fruits
        - **FELDA 2.0**: Modernize FELDA schemes with young farmers and new technologies
        """)
    
    with col2:
        st.markdown("""
        #### ⚠️ Strategic Challenges
        - **Land Scarcity**: Limited expansion opportunities require intensive productivity focus
        - **Environmental Pressure**: EU deforestation regulations and certification requirements
        - **Aging Workforce**: Second-generation FELDA settlers and smallholder succession issues
        - **Climate Change**: Weather variability affects yields and long-term sustainability
        - **Market Access**: Trade restrictions and changing global palm oil demand patterns
        - **Food Security**: Rice import dependency requires domestic production enhancement
        """)

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #6c757d; font-family: Times New Roman, serif; font-size: 0.9rem;">Data sources: Malaysian Palm Oil Board (MPOB), FELDA, Department of Statistics Malaysia, World Bank, Ministry of Plantation Industries and Commodities</p>',
    unsafe_allow_html=True
)
