import os
import json
import random
import string
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_PATH = os.path.join(DATA_DIR, "synthetic_dataset.json")

# Pools of data to inject into templates to mimic real-world diversity
NAMES = ["AMOS ILAVONGA SHIBUTSE", "JANE DOE", "JOHN KAMAU", "MARY WANGUI", "PETER NJOROGE", "GRAPHICSPALACELTD", "KAPULETU WELFARE"]
PROVIDERS = ["KCB", "EQUITY", "COOP", "ABSA"]

def generate_mpesa_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def generate_synthetic_data(num_samples=500):
    """
    Generates synthetic but highly realistic NLP dataset samples.
    It builds the string dynamically, meaning it calculates exact character 
    indexes for the annotations perfectly every single time.
    """
    dataset = []
    
    for _ in range(num_samples):
        code = generate_mpesa_code()
        name = random.choice(NAMES)
        amount_val = round(random.uniform(100.0, 50000.0), 2)
        amount_str = f"{amount_val:,.2f}"
        
        # Randomly choose a template type
        template_type = random.choice(["standard", "bank", "forwarded", "paybill"])
        
        if template_type == "standard":
            # [CODE] Confirmed.You have received Ksh[AMOUNT] from [NAME]...
            text = f"{code} Confirmed.You have received Ksh{amount_str} from {name} 0712345678 on 21/4/26"
            entities = [
                [0, len(code), "CODE"],
                [text.find(amount_str), text.find(amount_str) + len(amount_str), "AMOUNT"],
                [text.find(name), text.find(name) + len(name), "SENDER"]
            ]
            
        elif template_type == "bank":
            # [CODE] Confirmed! You have received KES [AMOUNT] from [NAME] ... via [PROVIDER].
            provider = random.choice(PROVIDERS)
            text = f"{code} Confirmed! You have received KES {amount_str} from {name} - 131****711 at 2026-04-01 10:45:18 AM via {provider}. Pata extra cash with a flexible Mobile Loan."
            entities = [
                [0, len(code), "CODE"],
                [text.find(amount_str), text.find(amount_str) + len(amount_str), "AMOUNT"],
                [text.find(name), text.find(name) + len(name), "SENDER"],
                [text.find(provider), text.find(provider) + len(provider), "PROVIDER"]
            ]
            
        elif template_type == "forwarded":
            # Fwd: [CODE] Confirmed. You have received Ksh [AMOUNT] from [NAME]...
            text = f"Fwd: {code} Confirmed. You have received Ksh {amount_str} from {name} on 12/10/25 at 9:00 AM."
            entities = [
                [text.find(code), text.find(code) + len(code), "CODE"],
                [text.find(amount_str), text.find(amount_str) + len(amount_str), "AMOUNT"],
                [text.find(name), text.find(name) + len(name), "SENDER"]
            ]
            
        elif template_type == "paybill":
            # Ksh [AMOUNT] sent to [PROVIDER] account [NAME] 5848028... M-PESA Ref [CODE].
            provider = random.choice(PROVIDERS)
            text = f"Ksh {amount_str} sent to {provider} account {name} 5848028 has been received. M-PESA Ref {code}. To reverse this transaction, SMS this message to 16120."
            entities = [
                [text.find(amount_str), text.find(amount_str) + len(amount_str), "AMOUNT"],
                [text.find(provider), text.find(provider) + len(provider), "PROVIDER"],
                [text.find(name), text.find(name) + len(name), "ACCOUNT"],
                [text.find(code), text.find(code) + len(code), "CODE"]
            ]

        dataset.append({"text": text, "entities": entities})
        
    # Save the synthetic dataset
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2)
        
    logger.info(f"Successfully generated {num_samples} synthetic samples at {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_synthetic_data(1000)
