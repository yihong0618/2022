from .cichang import get_cichang_daily
from .config import MY_CICHANG_URL, MY_DUOLINGO_URL, MY_SHANBAY_URL
from .duolingo import get_duolingo_daily
from .from_issues import get_info_from_issue_comments
from .shanbay import get_shanbay_daily

MY_STATUS_DICT_FROM_API = {
    # TODO url
    # "扇贝": {"daily_func": get_shanbay_daily, "url": MY_SHANBAY_URL, "unit_str": " (天)"},
}

MY_STATUS_DICT_FROM_COMMENTS = {
    "俯卧撑": {"daily_func": get_info_from_issue_comments, "unit_str": " (个)"},
    # "早起": {"daily_func": get_info_from_issue_comments, "unit_str": " (天)"},
}
