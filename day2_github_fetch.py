import requests
import json

# Your GitHub repo
url = "https://api.github.com/repos/2nothing4/ziad-devops-180"

# Fetch the data
response = requests.get(url)

# Check if it worked
if response.status_code == 200:
    data = response.json()
    
    # Print some info
    print("Repo name:", data["name"])
    print("Stars:", data["stargazers_count"])
    print("Forks:", data["forks_count"])
    print("Created:", data["created_at"])
    
    # Save to a file
    with open("repo_info.json", "w") as file:
        json.dump(data, file, indent=2)
    
    print("Data saved to repo_info.json")
else:
    print("Failed to fetch. Status code:", response.status_code)