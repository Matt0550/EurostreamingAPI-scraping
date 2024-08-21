import requests
from bs4 import BeautifulSoup

from models import Season, Episode, Show, StreamingService


class EurostreamingWorker:
    def __init__(self):
        # autoUrl = requests.get("https://api.matt05.ml/streaming-api/v1/eurostreaming")
        # Get json data
        # self.url = autoUrl.json()["message"]
        self.url = "https://eurostreaming.charity"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.timeout = 5

    def checkStatus(self):
        try:
            r = requests.get(self.url, headers=self.headers,
                             timeout=self.timeout)
            if r.status_code == 200:
                return True
            else:
                return False
        except:
            return False

    def getShows(self, page=1):
        url = self.url + "/page/" + str(page)
        try:
            r = requests.get(url, headers=self.headers, timeout=self.timeout)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                shows = soup.find_all("li", {"class": "post"})

                showList = []

                # Get the name, url and the image of the show
                for show in shows:
                    name = show.find("h2").text
                    url = show.find("a")["href"]
                    image = show.find("img")["src"]
                    showList.append(
                        {"title": name, "url": url, "image": image})

                maxPages = soup.find(
                    "div", {"class": "navigation"}).find_all("a")[-2].text
                return {"shows": showList, "maxPages": maxPages, "status": True}
            else:
                return {"shows": [], "maxPages": 0, "status": False}
        except:
            return {"shows": [], "maxPages": 0, "status": False}

    def searchShows(self, query, page=1):
        url = self.url + "/page/" + str(page) + "/?s=" + query
        try:
            r = requests.get(url, headers=self.headers, timeout=self.timeout)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                shows = soup.find_all("li", {"class": "post"})

                showList = []

                # Get the name, url and the image of the show
                for show in shows:
                    name = show.find("h2").text
                    url = show.find("a")["href"]
                    image = show.find("img")["src"]
                    showList.append(
                        {"title": name, "url": url, "image": image})
                if len(showList) > 0:
                    maxPages = soup.find(
                        "div", {"class": "navigation"}).find_all("a")[-2].text
                else:
                    maxPages = 0

                return {"shows": showList, "maxPages": maxPages, "status": True}
            else:
                return {"shows": [], "maxPages": 0, "status": False}
        except:
            return {"shows": [], "maxPages": 0, "status": False}

    def getShow(self, url_path):
        fullUrl = self.url + url_path
        try:
            r = requests.get(fullUrl, headers=self.headers,
                             timeout=self.timeout)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                show = soup.find("div", {"class": "post"})
                name = show.find("h1", {"class": "entry-title"}).text
                image = show.find("img")["src"]
                # Get the second p and the first span inside entry-content and merge the two texts
                # TODO: Fix this because it cut the first part
                description = show.find(
                    "div", {"class": "entry-content"}).find_all("span")[0].text
                # Remove "continua a leggere" text
                description = description.replace("Continua a leggere.", "")
                # Remove firsts spaces
                description = description.strip()

                link = show.find(
                    "h1", {"class": "entry-title"}).find("a")["href"]
                
                # Structure: "Season 1": [{"title": "Episode 1", "urls": {"server1": "url1", "server2": "url2"}}]
                # Find all su-spoiler-title that are a callout
                # # The episode name is the text before the a tag and the streaming services are all the a tags until the next text
                # Trovare le stagioni
                seasons = []

                # Trovare le stagioni
                seasonNames = show.find_all("div", {"class": "su-spoiler-title"})
                # Trovare gli episodi associati alle stagioni
                episodes = show.find_all("div", {"class": "su-spoiler-content"})

                for i in range(len(seasonNames)):
                    seasonName = seasonNames[i].text.strip()

                    seasonEpisodeList = []

                    current_episode = None
                    for content in episodes[i].contents:
                        # Se il contenuto è un testo e contiene un episodio
                        if content.name is None and "×" in content:
                            if current_episode:
                                seasonEpisodeList.append(current_episode)
                            episode_title = content.strip().replace("–", "-").replace("-", "").strip()
                            episode_parts = episode_title.split(" ", 1)  # Divide in numero e nome
                            episode_number = episode_parts[0]
                            episode_name = episode_parts[1] if len(episode_parts) > 1 else ""
                            current_episode = Episode(episodeNumber=episode_number, title=episode_name, urls=[])
                       
                        elif content.name == "a" and current_episode:
                            server_name = content.text.strip()
                            server_url = content["href"]
                            current_episode.urls.append(StreamingService(name=server_name, url=server_url))
                        
                        elif content.name == "br" and current_episode:
                            # Fine di un episodio
                            if current_episode:
                                seasonEpisodeList.append(current_episode)
                                current_episode = None

                    # Aggiungere l'ultimo episodio della stagione
                    if current_episode:
                        seasonEpisodeList.append(current_episode)

                    # Aggiungere la stagione alla lista principale
                    seasons.append(Season(season=seasonName, episodes=seasonEpisodeList))



                return {"title": name, "image": image, "description": description, "url": link, "seasons": seasons, "status": True}
            else:
                return {"title": "", "image": "", "description": "", "link": "", "status": False}
        except Exception as e:
            print(e)
            return {"title": "", "image": "", "description": "", "link": "", "status": False}
