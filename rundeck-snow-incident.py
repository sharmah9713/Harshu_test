import os
import requests
import sys

# Get Rundeck variables from environment
SNOW_INSTANCE = os.getenv('RD_OPTION_SNOW_INSTANCE', '')  # or use your Rundeck variable name
SNOW_USERNAME = os.getenv('RD_OPTION_SNOW_USERNAME', '')
SNOW_PASSWORD = os.getenv('RD_OPTION_SNOW_PASSWORD', '')
SNOW_CLIENT_ID = os.getenv('RD_OPTION_SNOW_CLIENT_ID', '')
SNOW_CLIENT_SECRET = os.getenv('RD_OPTION_SNOW_CLIENT_SECRET', '')

def get_snow_token():
    """Get OAuth token from ServiceNow"""
    token_url = f"https://{SNOW_INSTANCE}.service-now.com/oauth_token.do"
    
    data = {
        "grant_type": "password",
        "client_id": SNOW_CLIENT_ID,
        "client_secret": SNOW_CLIENT_SECRET,
        "username": SNOW_USERNAME,
        "password": SNOW_PASSWORD
    }
    
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"Error getting token: {e}")
        sys.exit(1)

def get_incidents():
    """Get incidents from ServiceNow"""
    token = get_snow_token()
    
    url = f"https://{SNOW_INSTANCE}.service-now.com/api/now/table/incident"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    params = {
        "sysparm_query": "active=true^state=15^assignment_group=abcdegeghfkkd",
        "sysparm_limit": 1000,
        "sysparm_fields": "number,short_description"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()["result"]
    except requests.exceptions.RequestException as e:
        print(f"Error getting incidents: {e}")
        sys.exit(1)

def main():
    # Check if required environment variables are set
    required_vars = ['RD_OPTION_SNOW_INSTANCE', 'RD_OPTION_SNOW_USERNAME', 
                    'RD_OPTION_SNOW_PASSWORD', 'RD_OPTION_SNOW_CLIENT_ID', 
                    'RD_OPTION_SNOW_CLIENT_SECRET']
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing required Rundeck variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    try:
        incidents = get_incidents()
        
        # Print results in a format that Rundeck can parse
        print(f"Found {len(incidents)} incidents:")
        for incident in incidents:
            print(f"Incident Number: {incident['number']}")
            print(f"Description: {incident['short_description']}")
            print("---")  # Separator for Rundeck log
            
        # Optionally save to a Rundeck job variable
        with open('incident_count.txt', 'w') as f:
            f.write(str(len(incidents)))
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()