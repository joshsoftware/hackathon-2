from fastapi import Request
from httpx import get

def get_location(request: Request):
    try:
        ip_address = request.headers.get('X-Forwarded-For')
        if ip_address:
            # X-Forwarded-For might contain a list of IPs, so split by commas and take the first one
            ip_address = ip_address.split(",")[0]
        else:
            # If no X-Forwarded-For header, fallback to the client host
            ip_address = request.client.host
        
        # Query the IP
        response = get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()

        if data.get("status") == "success":
            return {
                "ip": data.get("query"),
                "city": data.get("city"),
                "region": data.get("regionName"),
                "country": data.get("country"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon")
            }
        else:
            return {"error": data.get("message")}
    except Exception as e:
        return {"error": str(e)}

