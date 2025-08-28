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
