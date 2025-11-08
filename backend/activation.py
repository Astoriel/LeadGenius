from typing import Dict, Any, List
import requests
import os

class BaseDestination:
    @property
    def name(self) -> str:
        raise NotImplementedError

    def route(self, lead_data: Dict[str, Any]) -> bool:
        """
        Routes the lead data to the destination.
        Returns True if successful, False otherwise.
        """
        raise NotImplementedError

class SlackDestination(BaseDestination):
    @property
    def name(self) -> str:
        return "Slack"

    def route(self, lead_data: Dict[str, Any]) -> bool:
        webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        if not webhook_url:
            print(f"[{self.name}] Skipped: No SLACK_WEBHOOK_URL provided.")
            return False

        message = (
            f"🔥 *HOT LEAD ALERT* 🔥\n"
            f"Name: {lead_data['lead_name']}\n"
            f"Email: {lead_data['email']}\n"
            f"Company: {lead_data['company_name']}\n"
            f"Title: {lead_data['job_title']}\n"
            f"*Score*: {lead_data['lead_score']}"
        )
        try:
            requests.post(webhook_url, json={"text": message})
            print(f"[{self.name}] Sent alert for {lead_data['email']}")
            return True
        except Exception as e:
            print(f"[{self.name}] Error sending alert: {e}")
            return False

class HubSpotDestination(BaseDestination):
    @property
    def name(self) -> str:
        return "HubSpot CRM"

    def route(self, lead_data: Dict[str, Any]) -> bool:
        """
        Syncs lead score and industry to HubSpot via their Contacts API.
        """
        api_key = os.getenv("HUBSPOT_API_KEY")
        
        # HubSpot Contacts search API (v3)
        url = "https://api.hubapi.com/crm/v3/objects/contacts/search"

        # If no API key is provided, we simulate the request for demonstration
        if not api_key:
            print(f"[{self.name}] [MOCK] Would update Contact {lead_data['email']} with Score {lead_data['lead_score']} and Industry {lead_data['lead_tier']}")
            return True

        print(f"[{self.name}] Searching for contact {lead_data['email']} to update...")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        search_payload = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "email",
                    "operator": "EQ",
                    "value": lead_data["email"]
                }]
            }]
        }
        
        try:
            # 1. Search for the contact
            search_res = requests.post(url, json=search_payload, headers=headers)
            search_data = search_res.json()
            
            if search_data.get("total", 0) > 0:
                contact_id = search_data["results"][0]["id"]
                
                # 2. Update the contact with the new LeadGenius Score
                update_url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}"
                update_payload = {
                    "properties": {
                        "leadgenius_score": str(lead_data["lead_score"]),
                        "leadgenius_tier": lead_data["lead_tier"]
                    }
                }
                requests.patch(update_url, json=update_payload, headers=headers)
                print(f"[{self.name}] Successfully synced Score {lead_data['lead_score']} to HubSpot Contact {contact_id}")
            else:
                print(f"[{self.name}] Contact {lead_data['email']} not found in HubSpot. Skipping sync.")
            return True
            
        except Exception as e:
            print(f"[{self.name}] Error syncing to CRM: {e}")
            return False

class ActivationManager:
    """
    Manages routing of scored leads to multiple destinations.
    """
    def __init__(self):
        self.destinations: List[BaseDestination] = [
            SlackDestination(),
            HubSpotDestination()
        ]

    def route_lead(self, lead_data: Dict[str, Any]):
        print(f"[ActivationManager] Routing lead {lead_data['email']} ({lead_data['lead_tier']} - {lead_data['lead_score']} pts)")
        for dest in self.destinations:
            dest.route(lead_data)
