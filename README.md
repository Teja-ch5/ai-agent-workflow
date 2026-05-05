# AI Agent & Automated Workflow System

An AI-powered agent that processes property management tasks, extracts structured data, and automatically logs results to Google Sheets.

## What It Does
- Takes a property management task as input
- Sends it to Groq AI (LLaMA model) for processing
- AI extracts key info, generates a summary, decision support, and recommended action
- Automatically logs the result to Google Sheets via Zapier

## Tech Stack
- Python
- Groq API (LLaMA 3.3)
- Zapier Webhooks
- Google Sheets

## How to Run

1. Clone the repo
```
git clone https://github.com/Teja-ch5/ai-agent-workflow.git
```

2. Install dependencies
```
pip install requests python-dotenv
```

3. Create a `.env` file and add your Groq API key
```
GROQ_API_KEY=your-groq-api-key-here
```

4. Run the script
```
python project1.py
```

## Sample Output
```json
{
  "extracted_data": {
    "key_info": "Unit 204 vacant, minor repairs needed",
    "numbers": "45 days vacant, $1,850/month rent",
    "entities": "Maple Creek apartments, Unit 204"
  },
  "summary": "Unit 204 has been vacant for 45 days and requires minor repairs.",
  "decision_support": "Prioritize repairs to minimize lost revenue",
  "recommended_action": "Send work order to maintenance team",
  "priority": "high"
}
```

## Author
Bhagya Teja Chalicham  
MS Computer Science, Georgia State University
