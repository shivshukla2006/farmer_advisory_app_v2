import pandas as pd
import os
from datetime import datetime
from models import translate_to_hindi

# Path to community messages
COMMUNITY_FILE = "data/community_messages.csv"

# 📩 Post a new message
def post_message(name, region, message, language="english"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hindi_message = translate_to_hindi(message) if language == "english" else message

    new_entry = {
        "name": name,
        "region": region,
        "message": message,
        "hindi_message": hindi_message,
        "timestamp": timestamp
    }

    # Append to CSV
    if os.path.exists(COMMUNITY_FILE):
        df = pd.read_csv(COMMUNITY_FILE)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([new_entry])

    df.to_csv(COMMUNITY_FILE, index=False)
    return "✅ Message posted successfully."

# 📚 View recent messages
def get_recent_messages(limit=5, language="english"):
    if not os.path.exists(COMMUNITY_FILE):
        return []

    df = pd.read_csv(COMMUNITY_FILE)
    df = df.sort_values(by="timestamp", ascending=False).head(limit)

    if language == "hindi":
        return df[["name", "region", "hindi_message", "timestamp"]].to_dict(orient="records")
    else:
        return df[["name", "region", "message", "timestamp"]].to_dict(orient="records")