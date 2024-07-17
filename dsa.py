import requests

def scrape_github_profile(username):
    try:
        # Fetch user profile information
        user_url = f"https://api.github.com/users/{username}"
        user_response = requests.get(user_url)
        user_data = user_response.json()
        
        # Print profile information
        print(f"Username: {user_data['login']}")
        print(f"Name: {user_data['name']}")
        print(f"Bio: {user_data['bio']}")
        print(f"Followers: {user_data['followers']}")
        print(f"Following: {user_data['following']}")
        print(f"Public Repositories: {user_data['public_repos']}")
        
        # Fetch user's repositories
        repos_url = f"https://api.github.com/users/{username}/repos"
        repos_response = requests.get(repos_url)
        repos_data = repos_response.json()
        
        # Print repositories (up to 5)
        print("\nPublic Repositories:")
        for repo in repos_data[:5]:  # Limit to 5 repositories for brevity
            print(f"Repository Name: {repo['name']}")
            print(f"Description: {repo['description']}")
            print(f"URL: {repo['html_url']}")
            print("-------------")
            
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

# Example usage
username = input("Enter GitHub username to scrape: ")
scrape_github_profile(username)
