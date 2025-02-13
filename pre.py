import pandas as pd
import random
import datetime

# File to store interaction records
LOG_FILE = "client_interactions.csv"

# Possible outcomes with probabilities
PROBABILITIES = {
    "Accepted in 1st Attempt": 10,   # 10% chance
    "Rejected in 1st Attempt": 20,   # 20% chance
    "Revised and Accepted": 25,      # 25% chance
    "Revised and Rejected": 25,      # 25% chance
    "Accepted after Multiple Attempts": 20  # 20% chance
}

def simulate_client_interaction(client_name, product_name):
    """Simulates a client interaction and determines the outcome."""
    attempt = 1
    event_log = []
    
    while True:
        outcome = random.choices(list(PROBABILITIES.keys()), weights=PROBABILITIES.values())[0]
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log event
        event_log.append([client_name, product_name, attempt, outcome, date])
        
        if outcome in ["Accepted in 1st Attempt", "Rejected in 1st Attempt"]:
            break  # End if accepted or rejected on first attempt
        elif outcome == "Revised and Rejected":
            break  # End if revised but still rejected
        elif outcome == "Accepted after Multiple Attempts":
            # Simulate how many attempts it took to get accepted
            final_attempt = random.randint(2, 50)
            for i in range(attempt + 1, final_attempt + 1):
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                event_log.append([client_name, product_name, i, "Under Discussion", date])
            
            # Finally accepted at `final_attempt`
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            event_log.append([client_name, product_name, final_attempt, "Accepted", date])
            break
        
        attempt += 1  # Move to the next attempt
    
    # Save interaction log to CSV
    df = pd.DataFrame(event_log, columns=["Client Name", "Product", "Attempt", "Outcome", "Date"])
    
    try:
        existing_data = pd.read_csv(LOG_FILE)
        df = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        pass  # First-time run, no file exists yet
    
    df.to_csv(LOG_FILE, index=False)
    print(f"Interaction saved for {client_name} regarding {product_name}.")

def main():
    print("=== Client Interaction Tracker ===")
    client_name = input("Enter Client Name: ")
    product_name = input("Enter Product Name: ")
    simulate_client_interaction(client_name, product_name)

if __name__ == "__main__":
    main()
