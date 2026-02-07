"""
Configuration module for Match.com automation.
Centralizes all configuration settings for easy management.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class BrowserConfig:
    """Browser configuration settings."""
    headless: bool = False
    viewport_width: int = 1920
    viewport_height: int = 1080
    user_agent: str = None
    timeout: int = 30000  # milliseconds
    slow_mo: int = 0  # milliseconds to slow down operations
    
    
@dataclass
class RegionConfig:
    """Region-specific configuration."""
    region_code: str
    base_url: str
    registration_url: str
    
    
class Config:
    """Main configuration class."""
    
    # Region configurations
    REGIONS: Dict[str, RegionConfig] = {
        "us": RegionConfig(
            region_code="us",
            base_url="https://www.match.com",
            registration_url="https://www.match.com/reg"
        ),
        "uk": RegionConfig(
            region_code="uk",
            base_url="https://uk.match.com",
            registration_url="https://uk.match.com/registration"
        )
    }
    
    # Selectors for various elements
    SELECTORS = {
        "landing_form": {
            "gender_select": ["select#ggs_select", "[name='genderSeek']"],
            "min_age": ["select#desktop_landing_ages_lw"],
            "max_age": ["select#desktop_landing_ages_hg"],
            "zip_input": ["input#postalcode_input", "[name='postalCode']", ".css-13wap6q"],
            "zip_suggestions": ["[role='listbox'] [role='option']", ".suggestion-item", ".typeahead-result", "li[id*='suggestion']"],
            "submit_buttons": ["View Singles", "Get Started", "Continue", "Start now", "Begin", "Start", "Confirm"]
        },
        "registration": {
            "birthday_input": ["input[data-testid='birthday']", "input[name='birthdate']"],
            "birthday_submit": [".css-erglzy", ".css-impl9m" ],
            "name_input": ["input[data-testid='firstName']", "input[name='firstName']"],
            "email_input": ["input[name='email']", "input[type='email']"],
            "password_input": ["input[name='password']", "input[type='password']"],
        },
        "photo_upload": {
            "file_input": ["input[type='file']", "input[name='photo']", "#photo-to-upload", "input[accept*='image']"],
            "upload_trigger": [".css-17ertmd", "[aria-label='Add photo']"],
            "finalize_button": [".css-44m5wj", "button[data-testid='save-photo']", "button[aria-label='Save']"]
        },
        "overlays": {
            "cookie_accept": ["#onetrust-accept-btn-handler", ".onetrust-close-btn-handler", "button[id*='accept']"],
            "close_buttons": [".close-button", "[aria-label='Close']"]
        },
        "profile_questions": {
            "selects": ["select"],
            "radio_buttons": ["button[role='radio']", ".radio-button", "fieldset.css-0 label", "fieldset.css-0 input[type='radio']"],
            "checkboxes": ["fieldset.css-0 input[type='checkbox']"],
            "list_items": ["ul.css-1ls30xe li"]
        }
    }
    
    # Button text variations for different actions
    BUTTON_TEXTS = {
        "continue": ["continue", "Continue", "Next", "Save"],
        "skip": ["skip", "Skip", "Skip for now", "I'd rather not say", "I’d rather not say", "No, thanks", "No thanks"],
        "confirm": [
            "That's Right", "That's right", "That’s right", "That’s Right",
            "That's me", "That's Me", "That’s me", "That’s Me",
            "That's the one", "That's The One", "That’s the one", "That’s The One",
            "Confirm", "That's it", "That’s it", "Show me how"
        ],
        "submit": ["Join now", "Start now", "Done", "Create Account", "Sign Up", "Register"],
        "photo": ["upload photo", "Upload photo", "Upload", "upload"],
        "intro": ["Click here to get started"]
    }
    
    # Timeouts (in milliseconds)
    TIMEOUTS = {
        "short": 5000,
        "medium": 10000,
        "long": 20000,
        "upload": 30000
    }
    
    # Known URLs after login for flow control
    KNOWN_URLS = [
        'https://connect.facebook.net/en_US/sdk.js?hash=248c5303f7dcaac807e7f55da7948699',
        'https://www.match.com/home',
        'https://www.match.com/profile/me/create/celebration',
        'https://www.match.com/profile/me/create/core_values',
        'https://www.match.com/profile/me/create/intro',
        'https://www.match.com/profile/me/create/nextsteps',
        'https://www.match.com/profile/me/create/photo_upload_action_shot',
        'https://www.match.com/profile/me/create/photo_upload_additional_photos',
        'https://www.match.com/profile/me/create/photo_upload_full_body',
        'https://www.match.com/profile/me/create/seek_haskids',
        'https://www.match.com/profile/me/create/seek_wants_kids',
        'https://www.match.com/profile/me/create/self_body',
        'https://www.match.com/profile/me/create/self_drink',
        'https://www.match.com/profile/me/create/self_education',
        'https://www.match.com/profile/me/create/self_ethnicities',
        'https://www.match.com/profile/me/create/self_haskids',
        'https://www.match.com/profile/me/create/self_height',
        'https://www.match.com/profile/me/create/self_intent',
        'https://www.match.com/profile/me/create/self_interests',
        'https://www.match.com/profile/me/create/self_relationship',
        'https://www.match.com/profile/me/create/self_religion',
        'https://www.match.com/profile/me/create/self_smoke',
        'https://www.match.com/profile/me/create/self_topics',
        'https://www.match.com/profile/me/create/self_wantkids',
        'https://www.match.com/reg/registration/en',
        'https://www.match.com/profile/me/create/photo_upload_primary',
        'https://www.match.com/reg/registration/en-us/survey',
    ]
    
    # Delays (in milliseconds)
    DELAYS = {
        "short": 500,
        "medium": 1000,
        "long": 2000,
        "typing_min": 50,
        "typing_max": 150
    }
    
    @classmethod
    def get_region(cls, region_code: str) -> RegionConfig:
        """Get region configuration by code."""
        return cls.REGIONS.get(region_code.lower(), cls.REGIONS["us"])
    
    @classmethod
    def get_all_button_texts(cls) -> List[str]:
        """Get all button texts combined."""
        all_texts = []
        for texts in cls.BUTTON_TEXTS.values():
            all_texts.extend(texts)
        return all_texts
