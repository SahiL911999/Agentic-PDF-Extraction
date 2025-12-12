import os
import json
from pathlib import Path
from landingai_ade import LandingAIADE
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
client = LandingAIADE(
    apikey=os.environ.get("VISION_AGENT_API_KEY")
)

print("Client initialized successfully.")
print(f"API KEY: {os.environ.get('VISION_AGENT_API_KEY')}")

# Parse the PDF
response = client.parse(
    document=Path("dev-example.pdf"),
    model="dpt-2-latest",
)

# Convert response.chunks to JSON-serializable structure
json_output = []

for chunk in response.chunks:
    chunk_dict = {
        "id": chunk.id,
        "type": chunk.type,
        "page": chunk.grounding.page if chunk.grounding else None,
        "bounding_box": {
            "top": chunk.grounding.box.top if chunk.grounding else None,
            "bottom": chunk.grounding.box.bottom if chunk.grounding else None,
            "left": chunk.grounding.box.left if chunk.grounding else None,
            "right": chunk.grounding.box.right if chunk.grounding else None,
        } if chunk.grounding else None,
        "content": chunk.markdown.strip()
    }
    json_output.append(chunk_dict)

# Save to a JSON file
output_path = "parsed_pdf.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(json_output, f, indent=2, ensure_ascii=False)

print(f"✅ JSON schema saved to {output_path}")
