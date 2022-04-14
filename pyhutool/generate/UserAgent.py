import bisect
import re
from calendar import timegm
from collections import OrderedDict
from datetime import datetime, timedelta, date
from typing import Collection, TypeVar, Iterable, Union, Sequence, Literal, Dict
import random as random_module
import string
from datetime import date as dtdate
from dateutil.tz import tzutc

T = TypeVar("T")
ElementsType = Collection[T]
DateParseType = Union[date, datetime, timedelta, str, int]
HueType = TypeVar("HueType", str, float, Sequence[int])
GenderType = TypeVar("GenderType", bound=Literal["M", "F"])

_re_hash = re.compile(r"#")
_re_perc = re.compile(r"%")
_re_excl = re.compile(r"!")
_re_at = re.compile(r"@")
_re_qm = re.compile(r"\?")
_re_cir = re.compile(r"\^")

__use_weighting__ = False

userAgents: ElementsType = (
    "chrome",
    "firefox",
    "internet_explorer",
    "opera",
    "safari",
)

windows_platform_tokens: ElementsType = (
    "Windows 95",
    "Windows 98",
    "Windows 98; Win 9x 4.90",
    "Windows CE",
    "Windows NT 4.0",
    "Windows NT 5.0",
    "Windows NT 5.01",
    "Windows NT 5.1",
    "Windows NT 5.2",
    "Windows NT 6.0",
    "Windows NT 6.1",
    "Windows NT 6.2",
    "Windows NT 10.0",
)

linux_processors: ElementsType = ("i686", "x86_64")

mac_processors: ElementsType = ("Intel", "PPC", "U; Intel", "U; PPC")

android_versions: ElementsType = (
    "1.0",
    "1.1",
    "1.5",
    "1.6",
    "2.0",
    "2.0.1",
    "2.1",
    "2.2",
    "2.2.1",
    "2.2.2",
    "2.2.3",
    "2.3",
    "2.3.1",
    "2.3.2",
    "2.3.3",
    "2.3.4",
    "2.3.5",
    "2.3.6",
    "2.3.7",
    "3.0",
    "3.1",
    "3.2",
    "3.2.1",
    "3.2.2",
    "3.2.3",
    "3.2.4",
    "3.2.5",
    "3.2.6",
    "4.0",
    "4.0.1",
    "4.0.2",
    "4.0.3",
    "4.0.4",
    "4.1",
    "4.1.1",
    "4.1.2",
    "4.2",
    "4.2.1",
    "4.2.2",
    "4.3",
    "4.3.1",
    "4.4",
    "4.4.1",
    "4.4.2",
    "4.4.3",
    "4.4.4",
    "5.0",
    "5.0.1",
    "5.0.2",
    "5.1",
    "5.1.1",
    "6.0",
    "6.0.1",
    "7.0",
    "7.1",
    "7.1.1",
    "7.1.2",
    "8.0.0",
    "8.1.0",
    "9",
    "10",
    "11",
)

apple_devices: ElementsType = ("iPhone", "iPad")

ios_versions: ElementsType = (
    "3.1.3",
    "4.2.1",
    "5.1.1",
    "6.1.6",
    "7.1.2",
    "9.3.5",
    "9.3.6",
    "10.3.3",
    "10.3.4",
    "12.4.8",
    "14.2",
    "14.2.1",
)

random = random_module.Random()
mod_random = random  # compat with name released in 0.8


def random_sample(random=None) -> float:
    if random is None:
        random = mod_random
    return random.uniform(0.0, 1.0)


def cumsum(it: Iterable[float]):
    total: float = 0
    for x in it:
        total += x
        yield total


def choices_distribution_unique(
        a,
        p,
        random=None,
        length: int = 1,
):
    # As of Python 3.7, there isn't a way to sample unique elements that takes
    # weight into account.
    if random is None:
        random = mod_random

    assert p is not None
    assert len(a) == len(p)
    assert len(a) >= length, "You can't request more unique samples than elements in the dataset."

    choices = []
    items = list(a)
    probabilities = list(p)
    for i in range(length):
        cdf = tuple(cumsum(probabilities))
        normal = cdf[-1]
        cdf2 = [i / normal for i in cdf]
        uniform_sample = random_sample(random=random)
        idx = bisect.bisect_right(cdf2, uniform_sample)
        item = items[idx]
        choices.append(item)
        probabilities.pop(idx)
        items.pop(idx)
    return choices


