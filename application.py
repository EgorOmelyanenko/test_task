import json

from aiohttp import web

from analyzer import Analyzer
from cleaner import glue_fields
from requester import Requester


class Application:
    c_city_id = 826
    c_vacansies_count = 1000
    c_vacancies_count_in_response = 100

    c_requester = Requester("https://api.zp.ru/v1")

    @staticmethod
    def start_application():
        vacancies = {}

        for vacancy in Application._get_thousand_vacancies():
            vacancies.update({
                vacancy["id"]: glue_fields(
                    vacancy,
                    ["header", "description"]
                )
            })


        with open("vacansies.json", "w") as f:
            f.write(
                json.dumps(vacancies)
            )

    @staticmethod
    async def get_similar_vacancy(request):
        vacancy_id = request.rel_url.query["id"]

        try:
            vacancy = Application._get_vacancy(vacancy_id)
        except KeyError:
            return web.Response(text="Vacancy with id={} not found".format(vacancy_id))

        similar_vacancies_ids = Analyzer.find_similar(
            glue_fields(
                vacancy,
                ["header", "description"]
            )
        )

        similar_vacancies = []
        for vacancy in [Application._get_vacancy(id_) for id_ in similar_vacancies_ids]:
            similar_vacancies.append({
                "id": vacancy["id"],
                "header": vacancy["header"]
            })

        return web.Response(
            text=json.dumps(
                {
                    "vacancy": {
                        "id": vacancy_id,
                        "header": vacancy["header"]
                    },
                    "similar_vacansies": similar_vacancies
                },
                ensure_ascii=False
            )
        )

    # private

    @staticmethod
    def _get_thousand_vacancies():

        for offset in range(0, Application.c_vacansies_count, Application.c_vacancies_count_in_response):
            for vacancy in Application.c_requester.send_request(
                    "vacancies",
                    data={
                        "city_id": Application.c_city_id,
                        "limit": Application.c_vacancies_count_in_response,
                        "offset": offset,
                        "fields": "header, description, id"
                    }
            )["vacancies"]:
                yield vacancy


    @staticmethod
    def _get_vacancy(id_):
        result = Application.c_requester.send_request(
            "vacancies/{}".format(id_),
        )["vacancies"][0]

        return result
