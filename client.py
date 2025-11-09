import os
from dataclasses import dataclass
from typing import Any, Final, Iterable

import dacite
import requests

BASE_URL: Final = "https://freesound.org/apiv2"


@dataclass(frozen=True, slots=True)
class Result:
    pass


@dataclass(frozen=True, slots=True)
class TextSearchResult(Result):
    id: int
    name: str
    tags: list[str]
    license: str
    username: str


class Paginator:
    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        token: str,
        url: str,
        result_class: type[Result],
        query_params: dict[str, str] | None = None,
        max_pages: int = 1,
    ) -> None:
        self._token = token
        self._url = url
        self._params: dict[str, str] = {} if query_params is None else {}
        self._max_pages = max_pages
        self._curr_page = 0
        self._result_class = result_class

    # pylint: enable=too-many-positional-arguments

    def paginate(self) -> Iterable[Any]:
        while self._curr_page < self._max_pages:
            resp = requests.get(
                self._url, params={**self._params, "token": self._token}
            )
            assert resp.status_code == 200, resp.text
            json_dict = resp.json()
            for result in json_dict["results"]:
                yield dacite.from_dict(data_class=self._result_class, data=result)
            self._curr_page += 1


class FreesoundClient:
    def __init__(self, base_url: str | None = None) -> None:
        self._base_url: str = base_url or BASE_URL
        self._token = os.environ["FREESOUND_APIV2_TOKEN"]

    def text_search(self, query: str, max_pages: int = 1) -> Iterable[TextSearchResult]:
        yield from Paginator(
            token=self._token,
            url=f"{self._base_url}/search/text",
            query_params={"query": query},
            max_pages=max_pages,
            result_class=TextSearchResult,
        ).paginate()
