import os
import unittest
from unittest.mock import patch

from config import _get_bool_env


class TestConfig(unittest.TestCase):
    """测试配置模块。"""

    @patch.dict(os.environ, {}, clear=True)
    def test_get_bool_env_default(self):
        """测试没有设置环境变量时返回默认值。"""
        self.assertFalse(_get_bool_env("MISSING_VAR"))
        self.assertFalse(_get_bool_env("MISSING_VAR", default=False))
        self.assertTrue(_get_bool_env("MISSING_VAR", default=True))

    @patch.dict(os.environ, {
        "VAR_TRUE": "true",
        "VAR_1": "1",
        "VAR_YES": "yes",
        "VAR_ON": "on",
    }, clear=True)
    def test_get_bool_env_truthy(self):
        """测试 truthy 值。"""
        self.assertTrue(_get_bool_env("VAR_TRUE"))
        self.assertTrue(_get_bool_env("VAR_1"))
        self.assertTrue(_get_bool_env("VAR_YES"))
        self.assertTrue(_get_bool_env("VAR_ON"))

    @patch.dict(os.environ, {
        "VAR_FALSE": "false",
        "VAR_0": "0",
        "VAR_NO": "no",
        "VAR_OFF": "off",
        "VAR_RANDOM": "random_string",
        "VAR_EMPTY": "",
    }, clear=True)
    def test_get_bool_env_falsy(self):
        """测试 falsy 值。"""
        self.assertFalse(_get_bool_env("VAR_FALSE"))
        self.assertFalse(_get_bool_env("VAR_0"))
        self.assertFalse(_get_bool_env("VAR_NO"))
        self.assertFalse(_get_bool_env("VAR_OFF"))
        self.assertFalse(_get_bool_env("VAR_RANDOM"))
        self.assertFalse(_get_bool_env("VAR_EMPTY"))

    @patch.dict(os.environ, {
        "VAR_CAPS": "TRUE",
        "VAR_MIXED": "Yes",
        "VAR_SPACE_BEFORE": " 1",
        "VAR_SPACE_AFTER": "on ",
        "VAR_SPACE_BOTH": " true ",
    }, clear=True)
    def test_get_bool_env_format(self):
        """测试大小写不敏感和去除两端空格。"""
        self.assertTrue(_get_bool_env("VAR_CAPS"))
        self.assertTrue(_get_bool_env("VAR_MIXED"))
        self.assertTrue(_get_bool_env("VAR_SPACE_BEFORE"))
        self.assertTrue(_get_bool_env("VAR_SPACE_AFTER"))
        self.assertTrue(_get_bool_env("VAR_SPACE_BOTH"))


if __name__ == "__main__":
    unittest.main()
