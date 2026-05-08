"""
5G 信号可视化看板
Code with AI 挑战赛作品
团队: AI龙虾小分队
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
from datetime import datetime

# ==========================================
# 页面配置
# ==========================================
st.set_page_config(
    page_title="📡 5G 信号可视化看板",
    layout="wide",
    page_icon="📡"
)

# ==========================================
# 辅助函数
# ==========================================

def get_rsrp_color(rsrp: float) -> list:
    """
    根据 RSRP 值返回对应颜色
    RSRP > -90 dBm  → 绿色 (信号强)
    -110 < RSRP <= -90 dBm → 黄色 (信号中)
    RSRP <= -110 dBm → 红色 (信号弱)
    """
    if rsrp > -90:
        return [0, 200, 80]       # 绿色
    elif rsrp > -110:
        return [255, 220, 0]      # 黄色
    else:
        return [220, 30, 30]      # 红色


def get_rsrp_category(rsrp: float) -> str:
    """返回 RSRP 信号的分类标签"""
    if rsrp > -90:
        return "🟢 强信号"
    elif rsrp > -110:
        return "🟡 中等信号"
    else:
        return "🔴 弱信号"


# ==========================================
# 侧边栏：筛选控件
# ==========================================
with st.sidebar:
    st.header("🔍 数据筛选")

    # 加载数据用于生成筛选选项
    try:
        df_all = pd.read_csv("data/signal_samples.csv")
    except FileNotFoundError:
        st.error("未找到 data/signal_samples.csv，请确认数据文件路径！")
        st.stop()

    # 频段多选
    all_bands = sorted(df_all["Band"].unique().tolist())
    selected_bands = st.multiselect(
        "选择频段 (Band)",
        options=all_bands,
        default=all_bands,
        format_func=lambda x: f"Band {x}"
    )

    # RSRP 范围滑动条
    rsrp_min, rsrp_max = float(df_all["RSRP_dBm"].min()), float(df_all["RSRP_dBm"].max())
    rsrp_range = st.slider(
        "RSRP 范围 (dBm)",
        min_value=rsrp_min,
        max_value=rsrp_max,
        value=(rsrp_min, rsrp_max),
        step=1.0
    )

    # 终端类型多选
    all_terminals = sorted(df_all["TerminalType"].unique().tolist())
    selected_terminals = st.multiselect(
        "选择终端类型",
        options=all_terminals,
        default=all_terminals
    )

    # SINR 过滤
    sinr_min = float(df_all["SINR_dB"].min())
    sinr_max = float(df_all["SINR_dB"].max())
    sinr_filter = st.slider(
        "SINR 范围 (dB)",
        min_value=sinr_min,
        max_value=sinr_max,
        value=(sinr_min, sinr_max),
        step=0.5
    )

    st.divider()
    st.caption(f"📊 数据总量：{len(df_all)} 条记录")

# ==========================================
# 数据过滤
# ==========================================
df_filtered = df_all[
    (df_all["Band"].isin(selected_bands)) &
    (df_all["RSRP_dBm"] >= rsrp_range[0]) &
    (df_all["RSRP_dBm"] <= rsrp_range[1]) &
    (df_all["TerminalType"].isin(selected_terminals)) &
    (df_all["SINR_dB"] >= sinr_filter[0]) &
    (df_all["SINR_dB"] <= sinr_filter[1])
]

# ==========================================
# 主页面
# ==========================================
st.title("📡 5G 信号可视化看板")
st.markdown(
    "**Code with AI** 海选赛作品 · 5G 路测数据交互式可视化"
)

# ---- 统计指标卡片 ----
st.markdown("### 📈 数据概览")
col1, col2, col3, col4 = st.columns(4)

col1.metric("总采样点", f"{len(df_filtered):,}")
col2.metric("基站数量", f"{df_filtered['CellID'].nunique()}")
col3.metric(
    "平均 RSRP",
    f"{df_filtered['RSRP_dBm'].mean():.1f} dBm",
    delta=get_rsrp_category(df_filtered["RSRP_dBm"].mean())
)
col4.metric(
    "平均 SINR",
    f"{df_filtered['SINR_dB'].mean():.1f} dB"
)

st.divider()

# ---- 地图可视化 ----
st.markdown("### 🗺️ 信号覆盖地图")

tab_map_2d, tab_map_3d = st.tabs(["2D 散点地图", "3D 柱状地图"])

with tab_map_2d:
    # 使用 pydeck 渲染 2D 地图，颜色随 RSRP 变化
    df_map = df_filtered.copy()
    df_map["color"] = df_map["RSRP_dBm"].apply(lambda x: get_rsrp_color(x))
    df_map["lat"] = df_map["Latitude"]
    df_map["lon"] = df_map["Longitude"]

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_map,
        get_position="[lon, lat]",
        get_color="color",
        get_radius=60,
        radius_scale=1,
        radius_min_pixels=4,
        radius_max_pixels=20,
        pickable=True,
        opacity=0.85,
    )

    view_state = pdk.ViewState(
        latitude=df_map["Latitude"].mean(),
        longitude=df_map["Longitude"].mean(),
        zoom=12,
        pitch=0,
    )

    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v11",
            initial_view_state=view_state,
            layers=[layer],
            tooltip={"text": "{CellID} | RSRP: {RSRP_dBm} dBm | SINR: {SINR_dB} dB\nBand: {Band} | {TerminalType}"}
        ),
        use_container_width=True,
    )

    # 图例
    st.markdown(
        """
        **图例：** 🟢 强信号 (RSRP > -90 dBm) ｜ 🟡 中等信号 (-110 ~ -90 dBm) ｜ 🔴 弱信号 (RSRP ≤ -110 dBm)
        """
    )

with tab_map_3d:
    # 3D 柱状地图，高度随下载速率变化
    df_3d = df_filtered.copy()
    df_3d["color"] = df_3d["RSRP_dBm"].apply(lambda x: get_rsrp_color(x))
    df_3d["height"] = (df_3d["Download_Mbps"] / df_3d["Download_Mbps"].max()) * 500 + 10

    layer_3d = pdk.Layer(
        "ColumnLayer",
        data=df_3d,
        get_position="[Longitude, Latitude]",
        get_elevation="height",
        elevation_scale=2,
        radius=40,
        get_fill_color="color",
        pickable=True,
        extruded=True,
        opacity=0.8,
    )

    view_state_3d = pdk.ViewState(
        latitude=df_3d["Latitude"].mean(),
        longitude=df_3d["Longitude"].mean(),
        zoom=12,
        pitch=45,
        bearing=-15,
    )

    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v11",
            initial_view_state=view_state_3d,
            layers=[layer_3d],
            tooltip={"text": "Band {Band} | RSRP: {RSRP_dBm} dBm\n下载速率: {Download_Mbps:.1f} Mbps"},
        ),
        use_container_width=True,
    )
    st.caption("📌 柱高代表下载速率 (Download_Mbps)，颜色代表信号强度 (RSRP)")

st.divider()

# ---- 数据分析图表 ----
st.markdown("### 📊 数据统计分析")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("**📶 各频段基站数量分布**")
    band_counts = df_filtered["Band"].value_counts().reset_index()
    band_counts.columns = ["Band", "基站数量"]
    fig_band = px.bar(
        band_counts,
        x="Band",
        y="基站数量",
        color="Band",
        text_auto=True,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_band.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig_band, use_container_width=True)

with chart_col2:
    st.markdown("**📱 终端类型占比**")
    terminal_counts = df_filtered["TerminalType"].value_counts().reset_index()
    terminal_counts.columns = ["终端类型", "数量"]
    fig_terminal = px.pie(
        terminal_counts,
        names="终端类型",
        values="数量",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_terminal.update_layout(height=350)
    st.plotly_chart(fig_terminal, use_container_width=True)

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.markdown("**📶 RSRP 信号强度分布**")
    fig_rsrp = px.histogram(
        df_filtered,
        x="RSRP_dBm",
        nbins=30,
        color_discrete_sequence=["#4C78A8"],
        opacity=0.8
    )
    fig_rsrp.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig_rsrp, use_container_width=True)

with chart_col4:
    st.markdown("**📡 SINR vs 下载速率 关系**")
    fig_scatter = px.scatter(
        df_filtered,
        x="SINR_dB",
        y="Download_Mbps",
        color="Band",
        size="RSRP_dBm",
        color_discrete_sequence=px.colors.qualitative.Bold,
        opacity=0.7
    )
    fig_scatter.update_layout(height=300)
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ---- 详细数据表 ----
st.markdown("### 📋 采样点详细数据")
st.dataframe(
    df_filtered.rename(columns={
        "Latitude": "纬度",
        "Longitude": "经度",
        "CellID": "小区ID",
        "Band": "频段",
        "RSRP_dBm": "RSRP(dBm)",
        "SINR_dB": "SINR(dB)",
        "TerminalType": "终端类型",
        "Download_Mbps": "下载速率(Mbps)"
    }),
    use_container_width=True,
    height=400
)

# ---- 参赛说明 ----
st.divider()
st.caption(
    "🚀 Code with AI 海选赛作品 | 使用 Streamlit + PyDeck + Plotly 构建 | "
    f"筛选后 {len(df_filtered)} / {len(df_all)} 条记录"
)
