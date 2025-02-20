import requests
import json
import time

# Ollama API Endpoint
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

# Model Name (Adjust as per your setup)
MODEL_NAME = "llama3.2-vision"

# Define an extended structure for the black book
sections = [
    "Introduction",
    "History & Evolution of Insurance",
    "Fundamentals of Insurance & How It Works",
    "Types of Insurance & Their Importance",
    "Health Insurance: Policies, Benefits & Challenges",
    "Life Insurance: Term, Whole, & Universal Coverage",
    "Auto Insurance: Coverage, Claims & Industry Trends",
    "Home Insurance: Protection Against Property Risks",
    "Business & Commercial Insurance: Risk Management",
    "Travel Insurance: Policies & Global Coverage",
    "Insurance Industry Trends & Market Analysis",
    "Comparative Study of Insurance Across Different Countries",
    "Consumer Behavior & Preferences in Insurance",
    "Regulatory Framework Governing Insurance Worldwide",
    "Challenges & Risks in the Insurance Sector",
    "Impact of Technology & AI in Insurance",
    "Reinsurance: Concepts, Market Trends & Importance",
    "The Future of Insurance: Predictions & Innovations",
    "Conclusion & Recommendations"
]

# Initialize an empty document
document = ""

# Function to generate content using Ollama
def generate_section_content(section_title, previous_content=""):
    prompt = f"""
    # Research Document: Exploring the Most Popular Types of Insurance People Choose Today

    **Ensure at least 10+ pages of content for this section.**
    
    - **Use the following structure:**
      - **Section Title (H1)**
      - **Introduction to the Section (2 paragraphs)**
      - **Key Concepts & Definitions**
      - **Real-world Examples and Case Studies**
      - **Statistical Data (if applicable)**
      - **Challenges & Future Trends**
      - **Summary & Key Takeaways**
      
    **Content generated so far:**  
    {previous_content}
    
    Now, generate the next section:  
    ## {section_title}
    """

    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    print(f"⏳ Generating: {section_title} ...")  # Status update

    response = requests.post(OLLAMA_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        generated_text = json.loads(response_text).get("response", "")
        return generated_text.strip()
    else:
        print(f"❌ Error generating {section_title}: {response.status_code}")
        return ""

# Generate content for each section iteratively
for section in sections:
    section_content = generate_section_content(section, document)
    document += f"\n\n## {section}\n{section_content}\n"
    
    # Introduce a delay to prevent overloading the model
    time.sleep(2)

# Save the final document
file_name = "Insurance_Research_Blackbook.txt"
with open(file_name, "w", encoding="utf-8") as file:
    file.write(document)

print(f"✅ Document successfully generated and saved as '{file_name}'!")
