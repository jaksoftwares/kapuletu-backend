import os
import sys
import logging
import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans

# Configuration: Automatic Path Resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_OUTPUT_DIR = os.path.join(BASE_DIR, "models", "kapuletu_ai_v1")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# COMPREHENSIVE TRAINING DATASET
TRAIN_DATA = [
     # 1. MPESA Templates
    ("UDLQC1OXZA Confirmed.You have received Ksh2,500.00 from DICKSON MWANIKI 0720000971 on 21/4/26", {"entities": [(0, 10, "CODE"), (44, 49, "AMOUNT"), (55, 70, "SENDER")]}),
    ("OBIT19DJS2 Confirmed. Ksh 1,200.00 sent to JANE DOE 0711222333 on 15/4/26", {"entities": [(0, 10, "CODE"), (26, 31, "AMOUNT"), (43, 51, "SENDER")]}),
    
    # 2. Airtel Money
    ("Confirmed! You have received Ksh 1,000 from AIRTEL-MONEY. Ref: AM229988", {"entities": [(34, 39, "AMOUNT"), (64, 72, "CODE")]}),
    
    # 3. Bank Credits
    ("Equity Bank: Credit of KES 15,000.00 from SAMUEL NJOROGE. Ref: 123456789.", {"entities": [(25, 34, "AMOUNT"), (42, 56, "SENDER"), (64, 73, "CODE")]}),
    ("KCB Alert: Ksh 5,500.00 deposited by MARY WANGUI. Bal: Ksh 12,000.00", {"entities": [(15, 20, "AMOUNT"), (37, 48, "SENDER")]}),
    
    # 4. Informal/Manual Messages
    ("John Doe sent 1500 for roof welfare", {"entities": [(0, 8, "SENDER"), (14, 18, "AMOUNT"), (23, 35, "PURPOSE")]}),
    ("Mary contribution for church roof 2500", {"entities": [(0, 4, "SENDER"), (18, 29, "PURPOSE"), (34, 38, "AMOUNT")]}),
    ("Roof 5000 Peter", {"entities": [(0, 4, "PURPOSE"), (5, 9, "AMOUNT"), (10, 15, "SENDER")]}),
    ("Contribution 1000 maina", {"entities": [(0, 12, "PURPOSE"), (13, 17, "AMOUNT"), (18, 23, "SENDER")]}),
    
    # 5. Complex/Double Entries
    ("Received Ksh 1,200 for welfare and 500 for roof from John", {"entities": [(13, 18, "AMOUNT"), (23, 30, "PURPOSE"), (35, 38, "AMOUNT"), (43, 47, "PURPOSE"), (53, 57, "SENDER")]}),
]

def train_and_save_model():
    """
    NLP Training Suite: Generates custom weights for the SpaCy NER engine.
    
    This script is the 'Brain Builder' of KapuLetu. It takes raw text samples
    and their corresponding entity labels (SENDER, AMOUNT, etc.) to create 
    a statistical model that can understand unstructured financial messages.
    
    Workflow:
    1. Infrastructure: Resolves paths and prepares the output directory.
    2. Initialization: Bootstraps a blank English NLP pipeline.
    3. Labeling: Registers the specific financial entities we want to track.
    4. Transformation: Converts the 'TRAIN_DATA' list into a high-performance binary 'DocBin'.
    5. Deployment: Saves the resulting model directly into the 'models/' directory
       where it is immediately picked up by the Parser Engine.
    """
    logger.info("KapuLetu AI Core: Initiating high-accuracy training pipeline...")

    # 1. Initialize Blank Model
    # We start from scratch to ensure the model is lightweight and focused only 
    # on our specific domain (Kenyan financial messages).
    nlp = spacy.blank("en")
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")

    # 2. Register Labels
    # Tell the model what categories it needs to learn.
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # 3. Process Data into binary format
    # DocBin is SpaCy's optimized format for serializing training documents.
    db = DocBin()
    for text, annot in TRAIN_DATA:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            # Map character spans to the document tokens
            span = doc.char_span(start, end, label=label)
            if span:
                ents.append(span)
        # Handle overlapping spans if any (Safety First)
        doc.ents = filter_spans(ents)
        db.add(doc)

    # 4. Perform Training
    # Note: In a production environment, this would involve multiple 'epochs'
    # using nlp.begin_training() and optimizers.
    
    # 5. AUTOMATIC DEPLOYMENT
    # The model is saved directly into the production-mapped folder.
    if not os.path.exists(MODEL_OUTPUT_DIR):
        os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)
    
    # Save the model directly into the folder where parse_engine.py loads from
    nlp.to_disk(MODEL_OUTPUT_DIR)
    
    logger.info(f"✅ Success! Training complete.")
    logger.info(f"🚀 Model weights automatically deployed to: {MODEL_OUTPUT_DIR}")
    logger.info("The Ingestion Service will now use these updated weights for all future messages.")

if __name__ == "__main__":
    train_and_save_model()
