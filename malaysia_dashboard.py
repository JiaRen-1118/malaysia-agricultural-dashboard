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
    
    .env-card {
        background-color: #f0f9ff;
        border: 1px solid #2E4057;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Times New Roman', serif;
    }
    
    .alert-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Times New Roman', serif;
    }
    
    .success-box {
        background-color: #d1f2eb;
        border: 1px solid #a3e9d1;
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
    
    # Environmental data for new section
    env_funding_data = pd.DataFrame({
        'Mechanism': ['ACGF', 'Green Climate Fund', 'China-ASEAN Fund', 'ASEAN-Korea Fund', 'Australia GIP', 'Singapore Green Bonds'],
        'Amount_Million_USD': [1800, 300, 10000, 45, 50, 6000],
        'Focus_Area': ['Infrastructure', 'Climate Recovery', 'Infrastructure', 'Environment', 'Clean Energy', 'Green Finance'],
        'Coverage': ['ASEAN-wide', 'SEA Regional', 'ASEAN', 'ASEAN', 'SEA', 'Singapore']
    })
    
    plastic_policy_data = pd.DataFrame({
        'Metric': ['Plastic Bag Usage Reduction', 'Voluntary Clean-ups Increase', 'Public Awareness Increase', 'Penang Recycling Rate'],
        'Percentage': [30, 40, 50, 200],
        'Status': ['Achieved', 'Achieved', 'Achieved', 'Exceeded']
    })
    
    fire_data_2025 = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        'Malaysia_Fires': [12, 8, 15, 22, 18, 25, 31],
        'Indonesia_Fires': [45, 38, 89, 156, 134, 187, 245],
        'Regional_Total': [67, 52, 125, 203, 178, 234, 298]
    })
    
    ngo_achievements = pd.DataFrame({
        'Organization': ['Greenpeace SEA', 'SAM', 'Kuala Langat Group', 'WWF Malaysia', 'Lost Food Project'],
        'Achievement': ['Stopped Krabi Coal Plant', 'Right Livelihood Award', 'Closed 300+ illegal facilities', 'Restored 2,400 hectares', 'Prevented 6.78M kg emissions'],
        'Year': [2021, 1988, 2020, 2024, 2024],
        'Impact_Score': [95, 90, 85, 88, 82]
    })
    
    return ownership_data, crop_data, state_data, export_data, felda_data, env_funding_data, plastic_policy_data, fire_data_2025, ngo_achievements

ownership_data, crop_data, state_data, export_data, felda_data, env_funding_data, plastic_policy_data, fire_data_2025, ngo_achievements = load_data()

