"""
单元测试：5G 信号可视化看板
测试核心辅助函数的正确性
"""

import pytest
import sys, os

# 确保 app 模块可导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import get_rsrp_color, get_rsrp_category


class TestGetRsrpColor:
    """测试 RSRP 颜色映射函数"""

    def test_strong_signal_returns_green(self):
        """RSRP > -90 dBm 应返回绿色 [0, 200, 80]"""
        assert get_rsrp_color(-80) == [0, 200, 80]
        assert get_rsrp_color(-89) == [0, 200, 80]

    def test_moderate_signal_returns_yellow(self):
        """-110 < RSRP <= -90 dBm 应返回黄色 [255, 220, 0]"""
        assert get_rsrp_color(-100) == [255, 220, 0]
        assert get_rsrp_color(-90) == [255, 220, 0]
        assert get_rsrp_color(-95) == [255, 220, 0]

    def test_weak_signal_returns_red(self):
        """RSRP <= -110 dBm 应返回红色 [220, 30, 30]"""
        assert get_rsrp_color(-110) == [220, 30, 30]
        assert get_rsrp_color(-120) == [220, 30, 30]
        assert get_rsrp_color(-130) == [220, 30, 30]

    def test_boundary_values(self):
        """边界值测试"""
        assert get_rsrp_color(-90.0) == [255, 220, 0]   # 上边界 → 黄色
        assert get_rsrp_color(-110.0) == [220, 30, 30]  # 下边界 → 红色


class TestGetRsrpCategory:
    """测试 RSRP 信号分类函数"""

    def test_strong_signal_label(self):
        assert get_rsrp_category(-80) == "🟢 强信号"

    def test_moderate_signal_label(self):
        assert get_rsrp_category(-100) == "🟡 中等信号"

    def test_weak_signal_label(self):
        assert get_rsrp_category(-115) == "🔴 弱信号"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
