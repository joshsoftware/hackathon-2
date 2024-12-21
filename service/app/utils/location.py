import requests

def get_location_by_ip(ip_address):
    try:
        # Query the IP
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
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

