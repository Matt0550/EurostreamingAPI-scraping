from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

from models import Season, Episode, Show, ShowsResponse, StreamingService

class EurostreamingWorker:
    def __init__(self):
        autoUrl = requests.get("https://streaming.cloud.matteosillitti.it/v1/eurostreaming")
        # Get json data
        self.url = autoUrl.json()["message"]
        #self.url = "https://eurostreaming.recipes"
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
                    parsed_url = urlparse(url)
                    path = parsed_url.path
                    showList.append(
                        Show(title=name, url=url, image=image, path=path))

                maxPages = soup.find(
                    "div", {"class": "navigation"}).find_all("a")[-2].text
                return ShowsResponse(shows=showList, maxPages=maxPages)
            else:
                return ShowsResponse(shows=[], maxPages=0)
        except:
            return ShowsResponse(shows=[], maxPages=0)

    def searchShows(self, query, page=0):        
        query = query.replace(" ", "+")
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
                    parsed_url = urlparse(url)
                    path = parsed_url.path
                    showList.append(
                        Show(title=name, url=url, image=image, path=path))
                
                maxPages = soup.find(
                        "div", {"class": "navigation"}).find_all("a")
                if maxPages:
                    maxPages = maxPages[-2].text
                else:
                    maxPages = 1
               
                return ShowsResponse(shows=showList, maxPages=maxPages)
            else:
                return ShowsResponse(shows=[], maxPages=0)
        except Exception as e:
            print(e)
            return ShowsResponse(shows=[], maxPages=0)

    def getSeasons(self, html):
        seasons = []
        seasonNames = html.find_all("div", {"class": "su-spoiler-title"})
        episodes = html.find_all("div", {"class": "su-spoiler-content"})

        for i in range(len(seasonNames)):
            seasonName = seasonNames[i].text.strip()
            seasonEpisodeList = []

            current_episode = None
            episode_name_buffer = ""  # Buffer per memorizzare il nome dell'episodio
            collecting_title = False  # Flag per iniziare la raccolta del titolo
            for content in episodes[i].contents:
                # Se troviamo un tag <strong> con il numero dell'episodio, iniziamo a processare un nuovo episodio
                if content.name == "strong" and "×" in content.text:
                    if current_episode:
                        seasonEpisodeList.append(current_episode)

                    episode_title = content.text.strip().replace("–", "-").replace("-", "").strip()

                    episode_parts = episode_title.split(" ", 1)
                    episode_number = episode_parts[0]
                    episode_name_buffer = episode_parts[1] if len(episode_parts) > 1 else ""

                    current_episode = Episode(episodeNumber=episode_number, title=episode_name_buffer, urls=[])
                    collecting_title = True if not episode_name_buffer else False  # Se il titolo non è completo, continua a raccogliere
                    
                # Se il flag collecting_title è attivo, continua a raccogliere il titolo
                elif collecting_title and content.name is None and content.strip():
                    episode_name_buffer += " " + content.strip()
                    current_episode.title = episode_name_buffer.strip()
                    # Replace – with - and remove any extra spaces
                    current_episode.title = current_episode.title.replace("–", "-").replace("-", "").strip()
                    
                    collecting_title = False  # Una volta trovato il titolo completo, disattiva il flag
                
                # Gestione del titolo dell'episodio non racchiuso in <strong>
                elif content.name is None and "×" in content:
                    if current_episode:
                        seasonEpisodeList.append(current_episode)
                    episode_title = content.strip().replace("–", "-").replace("-", "").strip()

                    episode_parts = episode_title.split(" ", 1)
                    episode_number = episode_parts[0]
                    episode_name = episode_parts[1] if len(episode_parts) > 1 else ""

                    current_episode = Episode(episodeNumber=episode_number, title=episode_name, urls=[])
                    collecting_title = False  # Non raccogliere ulteriori parti del titolo
                
                elif content.name == "a" and current_episode:
                    server_name = content.text.strip()
                    if "href" in content.attrs:
                        server_url = content["href"]
                        current_episode.urls.append(StreamingService(name=server_name, url=server_url))
                
                elif content.name == "br" and current_episode:
                    if current_episode:
                        seasonEpisodeList.append(current_episode)
                        current_episode = None

            if current_episode:
                seasonEpisodeList.append(current_episode)

            seasons.append(Season(season=seasonName, episodes=seasonEpisodeList))
        return seasons

    def getShow(self, url_path, alsoEpisodes=False):
        fullUrl = self.url + url_path
        try:
            r = requests.get(fullUrl, headers=self.headers, timeout=self.timeout)
            
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                show = soup.find("div", {"class": "post"})
                name = show.find("h1", {"class": "entry-title"}).text
                image = show.find("img")["src"]

                description = show.find("div", {"class": "entry-content"}).find_all("span")[0].text
                description = description.replace("Continua a leggere.", "").strip()

                link = show.find("h1", {"class": "entry-title"}).find("a")["href"]
                
                if not alsoEpisodes:
                    return Show(title=name, image=image, description=description, url=link, path=url_path)
                
                seasons = self.getSeasons(show)
                
                return Show(title=name, image=image, description=description, url=link, path=url_path, seasons=seasons)
            else:
                return Show(title="")
        except Exception as e:
            print(e)
            return Show(title="")