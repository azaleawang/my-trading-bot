import uvicorn
from dotenv import load_dotenv
load_dotenv()  # This should be near the top of your main.py

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app", host="0.0.0.0", 
        port=8000, 
        reload=True)