def choices_distribution(
        a,
        p,
        random=None,
        length: int = 1,
):
    if random is None:
        random = mod_random

    if p is not None:
        assert len(a) == len(p)

    if hasattr(random, "choices"):
        if length == 1 and p is None:
            return [random.choice(a)]
        else:
            return random.choices(a, weights=p, k=length)
    else:
        choices = []

        if p is None:
            p = itertools.repeat(1, len(a))  # type: ignore

        cdf = list(cumsum(p))  # type: ignore
        normal = cdf[-1]
        cdf2 = [i / normal for i in cdf]
        for i in range(length):
            uniform_sample = random_sample(random=random)
            idx = bisect.bisect_right(cdf2, uniform_sample)
            item = a[idx]
            choices.append(item)
        return choices


def random_elements(
        elements: ElementsType = ("a", "b", "c"),
        length=None,
        unique: bool = False,
        use_weighting=None,
):
    use_weighting = use_weighting if use_weighting is not None else __use_weighting__

    if isinstance(elements, dict) and not isinstance(elements, OrderedDict):
        raise ValueError("Use OrderedDict only to avoid dependency on PYTHONHASHSEED (See #363).")

    fn = choices_distribution_unique if unique else choices_distribution

    if length is None:
        length = random.randint(1, len(elements))

    if unique and length > len(elements):
        raise ValueError("Sample length cannot be longer than the number of unique elements to pick from.")

    if isinstance(elements, dict):
        if not hasattr(elements, "_key_cache"):
            elements._key_cache = tuple(elements.keys())  # type: ignore

        choices = elements._key_cache  # type: ignore[attr-defined]
        probabilities = tuple(elements.values()) if use_weighting else None
    else:
        if unique:
            # shortcut
            return random.sample(elements, length)
        choices = elements
        probabilities = None

    return fn(
        tuple(choices),
        probabilities,
        random,
        length=length,
    )


def mac_processor() -> str:
    """Generate a MacOS processor token used in user agent strings."""
    return random_element(mac_processors)


def linux_processor() -> str:
    """Generate a Linux processor token used in user agent strings."""
    return random_element(linux_processors)


user_agents: ElementsType = (
    "chrome",
    "firefox",
    "internet_explorer",
    "opera",
    "safari",
)


def user_agent() -> str:
    name: str = random_element(user_agents)
    print(name)


def chrome(
        version_from: int = 13,
        version_to: int = 63,
        build_from: int = 800,
        build_to: int = 899,
) -> str:
    """Generate a Chrome web browser user agent string."""
    saf: str = f"{random.randint(531, 536)}.{random.randint(0, 2)}"
    bld: str = lexify(numerify("##?###"), string.ascii_uppercase)
    tmplt: str = "({0}) AppleWebKit/{1} (KHTML, like Gecko)" " Chrome/{2}.0.{3}.0 Safari/{4}"
    tmplt_ios: str = "({0}) AppleWebKit/{1} (KHTML, like Gecko)" " CriOS/{2}.0.{3}.0 Mobile/{4} Safari/{1}"
    platforms: ElementsType = (
        tmplt.format(
            linux_platform_token(),
            saf,
            random.randint(version_from, version_to),
            random.randint(build_from, build_to),
            saf,
        ),
        tmplt.format(
            windows_platform_token(),
            saf,
            random.randint(version_from, version_to),
            random.randint(build_from, build_to),
            saf,
        ),
        tmplt.format(
            mac_platform_token(),
            saf,
            random.randint(version_from, version_to),
            random.randint(build_from, build_to),
            saf,
        ),
        tmplt.format(
            "Linux; {}".format(android_platform_token()),
            saf,
            random.randint(version_from, version_to),
            random.randint(build_from, build_to),
            saf,
        ),
        tmplt_ios.format(
            ios_platform_token(),
            saf,
            random.randint(version_from, version_to),
            random.randint(build_from, build_to),
            bld,
        ),
    )
    return "Mozilla/5.0 " + random_element(platforms)


