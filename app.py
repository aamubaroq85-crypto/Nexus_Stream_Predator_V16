import streamlit as st
import pandas as pd
import numpy as np

# Konfigurasi Halaman ala Terminal Institusional
st.set_page_config(
    page_title="ZF-Core Predator & Nexus Monitor",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Styling CSS Kustom untuk Tampilan Dark Theme Modern ala Mobile Dashboard
st.markdown("""
    <style>
    /* Mengatur latar belakang utama aplikasi */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    /* Kartu Server Status */
    .server-card {
        background: #111827;
        border: 1px solid #1f2937;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Kartu Metrik Keuangan */
    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .metric-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #9ca3af;
        margin-bottom: 6px;
        font-weight: 600;
    }
    
    .metric-value-green {
        font-size: 1.8rem;
        font-weight: 700;
        color: #34d399;
    }
    
    .metric-value-red {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f87171;
    }
    
    .metric-value-white {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    .sub-text {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 4px;
    }
    
    /* Tombol Kustom */
    .stButton>button {
        width: 100%;
        background-color: #ef4444;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #dc2626;
    }
    </style>
    """, unsafe_allow_html=True)

# Header Status Server EA Cloud
st.markdown("""
    <div class="server-card">
        <div>
            <div style="font-size: 0.85rem; font-weight: bold; color: #ffffff;">SERVER EA CLOUD</div>
            <div style="font-size: 0.75rem; color: #9ca3af;">Metatrader 5 • Terminal #01</div>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="height: 10px; width: 10px; background-color: #34d399; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #34d399;"></span>
            <span style="font-size: 0.8rem; font-weight: bold; color: #34d399; letter-spacing: 0.05em;">CONNECTED</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Judul Utama Dashboard
st.markdown("<h2 style='font-size: 1.3rem; font-weight: 700; color: #f3f4f6; margin-bottom: 16px;'>Monitoring Ekuitas Live</h2>", unsafe_allow_html=True)

# Inisialisasi State Sesi untuk Simulasi Nilai Real-time
if 'equity' not in st.session_state:
    st.session_state.equity = 9976.88
if 'floating_pl' not in st.session_state:
    st.session_state.floating_pl = -23.12
if 'balance' not in st.session_state:
    st.session_state.balance = 10000.00
if 'drawdown' not in st.session_state:
    st.session_state.drawdown = 0.23

# Kartu 1: Total Ekuitas
st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TOTAL EKUITAS</div>
        <div class="metric-value-green">${st.session_state.equity:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# Kartu 2: Floating P/L
pl_color = "metric-value-green" if st.session_state.floating_pl >= 0 else "metric-value-red"
st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">FLOATING P/L</div>
        <div class="{pl_color}">${st.session_state.floating_pl:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# Kartu 3: Balance Awal
st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">BALANCE AWAL</div>
        <div class="metric-value-white">${st.session_state.balance:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# Kartu 4: Drawdown Saat Ini
st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">DRAWDOWN SAAT INI</div>
        <div class="metric-value-green">{st.session_state.drawdown:.2f}% <span class="sub-text">/ Max 1.5%</span></div>
    </div>
    """, unsafe_allow_html=True)

# Tombol Aksi Sinkronisasi
if st.button("Jalankan Sinkronisasi P/L Real-time"):
    st.session_state.equity += 15.50
    st.session_state.floating_pl += 15.50
    st.session_state.drawdown = max(0.0, st.session_state.drawdown - 0.02)
    st.rerun()
