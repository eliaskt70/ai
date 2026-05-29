"""
Rule-Based AI Agent: Local Service Locator
-------------------------------------------
Enhanced terminal application using explicit if/elif/else rule-based logic
to recommend local service providers based on user inputs.
No machine learning, no external APIs, no packages beyond Python standard library.

Features:
- Rich terminal UI with ANSI colors, box-drawing characters, and animations
- 8+ service categories with 20+ provider database
- 15+ explicit recommendation rules
- Matching score algorithm
- Session summary with file export option
"""

import sys
import time
import os
from datetime import datetime


# =============================================================================
# ANSI Color Codes and Terminal Styling
# =============================================================================

class Colors:
    """ANSI escape codes for terminal coloring."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


C = Colors


def colorize(text, *codes):
    """Apply color codes to text."""
    return "".join(codes) + text + C.RESET


def stars_display(rating):
    """Return a colored star representation of a rating."""
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    result = colorize("*" * full, C.BRIGHT_YELLOW)
    if half:
        result += colorize("*", C.YELLOW)
    result += colorize("." * empty, C.DIM)
    return result


# =============================================================================
# Box Drawing and UI Components
# =============================================================================

BOX_TL = "\u250c"  # Top-left corner
BOX_TR = "\u2510"  # Top-right corner
BOX_BL = "\u2514"  # Bottom-left corner
BOX_BR = "\u2518"  # Bottom-right corner
BOX_H = "\u2500"   # Horizontal line
BOX_V = "\u2502"   # Vertical line
BOX_LT = "\u251c"  # Left T-junction
BOX_RT = "\u2524"  # Right T-junction
BOX_TT = "\u252c"  # Top T-junction
BOX_BT = "\u2534"  # Bottom T-junction
BOX_CROSS = "\u253c"  # Cross


def draw_box(lines, width=60, title=None, color=C.CYAN):
    """Draw a box around text lines."""
    output = []
    inner_w = width - 2
    if title:
        title_str = f" {title} "
        pad = inner_w - len(title_str)
        left_pad = pad // 2
        right_pad = pad - left_pad
        top_line = color + BOX_TL + BOX_H * left_pad + C.BOLD + title_str + C.RESET + color + BOX_H * right_pad + BOX_TR + C.RESET
    else:
        top_line = color + BOX_TL + BOX_H * inner_w + BOX_TR + C.RESET
    output.append(top_line)
    for line in lines:
        # Strip ANSI for length calculation
        visible_len = len(strip_ansi(line))
        padding = inner_w - visible_len - 1
        if padding < 0:
            padding = 0
        output.append(color + BOX_V + C.RESET + " " + line + " " * padding + color + BOX_V + C.RESET)
    output.append(color + BOX_BL + BOX_H * inner_w + BOX_BR + C.RESET)
    return "\n".join(output)


def strip_ansi(text):
    """Remove ANSI escape codes for length calculations."""
    import re
    return re.sub(r'\033\[[0-9;]*m', '', text)


def draw_separator(width=60, char=BOX_H, color=C.DIM):
    """Draw a horizontal separator line."""
    return color + char * width + C.RESET


def spinner_animation(message, duration=1.0):
    """Show a simple spinner animation."""
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r  {colorize(frame, C.BRIGHT_CYAN)} {message}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r  {colorize('[done]', C.BRIGHT_GREEN)} {message}\n")
    sys.stdout.flush()


def progress_bar(message, steps=20, duration=1.0):
    """Show a progress bar animation."""
    delay = duration / steps
    for i in range(steps + 1):
        filled = "=" * i
        empty = " " * (steps - i)
        percent = int((i / steps) * 100)
        bar = colorize(f"[{filled}{empty}]", C.BRIGHT_GREEN)
        sys.stdout.write(f"\r  {bar} {percent}% {message}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()




# =============================================================================
# Welcome Banner (ASCII Art)
# =============================================================================

WELCOME_BANNER = f"""
{C.BRIGHT_CYAN}{C.BOLD}
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ░█░░░█▀█░█▀▀░█▀█░█░░░░░░█▀▀░█▀▀░█▀▄░█░█░▀█▀░█▀▀░█▀▀ ║
    ║   ░█░░░█░█░█░░░█▀█░█░░░░░░▀▀█░█▀▀░█▀▄░▀▄▀░░█░░█░░░█▀▀ ║
    ║   ░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░░░░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀▀▀░▀▀▀ ║
    ║                                                           ║
    ║        ░█░░░█▀█░█▀▀░█▀█░▀█▀░█▀█░█▀▄                     ║
    ║        ░█░░░█░█░█░░░█▀█░░█░░█░█░█▀▄                     ║
    ║        ░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀                     ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
{C.RESET}
    {C.BRIGHT_WHITE}{C.BOLD}Rule-Based AI Agent - Local Service Locator v2.0{C.RESET}
    {C.DIM}Powered by deterministic conditional logic - No ML used{C.RESET}
    {C.DIM}Python Standard Library Only - Works everywhere{C.RESET}
