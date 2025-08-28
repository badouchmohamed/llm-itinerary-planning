# LLM-Guided Hybrid Itinerary Planning

This repository contains the code and data for the paper:
**"Personalized Itinerary Planning with LLM-Guided Interaction"**

## Contents
- `data/` – Travel database (50,000 activities) and user study logs.
- `models/` – Scripts for inference and re-ranking with fine-tuned LLaMA-3.
- `embeddings/` – Scripts to generate embeddings using `all-MiniLM-L6-v2`.
- `analysis/` – Statistical analysis and plotting of results.

## Setup
```bash
git clone https://github.com/badouchmohamed/llm-itinerary-planning.git
cd llm-itinerary-planning
pip install -r requirements.txt

## Running Inference
python models/inference.py --query "Plan a family-friendly trip to Tokyo"

## Re-ranking with Implicit Feedback
python models/rerank.py --activities data/travel_activities.csv --logs data/user_study_logs.csv

## Analysis
python analysis/analyze_results.py


## Data
travel_activities.csv: 50,000 activity records.
user_study_logs.csv: 150 user study logs.

