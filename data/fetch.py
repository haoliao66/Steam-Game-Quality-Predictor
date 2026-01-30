import requests
import pandas as pd
import time

def fetch_all_pages(max_pages=86):
    """Step 1: Fetch all game listings from SteamSpy"""
    all_games = []
    
    for page in range(max_pages):
        try:
            resp = requests.get(
                f'https://www.steamspy.com/api.php?request=all&page={page}', 
                timeout=10
            )
            data = resp.json()
            
            if not data:
                break
                
            all_games.extend(list(data.values()))
            print(f"Fetched page {page + 1}: {len(all_games)} total games")
            time.sleep(60)  # 60s between pages as requested
            
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break
    
    return all_games

def fetch_details(games):
    """Step 2: Fetch tags, genres, and full details for each game"""
    details_list = []
    
    for i, game in enumerate(games):
        try:
            appid = game.get('appid')
            if not appid:
                continue
                
            resp = requests.get(
                f'https://www.steamspy.com/api.php?request=appdetails&appid={appid}',
                timeout=10
            )
            details = resp.json()
            
            # Convert tags dict to comma-separated string
            tags_dict = details.get('tags', {})
            details['tags'] = ','.join(tags_dict.keys()) if tags_dict else ''
            
            details_list.append(details)
            
            if (i + 1) % 100 == 0:
                print(f"Fetched details for {i + 1}/{len(games)} games")
                
            time.sleep(1.1)  # 1.1s between games as requested
            
        except Exception as e:
            print(f"Error on game {i} (appid {game.get('appid')}): {e}")
            continue
    
    return details_list

def main():
    # Step 1: Get all games
    print("Step 1: Fetching all game pages...")
    games = fetch_all_pages(max_pages=86)
    print(f"Found {len(games)} games\n")
    
    # Step 2: Enrich with details
    print("Step 2: Fetching tags and genres...")
    details = fetch_details(games)
    print(f"Fetched details for {len(details)} games\n")
    
    # Save two separate CSVs
    pd.DataFrame(games).to_csv('steam.csv', index=False)
    pd.DataFrame(details).to_csv('steamspy_appdetails.csv', index=False)
    
    print(f"Saved steam.csv ({len(games)} games)")
    print(f"Saved steamspy_appdetails.csv ({len(details)} details)")

if __name__ == "__main__":
    main()