language_locale_codes = {
    "aa": ("DJ", "ER", "ET"),
    "af": ("ZA",),
    "ak": ("GH",),
    "am": ("ET",),
    "an": ("ES",),
    "apn": ("IN",),
    "ar": (
        "AE",
        "BH",
        "DJ",
        "DZ",
        "EG",
        "EH",
        "ER",
        "IL",
        "IN",
        "IQ",
        "JO",
        "KM",
        "KW",
        "LB",
        "LY",
        "MA",
        "MR",
        "OM",
        "PS",
        "QA",
        "SA",
        "SD",
        "SO",
        "SS",
        "SY",
        "TD",
        "TN",
        "YE",
    ),
    "as": ("IN",),
    "ast": ("ES",),
    "ayc": ("PE",),
    "az": ("AZ", "IN"),
    "be": ("BY",),
    "bem": ("ZM",),
    "ber": ("DZ", "MA"),
    "bg": ("BG",),
    "bhb": ("IN",),
    "bho": ("IN",),
    "bn": ("BD", "IN"),
    "bo": ("CN", "IN"),
    "br": ("FR",),
    "brx": ("IN",),
    "bs": ("BA",),
    "byn": ("ER",),
    "ca": ("AD", "ES", "FR", "IT"),
    "ce": ("RU",),
    "ckb": ("IQ",),
    "cmn": ("TW",),
    "crh": ("UA",),
    "cs": ("CZ",),
    "csb": ("PL",),
    "cv": ("RU",),
    "cy": ("GB",),
    "da": ("DK",),
    "de": ("AT", "BE", "CH", "DE", "LI", "LU"),
    "doi": ("IN",),
    "dv": ("MV",),
    "dz": ("BT",),
    "el": ("GR", "CY"),
    "en": (
        "AG",
        "AU",
        "BW",
        "CA",
        "DK",
        "GB",
        "HK",
        "IE",
        "IN",
        "NG",
        "NZ",
        "PH",
        "SG",
        "US",
        "ZA",
        "ZM",
        "ZW",
    ),
    "eo": ("US",),
    "es": (
        "AR",
        "BO",
        "CL",
        "CO",
        "CR",
        "CU",
        "DO",
        "EC",
        "ES",
        "GT",
        "HN",
        "MX",
        "NI",
        "PA",
        "PE",
        "PR",
        "PY",
        "SV",
        "US",
        "UY",
        "VE",
    ),
    "et": ("EE",),
    "eu": ("ES", "FR"),
    "fa": ("IR",),
    "ff": ("SN",),
    "fi": ("FI",),
    "fil": ("PH",),
    "fo": ("FO",),
    "fr": ("CA", "CH", "FR", "LU"),
    "fur": ("IT",),
    "fy": ("NL", "DE"),
    "ga": ("IE",),
    "gd": ("GB",),
    "gez": ("ER", "ET"),
    "gl": ("ES",),
    "gu": ("IN",),
    "gv": ("GB",),
    "ha": ("NG",),
    "hak": ("TW",),
    "he": ("IL",),
    "hi": ("IN",),
    "hne": ("IN",),
    "hr": ("HR",),
    "hsb": ("DE",),
    "ht": ("HT",),
    "hu": ("HU",),
    "hy": ("AM",),
    "ia": ("FR",),
    "id": ("ID",),
    "ig": ("NG",),
    "ik": ("CA",),
    "is": ("IS",),
    "it": ("CH", "IT"),
    "iu": ("CA",),
    "iw": ("IL",),
    "ja": ("JP",),
    "ka": ("GE",),
    "kk": ("KZ",),
    "kl": ("GL",),
    "km": ("KH",),
    "kn": ("IN",),
    "ko": ("KR",),
    "kok": ("IN",),
    "ks": ("IN",),
    "ku": ("TR",),
    "kw": ("GB",),
    "ky": ("KG",),
    "lb": ("LU",),
    "lg": ("UG",),
    "li": ("BE", "NL"),
    "lij": ("IT",),
    "ln": ("CD",),
    "lo": ("LA",),
    "lt": ("LT",),
    "lv": ("LV",),
    "lzh": ("TW",),
    "mag": ("IN",),
    "mai": ("IN",),
    "mg": ("MG",),
    "mhr": ("RU",),
    "mi": ("NZ",),
    "mk": ("MK",),
    "ml": ("IN",),
    "mn": ("MN",),
    "mni": ("IN",),
    "mr": ("IN",),
    "ms": ("MY",),
    "mt": ("MT",),
    "my": ("MM",),
    "nan": ("TW",),
    "nb": ("NO",),
    "nds": ("DE", "NL"),
    "ne": ("NP",),
    "nhn": ("MX",),
    "niu": ("NU", "NZ"),
    "nl": ("AW", "BE", "NL"),
    "nn": ("NO",),
    "nr": ("ZA",),
    "nso": ("ZA",),
    "oc": ("FR",),
    "om": ("ET", "KE"),
    "or": ("IN",),
    "os": ("RU",),
    "pa": ("IN", "PK"),
    "pap": ("AN", "AW", "CW"),
    "pl": ("PL",),
    "ps": ("AF",),
    "pt": ("BR", "PT"),
    "quz": ("PE",),
    "raj": ("IN",),
    "ro": ("RO",),
    "ru": ("RU", "UA"),
    "rw": ("RW",),
    "sa": ("IN",),
    "sat": ("IN",),
    "sc": ("IT",),
    "sd": ("IN", "PK"),
    "se": ("NO",),
    "shs": ("CA",),
    "si": ("LK",),
    "sid": ("ET",),
    "sk": ("SK",),
    "sl": ("SI",),
    "so": ("DJ", "ET", "KE", "SO"),
    "sq": ("AL", "ML"),
    "sr": ("ME", "RS"),
    "ss": ("ZA",),
    "st": ("ZA",),
    "sv": ("FI", "SE"),
    "sw": ("KE", "TZ"),
    "szl": ("PL",),
    "ta": ("IN", "LK"),
    "tcy": ("IN",),
    "te": ("IN",),
    "tg": ("TJ",),
    "th": ("TH",),
    "the": ("NP",),
    "ti": ("ER", "ET"),
    "tig": ("ER",),
    "tk": ("TM",),
    "tl": ("PH",),
    "tn": ("ZA",),
    "tr": ("CY", "TR"),
    "ts": ("ZA",),
    "tt": ("RU",),
    "ug": ("CN",),
    "uk": ("UA",),
    "unm": ("US",),
    "ur": ("IN", "PK"),
    "uz": ("UZ",),
    "ve": ("ZA",),
    "vi": ("VN",),
    "wa": ("BE",),
    "wae": ("CH",),
    "wal": ("ET",),
    "wo": ("SN",),
    "xh": ("ZA",),
    "yi": ("US",),
    "yo": ("NG",),
    "yue": ("HK",),
    "zh": ("CN", "HK", "SG", "TW"),
    "zu": ("ZA",),
}


