import typer
import requests
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from requests.exceptions import RequestException

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
        return response.json()['data']
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

def display_game_choices(games):
    table = Table(title="Search Results")
    table.add_column("Number", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Type", style="yellow")
    table.add_column("Main Story", style="green")
    table.add_column("Main + Extra", style="blue")
    table.add_column("Completionist", style="red")
    
    for i, game in enumerate(games, 1):
        table.add_row(
            str(i),
            game['game_name'],
            game['game_type'],
            f"{game['comp_main'] // 3600} hours",
            f"{game['comp_plus'] // 3600} hours",
            f"{game['comp_100'] // 3600} hours"
        )
    
    console.print(table)

def format_game_details(game, steam_reviews):
    details = f"""
Title: {game['game_name']}
Type: {game['game_type']}
Main Story: {game['comp_main'] // 3600} hours
Main + Extra: {game['comp_plus'] // 3600} hours
Completionist: {game['comp_100'] // 3600} hours
User Score: {game['review_score']}%
Release Year: {game['release_world']}
Developer: {game['profile_dev']}
Publisher: {game['profile_pub']}
Platforms: {game['profile_platform']}
Genre: {game['profile_genre']}

Steam Reviews:
Total Reviews: {steam_reviews['query_summary']['total_reviews']}
Positive Reviews: {steam_reviews['query_summary']['total_positive']}
Negative Reviews: {steam_reviews['query_summary']['total_negative']}
Review Score: {steam_reviews['query_summary']['review_score']}

Recent Steam Reviews:
"""
    for review in steam_reviews['reviews'][:5]:
        details += f"\n{review['review']}\n"

    return details

@app.command()
def lookup(game_name: str):
    console.print(f"[bold blue]Searching for: {game_name}[/bold blue]")
    games = search_games(game_name)
    
    if not games:
        console.print("[bold red]No games found or there was an error in the search.[/bold red]")
        return
    
    display_game_choices(games)
    
    choice = typer.prompt("Enter the number of the game you want details for", type=int)
    if 1 <= choice <= len(games):
        selected_game = games[choice - 1]
        game_details = get_game_details(selected_game['game_id'])
        steam_app_id = game_details['profile_steam']
        steam_reviews = get_steam_reviews(steam_app_id)
        details = format_game_details(game_details, steam_reviews)
        console.print(Panel(details, title=f"Details for {selected_game['game_name']}", expand=False))
    else:
        console.print("[bold red]Invalid choice.[/bold red]")

if __name__ == "__main__":
    app()