"""


# =============================================================================
# Provider Database (Simulated)
# =============================================================================

PROVIDERS = [
    {
        "id": 1,
        "name": "QuickFix Handyman Services",
        "category": "Maintenance",
        "rating": 4.5,
        "price_range": "$50-150",
        "price_tier": 2,
        "distance_km": 0.8,
        "phone": "(555) 234-0011",
        "availability": "Mon-Sat 7AM-8PM",
        "specialties": ["plumbing", "electrical", "carpentry"],
        "urgency_capable": True,
        "response_time_min": 30,
    },
    {
        "id": 2,
        "name": "EliteRepair Pro",
        "category": "Maintenance",
        "rating": 4.9,
        "price_range": "$150-500",
        "price_tier": 3,
        "distance_km": 2.5,
        "phone": "(555) 234-0022",
        "availability": "24/7",
        "specialties": ["emergency repair", "HVAC", "roofing"],
        "urgency_capable": True,
        "response_time_min": 15,
    },
    {
        "id": 3,
        "name": "Budget Maintenance Co.",
        "category": "Maintenance",
        "rating": 3.8,
        "price_range": "$0-50",
        "price_tier": 1,
        "distance_km": 1.5,
        "phone": "(555) 234-0033",
        "availability": "Mon-Fri 9AM-5PM",
        "specialties": ["general maintenance", "painting"],
        "urgency_capable": False,
        "response_time_min": 120,
    },
    {
        "id": 4,
        "name": "SpeedDash Courier",
        "category": "Delivery",
        "rating": 4.7,
        "price_range": "$0-50",
        "price_tier": 1,
        "distance_km": 0.5,
        "phone": "(555) 345-0011",
        "availability": "Daily 8AM-10PM",
        "specialties": ["same-day delivery", "food delivery", "documents"],
        "urgency_capable": True,
        "response_time_min": 15,
    },
    {
        "id": 5,
        "name": "CrossTown Logistics",
        "category": "Delivery",
        "rating": 4.2,
        "price_range": "$50-150",
        "price_tier": 2,
        "distance_km": 4.0,
        "phone": "(555) 345-0022",
        "availability": "Mon-Sat 6AM-9PM",
        "specialties": ["large packages", "furniture", "appliances"],
        "urgency_capable": True,
        "response_time_min": 45,
    },
    {
        "id": 6,
        "name": "EcoShip Standard",
        "category": "Delivery",
        "rating": 3.9,
        "price_range": "$0-50",
        "price_tier": 1,
        "distance_km": 5.0,
        "phone": "(555) 345-0033",
        "availability": "Mon-Fri 9AM-6PM",
        "specialties": ["economy shipping", "bulk delivery"],
        "urgency_capable": False,
        "response_time_min": 1440,
    },
    {
        "id": 7,
        "name": "StrategyFirst Consulting",
        "category": "Consulting",
        "rating": 4.8,
        "price_range": "$150-500",
        "price_tier": 3,
        "distance_km": 3.0,
        "phone": "(555) 456-0011",
        "availability": "Mon-Fri 8AM-6PM",
        "specialties": ["business strategy", "finance", "growth"],
        "urgency_capable": True,
        "response_time_min": 60,
    },
    {
        "id": 8,
        "name": "QuickAdvice Online",
        "category": "Consulting",
        "rating": 4.3,
        "price_range": "$50-150",
        "price_tier": 2,
        "distance_km": 0.0,
        "phone": "(555) 456-0022",
        "availability": "24/7",
        "specialties": ["legal basics", "tax advice", "small business"],
        "urgency_capable": True,
        "response_time_min": 10,
    },
    {
        "id": 9,
        "name": "CityMed Urgent Care",
        "category": "Medical",
        "rating": 4.6,
        "price_range": "$150-500",
        "price_tier": 3,
        "distance_km": 1.2,
        "phone": "(555) 567-0011",
        "availability": "24/7",
        "specialties": ["urgent care", "general practice", "x-ray"],
        "urgency_capable": True,
        "response_time_min": 5,
    },
    {
        "id": 10,
        "name": "Neighborhood Clinic",
        "category": "Medical",
        "rating": 4.4,
        "price_range": "$50-150",
        "price_tier": 2,
        "distance_km": 0.7,
        "phone": "(555) 567-0022",
        "availability": "Mon-Sat 8AM-8PM",
        "specialties": ["family medicine", "vaccinations", "checkups"],
        "urgency_capable": False,
        "response_time_min": 30,
    },
    {
        "id": 11,
        "name": "BrightMinds Tutoring",
        "category": "Education",
        "rating": 4.7,
        "price_range": "$50-150",
        "price_tier": 2,
        "distance_km": 2.0,
        "phone": "(555) 678-0011",
        "availability": "Mon-Sun 9AM-9PM",
        "specialties": ["math", "science", "test prep", "languages"],
        "urgency_capable": True,
        "response_time_min": 60,
    },
    {
        "id": 12,
        "name": "LearnFast Academy",
        "category": "Education",
        "rating": 4.1,
        "price_range": "$0-50",
        "price_tier": 1,
        "distance_km": 3.5,
        "phone": "(555) 678-0022",
        "availability": "Mon-Fri 3PM-8PM, Sat 10AM-4PM",
        "specialties": ["homework help", "reading", "writing"],
        "urgency_capable": False,
        "response_time_min": 120,
    },
    {
        "id": 13,
        "name": "SparkleClean Services",
        "category": "Cleaning",
        "rating": 4.6,
        "price_range": "$50-150",
        "price_tier": 2,
        "distance_km": 1.0,
        "phone": "(555) 789-0011",
        "availability": "Mon-Sat 7AM-7PM",
        "specialties": ["residential", "deep cleaning", "move-out"],
        "urgency_capable": True,
        "response_time_min": 45,
    },
    {
        "id": 14,
        "name": "GreenSweep Eco Cleaning",
        "category": "Cleaning",
        "rating": 4.3,
        "price_range": "$50-150",
        "price_tier": 2,
        "distance_km": 2.2,
        "phone": "(555) 789-0022",
        "availability": "Mon-Fri 8AM-6PM",
        "specialties": ["eco-friendly", "office cleaning", "sanitization"],
        "urgency_capable": False,
        "response_time_min": 120,
    },
    {
        "id": 15,
        "name": "BudgetClean Express",
        "category": "Cleaning",
        "rating": 3.7,
        "price_range": "$0-50",
        "price_tier": 1,
        "distance_km": 0.9,
        "phone": "(555) 789-0033",
        "availability": "Daily 6AM-10PM",
        "specialties": ["quick tidy", "laundry", "dishes"],
        "urgency_capable": True,
        "response_time_min": 20,
    },
    {
        "id": 16,
        "name": "CityRide Transportation",
        "category": "Transportation",
        "rating": 4.5,
        "price_range": "$50-150",
        "price_tier": 2,
        "distance_km": 1.0,
        "phone": "(555) 890-0011",
        "availability": "24/7",
        "specialties": ["airport transfer", "city rides", "executive"],
        "urgency_capable": True,
        "response_time_min": 10,
    },
    {
        "id": 17,
        "name": "BudgetCab Local",
        "category": "Transportation",
        "rating": 3.9,
        "price_range": "$0-50",
        "price_tier": 1,
        "distance_km": 0.3,
        "phone": "(555) 890-0022",
        "availability": "Daily 5AM-1AM",
        "specialties": ["short trips", "shared rides", "errands"],
        "urgency_capable": True,
        "response_time_min": 5,
    },
    {
        "id": 18,
        "name": "LuxeMove Premium",
        "category": "Transportation",
        "rating": 4.9,
        "price_range": "$150-500",
        "price_tier": 3,
        "distance_km": 2.0,
        "phone": "(555) 890-0033",
        "availability": "24/7",
        "specialties": ["luxury vehicles", "events", "corporate"],
        "urgency_capable": True,
        "response_time_min": 20,
    },
    {
        "id": 19,
        "name": "TastyBites Catering",
        "category": "Food",
        "rating": 4.7,
        "price_range": "$150-500",
        "price_tier": 3,
        "distance_km": 3.0,
        "phone": "(555) 901-0011",
        "availability": "Mon-Sun 6AM-11PM",
        "specialties": ["events", "corporate catering", "weddings"],
        "urgency_capable": False,
        "response_time_min": 1440,
    },
    {
        "id": 20,
        "name": "QuickBite Express",
        "category": "Food",
        "rating": 4.4,
        "price_range": "$0-50",
        "price_tier": 1,
        "distance_km": 0.6,
        "phone": "(555) 901-0022",
        "availability": "Daily 10AM-12AM",
        "specialties": ["fast food", "lunch delivery", "snacks"],
        "urgency_capable": True,
        "response_time_min": 20,
    },
    {
        "id": 21,
        "name": "GourmetChef Home Dining",
        "category": "Food",
        "rating": 4.8,
        "price_range": "$150-500",
        "price_tier": 3,
        "distance_km": 1.5,
        "phone": "(555) 901-0033",
        "availability": "Tue-Sun 5PM-10PM",
        "specialties": ["private chef", "dinner parties", "fine dining"],
        "urgency_capable": False,
        "response_time_min": 480,
    },
    {
        "id": 22,
        "name": "NightOwl Emergency Services",
        "category": "Medical",
        "rating": 4.5,
        "price_range": "$500+",
        "price_tier": 4,
        "distance_km": 2.0,
        "phone": "(555) 567-0099",
        "availability": "24/7",
        "specialties": ["emergency", "ambulance", "night care"],
        "urgency_capable": True,
        "response_time_min": 5,
    },
    {
        "id": 23,
        "name": "ProConsult 24/7",
        "category": "Consulting",
        "rating": 4.6,
        "price_range": "$500+",
        "price_tier": 4,
        "distance_km": 0.0,
        "phone": "(555) 456-0099",
        "availability": "24/7",
        "specialties": ["crisis management", "legal emergency", "corporate"],
        "urgency_capable": True,
        "response_time_min": 5,
    },
]




# =============================================================================
# Service Categories
# =============================================================================

SERVICE_CATEGORIES = {
    "1": "Maintenance",
    "2": "Delivery",
    "3": "Consulting",
    "4": "Medical",
    "5": "Education",
    "6": "Cleaning",
    "7": "Transportation",
    "8": "Food",
}

DISTANCE_OPTIONS = {
    "1": "<1km",
    "2": "1-3km",
    "3": ">3km",
}

URGENCY_OPTIONS = {
    "1": "Immediate",
    "2": "Within a few hours",
    "3": "Scheduled (days)",
}

BUDGET_OPTIONS = {
    "1": "$0-50",
    "2": "$50-150",
    "3": "$150-500",
    "4": "$500+",
}

RATING_OPTIONS = {
    "1": "Any rating",
    "2": "4+ stars",
    "3": "Top rated only (4.5+)",
}

TIME_OPTIONS = {
    "1": "Morning (6AM-12PM)",
    "2": "Afternoon (12PM-5PM)",
    "3": "Evening (5PM-9PM)",
    "4": "Night (9PM-6AM)",
}

DAY_OPTIONS = {
    "1": "Weekday",
    "2": "Weekend",
    "3": "Any day",
}


# =============================================================================
# Input Collection with Validation
# =============================================================================

class QuestionNavigator:
    """Manages question flow with back-navigation support."""

    def __init__(self):
        self.answers = {}
        self.questions = [
            "service_type",
            "distance",
            "urgency",
            "budget",
            "rating",
            "time_of_day",
            "day_preference",
        ]
        self.current_index = 0

    def ask_question(self, question_func):
        """Ask a question with back-navigation support."""
        while True:
            result = question_func(self.current_index + 1, len(self.questions))
            if result == "BACK":
                if self.current_index > 0:
                    self.current_index -= 1
                    return "BACK"
                else:
                    print(colorize("  You are already at the first question.", C.YELLOW))
            else:
                return result


def print_question_header(num, total, title):
    """Print a styled question header."""
    print()
    bar_filled = int((num / total) * 20)
    bar_empty = 20 - bar_filled
    progress = colorize("=" * bar_filled, C.BRIGHT_GREEN) + colorize("-" * bar_empty, C.DIM)
    print(f"  [{progress}] {colorize(f'Question {num}/{total}', C.BRIGHT_WHITE)}")
    print(f"  {colorize(title, C.BOLD, C.BRIGHT_CYAN)}")
    back_msg = '(Type "b" to go back to previous question)'
    print(f"  {colorize(back_msg, C.DIM)}")
    print()


def get_validated_input(prompt, valid_options, allow_back=True):
    """Get and validate user input."""
    while True:
        choice = input(f"  {colorize('>', C.BRIGHT_GREEN)} {prompt} ").strip().lower()
        if allow_back and choice == "b":
            return "BACK"
        if choice in valid_options:
            return choice
        valid_str = ", ".join(valid_options)
        print(colorize(f"    Invalid input. Please enter one of: {valid_str}", C.BRIGHT_RED))


def ask_service_type(num, total):
    """Ask for service type."""
    print_question_header(num, total, "What type of service do you need?")
    for key, val in SERVICE_CATEGORIES.items():
        icon = {
            "Maintenance": "🔧", "Delivery": "📦", "Consulting": "💼",
            "Medical": "🏥", "Education": "📚", "Cleaning": "🧹",
            "Transportation": "🚗", "Food": "🍽️",
        }.get(val, " ")
        print(f"    {colorize(key, C.BRIGHT_YELLOW)}. {icon}  {val}")
    print()
    choice = get_validated_input("Your choice (1-8):", list(SERVICE_CATEGORIES.keys()))
    if choice == "BACK":
        return "BACK"
    return SERVICE_CATEGORIES[choice]


def ask_distance(num, total):
    """Ask for distance preference."""
    print_question_header(num, total, "How far are you willing to go?")
    print(f"    {colorize('1', C.BRIGHT_YELLOW)}. Less than 1 km (walking distance)")
    print(f"    {colorize('2', C.BRIGHT_YELLOW)}. 1-3 km (short drive / bike ride)")
    print(f"    {colorize('3', C.BRIGHT_YELLOW)}. More than 3 km (any distance is fine)")
    print()
    choice = get_validated_input("Your choice (1-3):", list(DISTANCE_OPTIONS.keys()))
    if choice == "BACK":
        return "BACK"
    return DISTANCE_OPTIONS[choice]


def ask_urgency(num, total):
    """Ask for urgency level."""
    print_question_header(num, total, "How urgent is your request?")
    print(f"    {colorize('1', C.BRIGHT_YELLOW)}. {colorize('Immediate', C.BRIGHT_RED)} - I need help right now!")
    print(f"    {colorize('2', C.BRIGHT_YELLOW)}. Within a few hours")
    print(f"    {colorize('3', C.BRIGHT_YELLOW)}. Scheduled (can wait days)")
    print()
    choice = get_validated_input("Your choice (1-3):", list(URGENCY_OPTIONS.keys()))
    if choice == "BACK":
        return "BACK"
    return URGENCY_OPTIONS[choice]


def ask_budget(num, total):
    """Ask for budget range."""
    print_question_header(num, total, "What is your budget range?")
    print(f"    {colorize('1', C.BRIGHT_YELLOW)}. $0 - $50     {colorize('(Budget-friendly)', C.DIM)}")
    print(f"    {colorize('2', C.BRIGHT_YELLOW)}. $50 - $150   {colorize('(Mid-range)', C.DIM)}")
    print(f"    {colorize('3', C.BRIGHT_YELLOW)}. $150 - $500  {colorize('(Premium)', C.DIM)}")
    print(f"    {colorize('4', C.BRIGHT_YELLOW)}. $500+        {colorize('(No limit)', C.DIM)}")
    print()
    choice = get_validated_input("Your choice (1-4):", list(BUDGET_OPTIONS.keys()))
    if choice == "BACK":
        return "BACK"
    return BUDGET_OPTIONS[choice]


def ask_rating(num, total):
    """Ask for rating preference."""
    print_question_header(num, total, "What minimum rating do you prefer?")
    print(f"    {colorize('1', C.BRIGHT_YELLOW)}. Any rating (show all options)")
    print(f"    {colorize('2', C.BRIGHT_YELLOW)}. 4+ stars (good and above)")
    print(f"    {colorize('3', C.BRIGHT_YELLOW)}. Top rated only (4.5+ stars)")
    print()
    choice = get_validated_input("Your choice (1-3):", list(RATING_OPTIONS.keys()))
    if choice == "BACK":
        return "BACK"
    return RATING_OPTIONS[choice]


def ask_time_of_day(num, total):
    """Ask for preferred time."""
    print_question_header(num, total, "What time of day do you need the service?")
    print(f"    {colorize('1', C.BRIGHT_YELLOW)}. Morning   (6AM - 12PM)")
    print(f"    {colorize('2', C.BRIGHT_YELLOW)}. Afternoon (12PM - 5PM)")
    print(f"    {colorize('3', C.BRIGHT_YELLOW)}. Evening   (5PM - 9PM)")
    print(f"    {colorize('4', C.BRIGHT_YELLOW)}. Night     (9PM - 6AM)")
    print()
    choice = get_validated_input("Your choice (1-4):", list(TIME_OPTIONS.keys()))
    if choice == "BACK":
        return "BACK"
    return TIME_OPTIONS[choice]


def ask_day_preference(num, total):
    """Ask for day preference."""
    print_question_header(num, total, "What day do you prefer?")
    print(f"    {colorize('1', C.BRIGHT_YELLOW)}. Weekday (Monday - Friday)")
    print(f"    {colorize('2', C.BRIGHT_YELLOW)}. Weekend (Saturday - Sunday)")
    print(f"    {colorize('3', C.BRIGHT_YELLOW)}. Any day")
    print()
    choice = get_validated_input("Your choice (1-3):", list(DAY_OPTIONS.keys()))
    if choice == "BACK":
        return "BACK"
    return DAY_OPTIONS[choice]




# =============================================================================
# Rule Engine - Recommendation Logic
# =============================================================================

def apply_rules(inputs):
    """
    Apply 20 explicit rules to generate recommendation text.
    Each rule checks a specific combination of user inputs and returns
    a tailored advisory message. This is purely rule-based logic with no ML.
    """

    service = inputs["service_type"]
    distance = inputs["distance"]
    urgency = inputs["urgency"]
    budget = inputs["budget"]
    time_of_day = inputs["time_of_day"]

    # Rule 1: Immediate medical needs at night
    if service == "Medical" and urgency == "Immediate" and time_of_day == "Night (9PM-6AM)":
        return (
            "CRITICAL: For immediate medical needs at night, call emergency services "
            "(911) or visit a 24-hour urgent care clinic. Do not delay treatment."
        )

    # Rule 2: Immediate medical with high budget
    elif service == "Medical" and urgency == "Immediate" and budget in ("$150-500", "$500+"):
        return (
            "Seek immediate care at a nearby urgent care center or emergency room. "
            "With your budget, consider a private urgent care facility for faster service."
        )

    # Rule 3: Scheduled medical, budget-friendly
    elif service == "Medical" and urgency == "Scheduled (days)" and budget == "$0-50":
        return (
            "Book an appointment at a community health clinic. Many offer sliding-scale "
            "fees. Call ahead to confirm availability and bring insurance info if available."
        )

    # Rule 4: Immediate maintenance nearby, low budget
    elif service == "Maintenance" and distance == "<1km" and urgency == "Immediate" and budget == "$0-50":
        return (
            "Contact a local neighborhood handyman for quick, affordable fixes. "
            "They are close, available immediately, and perfect for small jobs."
        )

    # Rule 5: Immediate maintenance with premium budget
    elif service == "Maintenance" and urgency == "Immediate" and budget in ("$150-500", "$500+"):
        return (
            "Call a premium emergency repair service. With your budget, you can get "
            "licensed professionals who guarantee their work and respond within minutes."
        )

    # Rule 6: Scheduled maintenance, mid-range
    elif service == "Maintenance" and urgency == "Scheduled (days)" and budget == "$50-150":
        return (
            "Book a local maintenance company for a scheduled visit. Planning ahead "
            "gets you competitive rates without emergency premiums."
        )

    # Rule 7: Immediate delivery, short distance
    elif service == "Delivery" and distance == "<1km" and urgency == "Immediate":
        return (
            "Use a local bike courier for ultra-fast nearby delivery. For distances "
            "under 1km, bike couriers are the fastest and most efficient option."
        )

    # Rule 8: Long-distance delivery, budget-friendly
    elif service == "Delivery" and distance == ">3km" and budget == "$0-50":
        return (
            "Use a standard economy shipping service. For longer distances on a "
            "tight budget, economy options deliver reliably within a few days."
        )

    # Rule 9: Urgent delivery, any distance, premium budget
    elif service == "Delivery" and urgency == "Immediate" and budget in ("$150-500", "$500+"):
        return (
            "Book a premium same-day courier service with guaranteed delivery times. "
            "Express logistics providers offer real-time tracking and insurance."
        )

    # Rule 10: Consulting, immediate, high budget
    elif service == "Consulting" and urgency == "Immediate" and budget in ("$150-500", "$500+"):
        return (
            "Engage an on-call expert consultant. Premium consultants offer "
            "immediate video calls or on-site visits for urgent business decisions."
        )

    # Rule 11: Consulting, scheduled, budget-friendly
    elif service == "Consulting" and urgency == "Scheduled (days)" and budget in ("$0-50", "$50-150"):
        return (
            "Book an online consultation session. Many experts offer affordable "
            "scheduled appointments via video call at reduced rates."
        )

    # Rule 12: Education/tutoring, immediate need
    elif service == "Education" and urgency == "Immediate":
        return (
            "Look for on-demand tutoring services. Many tutors offer instant "
            "online sessions for test prep or homework help."
        )

    # Rule 13: Education, scheduled, budget-friendly
    elif service == "Education" and urgency == "Scheduled (days)" and budget in ("$0-50", "$50-150"):
        return (
            "Enroll in group tutoring sessions or community learning programs. "
            "These offer excellent value with structured learning plans."
        )

    # Rule 14: Cleaning, immediate, budget-friendly
    elif service == "Cleaning" and urgency == "Immediate" and budget == "$0-50":
        return (
            "Book a quick-tidy express cleaning service. Budget cleaners can handle "
            "essential areas fast for an affordable price."
        )

    # Rule 15: Cleaning, scheduled, eco-conscious
    elif service == "Cleaning" and urgency == "Scheduled (days)":
        return (
            "Schedule a professional deep-cleaning service. Planning ahead gives you "
            "access to specialized crews and eco-friendly options."
        )

    # Rule 16: Transportation, immediate, night time
    elif service == "Transportation" and urgency == "Immediate" and time_of_day == "Night (9PM-6AM)":
        return (
            "Book a 24/7 ride service for safe nighttime transportation. "
            "Look for services with real-time tracking and verified drivers."
        )

    # Rule 17: Transportation, immediate, budget-friendly
    elif service == "Transportation" and urgency == "Immediate" and budget == "$0-50":
        return (
            "Use a budget ride-sharing service or local taxi. Shared rides "
            "significantly reduce costs for short-distance trips."
        )

    # Rule 18: Transportation, premium
    elif service == "Transportation" and budget in ("$150-500", "$500+"):
        return (
            "Book a premium transportation service with luxury vehicles. "
            "Perfect for airport transfers, events, or corporate needs."
        )

    # Rule 19: Food/catering, immediate
    elif service == "Food" and urgency == "Immediate":
        return (
            "Order from a nearby quick-service restaurant with delivery. "
            "Express food delivery can arrive in 15-30 minutes."
        )

    # Rule 20: Food/catering, scheduled, premium
    elif service == "Food" and urgency == "Scheduled (days)" and budget in ("$150-500", "$500+"):
        return (
            "Book a professional catering service or private chef. "
            "For events and special occasions, plan at least 48 hours ahead."
        )

    # Default catch-all rule
    else:
        return (
            "Based on your preferences, we recommend browsing our full provider "
            "directory. Your specific combination has multiple good options available."
        )




# =============================================================================
# Matching Score Algorithm
# =============================================================================

def calculate_match_score(provider, inputs):
    """
    Calculate a matching score (0-100) for a provider based on user inputs.
    Uses weighted criteria to determine relevance.
    """
    score = 0
    max_score = 0

    # Category match (mandatory - weight: 30)
    max_score += 30
    if provider["category"] == inputs["service_type"]:
        score += 30
    else:
        return 0  # Wrong category = no match

    # Distance match (weight: 20)
    max_score += 20
    user_distance = inputs["distance"]
    provider_dist = provider["distance_km"]
    if user_distance == "<1km":
        if provider_dist < 1.0:
            score += 20
        elif provider_dist < 2.0:
            score += 10
        else:
            score += 5
    elif user_distance == "1-3km":
        if 1.0 <= provider_dist <= 3.0:
            score += 20
        elif provider_dist < 1.0:
            score += 18  # Closer is still good
        else:
            score += 8
    elif user_distance == ">3km":
        score += 20  # Any distance is fine

    # Budget match (weight: 20)
    max_score += 20
    budget = inputs["budget"]
    price_tier = provider["price_tier"]
    budget_tier_map = {"$0-50": 1, "$50-150": 2, "$150-500": 3, "$500+": 4}
    user_tier = budget_tier_map.get(budget, 2)
    if price_tier <= user_tier:
        score += 20
    elif price_tier == user_tier + 1:
        score += 10
    else:
        score += 2

    # Urgency match (weight: 15)
    max_score += 15
    urgency = inputs["urgency"]
    if urgency == "Immediate":
        if provider["urgency_capable"]:
            score += 15
        else:
            score += 3
    elif urgency == "Within a few hours":
        if provider["urgency_capable"] or provider["response_time_min"] <= 180:
            score += 15
        else:
            score += 8
    else:  # Scheduled
        score += 15  # All providers can handle scheduled

    # Rating match (weight: 15)
    max_score += 15
    rating_pref = inputs["rating"]
    provider_rating = provider["rating"]
    if rating_pref == "Any rating":
        score += 15
    elif rating_pref == "4+ stars":
        if provider_rating >= 4.0:
            score += 15
        elif provider_rating >= 3.5:
            score += 8
        else:
            score += 3
    elif rating_pref == "Top rated only (4.5+)":
        if provider_rating >= 4.5:
            score += 15
        elif provider_rating >= 4.0:
            score += 7
        else:
            score += 2

    # Normalize to percentage
    return int((score / max_score) * 100)


def get_top_providers(inputs, top_n=3):
    """Get top N providers sorted by matching score."""
    scored = []
    for provider in PROVIDERS:
        score = calculate_match_score(provider, inputs)
        if score > 0:
            scored.append((score, provider))
    scored.sort(key=lambda x: (-x[0], -x[1]["rating"]))
    return scored[:top_n]


# =============================================================================
# Results Display
# =============================================================================

def display_provider_card(rank, score, provider):
    """Display a single provider in a card format."""
    # Rank badge
    rank_colors = {1: C.BRIGHT_YELLOW, 2: C.BRIGHT_WHITE, 3: C.BRIGHT_CYAN}
    rank_color = rank_colors.get(rank, C.WHITE)
    rank_badge = colorize(f"  #{rank}", rank_color, C.BOLD)

    # Score bar
    score_blocks = score // 5
    score_bar = colorize("=" * score_blocks, C.BRIGHT_GREEN) + colorize("-" * (20 - score_blocks), C.DIM)

    # Provider card
    print(f"\n  {colorize(BOX_TL + BOX_H * 56 + BOX_TR, rank_color)}")
    print(f"  {colorize(BOX_V, rank_color)} {rank_badge} {colorize(provider['name'], C.BOLD, C.BRIGHT_WHITE):<50} {colorize(BOX_V, rank_color)}")
    print(f"  {colorize(BOX_V, rank_color)}{' ' * 56}{colorize(BOX_V, rank_color)}")

    # Match score
    print(f"  {colorize(BOX_V, rank_color)}   Match Score: [{score_bar}] {colorize(f'{score}%', C.BRIGHT_GREEN, C.BOLD):<20}{colorize(BOX_V, rank_color)}")

    # Rating
    rating_str = stars_display(provider['rating'])
    print(f"  {colorize(BOX_V, rank_color)}   Rating:      {rating_str} ({provider['rating']}/5.0)             {colorize(BOX_V, rank_color)}")

    # Details
    print(f"  {colorize(BOX_V, rank_color)}   Phone:       {colorize(provider['phone'], C.BRIGHT_CYAN):<45}{colorize(BOX_V, rank_color)}")
    print(f"  {colorize(BOX_V, rank_color)}   Price:       {colorize(provider['price_range'], C.BRIGHT_GREEN):<45}{colorize(BOX_V, rank_color)}")

    dist_str = f"{provider['distance_km']} km away" if provider['distance_km'] > 0 else "Online/Remote"
    print(f"  {colorize(BOX_V, rank_color)}   Distance:    {dist_str:<44}{colorize(BOX_V, rank_color)}")

    # Response time
    rt = provider['response_time_min']
    if rt < 60:
        time_str = f"~{rt} min"
    elif rt < 1440:
        time_str = f"~{rt // 60} hour(s)"
    else:
        time_str = f"~{rt // 1440} day(s)"
    print(f"  {colorize(BOX_V, rank_color)}   Est. Time:   {time_str:<44}{colorize(BOX_V, rank_color)}")

    print(f"  {colorize(BOX_V, rank_color)}   Hours:       {provider['availability']:<44}{colorize(BOX_V, rank_color)}")

    # Specialties
    specs = ", ".join(provider['specialties'][:3])
    print(f"  {colorize(BOX_V, rank_color)}   Specialties: {colorize(specs, C.DIM):<44}{colorize(BOX_V, rank_color)}")

    print(f"  {colorize(BOX_BL + BOX_H * 56 + BOX_BR, rank_color)}")


def display_results(inputs, rule_advice, top_providers):
    """Display the full results section."""
    print("\n")
    print(draw_separator(60, "=", C.BRIGHT_GREEN))
    print(colorize("  RESULTS", C.BOLD, C.BRIGHT_GREEN))
    print(draw_separator(60, "=", C.BRIGHT_GREEN))

    # Rule-based advice
    print(f"\n  {colorize('Advisory:', C.BOLD, C.BRIGHT_YELLOW)}")
    # Word-wrap the advice
    words = rule_advice.split()
    line = "  "
    for word in words:
        if len(line) + len(word) + 1 > 60:
            print(line)
            line = "  " + word
        else:
            line += " " + word if line.strip() else "  " + word
    if line.strip():
        print(line)

    # Top providers
    print(f"\n  {colorize('Top Matching Providers:', C.BOLD, C.BRIGHT_WHITE)}")
    if not top_providers:
        print(colorize("    No providers found matching your criteria.", C.YELLOW))
    else:
        for rank, (score, provider) in enumerate(top_providers, 1):
            display_provider_card(rank, score, provider)




# =============================================================================
# Session Summary
# =============================================================================

def display_session_summary(inputs, rule_advice, top_providers):
    """Display a full session summary."""
    print("\n")
    print(draw_separator(60, "=", C.BRIGHT_MAGENTA))
    print(colorize("  SESSION SUMMARY", C.BOLD, C.BRIGHT_MAGENTA))
    print(draw_separator(60, "=", C.BRIGHT_MAGENTA))

    print(f"\n  {colorize('Your Preferences:', C.BOLD, C.BRIGHT_WHITE)}")
    print(f"  {colorize(BOX_H * 40, C.DIM)}")
    labels = [
        ("Service Type", inputs["service_type"]),
        ("Distance", inputs["distance"]),
        ("Urgency", inputs["urgency"]),
        ("Budget", inputs["budget"]),
        ("Min. Rating", inputs["rating"]),
        ("Time of Day", inputs["time_of_day"]),
        ("Day Preference", inputs["day_preference"]),
    ]
    for label, value in labels:
        print(f"    {colorize(label + ':', C.CYAN):>30} {colorize(value, C.BRIGHT_WHITE)}")

    print(f"\n  {colorize('Recommendation:', C.BOLD, C.BRIGHT_WHITE)}")
    print(f"  {colorize(BOX_H * 40, C.DIM)}")
    # Word wrap
    words = rule_advice.split()
    line = "    "
    for word in words:
        if len(line) + len(word) + 1 > 58:
            print(line)
            line = "    " + word
        else:
            line += " " + word if line.strip() else "    " + word
    if line.strip():
        print(line)

    if top_providers:
        print(f"\n  {colorize('Top Providers:', C.BOLD, C.BRIGHT_WHITE)}")
        print(f"  {colorize(BOX_H * 40, C.DIM)}")
        for rank, (score, provider) in enumerate(top_providers, 1):
            print(f"    {rank}. {provider['name']} - {score}% match, {stars_display(provider['rating'])}")
    print()


def generate_report_text(inputs, rule_advice, top_providers):
    """Generate a plain-text report for file saving."""
    lines = []
    lines.append("=" * 60)
    lines.append("  LOCAL SERVICE LOCATOR - SESSION REPORT")
    lines.append("=" * 60)
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("  YOUR PREFERENCES:")
    lines.append("  " + "-" * 40)
    lines.append(f"    Service Type:  {inputs['service_type']}")
    lines.append(f"    Distance:      {inputs['distance']}")
    lines.append(f"    Urgency:       {inputs['urgency']}")
    lines.append(f"    Budget:        {inputs['budget']}")
    lines.append(f"    Min. Rating:   {inputs['rating']}")
    lines.append(f"    Time of Day:   {inputs['time_of_day']}")
    lines.append(f"    Day Pref:      {inputs['day_preference']}")
    lines.append("")
    lines.append("  RECOMMENDATION:")
    lines.append("  " + "-" * 40)
    lines.append(f"    {rule_advice}")
    lines.append("")
    if top_providers:
        lines.append("  TOP MATCHING PROVIDERS:")
        lines.append("  " + "-" * 40)
        for rank, (score, provider) in enumerate(top_providers, 1):
            lines.append(f"    #{rank} - {provider['name']}")
            lines.append(f"         Match Score: {score}%")
            lines.append(f"         Rating: {provider['rating']}/5.0")
            lines.append(f"         Phone: {provider['phone']}")
            lines.append(f"         Price: {provider['price_range']}")
            lines.append(f"         Distance: {provider['distance_km']} km")
            lines.append(f"         Availability: {provider['availability']}")
            lines.append(f"         Specialties: {', '.join(provider['specialties'])}")
            lines.append("")
    lines.append("=" * 60)
    lines.append("  Thank you for using Local Service Locator!")
    lines.append("=" * 60)
    return "\n".join(lines)


def offer_save_report(inputs, rule_advice, top_providers):
    """Offer to save the session report to a file."""
    print(f"\n  {colorize('Would you like to save this report to a file?', C.BRIGHT_WHITE)}")
    print(f"    {colorize('1', C.BRIGHT_YELLOW)}. Yes, save report")
    print(f"    {colorize('2', C.BRIGHT_YELLOW)}. No, exit")
    print()
    while True:
        choice = input(f"  {colorize('>', C.BRIGHT_GREEN)} Your choice (1/2): ").strip()
        if choice == "1":
            report = generate_report_text(inputs, rule_advice, top_providers)
            filename = f"service_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            try:
                with open(filename, "w") as f:
                    f.write(report)
                print(f"\n  {colorize('[saved]', C.BRIGHT_GREEN)} Report saved to: {colorize(filename, C.BRIGHT_CYAN)}")
            except IOError as e:
                print(f"\n  {colorize('[error]', C.BRIGHT_RED)} Could not save file: {e}")
            break
        elif choice == "2":
            break
        else:
            print(colorize("    Invalid input. Please enter 1 or 2.", C.BRIGHT_RED))




# =============================================================================
# Main Application Flow
# =============================================================================

def collect_all_inputs():
    """
    Collect all user inputs with back-navigation support.
    Returns a dictionary of all answers.
    """
    question_funcs = [
        ask_service_type,
        ask_distance,
        ask_urgency,
        ask_budget,
        ask_rating,
        ask_time_of_day,
        ask_day_preference,
    ]
    question_keys = [
        "service_type",
        "distance",
        "urgency",
        "budget",
        "rating",
        "time_of_day",
        "day_preference",
    ]

    answers = {}
    index = 0

    while index < len(question_funcs):
        result = question_funcs[index](index + 1, len(question_funcs))
        if result == "BACK":
            if index > 0:
                index -= 1
        else:
            answers[question_keys[index]] = result
            index += 1

    return answers


def main():
    """Main entry point for the Local Service Locator Agent."""
    # Clear screen (optional, works on most terminals)
    os.system('cls' if os.name == 'nt' else 'clear')

    # Display welcome banner
    print(WELCOME_BANNER)
    print(colorize("  Welcome! Answer 7 quick questions to get personalized", C.BRIGHT_WHITE))
    print(colorize("  service provider recommendations in your area.", C.BRIGHT_WHITE))
    print()
    print(colorize("  Press Enter to begin...", C.DIM))
    input()

    # Collect user inputs
    inputs = collect_all_inputs()

    # Processing animation
    print()
    spinner_animation("Analyzing your preferences...", 0.8)
    spinner_animation("Searching provider database...", 0.6)
    progress_bar("Calculating match scores", steps=20, duration=0.8)
    spinner_animation("Generating recommendations...", 0.5)

    # Apply rules
    rule_advice = apply_rules(inputs)

    # Get top providers
    top_providers = get_top_providers(inputs, top_n=3)

    # Display results
    display_results(inputs, rule_advice, top_providers)

    # Display session summary
    display_session_summary(inputs, rule_advice, top_providers)

    # Offer to save
    offer_save_report(inputs, rule_advice, top_providers)

    # Farewell
    print()
    print(draw_separator(60, "=", C.BRIGHT_CYAN))
    print(colorize("  Thank you for using the Local Service Locator!", C.BOLD, C.BRIGHT_CYAN))
    print(colorize("  Have a great day!", C.BRIGHT_WHITE))
    print(draw_separator(60, "=", C.BRIGHT_CYAN))
    print()


if __name__ == "__main__":
    main()