def languageCode():
    return random_element(language_locale_codes.keys())


def localeLang():
    language_code = languageCode()
    return (
            language_code
            + "_"
            + random_element(
            language_locale_codes[language_code],
        )
    )


def random_int(min: int = 0, max: int = 9999, step: int = 1) -> int:
    return random.randrange(min, max + 1, step)


def random_digit() -> int:
    """Generate a random digit (0 to 9)."""

    return random.randint(0, 9)


def random_digit_not_null() -> int:
    return random.randint(1, 9)


def random_digit_or_empty() -> Union[int, str]:
    if random.randint(0, 1):
        return random.randint(0, 9)
    else:
        return ""


def random_digit_not_null_or_empty() -> Union[int, str]:
    if random.randint(0, 1):
        return random.randint(1, 9)
    else:
        return ""


def random_number(digits=None, fix_len: bool = False) -> int:
    if digits is None:
        digits = random_digit_not_null()
    if digits < 0:
        raise ValueError("The digit parameter must be greater than or equal to 0.")
    if fix_len:
        if digits > 0:
            return random.randint(pow(10, digits - 1), pow(10, digits) - 1)
        else:
            raise ValueError("A number of fixed length cannot have less than 1 digit in it.")
    else:
        return random.randint(0, pow(10, digits) - 1)


def random_letter() -> str:
    return random.choice(getattr(string, "letters", string.ascii_letters))


def random_choices(self, elements: ElementsType = ("a", "b", "c"), length: int = None) -> Sequence[T]:
    return self.random_elements(elements, length, unique=False)


def random_letters(length: int = 16) -> Sequence[str]:
    return random_choices(
        getattr(string, "letters", string.ascii_letters),
        length=length,
    )


def random_lowercase_letter() -> str:
    return random.choice(string.ascii_lowercase)


def random_uppercase_letter() -> str:
    return random.choice(string.ascii_uppercase)


