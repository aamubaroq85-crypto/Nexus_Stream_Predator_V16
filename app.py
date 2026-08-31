import streamlit as st
import numpy as np
import pandas as pd
import datetime
import math
import time

# --- KONFIGURASI HALAMAN & TEMA ---
st.set_page_config(
    page_title="ZF-Core V16.7-PREDATOR & Nexus Stream", 
    page_icon="🛡️", 
    layout="wide"
)

# Kustomisasi CSS Tampilan Profesional
st.markdown("""
    <style>
    .main { background-color: #121212; color: #e0e0e0; }
    .stButton>button {
        background-color: #b71c1c;
        color: white;
        border-radius: 6px;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton>button:hover { background-color: #d32f2f; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- 1. NEXUS STREAM CORE (LIGHTWEIGHT VECTOR MEMORY) ---
class NexusStreamCoreLightweight:
    def __init__(self, vector_dim=64, capacity=5000):
        self.vector_dim = vector_dim
        self.capacity = capacity
        if 'lattice_grid' not in st.session_state:
            st.session_state.lattice_grid = [[0.0 * vector_dim] for _ in range(capacity)]
            st.session_state.cursor = 0
            st.session_state.total_stored = 0

    def fast_ingest(self, data_vector: list):
        if len(data_vector) != self.vector_dim:
            data_vector = data_vector + [0.0] * (self.vector_dim - len(data_vector)) if len(data_vector) < self.vector_dim else data_vector[:self.vector_dim]
        
        st.session_state.lattice_grid[st.session_state.cursor] = data_vector
        st.session_state.cursor = (st.session_state.cursor + 1) % self.capacity
        if st.session_state.total_stored < self.capacity:
            st.session_state.total_stored += 1

    def instant_query(self, query_vec: list):
        limit = st.session_state.total_stored
        if limit == 0:
            return 0.0, 0.0
        
        if len(query_vec) != self.vector_dim:
            query_vec = query_vec + [0.0] * (self.vector_dim - len(query_vec)) if len(query_vec) < self.vector_dim else query_vec[:self.vector_dim]

        min_dist = float('inf')
        for i in range(limit):
            row = st.session_state.lattice_grid[i]
            dist_sq = sum((row[j] - query_vec[j]) ** 2 for j in range(len(query_vec)))
            dist = math.sqrt(dist_sq)
            if dist < min_dist:
                min_dist = dist
        return min_dist, float(limit)

# --- 2. ZF-CORE V16.7-PREDATOR ENGINE ---
class ZFCorePredatorEngine:
    def __init__(self):
        self.v_thresh = 5.0           
        self.lambda_0 = 0.15          
        self.nexus_core = NexusStreamCoreLightweight(vector_dim=64, capacity=5000)

    def calculate_matrix_drift(self, p_market: float, p_pure: float, crx: float) -> float:
        d_res = (abs(p_market - p_pure) / p_pure) * 100
        return d_res * (1 + abs(crx))

    def calculate_kinetic_force(self, delta_oi: float, oi_avg: float, v_liq: float, depth_live: float) -> float:
        if oi_avg == 0 or depth_live == 0:
            return 0.0
        return (delta_oi / oi_avg) * math.log(1 + (v_liq / depth_live))

    def calculate_zf_score(self, d_matrix: float, k_force: float) -> float:
        return math.tanh(d_matrix * (1 + k_force))

    def process_cycle(self, data_list: list):
        calculated_pairs = []
        global_max_zf = 0.0

        for data in data_list:
            pair = data['pair']
            d_matrix = self.calculate_matrix_drift(data['p_market'], data['p_pure'], crx=data['crx'])
            k_force = self.calculate_kinetic_force(data['delta_oi'], data['oi_avg'], data['v_liq'], data['depth_live'])
            zf_score = self.calculate_zf_score(d_matrix, k_force)
            
            # Ingest Vektor ke Nexus Stream Core
            market_vector = [data['p_market'], data['p_pure'], d_matrix, k_force, zf_score, data['crx'], data['delta_oi'], data['v_liq']] * 8
            self.nexus_core.fast_ingest(market_vector)
            min_dist, total_stored = self.nexus_core.instant_query(market_vector)

            if zf_score > global_max_zf:
                global_max_zf = zf_score

            calculated_pairs.append({
                "Forex Pair": pair,
                "D_Matrix": f"{d_matrix:.2f}%",
                "ZF-Score": f"{zf_score:.4f}",
                "Lambda (λ)": f"{self.lambda_0:.4f}",
                "Nexus Dist": f"{min_dist:.3f}",
                "Rekomendasi": "Predator Re-entry Valid" if zf_score < 0.50 else "Waspada Kritis"
            })

        return global_max_zf, calculated_pairs

engine = ZFCorePredatorEngine()

# --- 3. ANTARMUKA STREAMLIT ---
st.title("🛡️ ZF-CORE V16.7-PREDATOR & NEXUS MONITOR")
st.markdown("Sistem Pengaman Likuidasi Otomatis & Analisis Volatilitas HFT berbasis Vektor.")
st.markdown("---")

# Simulasi Input Pasar Live
col1, col2 = st.columns(2)
with col1:
    market_price = st.number_input("Harga Market (P_Market)", value=1.0850, format="%.4f")
    pure_price = st.number_input("Harga Murni (P_Pure)", value=1.0820, format="%.4f")
with col2:
    delta_open_interest = st.number_input("Delta Open Interest (Delta OI)", value=5000.0, step=500.0)
    liquidity_vol = st.number_input("Volume Likuiditas (V_Liq)", value=12000.0, step=1000.0)

st.markdown("")
if st.button("Jalankan Siklus Analisis Predator"):
    mock_feed = [
        {
            'pair': 'EXOTIC/P164', 'p_market': market_price, 'p_pure': pure_price,
            'crx': 0.12, 'delta_oi': delta_open_interest, 'oi_avg': 150000.0, 
            'v_liq': liquidity_vol, 'depth_live': 50000.0
        },
        {
            'pair': 'EXOTIC/P91', 'p_market': 1.2450, 'p_pure': 1.2410,
            'crx': 0.08, 'delta_oi': 3200.0, 'oi_avg': 120000.0, 
            'v_liq': 9000.0, 'depth_live': 45000.0
        }
    ]
    
    global_max_zf, data_pairs = engine.process_cycle(mock_feed)
    
    # Logika Warna Status Sistem
    status_sistem = "OPERASIONAL NORMAL"
    status_color = "green"
    if global_max_zf > 0.99:
        status_sistem = "CIRCUIT BREAKER AKTIF (EMERGENCY ALL-STOP)"
        status_color = "red"
    elif global_max_zf > 0.70:
        status_sistem = "WASPADA KRITIS"
        status_color = "orange"

    st.markdown("---")
    
    # Panel Status Indikator
    st.subheader("📊 Status Pengamanan Sistem")
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Global Max ZF-Score", value=f"{global_max_zf:.4f}")
    m2.metric(label="Total Vektor Tersimpan", value=f"{st.session_state.total_stored} Record")
    m3.metric(label="Status Sistem", value=status_sistem)

    if global_max_zf > 0.99:
        st.error(f"🚨 TOPOLOGICAL FRACTURE TERDETEKSI! {status_sistem}")
    elif global_max_zf > 0.70:
        st.warning(f"⚠️ PERINGATAN: Pasar mendekati ambang batas kritis.")
    else:
        st.success("✅ Sistem stabil. Kondisi pasar dalam batas aman.")

    st.markdown("---")
    st.subheader("📋 10 Pasangan Aset Prioritas Utama")
    
    df_results = pd.DataFrame(data_pairs)
    st.dataframe(df_results, use_container_width=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #ffa000; font-style: italic;'>Jaga Ibadahmu - System Core V16.7-PREDATOR & Nexus Stream</p>", unsafe_allow_html=True)
