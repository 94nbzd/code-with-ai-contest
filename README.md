# 📡 5G 信号可视化看板

> Code with AI 海选赛作品 · 5G 路测数据交互式可视化

## 项目简介

本项目将 5G 路测数据（包含经纬度、频段、RSRP、SINR、终端类型、下载速率等字段）转化为一个高大上的交互式 Web 可视化看板，基于 **Streamlit + PyDeck + Plotly** 构建。

## 功能特性

### ✅ 基础关卡
- [x] **数据加载**：使用 pandas 读取 CSV 数据
- [x] **2D 信号散点地图**：使用 PyDeck 渲染，颜色随 RSRP 变化（绿/黄/红）
- [x] **数据统计分析**：各频段基站数量柱状图、终端类型占比饼图

### 🎖️ 进阶关卡
- [x] **侧边栏联动筛选**：支持按频段、RSRP 范围、SINR 范围、终端类型实时过滤
- [x] **3D 柱状地图**：信号点以 3D 柱状图呈现，高度随下载速率变化
- [x] **多维度图表**：RSRP 分布直方图、SINR vs 下载速率散点图

## 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行看板

```bash
streamlit run app.py --server.port 8501
```

浏览器自动打开 `http://localhost:8501`

## 项目结构

```
├── app.py                      # 主应用入口
├── data/
│   └── signal_samples.csv      # 5G 信号样本数据
├── requirements.txt            # Python 依赖
├── README.md                   # 本文件
├── AI_PROMPTS.md               # AI 交互日志（参赛必需）
└── tests/
    └── test_app.py             # 单元测试
```

## 数据字段说明

| 字段 | 说明 |
|------|------|
| Latitude / Longitude | 经纬度坐标 |
| CellID | 小区 ID |
| Band | 频段 (n28 / n41 / n78) |
| RSRP_dBm | 参考信号接收功率 (dBm) |
| SINR_dB | 信噪比 (dB) |
| TerminalType | 终端类型 (Smartphone / CPE / IoT) |
| Download_Mbps | 下载速率 (Mbps) |

## RSRP 信号强度等级

| 等级 | 范围 | 颜色 |
|------|------|------|
| 🟢 强信号 | RSRP > -90 dBm | 绿色 |
| 🟡 中等信号 | -110 < RSRP ≤ -90 dBm | 黄色 |
| 🔴 弱信号 | RSRP ≤ -110 dBm | 红色 |

## 参赛信息

- **赛事**：Code with AI 海选赛
- **作品**：5G 信号可视化看板挑战
- **框架**：Streamlit · PyDeck · Plotly
