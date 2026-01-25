import requests

def handle_api_errors(func):
    """Wrapper to handle common API errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"Network/Request error: {e}")
            return None
        except (KeyError, ValueError, IndexError) as e:
            print(f"Data parsing error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    return wrapper
