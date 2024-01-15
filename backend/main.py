import uvicorn
from dotenv import load_dotenv
import os
load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app", host="0.0.0.0", 
        port=int(os.getenv("PORT")), 
        reload=True)