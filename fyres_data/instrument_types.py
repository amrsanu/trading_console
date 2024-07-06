from enum import Enum


class InstrumentType(Enum):
    """sumary_line"""
    
    # CM_SEGMENT
    EQ = 0
    PREFSHARES = 1
    DEBENTURES = 2
    WARRANTS = 3
    MISC_NSE_BSE = 4
    INDEX = 10
    MISC_BSE = 50

    # FO_SEGMENT
    FUTIDX = 11
    FUTIVX = 12
    FUTSTK = 13
    OPTIDX = 14
    OPTSTK = 15

    # CD_SEGMENT
    FUTCUR = 16
    FUTIRT = 17
    FUTIRC = 18
    OPTCUR = 19
    UNDCUR = 20
    UNDIRC = 21
    UNDIRT = 22
    UNDIRD = 23
    INDEX_CD = 24
    FUTIRD = 25

    # COM_SEGMENT
    FUTCOM = 30
    OPTFUT = 31
    OPTCOM = 32


# Example usage:
value = 0
instrument_type = InstrumentType(value)
print(instrument_type)           # Output: InstrumentType.EQ
print(instrument_type.name)      # Output: EQ
print(instrument_type.value)     # Output: 0
