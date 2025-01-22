import os
import requests
import sys

# Get Rundeck variables from environment
SNOW_INSTANCE = os.getenv('RD_OPTION_SNOW_INSTANCE', '')
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

def get_change_requests():
    """Get change requests from ServiceNow"""
    token = get_snow_token()
    
    # Note: Using change_request table instead of incident
    url = f"https://{SNOW_INSTANCE}.service-now.com/api/now/table/change_request"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Modified query for change requests
    # Common fields for change requests: state, type, risk, phase, approval
    params = {
        "sysparm_query": "active=true^state=15^assignment_group=abcdegeghfkkd",
        "sysparm_limit": 1000,
        "sysparm_fields": ",".join([
            "number",              # Change request number (CHG0000001)
            "short_description",   # Brief description
            "description",         # Detailed description
            "type",               # Type of change (normal, standard, emergency)
            "state",              # Current state
            "phase",              # Current phase
            "risk",               # Risk level
            "priority",           # Priority
            "start_date",         # Planned start date
            "end_date",           # Planned end date
            "approval",           # Approval status
            "requested_by",       # Requester
            "assignment_group"    # Assigned group
        ])
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()["result"]
    except requests.exceptions.RequestException as e:
        print(f"Error getting change requests: {e}")
        sys.exit(1)

def format_date(date_str):
    """Format ServiceNow date string for display"""
    if not date_str:
        return "Not set"
    return date_str.split(" ")[0]  # Simple date format YYYY-MM-DD

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
        changes = get_change_requests()
        
        # Print results in a format that Rundeck can parse
        print(f"Found {len(changes)} change requests:")
        for change in changes:
            print("\n" + "="*50)  # Separator for readability in Rundeck logs
            print(f"Change Number: {change.get('number', 'N/A')}")
            print(f"Type: {change.get('type', 'N/A')}")
            print(f"State: {change.get('state', 'N/A')}")
            print(f"Phase: {change.get('phase', 'N/A')}")
            print(f"Risk: {change.get('risk', 'N/A')}")
            print(f"Priority: {change.get('priority', 'N/A')}")
            print(f"Start Date: {format_date(change.get('start_date', 'N/A'))}")
            print(f"End Date: {format_date(change.get('end_date', 'N/A'))}")
            print(f"Approval: {change.get('approval', 'N/A')}")
            print(f"Description: {change.get('short_description', 'N/A')}")
            print("="*50)
            
        # Save results to a file that Rundeck can use
        with open('change_request_summary.txt', 'w') as f:
            f.write(f"Total Change Requests: {len(changes)}\n")
            for change in changes:
                f.write(f"{change['number']}: {change['short_description']}\n")
        
        # Store the count in a separate file for easy reference
        with open('change_count.txt', 'w') as f:
            f.write(str(len(changes)))
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()