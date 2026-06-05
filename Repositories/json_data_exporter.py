import json

from Repositories.models import Rate


class JsonDataExporter:

    @staticmethod
    def export_rates(rates : list[Rate], path : str):
        data = {}

        for rate in rates:
            title = rate.Movie.Title

            data[title].append({
                "User_login": rate.User.Login,
                "Rate" : rate.Score
            })

        try:
            with open(path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(e)

