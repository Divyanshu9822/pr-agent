# Utility functions for PR Review Bot
import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()
    return os.environ
