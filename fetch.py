
import requests
from bs4 import BeautifulSoup


def batch(it, sz):
    for i in range(0, len(it), sz):
        yield it[i:i+sz]


r = requests.get("http://www.linusakesson.net/games/autosokoban/board.php?v=1&seed=1179617834&level=1")

soup = BeautifulSoup(r.content)
c = soup.text.strip()


