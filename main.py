import typer
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from requests.exceptions import RequestException
from datetime import datetime
import shutil

app = typer.Typer()
console = Console()

HLTB_API_URL = "https://howlongtobeat.com/api/search/21fda17e4a1d49be"
HLTB_GAME_URL = "https://howlongtobeat.com/_next/data/bjO-XdO0-1kFVCUKWjVm0/game/{}.json?gameId={}"
STEAM_REVIEW_URL = "https://store.steampowered.com/appreviews/{}?json=1"

# Get console width
CONSOLE_WIDTH = shutil.get_terminal_size().columns

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
    table = Table(title="Search Results", width=CONSOLE_WIDTH)
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
"""
    return details


def display_instructions(current_screen):
    common_instructions = [
        "• 's' to start a new search",
        "• 'q' to quit the application"
    ]
    
    screen_specific_instructions = {
        "search_results": ["• Enter a number to select a game"],
        "game_details": ["• 'r' to read reviews"],
        "review_navigation": [
            "• 'p' for previous review",
            "• 'n' for next review",
            "• 'b' to go back to game details"
        ]
    }
    
    all_instructions = screen_specific_instructions.get(current_screen, []) + common_instructions
    
    console.print(Panel(
        "\n".join(all_instructions),
        title="Instructions",
        expand=False,
        width=CONSOLE_WIDTH
    ))


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

        console.print(Panel(review_text, expand=False, width=CONSOLE_WIDTH))
        display_instructions("review_navigation")
        
        choice = console.input("Enter your choice: ").lower()

        if choice == 'p' and current_index > 0:
            current_index -= 1
        elif choice == 'n' and current_index < total_reviews - 1:
            current_index += 1
        elif choice == 'b':
            break
        elif choice == 's':
            return 'new_search'
        elif choice == 'q':
            return 'quit'
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
            display_instructions("search_results")
            choice = console.input("Enter your choice: ").lower()
            if choice == 's':
                game_name = console.input("Enter a new game name to search: ")
                continue
            elif choice == 'q':
                break
            else:
                console.print("[bold red]Invalid choice.[/bold red]")
                continue

        display_search_results(games)
        display_instructions("search_results")

        choice = console.input("Enter your choice: ").lower()
        if choice == 'q':
            break
        elif choice == 's':
            game_name = console.input("Enter a new game name to search: ")
            continue
        elif choice.isdigit() and 1 <= int(choice) <= len(games):
            selected_game = games[int(choice) - 1]
            game_details = get_game_details(selected_game['game_id'])
            steam_app_id = game_details['profile_steam']
            steam_reviews = get_steam_reviews(steam_app_id)
            
            while True:
                details = format_game_details(game_details, steam_reviews)
                console.print(Panel(details, title=f"Details for {selected_game['game_name']}", expand=False, width=CONSOLE_WIDTH))
                display_instructions("game_details")

                choice = console.input("Enter your choice: ").lower()
                if choice == 'r':
                    review_choice = display_reviews(steam_reviews)
                    if review_choice == 'new_search':
                        game_name = console.input("Enter a new game name to search: ")
                        break
                    elif review_choice == 'quit':
                        return
                elif choice == 's':
                    game_name = console.input("Enter a new game name to search: ")
                    break
                elif choice == 'q':
                    return
                else:
                    console.print("[bold red]Invalid choice.[/bold red]")
        else:
            console.print("[bold red]Invalid choice.[/bold red]")

if __name__ == "__main__":
    app()