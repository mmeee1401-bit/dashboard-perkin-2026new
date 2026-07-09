import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import requests

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Dashboard PERKIN 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CSS
# =====================================================
st.markdown("""
<style>

/* ===========================
BACKGROUND
=========================== */
.stApp{
    background:#EEF4FB;
}

/* ===========================
HIDE STREAMLIT
=========================== */
#MainMenu{
    visibility:hidden;
}
header{
    visibility:transparent !important;
};
}
footer{
    visibility:hidden;
}

/* ===========================
SIDEBAR
=========================== */
[data-testid="stSidebar"]{
    background:linear-gradient(
    180deg,
    #0B2F6A,
    #1565C0);
    width:280px;
}

[data-testid="stSidebar"] *{
    color:white;
}

/* ===========================
HEADER
=========================== */
.header{
background:linear-gradient(
135deg,
#0B4EA2,
#42A5F5);
border-radius:28px;
padding:32px 35px;
color:white;
box-shadow:0 12px 30px rgba(0,0,0,.15);
margin-bottom:25px;           
min-height:170px;
}

/* ===========================
CARD
=========================== */
.card{
background:linear-gradient(
135deg,
#0B4EA2,
#42A5F5);
padding:25px;
border-radius:22px;
box-shadow:0 10px 25px rgba(0,0,0,.08);
margin-bottom:20px;
}

/* ===========================
KPI
=========================== */
.kpi{
background:white;
padding:22px;
border-radius:20px;
box-shadow:0 8px 20px rgba(0,0,0,.08);
transition:.3s;
height:165px;
}

.kpi:hover{
transform:translateY(-6px);
}
            
.kpi-icon{
width:65px;
height:65px;
line-height:65px;
text-align:center;
border-radius:50%;
font-size:30px;
margin:auto;
margin-bottom:15px;
}

.kpi-title{
color:#666;
font-size:15px;
}

.kpi-value{
font-size:34px;
font-weight:bold;
color:#0B4EA2;
}

/* ===========================
CHART
=========================== */
.chart-card{
background:white;
border-radius:40px;
padding:22px;
box-shadow:0 8px 20px rgba(0,0,0,.08);
border:1px solid #E7EEF8;
margin-top:10px;
}          

/* ===========================
TABLE
=========================== */
[data-testid="stDataFrame"]{
border-radius:15px;
overflow:hidden;
}

/* ===========================
DOWNLOAD BUTTON
=========================== */
.stDownloadButton>button{
width:100%;
height:48px;
border-radius:12px;
background:#1565C0;
color:white;
border:none;
font-weight:bold;
}

.stDownloadButton>button:hover{
background:#0B4EA2;
color:white;
}

/* ===========================
KPI CARD
=========================== */
div[data-testid="stMetric"]{
background:white;
border-radius:20px;
padding:20px;
border:1px solid #E8EDF5;
box-shadow:0 8px 20px rgba(0,0,0,.08);
}

div[data-testid="stMetric"]:hover{
transform:translateY(-5px);
transition:.25s;
box-shadow:0 12px 28px rgba(0,0,0,.12);
}
            
/* ===========================
SELECTBOX
=========================== */
div[data-baseweb="select"]{
background:white !important;
border-radius:12px !important;
}

div[data-baseweb="select"] > div{
background:white !important;
border:1px solid #D9E2EF !important;
border-radius:12px !important;
}
            
/* ===========================
DOWNLOAD BUTTON
=========================== */
div.stLinkButton > a{
background:#0B4EA2 !important;
color:white !important;
border:none !important;
border-radius:12px !important;
padding:12px 18px !important;
text-decoration:none !important;
text-align:center !important;
font-weight:600 !important;
width:100%;
}

div.stLinkButton > a:hover{
background:#1565C0 !important;
}

/* ===========================
FOOTER
=========================== */
.footer{
margin-top:40px;
padding:22px;
background:linear-gradient(
90deg,
#0B4EA2,
#1976D2);
border-radius:18px;
color:white;
text-align:center;
}

.footer h2 a{
    display:none !important;
}
            
.footer h2::after{
    display:none !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# GOOGLE SHEETS
# =====================================================

sheet_id = "13TQ-GJ9cpEkLmDhfi31bcgs5GmZGNBvpLJIrjQeddc8"

bulan_sheet = {
    "Januari": "JAN",
    "Februari": "FEB",
    "Maret": "MAR",
    "April": "APRIL",
    "Mei": "MEI",
    "Juni": "JUNI",
    "Juli": "JULI",
    "Agustus": "AGS",
    "September": "SEP",
    "Oktober": "OKT",
    "November": "NOV",
    "Desember": "DES"
}

# =====================================================
# LOAD DATA
# =====================================================

bulan = "Januari"
nama_sheet = bulan_sheet[bulan]
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nama_sheet}"

df = pd.read_csv(url)
df.columns = df.columns.str.strip()
df["Indikator"] = df["Indikator"].astype(str).str.strip()
df["Kabupaten"] = df["Kabupaten"].astype(str).str.strip()
df["Target"] = pd.to_numeric(
    df["Target"],
    errors="coerce"
)
df["Realisasi"] = pd.to_numeric(
    df["Realisasi"],
    errors="coerce"
)

# =====================================================
# HEADER
# =====================================================

col1, col2 = st.columns([8,4.5])

with col1:
    st.markdown("""
    <div class="header">
    <div style="
    font-size:42px;
    font-weight:700;
    margin-bottom:8px;">

    <b> 📊 Dashboard PERKIN 2026</b>
    </div>
    <div style="
    font-size:18px;
    opacity:.95;
    ">
    Monitoring Kinerja Program Bangka Belitung
    </div>
    <div style="
    margin-top:18px;
    font-size:15px;">
    Kementerian Kependudukan dan Pembangunan Keluarga / BKKBN
    </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
    st.image(
        "logo_bkkbnbaru.png",
        width=380
    )
    st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)

   # st.markdown("""
   # <div style="
    #    text-align:center;
    #    margin-top:10px;
      #  color:#0B4EA2;
    #    font-size:30px;
     #   font-weight:600;
    # line-height:1.5;
    # ">
    #    Berencana <br>
     #   itu Keren!
    #</div>
    # """, unsafe_allow_html=True)

