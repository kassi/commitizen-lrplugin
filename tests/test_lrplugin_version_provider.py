import pytest
from src.commitizen_lrplugin.lrplugin_version_provider import LRPluginVersionProvider
from unittest.mock import patch

import inspect
import pathlib

info_lua = inspect.cleandoc("""{
        VERSION = { major = 1, minor = 2, revision = 3, },
        something else
    }
    """)

@pytest.fixture()
def mocker(mocker):
    mocker.patch("pathlib.Path.read_text", return_value = info_lua)
    yield mocker

class TestLRPluginVersionProvider:
    def test_get_version(self, mocker):
        assert LRPluginVersionProvider({}).get_version() == "1.2.3"

    def test_set_version(self, mocker):
        patcher = patch("pathlib.Path.write_text")
        mpatch = patcher.start()

        LRPluginVersionProvider({}).set_version("4.5.6")

        mpatch.assert_called_once()
        mpatch.assert_called_with(inspect.cleandoc("""{
            VERSION = { major = 4, minor = 5, revision = 6, },
            something else
        }
        """))
        patcher.stop()
