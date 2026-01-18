import os
import sys

# Add the parent directory to sys.path so we can import from the backend root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app()