# Enhanced Sidebar for navigation
st.sidebar.markdown("## Navigation")
section = st.sidebar.selectbox(
    "Choose Section:",
    ["Overview", "FELDA Vision & History", "Interactive Plantation Map", "Trade Analysis", "Historical Timeline", "Economic Analysis", "Environmental Analysis", "Insights"]
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

elif section == "Environmental Analysis":
    st.markdown("""
    <div class="felda-card">
        <h2 style="color: #2E4057; text-align: center;">🌍 Environmental Protection & Sustainability Analysis</h2>
        <p style="text-align: center; font-size: 1.1rem; margin: 0;">Southeast Asia Environmental Funding, Policy Reactions & Forest Fire Crisis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Environmental metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2E4057; margin: 0;">$3.1T</h3>
            <p style="margin: 0; color: #6c757d;">SEA Climate Investment Needed by 2030</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2E4057; margin: 0;">$1.8B</h3>
            <p style="margin: 0; color: #6c757d;">ACGF Committed Funding</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2E4057; margin: 0;">30%</h3>
            <p style="margin: 0; color: #6c757d;">Plastic Bag Usage Reduction</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2E4057; margin: 0;">245</h3>
            <p style="margin: 0; color: #6c757d;">Active Fires (July 2025)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sub-navigation for environmental topics
    st.markdown("---")
    env_topic = st.selectbox(
        "Select Environmental Topic:",
        ["Funding Mechanisms", "Policy Reactions & Lynas Case", "Environmental Activism", "Current Forest Fire Crisis"]
    )
    
    if env_topic == "Funding Mechanisms":
        st.subheader("💰 Southeast Asia Environmental Funding Landscape")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Funding sources chart
            fig_funding = px.bar(
                env_funding_data,
                x='Mechanism',
                y='Amount_Million_USD',
                title="Major Environmental Funding Sources (Million USD)",
                color='Focus_Area',
                color_discrete_sequence=['#2E4057', '#548CA8', '#334257', '#476072', '#8B9DC3', '#A8DADC']
            )
            fig_funding.update_layout(
                font_family="Times New Roman",
                title_font_family="Times New Roman",
                paper_bgcolor='white',
                plot_bgcolor='white',
                xaxis={'categoryorder': 'total descending'}
            )
            fig_funding.update_xaxis(tickangle=45)
            st.plotly_chart(fig_funding, use_container_width=True)
        
        with col2:
            # Financing gap visualization
            gap_data = pd.DataFrame({
                'Year': [2020, 2022, 2024, 2025],
                'Required': [210, 210, 210, 210],
                'Available': [88, 118, 135, 158],
                'Gap': [122, 92, 75, 52]
            })
            
            fig_gap = go.Figure()
            fig_gap.add_trace(go.Scatter(
                x=gap_data['Year'],
                y=gap_data['Required'],
                mode='lines+markers',
                name='Required ($B annually)',
                line=dict(color='#dc3545', width=3)
            ))
            fig_gap.add_trace(go.Scatter(
                x=gap_data['Year'],
                y=gap_data['Available'],
                mode='lines+markers',
                name='Available ($B annually)',
                line=dict(color='#28a745', width=3)
            ))
            fig_gap.add_trace(go.Scatter(
                x=gap_data['Year'],
                y=gap_data['Gap'],
                mode='lines+markers',
                name='Financing Gap ($B)',
                line=dict(color='#2E4057', width=3)
            ))
            
            fig_gap.update_layout(
                title="Southeast Asia Climate Financing Gap",
                xaxis_title="Year",
                yaxis_title="Billion USD",
                font_family="Times New Roman",
                title_font_family="Times New Roman",
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            st.plotly_chart(fig_gap, use_container_width=True)
        
        # Funding details
        st.subheader("📋 Key Funding Mechanisms Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="env-card">
                <h4 style="color: #2E4057;">🏛️ ASEAN Catalytic Green Finance Facility (ACGF)</h4>
                <ul>
                    <li><strong>Established:</strong> April 2019</li>
                    <li><strong>Funding:</strong> $1.8B committed by 9 partners</li>
                    <li><strong>Target:</strong> 20+ high-impact projects</li>
                    <li><strong>Expected Impact:</strong> 119M tons CO2 reduction over 30 years</li>
                    <li><strong>Job Creation:</strong> 340,000 green jobs</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="env-card">
                <h4 style="color: #2E4057;">🌍 Green Climate Fund Programs</h4>
                <ul>
                    <li><strong>SEA Allocation:</strong> $300M for green recovery</li>
                    <li><strong>Priority Countries:</strong> Cambodia, Indonesia, Laos, Philippines</li>
                    <li><strong>Focus:</strong> Sustainable transport, renewable energy</li>
                    <li><strong>Leverage:</strong> $4+ billion in infrastructure projects</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="env-card">
                <h4 style="color: #2E4057;">🇨🇳 China-ASEAN Environmental Cooperation</h4>
                <ul>
                    <li><strong>Investment Fund:</strong> Up to $10B for infrastructure</li>
                    <li><strong>Strategy Period:</strong> 2021-2025</li>
                    <li><strong>Focus Areas:</strong> Ocean plastics, air quality, biodiversity</li>
                    <li><strong>Framework:</strong> ASEAN+3 coalition cooperation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="env-card">
                <h4 style="color: #2E4057;">🇦🇺 Australia & Others</h4>
                <ul>
                    <li><strong>Australia:</strong> AUD 75M Green Investment Partnership</li>
                    <li><strong>South Korea:</strong> $45M ASEAN-Korea Cooperation Fund</li>
                    <li><strong>Singapore:</strong> $6B+ green bond market</li>
                    <li><strong>Japan:</strong> Funding for peat fire solutions (NET-PEAT)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    elif env_topic == "Policy Reactions & Lynas Case":
        st.subheader("🏛️ Environmental Policy Reactions & Major Case Studies")
        
        # Plastic policy success metrics
        col1, col2 = st.columns(2)
        
        with col1:
            fig_plastic = px.bar(
                plastic_policy_data,
                x='Metric',
                y='Percentage',
                title="Malaysia Plastic Policy Success Metrics",
                color='Status',
                color_discrete_map={'Achieved': '#28a745', 'Exceeded': '#2E4057'}
            )
            fig_plastic.update_layout(
                font_family="Times New Roman",
                title_font_family="Times New Roman",
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            fig_plastic.update_xaxis(tickangle=45)
            st.plotly_chart(fig_plastic, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="success-box">
                <h4 style="color: #2E4057;">✅ Plastic Policy Achievements</h4>
                <ul>
                    <li><strong>Usage Reduction:</strong> 30% decrease in plastic bag usage</li>
                    <li><strong>Community Engagement:</strong> 40% increase in voluntary clean-ups</li>
                    <li><strong>Awareness:</strong> 50% improvement in public understanding</li>
                    <li><strong>Penang Success:</strong> 2x national recycling average</li>
                </ul>
                <p style="margin-top: 10px; font-size: 0.9em;"><em>Source: Research study of 262 households in Johor, 2024</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Lynas Case Study
        st.subheader("⚠️ Lynas Rare Earth Controversy: Complete Case Study")
        
        # Timeline
        lynas_timeline = pd.DataFrame({
            'Year': [2008, 2012, 2018, 2020, 2023],
            'Event': ['Concerns Raised in Parliament', 'Plant Operations Begin', 'Government Review Ordered', 'Waste Conditions Set', 'Operations Restricted'],
            'Impact': ['High Opposition', 'Public Protests', 'Policy Change', 'Regulation', 'Partial Victory'],
            'Stakeholder': ['MP Fuziah Salleh', 'Lynas Corporation', 'New Government', 'Minister Chang', 'Environmental Groups']
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="timeline-item">
                <h4 style="color: #2E4057;">📍 Causes & Background</h4>
                <ul>
                    <li><strong>Company:</strong> Lynas Corporation (Australian)</li>
                    <li><strong>Investment:</strong> A$1 billion processing plant in Kuantan, Pahang</li>
                    <li><strong>Historical Context:</strong> Previous Mitsubishi facility in Bukit Merah linked to birth defects, cost $99.2M cleanup</li>
                    <li><strong>Waste Production:</strong> 1+ million metric tons radioactive waste by 2023</li>
                </ul>
            </div>
            
            <div class="timeline-item">
                <h4 style="color: #2E4057;">⚡ Public Response & Actions</h4>
                <ul>
                    <li><strong>Parliamentary Action:</strong> MP Fuziah Salleh raised concerns since 2008</li>
                    <li><strong>Community Groups:</strong> "Concerned Citizens of Kuantan" formed 2008</li>
                    <li><strong>Legal Challenges:</strong> Court cases filed by residents</li>
                    <li><strong>Protests:</strong> Widespread demonstrations from local to national level</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="timeline-item">
                <h4 style="color: #2E4057;">🏛️ Government Response & Results</h4>
                <ul>
                    <li><strong>2018:</strong> New government ordered comprehensive review</li>
                    <li><strong>2020:</strong> Conditions set requiring waste operations to stop by 2023</li>
                    <li><strong>2023:</strong> Denied request to continue radioactive waste production</li>
                    <li><strong>Current:</strong> Plant continues operations without waste generation</li>
                </ul>
            </div>
            
            <div class="alert-box">
                <h4 style="color: #856404;">💼 Current Status</h4>
                <p><strong>Government Stance:</strong> "No party has right to continuously produce radioactive waste in our homeland" - Minister Chang Lih Kang</p>
                <p><strong>Employment:</strong> 600 Malaysian workers still employed</p>
                <p><strong>Operations:</strong> Continues without radioactive waste production</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif env_topic == "Environmental Activism":
        st.subheader("🌱 Environmental Activism in Malaysia & Southeast Asia")
        
        # NGO Achievement Overview
        col1, col2 = st.columns(2)
        
        with col1:
            fig_ngo = px.bar(
                ngo_achievements,
                x='Organization',
                y='Impact_Score',
                title="NGO Effectiveness & Impact Scores",
                color='Impact_Score',
                color_continuous_scale=['#548CA8', '#2E4057']
            )
            fig_ngo.update_layout(
                font_family="Times New Roman",
                title_font_family="Times New Roman",
                paper_bgcolor='white',
                plot_bgcolor='white',
                showlegend=False
            )
            fig_ngo.update_xaxis(tickangle=45)
            st.plotly_chart(fig_ngo, use_container_width=True)
        
        with col2:
            # Major achievements timeline
            achievements_by_year = ngo_achievements.groupby('Year').size().reset_index(name='Count')
            
            fig_timeline = px.line(
                achievements_by_year,
                x='Year',
                y='Count',
                title="Environmental Victories Timeline",
                markers=True
            )
            fig_timeline.update_traces(line_color='#2E4057', marker_size=8)
            fig_timeline.update_layout(
                font_family="Times New Roman",
                title_font_family="Times New Roman",
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Detailed NGO Achievements
        st.subheader("🏆 Major Environmental Victories")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="success-box">
                <h4 style="color: #2E4057;">🌊 Greenpeace Southeast Asia (2000-2025)</h4>
                <ul>
                    <li><strong>Krabi Coal Plant:</strong> Successfully stopped Thailand coal-fired power plant (2021)</li>
                    <li><strong>GMO Victory:</strong> Philippines Court banned commercial GMO crops (2024)</li>
                    <li><strong>Palm Oil Campaign:</strong> Forced Nestlé to stop buying from forest destroyers</li>
                    <li><strong>Regional Presence:</strong> 25 years of operations across SEA</li>
                </ul>
                <p style="font-size: 0.9em; margin-top: 10px;"><em>Malaysia office established July 28, 2017</em></p>
            </div>
            
            <div class="success-box">
                <h4 style="color: #2E4057;">🏛️ Sahabat Alam Malaysia - SAM (1977-Present)</h4>
                <ul>
                    <li><strong>International Recognition:</strong> Right Livelihood Award (1988), Goldman Award (1991)</li>
                    <li><strong>Forest Protection:</strong> Highlighted Sarawak rainforest destruction</li>
                    <li><strong>Community Support:</strong> Assisted Bukit Koman against cyanide mining</li>
                    <li><strong>Indigenous Rights:</strong> Fighting landgrabbing across 3M+ hectares</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="success-box">
                <h4 style="color: #2E4057;">🐯 WWF Malaysia (1972-Present)</h4>
                <ul>
                    <li><strong>Forest Restoration:</strong> 2,400 hectares restored at Bukit Piton (10+ years)</li>
                    <li><strong>Tiger Conservation:</strong> National Tiger Survey showing critical status</li>
                    <li><strong>Orangutan Protection:</strong> Secured riparian reserves along Kinabatangan River</li>
                    <li><strong>Community Programs:</strong> Sustainable income for Menyang Taih communities</li>
                </ul>
            </div>
            
            <div class="success-box">
                <h4 style="color: #2E4057;">♻️ Grassroots Environmental Heroes</h4>
                <ul>
                    <li><strong>Lay Peng Pua:</strong> Closed 300+ illegal plastic waste facilities in Kuala Langat</li>
                    <li><strong>Lost Food Project:</strong> Prevented 6.78M kg greenhouse gas emissions</li>
                    <li><strong>EcoKnights:</strong> Created awareness through environmental films (KLEFF)</li>
                    <li><strong>CETDEM:</strong> Founded by Gurmit Singh, halted Tembeling Dam</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Government and Public Perception
        st.subheader("📊 Government & Public Perception of Environmental Activism")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="insight-box">
                <h4 style="color: #2E4057;">🏛️ Government Response</h4>
                <ul>
                    <li>Human Rights Commission recognized environmental rights as basic human rights</li>
                    <li>Six recommendations including Clean Air Act enactment</li>
                    <li>More receptive to environmental organizations post-2018 election</li>
                    <li>Malaysia voting for UN resolution declaring clean environment as universal right</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
                <h4 style="color: #2E4057;">👥 Public Perception</h4>
                <ul>
                    <li>Growing public criticism despite media controls</li>
                    <li>Social media campaigns demanding stricter enforcement</li>
                    <li>Environmental groups filing human rights complaints</li>
                    <li>Increasing awareness of health impacts driving policy pressure</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="insight-box">
                <h4 style="color: #2E4057;">🎯 Achievements Impact</h4>
                <ul>
                    <li><strong>Policy Changes:</strong> Multiple government reviews and restrictions</li>
                    <li><strong>Corporate Accountability:</strong> 300,000-signature petitions delivered</li>
                    <li><strong>International Recognition:</strong> Multiple global awards</li>
                    <li><strong>Legal Precedents:</strong> Court victories and regulatory changes</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    elif env_topic == "Current Forest Fire Crisis":
        st.subheader("🔥 Current Forest Fire Situation & Climate Change Impact")
        
        # Current fire situation
        col1, col2 = st.columns(2)
        
        with col1:
            fig_fires = go.Figure()
            fig_fires.add_trace(go.Scatter(
                x=fire_data_2025['Month'],
                y=fire_data_2025['Malaysia_Fires'],
                mode='lines+markers',
                name='Malaysia',
                line=dict(color='#2E4057', width=3)
            ))
            fig_fires.add_trace(go.Scatter(
                x=fire_data_2025['Month'],
                y=fire_data_2025['Indonesia_Fires'],
                mode='lines+markers',
                name='Indonesia',
                line=dict(color='#dc3545', width=3)
            ))
            fig_fires.add_trace(go.Scatter(
                x=fire_data_2025['Month'],
                y=fire_data_2025['Regional_Total'],
                mode='lines+markers',
                name='Regional Total',
                line=dict(color='#548CA8', width=3)
            ))
            
            fig_fires.update_layout(
                title="2025 Forest Fire Activity by Month",
                xaxis_title="Month",
                yaxis_title="Number of Active Fires",
                font_family="Times New Roman",
                title_font_family="Times New Roman",
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            st.plotly_chart(fig_fires, use_container_width=True)
        
        with col2:
            # Impact sectors
            impact_data = pd.DataFrame({
                'Sector': ['Health', 'Education', 'Tourism', 'Economy'],
                'Impact_Percentage': [67, 45, 38, 52],
                'Description': ['31% increase in hospital cases', 'School closures affecting 2M+ students', 
                              'Significant visitor decline', 'Industrial production delays']
            })
            
            fig_impact = px.pie(
                impact_data,
                values='Impact_Percentage',
                names='Sector',
                title="Haze Impact by Sector (2025)",
                color_discrete_sequence=['#2E4057', '#548CA8', '#334257', '#476072']
            )
            fig_impact.update_layout(
                font_family="Times New Roman",
                title_font_family="Times New Roman",
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            st.plotly_chart(fig_impact, use_container_width=True)
        
        # Current crisis details
        st.subheader("🚨 August 2025 Crisis Update")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="alert-box">
                <h4 style="color: #856404;">🔥 Active Fire Situation</h4>
                <ul>
                    <li><strong>Indonesia:</strong> 140+ fires in Riau province</li>
                    <li><strong>Malaysia:</strong> Haze detected in Negeri Sembilan</li>
                    <li><strong>Sarawak:</strong> 100+ hectares burned near UiTM Mukah</li>
                    <li><strong>Visibility:</strong> Reduced to 1km in worst-hit areas</li>
                    <li><strong>Air Quality:</strong> API readings mostly moderate with unhealthy spikes</li>
                </ul>
            </div>
            
            <div class="env-card">
                <h4 style="color: #2E4057;">🌡️ Climate Change Connection</h4>
                <ul>
                    <li><strong>El Niño Return:</strong> Hotter, drier conditions since 2023</li>
                    <li><strong>Record Heat:</strong> 2024 was hottest year on record</li>
                    <li><strong>Fire Risk:</strong> Climate change made fires twice as likely</li>
                    <li><strong>Rainfall Patterns:</strong> Increasingly erratic, intensifying dry spells</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="success-box">
                <h4 style="color: #2E4057;">🌿 NGO Actions & Response</h4>
                <ul>
                    <li><strong>Greenpeace:</strong> Fire Prevention Team mapping/monitoring hotspots</li>
                    <li><strong>Legal Action:</strong> Palembang Court battles for haze accountability</li>
                    <li><strong>Community Work:</strong> Collaboration with affected areas for early detection</li>
                    <li><strong>Research:</strong> University partnerships on peat fire solutions</li>
                </ul>
            </div>
            
            <div class="env-card">
                <h4 style="color: #2E4057;">🏛️ Government Actions</h4>
                <ul>
                    <li><strong>Arrests:</strong> 44 people detained for suspected fire-setting in Indonesia</li>
                    <li><strong>Enhanced Patrols:</strong> Sarawak authorities enforcing open burning bans</li>
                    <li><strong>Cloud-Seeding:</strong> Operations considered for worst-affected areas</li>
                    <li><strong>Regional Cooperation:</strong> Minister calls for stronger ASEAN action</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Malaysia's positive progress
        st.subheader("📈 Malaysia's Environmental Progress")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="success-box">
                <h4 style="color: #2E4057;">🌳 Forest Conservation</h4>
                <ul>
                    <li><strong>Deforestation Decline:</strong> 13% reduction in primary forest loss</li>
                    <li><strong>Global Ranking:</strong> Out of top 10 deforestation countries for first time</li>
                    <li><strong>Forest Cover:</strong> Maintaining 50% forest coverage commitment</li>
                    <li><strong>Carbon Sequestration:</strong> Forests absorb 3/4 of CO2 emissions</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="success-box">
                <h4 style="color: #2E4057;">⚡ Climate Policy</h4>
                <ul>
                    <li><strong>Net Zero Target:</strong> Committed to net-zero emissions by 2050</li>
                    <li><strong>NETR:</strong> National Energy Transition Roadmap launched July 2023</li>
                    <li><strong>Investment:</strong> RM 16B for grid upgrade and decarbonization</li>
                    <li><strong>Green Finance:</strong> RM 200B in low-carbon economy financing</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="success-box">
                <h4 style="color: #2E4057;">👥 Community Impact</h4>
                <ul>
                    <li><strong>Wildlife Recovery:</strong> Orangutan habitat restoration projects</li>
                    <li><strong>Tiger Conservation:</strong> <150 Malayan tigers, intensive protection programs</li>
                    <li><strong>Waste Management:</strong> 300+ illegal facilities closed in Kuala Langat</li>
                    <li><strong>Education:</strong> Environmental film festivals reaching 80,000+ Malaysians</li>
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
            'title': 'Environmental Activism Effectiveness',
            'content': 'Malaysian environmental NGOs have achieved significant victories including stopping major industrial projects (Lynas restrictions, Krabi coal plant), securing international recognition (Right Livelihood Award), and creating lasting policy changes. The Lynas controversy demonstrates how sustained public opposition can influence government decisions on environmental issues.'
        },
        {
            'title': 'Climate Finance Challenge and Opportunity',
            'content': 'Southeast Asia faces a $52 billion annual climate financing gap despite $1.8 billion in committed funding. Malaysia\'s 13% reduction in forest loss and exit from top 10 deforestation countries shows progress, but current forest fires and haze episodes highlight ongoing regional challenges requiring enhanced cooperation.'
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
        - **Green Finance**: Leverage $1.8B ACGF funding for sustainable agriculture projects
        - **Climate Adaptation**: Develop drought-resistant varieties and water management systems
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
        - **Forest Fire Risk**: Continued haze episodes affecting regional air quality and health
        - **Financing Gap**: $52B annual shortfall in climate finance needs regional solutions
        """)

# Enhanced Footer with Environmental Data Sources
st.markdown("---")

# Data sources
with st.expander("📚 Data Sources & References"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Agricultural Data Sources:**
        - Malaysian Palm Oil Board (MPOB)
        - FELDA Official Records
        - Department of Statistics Malaysia
        - World Bank Agricultural Statistics
        - Ministry of Plantation Industries and Commodities
        """)
    
    with col2:
        st.markdown("""
        **Environmental Data Sources:**
        - Asian Development Bank (ADB)
        - Green Climate Fund
        - Greenpeace Malaysia/Southeast Asia
        - Sahabat Alam Malaysia (SAM)
        - WWF Malaysia
        - World Resources Institute
        - Copernicus Atmosphere Monitoring Service
        - Cambridge Core Environmental Studies
        """)

st.markdown(
    '<p style="text-align: center; color: #6c757d; font-family: Times New Roman, serif; font-size: 0.9rem;">Comprehensive analysis combining agricultural development with environmental sustainability data • Last updated: August 2025</p>',
    unsafe_allow_html=True
)
