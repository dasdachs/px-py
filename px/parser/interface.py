from enum import Enum, IntEnum
from typing import List, Optional, TypedDict, Union


class ParsedPxFile(TypedDict):
    aggregallowed: Optional[YesNoEnum]
    attribute_id: Optional[List[str]]
    attribute_text: Optional[List[str]]
    attributes: Optional[List[str]]
    autopen: Optional[YesNoEnum]
    axis_version: Optional[str]
    baseperiod: Optional[List[str]]
    cellnote: Optional[List[str]]
    cellnotex: Optional[List[str]]
    cfprices: Optional[CFPrices]
    charset: Optional[str]
    codepage: Optional[str]
    codes: Optional[List[str]]
    confidential: Optional[ConfidentialEnum]
    contact: Optional[str]
    contents: str
    contvariable: Optional[str]
    copyright: Optional[str]
    creation_date: Optional[str]
    data: List[Union[str, int]]
    database: Optional[List[str]]
    datanote: Optional[List[str]]
    datanotecell: Optional[str]
    datanotesum: Optional[str]
    datasymbol1: Optional[str]
    datasymbol2: Optional[str]
    datasymbol3: Optional[str]
    datasymbol4: Optional[str]
    datasymbol5: Optional[str]
    datasymbol6: Optional[str]
    datasymbolnil: Optional[str]
    datasymbolsum: Optional[str]
    dayadj: Optional[YesNoEnum]
    decimals: int
    default_graph: Optional[int]
    description: str
    descriptiondefault: Optional[YesNoEnum]
    directory_path: Optional[List[str]]
    domain: Optional[str]
    doublecolumn: Optional[YesNoEnum]
    elimination: Optional[List[Union[YesNoEnum, str]]]
    first_published: Optional[List[Union[YesNoEnum, str]]]
    heading: str
    hierarchies: Optional[List[str]]
    hierarchylevels: Optional[int]
    hierarchylevelsopen: Optional[int]
    hierarchynames: Optional[List[str]]
    info: Optional[str]
    infofile: Optional[List[str]]
    keys: Optional[List[str]]
    language: Optional[str]
    languages: Optional[List[str]]
    last_updated: Optional[str]
    link: Optional[str]
    map: Optional[str]
    matrix: str
    meta_id: Optional[str]
    next_update: Optional[str]
    note: Optional[List[str]]
    notex: Optional[List[str]]
    official_statistics: Optional[YesNoEnum]
    partitioned: Optional[str]
    precision: Optional[int]
    prestext: Optional[int]
    px_server: Optional[str]
    refperiod: Optional[str]
    rounding: Optional[int]
    seasadj: Optional[YesNoEnum]
    showdecimals: Optional[int]
    source: Optional[List[str]]
    stockfa: Optional[StockFaEnum]
    stub: str
    subject_area: str
    subject_code: str
    survey: Optional[List[str]]
    synonyms: Optional[List[str]]
    tableid: Optional[List[str]]
    timeval: Optional[str]
    title: str
    units: str
    update_frequency: Optional[List[str]]
    valuenote: Optional[List[str]]
    valuenotex: Optional[List[str]]
    values: List[str]
    variable_type: Optional[List[str]]
    valuenote: Optional[List[str]]
    valuenotex: Optional[List[str]]
    values: List[str]
    variable_type: Optional[List[str]]


class YesNoEnum(Enum):
    YES = "YES"
    NO = "NO"


class CFPrices(Enum):
    C = "C"
    F = "F"


class StockFaEnum(Enum):
    A = "A"
    F = "F"
    S = "S"


class ConfidentialEnum(IntEnum):
    1
    2