from flask import Flask, render_template, request, jsonify
import pandas as pd
from ai_engine import get_gemini_labels  # all LLM to solve word meaning understanding problems
from scraper import get_business_description  # custom model fetched
from dotenv import load_dotenv
load_dotenv() # read API KEY in .env

app = Flask(__name__)

# define tech fields as required by EY 
TECH_DOMAINS = [
    "Communications & connectivity", "Privacy & security", 
    "Blockchain", "Digital content management", 
    "Artificial intelligence", "Human-machine collaboration system", 
    "Cloud & quantum computing"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_input = request.json.get('url', '').strip()

    # 1. identify the input as URL or enterprise name
    if user_input.startswith('http'):
        target_url = user_input
        desc, _ = get_business_description(target_url)
    else:
        # if its enterprise name, build Wikipedia link (steady and open-source)
        # e.g.: "NVIDIA" -> "https://en.wikipedia.org/wiki/NVIDIA"
        target_url = f"https://en.wikipedia.org/wiki/{user_input.replace(' ', '_')}"
        desc, _ = get_business_description(target_url)
    
    # 2. if failed to fetch model（i.e., Wikipedia does not include the link），then enable LLM generate by itself
    if not desc or "failed" in desc.lower() or len(desc) < 50:
        desc = f"Internal Knowledge Retrieval: Generating tech profile for {user_input}..."
        
        # give LLM Prompt to solve
        ai_input = f"Based on your knowledge, describe the core business and tech sectors of {user_input}."
    else:
        ai_input = desc
    
    # 3. Using AI for semantic annotation
    ai_result = get_gemini_labels(ai_input)
    
    return jsonify({
        "description": desc,
        "labels": ai_result.get('labels', []),
        "sector": ai_result.get('reasoning', "Sector analysis unavailable")
    })

def ai_semantic_labeling(description):
    """
    Use AI for mutually exclusive and complete classification
    """
    prompt = f"Analyze the following business description, choose the most matching labels from{TECH_DOMAINS}: {description}"
    # call Gemini API
    # response = gemini.ChatCompletion.create(...)
    return "Artificial intelligence" # example of return value

if __name__ == '__main__':
    app.run(debug=True)
