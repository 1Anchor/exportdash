#!/usr/bin/python3.8

import os
import requests
import json

GRAFANA_API_TOKEN = "glsa_2m1X6Mx6AUFiS0AgruMVCUH1uOhZHI9L_33df42d9"
#GRAFANA_API_TOKEN = "glsa_Buy30YQnFwZSC8Mc0nOGRzIEezOFyS4k_ff962c53" #Dev
GRAFANA_URL = "https://grafana.prosebya.ru"

def get_dashboard_uids():
    headers = {
        "Authorization": f"Bearer {GRAFANA_API_TOKEN}",
        "Content-Type": "application/json",
    }
    url = f"{GRAFANA_URL}/api/search?query=&folderIds=&starred=&limit=1000"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    dashboard_list = response.json()
    return [(dashboard["uid"], dashboard["title"]) for dashboard in dashboard_list]

def export_dashboard(uid, title):
    headers = {
        "Authorization": f"Bearer {GRAFANA_API_TOKEN}",
        "Content-Type": "application/json",
    }
    url = f"{GRAFANA_URL}/api/dashboards/uid/{uid}"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    dashboard_data = response.json()["dashboard"]

    # Избегаем недопустимых символов в названии файла
    valid_filename = ''.join(c if c.isalnum() or c in ['-', '_'] else '_' for c in title)
    
    file_path = os.path.join("dashboards", f"{valid_filename}_dashboard.json")
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(dashboard_data, file, ensure_ascii=False, indent=4)

def main():
    dashboard_uids = get_dashboard_uids()
    os.makedirs("dashboards", exist_ok=True)

    for uid, title in dashboard_uids:
        export_dashboard(uid, title)

if __name__ == "__main__":
    main()
