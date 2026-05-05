from dotenv import load_dotenv
import os
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
import requests
import json
from datetime import datetime

# ============================================================
# PROJECT 1: AI Agent & Automated Workflow Deployment System
# Built with Groq (Free) + Zapier
# Bhagya Teja Chalicham
# ============================================================

# --- STEP 1: PUT YOUR GROQ API KEY HERE ---
# Get it free at: console.groq.com → API Keys → Create API Key
GROQ_API_KEY = "Your-Groq-API-Key-Here"

# --- STEP 2: PUT YOUR ZAPIER WEBHOOK URL HERE (optional) ---
# Skip this for now, script works without it
ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/27481073/uv76030/"

# ============================================================
# GROQ AI AGENT FUNCTION
# ============================================================
def run_ai_agent(task_text):
    """Send a task to Groq AI and get structured output back."""

    system_prompt = """You are an AI data extraction and reporting agent for a real estate company.

When given any text or task, you will:
1. Extract key information (names, dates, numbers, actions)
2. Identify any decision points or issues
3. Generate a concise summary
4. Suggest one automated action that could be taken

Always respond in this exact JSON format and nothing else:
{
  "extracted_data": {
    "key_info": "main points extracted",
    "numbers": "any numbers or metrics found",
    "entities": "people, places, or systems mentioned"
  },
  "summary": "2-3 sentence summary",
  "decision_support": "what decision this data supports",
  "recommended_action": "one specific automated action to take",
  "priority": "high / medium / low"
}"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Process this task: {task_text}"}
        ],
        "temperature": 0.3,
        "max_tokens": 1024
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None

    response_text = response.json()["choices"][0]["message"]["content"]

    # Parse JSON from response
    try:
        structured_data = json.loads(response_text)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            structured_data = json.loads(json_match.group())
        else:
            structured_data = {"raw_response": response_text}

    return structured_data

# ============================================================
# ZAPIER LOGGING FUNCTION
# ============================================================
def log_to_zapier(task_text, ai_output):
    """Send the result to Zapier which logs it to Google Sheets."""

    payload = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original_task": task_text,
        "summary": ai_output.get("summary", "N/A"),
        "decision_support": ai_output.get("decision_support", "N/A"),
        "recommended_action": ai_output.get("recommended_action", "N/A"),
        "priority": ai_output.get("priority", "N/A"),
        "key_info": ai_output.get("extracted_data", {}).get("key_info", "N/A")
    }

    if "zapier-webhook" not in ZAPIER_WEBHOOK_URL and "your-zapier" not in ZAPIER_WEBHOOK_URL:
        try:
            response = requests.post(
                ZAPIER_WEBHOOK_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print("✅ Successfully logged to Google Sheets via Zapier!")
            else:
                print(f"⚠️  Zapier returned status: {response.status_code}")
        except Exception as e:
            print(f"⚠️  Zapier connection failed: {e}")
    else:
        print("ℹ️  Zapier not configured yet — skipping Google Sheets logging")

    return payload

# ============================================================
# MAIN AGENT
# ============================================================
def run_agent():
    print("=" * 60)
    print("🤖 AI Agent & Automated Workflow System")
    print("   Built with Groq LLaMA + Python + Zapier")
    print("=" * 60)
    print()

    sample_tasks = [
        "Unit 204 at Maple Creek apartments has been vacant for 45 days. Rent is $1,850/month. Last inspection showed minor repairs needed: broken faucet and carpet cleaning required.",
        "Tenant John Smith in Building B submitted a maintenance request for HVAC issues. He has been a tenant for 3 years with no late payments. Issue reported at 2pm today.",
        "Monthly report: Property occupancy is at 87%. Revenue collected this month is $42,500 out of $48,000 expected. 3 units are 30 days past due totaling $5,500."
    ]

    print("Choose input mode:")
    print("1. Type your own task")
    print("2. Use a sample task")
    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "1":
        task = input("\nEnter your task or text to process:\n> ")
    else:
        print("\nSample tasks:")
        for i, t in enumerate(sample_tasks, 1):
            print(f"\n{i}. {t[:80]}...")
        task_num = int(input("\nChoose sample (1-3): ")) - 1
        task = sample_tasks[task_num]
        print(f"\n✅ Using sample task {task_num + 1}")

    print("\n⏳ Sending to AI for processing...")
    print("-" * 60)

    ai_output = run_ai_agent(task)

    if ai_output:
        print("\n📊 AI AGENT OUTPUT:")
        print("-" * 60)
        print(json.dumps(ai_output, indent=2))

        print("\n📤 Logging to Google Sheets via Zapier...")
        log_to_zapier(task, ai_output)

        print("\n" + "=" * 60)
        print("✅ Agent workflow complete!")
        print("=" * 60)
    else:
        print("❌ Something went wrong. Check your API key.")

if __name__ == "__main__":
    run_agent()