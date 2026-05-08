# 🤖 Agent 交互日志

**团队名称：** AI龙虾小分队
**成员名单：** 龙虾一号、龙虾二号、龙虾三号
**使用的 AI Coding Agent 工具：** OpenClaw (Miaoda) · 内置 AI 编程助手
**提交时间：** 2026-05-08

---

## 交互记录

### 阶段一：理解赛题与数据

**Prompt：**
> 请读取 data/signal_samples.csv，告诉我数据有哪些字段，并统计各字段的基本信息（均值、最大最小值等）。

**AI 响应：**
AI 分析了 CSV 数据，确认包含以下字段：
- Latitude, Longitude（经纬度）
- CellID（小区ID）
- Band（频段：n28, n41, n78）
- RSRP_dBm（信号强度，均值约 -93 dBm）
- SINR_dB（信噪比）
- TerminalType（Smartphone/CPE/IoT）
- Download_Mbps（下载速率）

---

### 阶段二：构建 Streamlit 基础框架

**Prompt：**
> 请帮我写一个 Streamlit 应用，读取 data/signal_samples.csv，在页面上显示大标题"5G 信号可视化看板"，并在下方用 pandas 展示前5行数据。

**AI 响应（核心代码片段）：**
```python
import streamlit as st
import pandas as pd

st.set_page_config(page_title="5G 信号可视化看板", layout="wide")
st.title("📡 5G 信号可视化看板")

df = pd.read_csv("data/signal_samples.csv")
st.dataframe(df.head())
```

---

### 阶段三：添加 2D 散点地图（PyDeck）

**Prompt：**
> 请在数据表格下方，用 pydeck 添加一张散点地图，把所有经纬度点打在地图上，点的大小固定，颜色根据 RSRP_dBm 字段变化：大于 -90 为绿色，-110 到 -90 之间为黄色，小于 -110 为红色。地图使用 dark 主题。

**AI 响应（核心代码片段）：**
```python
import pydeck as pdk

def get_rsrp_color(rsrp):
    if rsrp > -90:
        return [0, 200, 80]
    elif rsrp > -110:
        return [255, 220, 0]
    else:
        return [220, 30, 30]

df['color'] = df['RSRP_dBm'].apply(get_rsrp_color)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[Longitude, Latitude]",
    get_color="color",
    get_radius=60,
    radius_scale=1,
)

view_state = pdk.ViewState(
    latitude=df["Latitude"].mean(),
    longitude=df["Longitude"].mean(),
    zoom=12,
)

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v11",
    initial_view_state=view_state,
    layers=[layer],
))
```

---

### 阶段四：添加侧边栏筛选器

**Prompt：**
> 请在页面左侧添加一个侧边栏，包含：1）频段（Band）的多选下拉菜单；2）RSRP 范围的滑动条；3）终端类型的多选。筛选时地图和图表要实时联动更新。

**AI 响应（核心代码片段）：**
```python
with st.sidebar:
    all_bands = sorted(df_all["Band"].unique())
    selected_bands = st.multiselect("选择频段", options=all_bands, default=all_bands)
    rsrp_range = st.slider("RSRP 范围", min_value=-130.0, max_value=-60.0, value=(-130, -60))

df_filtered = df_all[
    (df_all["Band"].isin(selected_bands)) &
    (df_all["RSRP_dBm"] >= rsrp_range[0]) &
    (df_all["RSRP_dBm"] <= rsrp_range[1])
]
```

---

### 阶段五：添加图表统计

**Prompt：**
> 请在地图下方，用 plotly 生成两个图表：1）各频段的基站数量柱状图；2）终端类型的占比饼图。

**AI 响应（核心代码片段）：**
```python
import plotly.express as px

# 柱状图
band_counts = df_filtered["Band"].value_counts().reset_index()
fig_band = px.bar(band_counts, x="Band", y="count", color="Band")
st.plotly_chart(fig_band, use_container_width=True)

# 饼图
terminal_counts = df_filtered["TerminalType"].value_counts().reset_index()
fig_pie = px.pie(terminal_counts, names="TerminalType", values="count", hole=0.4)
st.plotly_chart(fig_pie, use_container_width=True)
```

---

### 阶段六：3D 柱状地图

**Prompt：**
> 请添加一个 Tab，支持切换到 3D 柱状地图模式，柱的高度随 Download_Mbps 变化，颜色仍然按 RSRP 着色，地图倾斜 45 度。

**AI 响应（核心代码片段）：**
```python
layer_3d = pdk.Layer(
    "ColumnLayer",
    data=df_3d,
    get_position="[Longitude, Latitude]",
    get_elevation="Download_Mbps",
    elevation_scale=3,
    radius=40,
    get_fill_color="color",
    extruded=True,
)
```

---

### 阶段七：工程化完善（注释 + 单元测试）

**Prompt：**
> 请为 app.py 的核心函数添加规范注释，并写一份单元测试文件 tests/test_app.py，测试 get_rsrp_color 函数在不同 RSRP 值下的返回值。

**AI 响应：**
见 app.py 源码及 tests/test_app.py。

---

## 总结

本作品通过 **7 轮渐进式 AI 交互** 完成，涵盖数据加载、地图可视化、筛选联动、3D 可视化、统计分析等核心功能，充分展示了如何借助 AI Coding Agent 从零开始构建一个完整的交互式数据看板。