def numerify(text: str = "###") -> str:
    text = _re_hash.sub(lambda x: str(random_digit()), text)
    text = _re_perc.sub(lambda x: str(random_digit_not_null()), text)
    text = _re_excl.sub(lambda x: str(random_digit_or_empty()), text)
    text = _re_at.sub(lambda x: str(random_digit_not_null_or_empty()), text)
    return text


def lexify(text: str = "????", letters: str = string.ascii_letters) -> str:
    return _re_qm.sub(lambda x: random_element(letters), text)


def datetime_to_timestamp(dt: Union[dtdate, datetime]) -> int:
    if isinstance(dt, datetime) and getattr(dt, "tzinfo", None) is not None:
        dt = dt.astimezone(tzutc())
    return timegm(dt.timetuple())

def parse_date_string(cls, value: str) -> Dict[str, float]:
    parts = cls.regex.match(value)
    if not parts:
        raise Exception(f"Can't parse date string `{value}`")
    parts = parts.groupdict()
    time_params: Dict[str, float] = {}
    for (name_, param_) in parts.items():
        if param_:
            time_params[name_] = int(param_)

    if "years" in time_params:
        if "days" not in time_params:
            time_params["days"] = 0
        time_params["days"] += 365.24 * time_params.pop("years")
    if "months" in time_params:
        if "days" not in time_params:
            time_params["days"] = 0
        time_params["days"] += 30.42 * time_params.pop("months")

    if not time_params:
        raise Exception(f"Can't parse date string `{value}`")
    return time_params

def _parse_date_time(value: DateParseType, tzinfo=None) -> int:
    if isinstance(value, (datetime, dtdate)):
        return datetime_to_timestamp(value)
    now = datetime.now(tzinfo)
    if isinstance(value, timedelta):
        return datetime_to_timestamp(now + value)
    if isinstance(value, str):
        if value == "now":
            return datetime_to_timestamp(datetime.now(tzinfo))
        time_params = parse_date_string(value)
        return datetime_to_timestamp(now + timedelta(**time_params))  # type: ignore
    if isinstance(value, int):
        return datetime_to_timestamp(now + timedelta(value))
    raise Exception(f"Invalid format for date {value!r}")


def _parse_date(cls, value: DateParseType) -> dtdate:
    if isinstance(value, datetime):
        return value.date()
    elif isinstance(value, dtdate):
        return value
    today = dtdate.today()
    if isinstance(value, timedelta):
        return today + value
    if isinstance(value, str):
        if value in ("today", "now"):
            return today
        time_params = cls._parse_date_string(value)
        return today + timedelta(**time_params)  # type: ignore
    if isinstance(value, int):
        return today + timedelta(value)
    raise Exception(f"Invalid format for date {value!r}")


def date_time_between(
        start_date: DateParseType = "-30y",
        end_date: DateParseType = "now",
        tzinfo=None,
) -> datetime:
    start_date = _parse_date_time(start_date, tzinfo=tzinfo)
    end_date = _parse_date_time(end_date, tzinfo=tzinfo)
    if end_date - start_date <= 1:
        ts = start_date + random.random()
    else:
        ts = random.randint(start_date, end_date)
    if tzinfo is None:
        return datetime(1970, 1, 1, tzinfo=tzinfo) + timedelta(seconds=ts)
    else:
        return (datetime(1970, 1, 1, tzinfo=tzutc()) + timedelta(seconds=ts)).astimezone(tzinfo)


