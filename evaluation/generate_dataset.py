import json
import os

os.makedirs('evaluation/datasets', exist_ok=True)

dataset = []

# 4 ANSWERABLE
for i in range(1, 5):
    dataset.append({
        "id": f"ans_{i}",
        "category": "ANSWERABLE",
        "question": f"What is fact {i}?",
        "initial_context": [f"Fact {i} is exactly X{i}."],
        "corrective_context": [],
        "expected_behavior": "ANSWER",
        "should_abstain": False,
        "supported_claims": [f"Fact {i} is exactly X{i}."],
        "unsupported_claims": []
    })

# 4 UNANSWERABLE
for i in range(1, 5):
    dataset.append({
        "id": f"unans_{i}",
        "category": "UNANSWERABLE",
        "question": f"What is unknown fact {i}?",
        "initial_context": [f"The system contains random data {i}."],
        "corrective_context": [],
        "expected_behavior": "ASK_FOR_CLARIFICATION",
        "should_abstain": True,
        "supported_claims": [],
        "unsupported_claims": [f"Unknown fact {i} is Y{i}."]
    })

# 4 AMBIGUOUS
for i in range(1, 5):
    dataset.append({
        "id": f"ambig_{i}",
        "category": "AMBIGUOUS",
        "question": f"Tell me about it {i}.",
        "initial_context": [f"It {i} could be many things."],
        "corrective_context": [],
        "expected_behavior": "ASK_FOR_CLARIFICATION",
        "should_abstain": True,
        "supported_claims": [],
        "unsupported_claims": [f"It {i} is specifically Z{i}."]
    })

# 4 OUT_OF_DOCUMENT
for i in range(1, 5):
    dataset.append({
        "id": f"ood_{i}",
        "category": "OUT_OF_DOCUMENT",
        "question": f"What is external fact {i}?",
        "initial_context": [],
        "corrective_context": [],
        "expected_behavior": "ASK_FOR_CLARIFICATION",
        "should_abstain": True,
        "supported_claims": [],
        "unsupported_claims": [f"External fact {i} is W{i}."]
    })

# 4 CONFLICTING_CONTEXT
# 1. Resolves
dataset.append({
    "id": "conf_1",
    "category": "CONFLICTING_CONTEXT",
    "question": "What is the CPU speed?",
    "initial_context": ["The CPU operates at 3 GHz.", "The CPU operates at 2.5 GHz."],
    "corrective_context": ["The CPU operates at 3 GHz.", "The CPU operates at 3 GHz."],
    "expected_behavior": "ANSWER",
    "should_abstain": True,
    "supported_claims": ["The CPU operates at 3 GHz."],
    "unsupported_claims": ["The CPU operates at 2.5 GHz."]
})

# 2. Persists
dataset.append({
    "id": "conf_2",
    "category": "CONFLICTING_CONTEXT",
    "question": "What is the GPU memory?",
    "initial_context": ["The GPU has 8GB memory.", "The GPU has 16GB memory."],
    "corrective_context": ["The GPU has 8GB memory.", "The GPU has 16GB memory."],
    "expected_behavior": "ASK_FOR_CLARIFICATION",
    "should_abstain": True,
    "supported_claims": [],
    "unsupported_claims": ["The GPU has 8GB memory.", "The GPU has 16GB memory."]
})

# 3. Insufficient correction
dataset.append({
    "id": "conf_3",
    "category": "CONFLICTING_CONTEXT",
    "question": "What is the battery capacity?",
    "initial_context": ["The battery is 5000 mAh.", "The battery is 4000 mAh."],
    "corrective_context": ["The laptop is grey.", "It comes with a charger."],
    "expected_behavior": "ASK_FOR_CLARIFICATION",
    "should_abstain": True,
    "supported_claims": [],
    "unsupported_claims": ["The battery is 5000 mAh.", "The battery is 4000 mAh."]
})

# 4. Resolves
dataset.append({
    "id": "conf_4",
    "category": "CONFLICTING_CONTEXT",
    "question": "Is the server online?",
    "initial_context": ["The server is online.", "The server is offline."],
    "corrective_context": ["The server is currently online.", "The server is online and healthy."],
    "expected_behavior": "ANSWER",
    "should_abstain": True,
    "supported_claims": ["The server is online."],
    "unsupported_claims": ["The server is offline."]
})

with open('evaluation/datasets/self_correction_benchmark.json', 'w') as f:
    json.dump(dataset, f, indent=2)

print("Dataset generated.")
