"""
Run LLM inference for itinerary suggestions.

Usage:
  python models/inference.py --query "Plan a 3-day family trip in Tokyo" --max_new_tokens 300

Supports either:
  1) Local Transformers model (if available), or
  2) Hugging Face Inference Endpoint via REST (set HF_ENDPOINT + HF_TOKEN)
"""

import os
import json
import argparse
import requests

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
except Exception:
    AutoTokenizer = AutoModelForCausalLM = None

DEFAULT_MODEL = os.getenv("LLM_MODEL_NAME", "meta-llama/Meta-Llama-3-8B-Instruct")

def _inference_via_hf_endpoint(prompt: str, max_new_tokens: int = 300,
                               temperature: float = 0.7, top_p: float = 0.9) -> str:
    url = os.getenv("HF_ENDPOINT")  # e.g., https://api-inference.huggingface.co/models/your-endpoint
    token = os.getenv("HF_TOKEN")
    if not url or not token:
        raise RuntimeError("HF_ENDPOINT and HF_TOKEN must be set for endpoint inference.")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "inputs": prompt,
        "parameters": {"temperature": temperature, "top_p": top_p, "max_new_tokens": max_new_tokens}
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
    r.raise_for_status()
    out = r.json()
    if isinstance(out, list) and len(out) and "generated_text" in out[0]:
        return out[0]["generated_text"]
    # Some endpoints return a dict
    return out.get("generated_text", str(out))

def _inference_via_transformers(prompt: str, max_new_tokens: int = 300,
                                temperature: float = 0.7, top_p: float = 0.9) -> str:
    if AutoTokenizer is None:
        raise RuntimeError("Transformers not available. Install requirements or use HF endpoint.")
    tokenizer = AutoTokenizer.from_pretrained(DEFAULT_MODEL)
    model = AutoModelForCausalLM.from_pretrained(DEFAULT_MODEL, torch_dtype=torch.float16, device_map="auto")
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        do_sample=True,
        temperature=temperature,
        top_p=top_p,
        max_new_tokens=max_new_tokens,
        eos_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True, help="User query for itinerary planning")
    ap.add_argument("--max_new_tokens", type=int, default=300)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--top_p", type=float, default=0.9)
    ap.add_argument("--use_endpoint", action="store_true", help="Use HF Inference Endpoint if set")
    args = ap.parse_args()

    system_prompt = (
        "You are an itinerary planning assistant. "
        "Generate concise, structured day-by-day plans with activities, time windows, and brief rationale."
    )
    prompt = f"{system_prompt}\n\nUser: {args.query}\nAssistant:"
    if args.use_endpoint:
        text = _inference_via_hf_endpoint(prompt, args.max_new_tokens, args.temperature, args.top_p)
    else:
        text = _inference_via_transformers(prompt, args.max_new_tokens, args.temperature, args.top_p)
    print(text)

if __name__ == "__main__":
    main()
