from requests import get
from src.schemas import ArchiveResponse, Draw


class Stoloto:
    def __init__(self, gosloto_parthner: str):
        self.headers = {'gosloto_parthner': gosloto_parthner}

    def get_arhive_draws(self, game: str = "4x20", count: int = 50, page: int = 1) -> list[Draw]:
        params = {
            "game": game,
            "count": count,
            "page": page
        }
        url = "https://www.stoloto.ru/p/api/mobile/api/v35/service/draws/archive"
        response = get(url=url, params=params, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        archive = ArchiveResponse.model_validate(data)
        return archive.draws
