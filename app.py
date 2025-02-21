import requests
import json
import time
from tqdm import tqdm  # For progress bar

# Ollama API Endpoint
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MAX_RETRIES = 3

# Define sections
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

# Model Name
MODEL_NAME = "mistral"

def check_ollama_status():
    try:
        response = requests.get("http://127.0.0.1:11434/api/tags")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def generate_section_content(section_title, previous_content="", retries=0):
    if retries >= MAX_RETRIES:
        print(f"❌ Failed to generate content for {section_title} after {MAX_RETRIES} attempts")
        return ""

    try:
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

        response = requests.post(OLLAMA_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        generated_text = json.loads(response.text).get("response", "")
        return generated_text.strip()

    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"⚠️ Attempt {retries + 1} failed for {section_title}: {str(e)}")
        time.sleep(5)  # Wait before retry
        return generate_section_content(section_title, previous_content, retries + 1)

def main():
    if not check_ollama_status():
        print("❌ Ollama is not running or not accessible!")
        return

    document = ""
    
    # Use tqdm for progress tracking
    for section in tqdm(sections, desc="Generating sections"):
        section_content = generate_section_content(section, document)
        if section_content:
            document += f"\n\n## {section}\n{section_content}\n"
            time.sleep(2)  # Rate limiting
        else:
            print(f"⚠️ Warning: No content generated for {section}")

    # Save the final document
    file_name = "Insurance_Research_Blackbook.txt"
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(document)
        print(f"✅ Document successfully generated and saved as '{file_name}'!")
    except IOError as e:
        print(f"❌ Error saving document: {str(e)}")

if __name__ == "__main__":
    main()