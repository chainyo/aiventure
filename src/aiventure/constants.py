"""Constants for the game."""

# BASE_PLAYER_FUNDS = 110_100.0
BASE_PLAYER_FUNDS = 100_000_000
"""Base funds for a player."""
CREATE_LAB_COST = 100_000
"""Cost to create a lab."""
CREATE_MODEL_COST = 10_000
"""Cost to create a model for any lab."""
EMPLOYEE_VALUATION_QUALITY_MULTIPLIERS = {
    1: 0.5,
    2: 0.9,
    3: 1.1,
    4: 1.4,
    5: 1.8,
    6: 2.2,
    7: 3.0,
}
"""Multiplier for the income of an employee based on their quality.

    Poor: 0.5 = -50%
    Common: 0.9 = -10%
    Uncommon: 1.1 = +10%
    Rare: 1.4 = +40%
    Epic: 1.8 = +80%
    Legendary: 2.2 = +120%
    Star: 3.0 = +200%
"""
INCOME_TICK_RATE = 60
"""Number of seconds per tick for handling income for labs."""
LOCATION_VALUATION_MULTIPLIER = {
    "us": 1.05,
    "eu": 0.95,
    "apac": 1.00,
}
"""Multiplier for the valuation of a lab based on its location.

    US: 1.05 = +5%
    EU: 0.95 = -5%
    APAC: 1.00 = +0%
"""
LOCATION_INCOME_MULTIPLIER = {
    "us": 1.05,
    "eu": 1.00,
    "apac": 1.05,
}
"""Multiplier for the income of a lab based on its location.

    US: 1.05 = +5%
    EU: 1.00 = +0%
    APAC: 1.05 = +5%
"""
LOCATION_RESEARCH_MULTIPLIER = {
    "us": 1.00,
    "eu": 1.15,
    "apac": 1.05,
}
"""Multiplier for the research speed of a lab based on its location.

    US: 1.00 = +0%
    EU: 1.15 = +15%
    APAC: 1.05 = +5%
"""
