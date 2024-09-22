import typer
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from requests.exceptions import RequestException
from datetime import datetime

app = typer.Typer()
console = Console()

HLTB_API_URL = "https://howlongtobeat.com/api/search/21fda17e4a1d49be"
HLTB_GAME_URL = "https://howlongtobeat.com/_next/data/bjO-XdO0-1kFVCUKWjVm0/game/{}.json?gameId={}"
STEAM_REVIEW_URL = "https://store.steampowered.com/appreviews/{}?json=1"

def search_games(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://howlongtobeat.com/',
        'Content-Type': 'application/json',
        'Origin': 'https://howlongtobeat.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    data = {
        "searchType": "games",
        "searchTerms": query.split(),
        "searchPage": 1,
        "size": 20,
        "searchOptions": {
            "games": {
                "userId": 0,
                "platform": "",
                "sortCategory": "popular",
                "rangeCategory": "main",
                "rangeTime": {"min": None, "max": None},
                "gameplay": {"perspective": "", "flow": "", "genre": ""},
                "rangeYear": {"min": "", "max": ""},
                "modifier": ""
            },
            "users": {"sortCategory": "postcount"},
            "lists": {"sortCategory": "follows"},
            "filter": "",
            "sort": 0,
            "randomizer": 0
        },
        "useCache": True
    }

    try:
        response = requests.post(HLTB_API_URL, headers=headers, json=data)
        response.raise_for_status()
        games = response.json()['data']
        
        # Pre-fetch detailed data for the first 3 games
        for i in range(min(3, len(games))):
            game_details = get_game_details(games[i]['game_id'])
            games[i]['release_year'] = game_details.get('release_world', 'N/A')[:4]  # Get just the year
        
        return games
    except RequestException as e:
        console.print(f"[bold red]Error accessing HowLongToBeat API: {str(e)}[/bold red]")
        return []
    except ValueError as e:
        console.print(f"[bold red]Error parsing JSON response: {str(e)}[/bold red]")
        return []

def get_game_details(game_id):
    url = HLTB_GAME_URL.format(game_id, game_id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
        'Accept': '*/*',
        'x-nextjs-data': '1',
    }
    response = requests.get(url, headers=headers)
    return response.json()['pageProps']['game']['data']['game'][0]

def get_steam_reviews(app_id):
    url = STEAM_REVIEW_URL.format(app_id)
    response = requests.get(url)
    return response.json()

def display_search_results(games):
    table = Table(title="Search Results")
    table.add_column("#", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Type", style="yellow")
    table.add_column("Main Story", style="green")
    table.add_column("User Score", style="blue")
    table.add_column("Release Year", style="white")

    for i, game in enumerate(games[:10], 1):  # Limit to 10 games
        score = game['review_score']
        score_color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
        release_year = game.get('release_year', 'N/A')
        table.add_row(
            str(i),
            game['game_name'],
            game['game_type'],
            f"{game['comp_main'] // 3600} hours",
            f"[{score_color}]{score}%[/{score_color}]",
            release_year
        )

    console.print(table)

def get_user_choice(max_choice):
    while True:
        choice = console.input("\nEnter the number of the game you want details for, 'n' to search again, or 'q' to quit: ")
        if choice.lower() == 'q':
            return 'quit'
        if choice.lower() == 'n':
            return 'new_search'
        if choice.isdigit() and 1 <= int(choice) <= max_choice:
            return int(choice)
        console.print("[bold red]Invalid choice. Please try again.[/bold red]")

def format_game_details(game, steam_reviews):
    details = f"""
Title: {game['game_name']}
Type: {game['game_type']}
Main Story: {game['comp_main'] // 3600} hours
Main + Extra: {game['comp_plus'] // 3600} hours
Completionist: {game['comp_100'] // 3600} hours
User Score: {game['review_score']}%
Release Year: {game['release_world'][:4]}
Developer: {game['profile_dev']}
Publisher: {game['profile_pub']}
Platforms: {game['profile_platform']}
Genre: {game['profile_genre']}

Steam Reviews:
Total Reviews: {steam_reviews['query_summary']['total_reviews']}
Positive Reviews: {steam_reviews['query_summary']['total_positive']}
Negative Reviews: {steam_reviews['query_summary']['total_negative']}
Review Score: {steam_reviews['query_summary']['review_score']}

Press 'r' to read reviews.
Press any other key to return to the main menu.
"""
    return details



def display_reviews(steam_reviews):
    reviews = steam_reviews['reviews']
    total_reviews = len(reviews)
    current_index = 0

    while True:
        review = reviews[current_index]
        review_date = datetime.fromtimestamp(review['timestamp_created']).strftime('%Y-%m-%d')
        
        review_text = Text.assemble(
            (f"Review {current_index + 1} of {total_reviews}\n", "bold"),
            f"Reviewer: {review['author']['steamid']} | Date: {review_date}\n\n",
            review['review']
        )

        console.print(Panel(review_text, expand=False))

        console.print("\nNavigation:")
        if current_index > 0:
            console.print("  [p] Previous review")
        if current_index < total_reviews - 1:
            console.print("  [n] Next review")
        console.print("  [q] Quit review mode")
        
        choice = console.input("\nEnter your choice: ").lower()

        if choice == 'p' and current_index > 0:
            current_index -= 1
        elif choice == 'n' and current_index < total_reviews - 1:
            current_index += 1
        elif choice == 'q':
            break
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")

        console.clear()



@app.command()
def lookup(game_name: str):
    while True:
        console.print(f"\n[bold blue]Searching for: {game_name}[/bold blue]")
        games = search_games(game_name)

        if not games:
            console.print("[bold red]No games found.[/bold red]")
            if console.input("Press 'n' to search again or any other key to quit: ").lower() != 'n':
                break
            game_name = console.input("Enter a new game name to search: ")
            continue

        display_search_results(games)

        choice = get_user_choice(min(len(games), 10))
        if choice == 'quit':
            break
        elif choice == 'new_search':
            game_name = console.input("Enter a new game name to search: ")
            continue

        selected_game = games[choice - 1]
        game_details = get_game_details(selected_game['game_id'])
        steam_app_id = game_details['profile_steam']
        steam_reviews = get_steam_reviews(steam_app_id)
        
        while True:
            details = format_game_details(game_details, steam_reviews)
            console.print(Panel(details, title=f"Details for {selected_game['game_name']}", expand=False))

            more_choice = console.input("\nEnter your choice: ").lower()
            if more_choice == 'r':
                display_reviews(steam_reviews)
            else:
                break

        if console.input("\nPress 'n' to search for another game or any other key to quit: ").lower() != 'n':
            break
        game_name = console.input("Enter a new game name to search: ")



if __name__ == "__main__":
    app()
