import requests
from bs4 import BeautifulSoup


def fetch_sunday_funnies(page: int = 1):
    """Return Sunday Funnies posts from the given page."""
    url = (
        "https://greatawakening.win/u/Uncle_Fester?type=post&sort=new&page="
        f"{page}"
    )
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    posts = []
    for post in soup.find_all("div", class_="post"):
        title_tag = post.find("a", class_="title")
        if not title_tag:
            continue
        if title_tag.get_text(strip=True) != "Sunday Funnies":
            continue
        link = "https://greatawakening.win" + title_tag["href"]
        time_tag = post.find("time", class_="timeago")
        date = time_tag["datetime"] if time_tag else ""
        content_div = post.find("div", class_="content")
        content = content_div.get_text(" ", strip=True) if content_div else ""
        posts.append({"date": date, "link": link, "content": content})

    return posts


if __name__ == "__main__":
    for p in fetch_sunday_funnies(1):
        print(f"Date: {p['date']}")
        print(f"Link: {p['link']}")
        print(f"Content: {p['content']}")
        print()