# =====================================================
# FILTER
# =====================================================

f1, f2 = st.columns(2)

with f1:
    with st.container():
        st.markdown("""
        <div class="card">
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="
        font-size:30px;
        font-weight:700;
        color:#0B4EA2;
        margin-bottom:15px;">
        📅 Pilih Bulan
        </h4>
        """, unsafe_allow_html=True)

        bulan = st.selectbox(
            "",
            list(bulan_sheet.keys()),
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

with f2:
    nama_sheet = bulan_sheet[bulan]
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={nama_sheet}"

    df = pd.read_csv(url)
    df.columns = df.columns.str.strip() # Bersihkan nama kolom
    df["Indikator"] = df["Indikator"].astype(str).str.strip() # Bersihkan kolom teks
    df["Kabupaten"] = df["Kabupaten"].astype(str).str.strip()

    df["Target"] = (
        df["Target"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    df["Target"] = pd.to_numeric(df["Target"], errors="coerce")

    df["Realisasi"] = (
        df["Realisasi"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    df["Realisasi"] = pd.to_numeric(df["Realisasi"], errors="coerce")

    df["Capaian"] = (
        df["Capaian"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    df["Capaian"] = pd.to_numeric(df["Capaian"], errors="coerce")

    st.markdown("""
    <div class="card">
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="
    font-size:30px;
    font-weight:700;
    color:#0B4EA2;
    margin-bottom:15px;">
    📊 Pilih Indikator
    </div>
    """, unsafe_allow_html=True)

    indikator = st.selectbox(
        "",
        sorted(df["Indikator"].unique()),
        label_visibility="collapsed"
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# FILTER DATA
# =====================================================

df_filter = df[
    df["Indikator"] == indikator
].copy()
df_filter = df[
    df["Indikator"] == indikator
].copy()

df_filter["Capaian"] = df_filter["Capaian"].fillna(0)

# =====================================================
# KPI
# =====================================================

total_target = df_filter["Target"].sum()
total_realisasi = df_filter["Realisasi"].sum()
persen = 0

if total_target > 0:
    persen = round(
        total_realisasi / total_target * 100,
        2
    )
jumlah_kab = df_filter["Kabupaten"].nunique()

k1, k2, k3, k4 = st.columns(4)

# =====================================================
# KPI
# =====================================================

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        label="🎯 Total Target",
        value=f"{total_target:,.0f}",
        help="Total target pada indikator yang dipilih"
    )

with k2:
    st.metric(
        label="✅ Total Realisasi",
        value=f"{total_realisasi:,.0f}",
        help="Total realisasi pada indikator yang dipilih"
    )

with k3:
    st.metric(
        label="📈 Persentase Capaian",
        value=f"{persen:.2f}%"
    )

with k4:
    st.metric(
        label="🏛️ Kabupaten/Kota",
        value=f"{jumlah_kab}"
    )

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# GRAFIK
# =====================================================

st.markdown(
    """
    <div style="height:35px;"></div>
    """,
    unsafe_allow_html=True
)

left_chart, right_chart = st.columns([1.4, 1])


# =====================================================
# GRAFIK TARGET VS REALISASI
# =====================================================

with left_chart:

    st.markdown("""
    <div style="
    font-size:30px;
    font-weight:700;
    color:#0B4EA2;
    margin-bottom:15px;">
    📊 Target vs Realisasi
    </div>
    """, unsafe_allow_html=True)

    df_bar = pd.melt(
        df_filter,
        id_vars="Kabupaten",
        value_vars=["Target", "Realisasi"],
        var_name="Kategori",
        value_name="Nilai"
    )

    fig1 = px.bar(
        df_bar,
        x="Kabupaten",
        y="Nilai",
        color="Kategori",
        barmode="group",
        text="Nilai",
        color_discrete_map={
            "Target": "#2F80ED",
            "Realisasi": "#2ECC71"
        }
    )

    fig1.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False
    )

    fig1.update_layout(
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title="",
        legend=dict(
            orientation="h",
            y=1.12,
            x=0.18
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

         yaxis=dict(
        title="Jumlah",
        range=[0, df_filter["Target"].max() * 1.15]   # beri ruang 15%
        ),
        
        xaxis_title="",
        yaxis_title="Jumlah"
        
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# =====================================================
# GRAFIK PERSENTASE CAPAIAN
# =====================================================

with right_chart:

    st.markdown("""
    <div style="
    font-size:30px;
    font-weight:700;
    color:#0B4EA2;
    margin-bottom:15px;">
    📈 Persentase Capaian
    </h4>
    """, unsafe_allow_html=True)

    fig2 = px.bar(
        df_filter.sort_values("Capaian", ascending=True),
        x="Capaian",
        y="Kabupaten",
        orientation="h",
        text="Capaian",
        color="Capaian",
        color_continuous_scale="Blues"
    )

    fig2.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False
    )

    fig2.update_layout(
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        coloraxis_showscale=False,
        margin=dict(
            l=70,
            r=80,
            t=30,
            b=20
        ),
        xaxis_title="Persentase (%)",
        yaxis_title=""
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==========================================
# LINK DOWNLOAD EXCEL GOOGLE SHEETS
# ==========================================

download_url = (
    "https://docs.google.com/spreadsheets/d/"
    "1RRXLSU-hcHwfUaiOPEGW0UTgYuy3ygp3"
    "/export?format=xlsx"
)

response = requests.get(download_url)
sheet_url = "https://docs.google.com/spreadsheets/d/1RRXLSU-hcHwfUaiOPEGW0UTgYuy3ygp3/edit?usp=sharing"

kosong, kanan = st.columns([7, 2])

with kanan:
    st.markdown("""
    <style>
    div.stLinkButton > a{
        font-weight:700 !important;
        font-size:16px;
        border-radius:12px;
        background:#0B4EA2;
        color:white !important;
        padding:10px 18px;
        text-decoration:none;
        text-align:center;
        display:block;
    }

    div.stLinkButton > a:hover{
        background:#083D80;
        color:white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.link_button(
        "📄 Lihat Laporan PERKIN 2026",
        sheet_url,
        use_container_width=True
    )

    # Tombol di kanan bawah
    kosong, kanan = st.columns([7, 2])

    with kanan:
        st.markdown("""
    <style>
        div.stDownloadButton > button{
        font-weight:700 !important;
        font-size:16px;
        border-radius:12px;
        background:#0B4EA2;
        color:white;
        padding:10px 18px;
    }

        div.stDownloadButton > button:hover{
        background:#083D80;
        color:white;
    }
    </style>
    """, unsafe_allow_html=True)
    

    st.download_button(
        label="📥 Download Laporan PERKIN 2026",
        data=response.content,
        file_name="PERKIN & REALISASI PER KAB_KOTA 2026.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
            
<h2 style="margin-bottom:8px;">
Dashboard PERKIN 2026
</h2>
<div style="font-size:16px; opacity:.95;">
Monitoring Kinerja Program Bangka Belitung
</div>
<br>
<hr style="
border:1px solid rgba(255,255,255,.25);
">
<div style="
font-size:15px;
line-height:1.8;
">
<b>Kementerian Kependudukan dan Pembangunan Keluarga / BKKBN</b><br>
<b> Perwakilan BKKBN</b><br>
<b> Provinsi Kepulauan Bangka Belitung</b><br>
<br>   
 © 
<b>BKKBN</b> -
<b>BANGKA BELITUNG</b> -
<b>2026</b>

</div>

</div>
""", unsafe_allow_html=True)
