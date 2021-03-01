from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution("prpd_usb").version
except DistributionNotFound:
    pass
