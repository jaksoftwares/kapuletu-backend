# 🧠 Kapuletu AI: Model Architecture & Training Guide

## 1. The Machine Learning Engine
The Kapuletu Treasury system uses a **Propietary Named Entity Recognition (NER)** model built on top of the Spacy NLP framework. Unlike traditional regular expressions, this model uses **Statistical Weights** to understand the context of a message.

### 🎯 What it Learns
The model is trained at Identifying four critical entities in any community financial message:
- **`SENDER`**: The person contributing the money.
- **`AMOUNT`**: The numerical value of the contribution.
- **`CODE`**: Financial transaction reference numbers (MPESA, Bank Ref).
- **`PURPOSE`**: What the money is for (Welfare, Campaign, Fee).

---

## 2. The Training Lifecycle (Automatic)

We have eliminated manual file management. The training process follows an automated **"Learn & Deploy"** cycle:

1.  **Preparation**: Gather labeled messages (JSON format) from the `pending_transactions` table.
2.  **Execution**: Run the Training Script.
3.  **Automatic Deployment**: The script saves the weights directly to the `models/kapuletu_ai_v1` directory.
4.  **Instant Hot-Reload**: The Ingestion Service (Parser Engine) checks this directory on every request. As soon as the training finishes, the **new intelligence is live**.

### How to Run the Training
Ensure you are in the project root and have the virtual environment active:

```bash
python scripts/train_model.py
```

---

## 3. Progressive Accuracy Strategy
The "101% Accuracy" goal is achieved through **Iterative Refinement**:

| Phase | Dataset Size | Expected Accuracy |
| :--- | :--- | :--- |
| **Initial** | 0 - 50 messages | 70% (Uses Base Heuristics) |
| **Foundation** | 100 - 500 messages | 85% (Model begins recognizing name patterns) |
| **Production** | 1,000+ messages | 95%+ (Model understands specific community terminology) |
| **Elite** | 5,000+ messages | **Near 100%** (Virtually all variations are learned) |

---

## 4. Technical File Structure
The model resides in the `/models` directory to ensure it is packaged during AWS Lambda deployment:

```text
kapuletu-backend/
├── models/
│   └── kapuletu_ai_v1/     # <--- AUTOMATICALLY UPDATED BY SCRIPTS
│       ├── meta.json       # Model metadata
│       ├── tokenizer       # Language rules
│       └── ner/            # Neural network weights
├── scripts/
│   └── train_model.py      # <--- RUN THIS TO IMPROVE ACCURACY
└── services/ingestion/
    └── parser_engine.py    # <--- CONSUMES THE MODEL AUTOMATICALLY
```

> [!IMPORTANT]
> **No Manual Moving Required**: The `train_model.py` script is aware of your project structure. It handles directory creation and weight placement automatically. Your only task is to provide the "Huge Data" in the `TRAIN_DATA` list or connect it to your database.
