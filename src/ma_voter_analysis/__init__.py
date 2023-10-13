"""tools for analy voter histories in MA."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("ma-voter-analysis")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Ian Hunt-Isaak"
__email__ = "ianhuntisaak@gmail.com"
