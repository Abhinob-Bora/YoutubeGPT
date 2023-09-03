from dotenv import load_dotenv
import os 

# Load environment variables from the .env file
load_dotenv()

# Access the APIKEY variable
apikey = os.getenv("APIKEY")

