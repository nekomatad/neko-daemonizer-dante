import warnings

warnings.filterwarnings(
    action="ignore",
    category=RuntimeWarning,
    module='runpy',
    lineno=128
)
