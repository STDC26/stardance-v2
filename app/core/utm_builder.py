from urllib.parse import urlencode
import os

HUB_BASE_URL = os.environ.get("HUB_BASE_URL", "https://hubs.stardance.studio")

def build_hub_url(
    hub_id: str,
    allocation_id: str,
    campaign_id: str,
    brand_id: str,
    utm_source: str = "direct",
    utm_medium: str = "none"
) -> str:
    params = {
        "utm_source": utm_source,
        "utm_medium": utm_medium,
        "utm_campaign": campaign_id,
        "utm_content": allocation_id,
        "utm_term": brand_id
    }
    return f"{HUB_BASE_URL}/{hub_id}?{urlencode(params)}"
