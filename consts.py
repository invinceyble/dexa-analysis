from enum import Enum

DATE_STRING_FORMAT = "%Y-%m-%d"


class Column:
    """Data column names."""

    SCAN_DATE = "scan_date"
    TOTAL_FAT_PERC = "total_fatperc"
    TOTAL_BMC = "total_bmc"
    TOTAL_LEAN = "total_leanmass"
    TOTAL_LEAN_AND_BMC = "total_leanandbmc"
    TOTAL_FAT = "total_fatmass"
    LEFT_ARM_FAT = "l_arm_fat"
    LEFT_ARM_LEAN = "l_arm_lean"
    LEFT_ARM_FAT_PERC = "l_arm_fatperc"
    RIGHT_ARM_FAT = "r_arm_fat"
    RIGHT_ARM_LEAN = "r_arm_lean"
    RIGHT_ARM_FAT_PERC = "r_arm_fatperc"
    TRUNK_FAT = "trunk_fat"
    TRUNK_LEAN = "trunk_lean"
    TRUNK_FAT_PERC = "trunk_fatperc"
    LEFT_LEG_FAT = "l_leg_fat"
    LEFT_LEG_LEAN = "l_leg_lean"
    LEFT_LEG_FAT_PERC = "l_leg_fatperc"
    RIGHT_LEG_FAT = "r_leg_fat"
    RIGHT_LEG_LEAN = "r_leg_lean"
    RIGHT_LEG_FAT_PERC = "r_leg_fatperc"