def firefox() -> str:
    """Generate a Mozilla Firefox web browser user agent string."""
    ver: ElementsType = (
        (
            f"Gecko/{date_time_between(datetime(2011, 1, 1))} "
            f"Firefox/{random.randint(4, 15)}.0"
        ),
        (
            f"Gecko/{date_time_between(datetime(2010, 1, 1))} "
            f"Firefox/3.6.{random.randint(1, 20)}"
        ),
        f"Gecko/{date_time_between(datetime(2010, 1, 1))} Firefox/3.8",
    )
    tmplt_win: str = "({0}; {1}; rv:1.9.{2}.20) {3}"
    tmplt_lin: str = "({0}; rv:1.9.{1}.20) {2}"
    tmplt_mac: str = "({0}; rv:1.9.{1}.20) {2}"
    tmplt_and: str = "({0}; Mobile; rv:{1}.0) Gecko/{1}.0 Firefox/{1}.0"
    tmplt_ios: str = "({0}) AppleWebKit/{1} (KHTML, like Gecko) FxiOS/{2}.{3}.0 Mobile/{4} Safari/{1}"
    saf: str = "{}.{}".format(random.randint(531, 536), random.randint(0, 2))
    bld: str = lexify(numerify("##?###"), string.ascii_uppercase)
    bld2: str = lexify(numerify("#?####"), string.ascii_lowercase)
    platforms: ElementsType = (
        tmplt_win.format(
            windows_platform_token(),
            localeLang().replace("_", "-"),
            random.randint(0, 2),
            random.choice(ver),
        ),
        tmplt_lin.format(
            linux_platform_token(),
            random.randint(5, 7),
            random.choice(ver),
        ),
        tmplt_mac.format(
            mac_platform_token(),
            random.randint(2, 6),
            random.choice(ver),
        ),
        tmplt_and.format(android_platform_token(), random.randint(5, 68)),
        tmplt_ios.format(
            ios_platform_token(),
            saf,
            random.randint(9, 18),
            bld2,
            bld,
        ),
    )

    return "Mozilla/5.0 " + random_element(platforms)


def localeLang() -> str:
    language_code = languageCode()
    return (
            language_code
            + "_"
            + random_element(
        language_locale_codes[language_code],
        )
    )


def safari() -> str:
    saf: str = (
        f"{random.randint(531, 535)}."
        f"{random.randint(1, 50)}."
        f"{random.randint(1, 7)}"
    )

    ver: str = (
        f"{random.randint(4, 5)}.{random.randint(0, 1)}"
        if not random.getrandbits(1)
        else f"{random.randint(4, 5)}.0.{random.randint(1, 5)}"
    )

    tmplt_win: str = "(Windows; U; {0}) AppleWebKit/{1} (KHTML, like Gecko)" " Version/{2} Safari/{3}"
    tmplt_mac: str = "({0} rv:{1}.0; {2}) AppleWebKit/{3} (KHTML, like Gecko)" " Version/{4} Safari/{5}"
    tmplt_ipod: str = (
        "(iPod; U; CPU iPhone OS {0}_{1} like Mac OS X; {2})"
        " AppleWebKit/{3} (KHTML, like Gecko) Version/{4}.0.5"
        " Mobile/8B{5} Safari/6{6}"
    )
    locale: str = localeLang().replace("_", "-")
    platforms: ElementsType = (
        tmplt_win.format(windows_platform_token(), saf, ver, saf),
        tmplt_mac.format(
            mac_platform_token(),
            random.randint(2, 6),
            locale,
            saf,
            ver,
            saf,
        ),
        tmplt_ipod.format(
            random.randint(3, 4),
            random.randint(0, 3),
            locale,
            saf,
            random.randint(3, 4),
            random.randint(111, 119),
            saf,
        ),
    )

    return "Mozilla/5.0 " + random_element(platforms)


def opera() -> str:
    token: str = (
        linux_platform_token() if random.getrandbits(1) else windows_platform_token()
    )
    locale: str = localeLang().replace("_", "-")
    platform: str = (
        f"({token}; {locale}) Presto/2.9.{random.randint(160, 190)} "
        f"Version/{random.randint(10, 12)}.00"
    )
    return f"Opera/{random.randint(8, 9)}.{random.randint(10, 99)}.{platform}"


def internet_explorer() -> str:
    return (
        f"Mozilla/5.0 (compatible; MSIE {random.randint(5, 9)}.0; "
        f"{windows_platform_token()}; "
        f"Trident/{random.randint(3, 5)}.{random.randint(0, 1)})"
    )


def random_element(elements: ElementsType = ("a", "b", "c")) -> T:
    return random_elements(elements, length=1)[0]


def windows_platform_token() -> str:
    return random_element(windows_platform_tokens)


def linux_platform_token() -> str:
    return f"X11; Linux {random_element(linux_processors)}"


def mac_platform_token() -> str:
    return (
        f"Macintosh; {random_element(mac_processors)} Mac OS X 10_"
        f"{random.randint(5, 12)}_{random.randint(0, 9)}"
    )


def android_platform_token() -> str:
    return f"Android {random_element(android_versions)}"


def ios_platform_token() -> str:
    apple_device: str = random_element(apple_devices)
    ios_version: str = random_element(ios_versions)
    return f"{apple_device}; CPU {apple_device} " f'OS {ios_version.replace(".", "_")} like Mac OS X'
