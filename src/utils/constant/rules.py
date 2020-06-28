"""
    Password Policy Rules
"""
from password_strength import PasswordPolicy


password_policy = PasswordPolicy.from_names(
    # min length: 8
    length=8,
    # need min. 1 uppercase letters
    uppercase=1,
    # need min. 2 digits
    numbers=2,
    # need min. 1 special characters
    special=1,
    # need min. 1 non-letter characters (digits, specials, anything)
    nonletters=2,
)
