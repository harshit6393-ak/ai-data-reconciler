import json
import os
import google.generativeai as genai

# 1. Configure the LLM API
# In production, use os.environ.get("GEMINI_API_KEY")
genai.configure(api_key="YOUR_API_KEY_HERE") 
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Mock Data: Two systems with slightly different formats
system_a_database = [
    {"transaction_id": "101", "vendor": "Microsoft Corp", "total_billed": "$500.00"}
]

system_b_invoices = [
    {"ref_num": "TXN-101", "supplier": "MSFT", "amount_paid": 500}
]

# 3. The Core Reconciliation Function
def reconcile_records(record_a, record_b):
    print(f"Analyzing records...\nSystem A: {record_a}\nSystem B: {record_b}\n")
    
    # 4. Prompt Engineering: Instructing the LLM
    prompt = f"""
    You are an expert data engineer performing data reconciliation.
    Compare Record A and Record B and determine if they represent the exact same transaction.
    They may use different naming conventions, abbreviations, or data types (e.g., strings vs integers).
    
    Record A: {record_a}
    Record B: {record_b}
    
    Return ONLY a valid JSON object with no markdown formatting. The JSON must have these exact keys:
    "is_match": boolean,
    "confidence_score": integer from 1 to 100,
    "explanation": a short string explaining your reasoning.
    """
    
    # 5. Calling the LLM
    response = model.generate_content(prompt)
    
    # 6. Parsing the Output
    try:
        # Clean up any potential markdown code blocks the LLM might return
        clean_text = response.text.strip().replace('```json', '').replace('```', '')
        result_json = json.loads(clean_text)
        return result_json
    except json.JSONDecodeError:
        return {"error": "Failed to parse LLM response into JSON."}

# 7. Execution
if __name__ == "__main__":
    record_from_a = system_a_database[0]
    record_from_b = system_b_invoices[0]
    
    reconciliation_result = reconcile_records(record_from_a, record_from_b)
    
    # 8. Outputting the Final JSON
    print("--- Reconciliation Result ---")
    print(json.dumps(reconciliation_result, indent=4))