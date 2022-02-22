from .cichang import get_cichang_daily
from .config import MY_CICHANG_URL, MY_DUOLINGO_URL, MY_SHANBAY_URL
from .duolingo import get_duolingo_daily
from .forst import get_forst_daily
from .from_issues import get_info_from_issue_comments
from .shanbay import get_shanbay_daily

MY_STATUS_DICT_FROM_API = {
    "词场": {"daily_func": get_cichang_daily, "url": "", "unit_str": " (天)"},
    "番茄": {"daily_func": get_forst_daily, "url": "", "unit_str": " (个)"},
}

MY_STATUS_DICT_FROM_COMMENTS = {
    "俯卧撑": {"daily_func": get_info_from_issue_comments, "unit_str": " (个)"},
    "深蹲": {"daily_func": get_info_from_issue_comments, "unit_str": " (个)"},
    "GTD": {"daily_func": get_info_from_issue_comments, "unit_str": " (个)"},
    "周记": {"daily_func": get_info_from_issue_comments, "unit_str": " (周)"},
    "早起": {"daily_func": get_info_from_issue_comments, "unit_str": " (天)"},
}
