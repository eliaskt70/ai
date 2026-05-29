"""
Rule-Based AI Agent: Local Service Locator
-------------------------------------------
This script uses explicit if/elif/else rule-based logic to recommend
local service providers based on user inputs. No machine learning is used;
all decisions are made through deterministic conditional rules.
"""


def get_service_type():
    """Prompt the user to select a service type."""
    print("\n--- Question 1 of 4 ---")
    print("What type of service do you need?")
    print("  1. Maintenance")
    print("  2. Delivery")
    print("  3. Consulting")
    while True:
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            return "Maintenance"
        elif choice == "2":
            return "Delivery"
        elif choice == "3":
            return "Consulting"
        else:
            print("Invalid input. Please enter 1, 2, or 3.")


def get_distance():
    """Prompt the user to select the preferred distance range."""
    print("\n--- Question 2 of 4 ---")
    print("How far are you willing to go?")
    print("  1. Less than 1 km")
    print("  2. 1-3 km")
    print("  3. More than 3 km")
    while True:
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            return "<1km"
        elif choice == "2":
            return "1-3km"
        elif choice == "3":
            return ">3km"
        else:
            print("Invalid input. Please enter 1, 2, or 3.")


def get_urgency():
    """Prompt the user to select the urgency level."""
    print("\n--- Question 3 of 4 ---")
    print("How urgent is your request?")
    print("  1. Immediate")
    print("  2. Scheduled")
    while True:
        choice = input("Enter your choice (1/2): ").strip()
        if choice == "1":
            return "Immediate"
        elif choice == "2":
            return "Scheduled"
        else:
            print("Invalid input. Please enter 1 or 2.")


def get_budget():
    """Prompt the user to select their budget preference."""
    print("\n--- Question 4 of 4 ---")
    print("What is your budget?")
    print("  1. Low")
    print("  2. Open")
    while True:
        choice = input("Enter your choice (1/2): ").strip()
        if choice == "1":
            return "Low"
        elif choice == "2":
            return "Open"
        else:
            print("Invalid input. Please enter 1 or 2.")


def recommend_service(service_type, distance, urgency, budget):
    """
    Apply 7 explicit rules to determine the best recommendation.
    Each rule checks a specific combination of user inputs and returns
    a tailored suggestion. This is purely rule-based logic with no ML.
    """

    # Rule 1: Immediate maintenance nearby on a low budget
    # Best match: a local handyman who can respond quickly at low cost
    if service_type == "Maintenance" and distance == "<1km" and urgency == "Immediate" and budget == "Low":
        return (
            "Recommendation: Contact a nearby neighborhood handyman.\n"
            "Reason: They are close, available immediately, and affordable for quick fixes."
        )

    # Rule 2: Immediate maintenance with an open budget (any distance)
    # Best match: a premium emergency repair service
    elif service_type == "Maintenance" and urgency == "Immediate" and budget == "Open":
        return (
            "Recommendation: Call a premium emergency repair service.\n"
            "Reason: With an open budget and immediate need, a professional emergency "
            "service will provide fast, reliable results regardless of distance."
        )

    # Rule 3: Scheduled maintenance within 1-3 km on a low budget
    # Best match: a local maintenance company with scheduled appointments
    elif service_type == "Maintenance" and distance == "1-3km" and urgency == "Scheduled" and budget == "Low":
        return (
            "Recommendation: Book a local maintenance company for a scheduled visit.\n"
            "Reason: Scheduling ahead allows you to get a competitive rate from a "
            "nearby provider without paying emergency premiums."
        )

    # Rule 4: Delivery service needed immediately within a short distance
    # Best match: a local courier or bike delivery service
    elif service_type == "Delivery" and distance == "<1km" and urgency == "Immediate":
        return (
            "Recommendation: Use a local bike courier or on-demand delivery app.\n"
            "Reason: For short-distance immediate deliveries, bike couriers are the "
            "fastest and most efficient option available."
        )

    # Rule 5: Delivery over a longer distance with a low budget (scheduled)
    # Best match: a standard postal or economy shipping service
    elif service_type == "Delivery" and distance == ">3km" and budget == "Low":
        return (
            "Recommendation: Use a standard postal or economy shipping service.\n"
            "Reason: For longer distances on a tight budget, economy shipping keeps "
            "costs down while still delivering reliably within a few days."
        )

    # Rule 6: Consulting service needed immediately with an open budget
    # Best match: an on-call expert consultant
    elif service_type == "Consulting" and urgency == "Immediate" and budget == "Open":
        return (
            "Recommendation: Hire an on-call expert consultant.\n"
            "Reason: With an open budget and immediate need, engaging a specialist "
            "consultant ensures you get high-quality advice right away."
        )

    # Rule 7: Catch-all rule for any remaining combinations
    # Best match: a general-purpose service directory search
    else:
        return (
            "Recommendation: Search a general service directory for local providers.\n"
            "Reason: Your combination of preferences doesn't match a specific fast-track "
            "rule. A directory search will help you compare options based on reviews, "
            "pricing, and availability in your area."
        )


def main():
    """Main entry point for the Local Service Locator Agent."""
    print("=" * 55)
    print("   Rule-Based AI Agent: Local Service Locator")
    print("=" * 55)
    print("\nAnswer 4 quick questions to get a service recommendation.")

    # Gather user inputs through the CLI
    service_type = get_service_type()
    distance = get_distance()
    urgency = get_urgency()
    budget = get_budget()

    # Display a summary of user inputs
    print("\n" + "-" * 55)
    print("Your Inputs:")
    print(f"  Service Type : {service_type}")
    print(f"  Distance     : {distance}")
    print(f"  Urgency      : {urgency}")
    print(f"  Budget       : {budget}")
    print("-" * 55)

    # Apply rule-based logic to generate a recommendation
    result = recommend_service(service_type, distance, urgency, budget)

    # Display the final recommendation
    print(f"\n{result}")
    print("\n" + "=" * 55)
    print("Thank you for using the Local Service Locator Agent!")
    print("=" * 55)


if __name__ == "__main__":
    main()
