from cmath import sqrt
from typing import Generator

from Repositories.models import Movie, User
from Services.decorators import timer


class Recommender:
    def __init__(self, movies : list[Movie]):
        self.all_movies = movies
        self.attribute_list = []
        self.attribute_index = {}
        self.number_of_attributes =0
        self._build_attribute_dictionary()

    def _build_attribute_dictionary(self):
        genres = {("genre", genre.Id) for movie in self.all_movies for genre in movie.Genres}
        countries = {("country", country.Id) for movie in self.all_movies for country in movie.Countries}
        persons = {("person_role", movie_person.Person_id, movie_person.Role_id)
                   for movie in self.all_movies for movie_person in movie.MoviePersons}

        self.attribute_list = list(genres.union(countries).union(persons))
        self.attribute_index = {attribute: i for i, attribute in enumerate(self.attribute_list)}
        self.number_of_attributes = len(self.attribute_list)

    def _convert_attributes_to_vector(self, movie : Movie) -> list:
        vec = [0] * self.number_of_attributes

        attributes_of_movie = ([("genre", genre.Id) for genre in movie.Genres]
            + [("country", country.Id) for country in movie.Countries]
            + [("person_role", movie_person.Person_id, movie_person.Role_id)
               for movie_person in movie.MoviePersons]
        )

        for attribute in attributes_of_movie:
            if attribute in self.attribute_index:
                vec[self.attribute_index[attribute]] = 1

        return vec

    @timer
    def create_recommendations(self, user : User) -> Generator[Movie]:
        if not user.Rate or not self.all_movies:
            return []

        user_rates = {rate.Movie_Id : rate.Score for rate in user.Rate}
        rated_movies = [movie for movie in self.all_movies if movie.Id in user_rates]
        not_rated_movies = [movie for movie in self.all_movies if movie.Id not in user_rates]
        if not not_rated_movies:
            return []

        user_profiled_vec = [0.0] * self.number_of_attributes
        final_weight = 0

        for movie in rated_movies:
            weight = user_rates[movie.Id] - 5
            movie_vec = self._convert_attributes_to_vector(movie)

            for i in range(self.number_of_attributes):
                user_profiled_vec[i] += weight * movie_vec[i]

            final_weight += abs(weight)

        if final_weight == 0 and rated_movies:
            movie_vectors = [self._convert_attributes_to_vector(movie) for movie in rated_movies]
            user_profiled_vec = [sum(collumn) for collumn in zip(*movie_vectors)]

        recommendations_results = []
        for movie in not_rated_movies:
            m_v = self._convert_attributes_to_vector(movie)
            result = self._cosinus_similarity(user_profiled_vec, m_v)
            recommendations_results.append((movie, result))


        recommendations_results.sort(key=lambda x: x[1], reverse=True)

        for movie, result in recommendations_results:
            yield movie
        return None

    def _scalar_product(self, v1, v2):
        return sum(x * y for x, y in zip(v1, v2))

    def _magnitude(self, v):
        return sqrt(sum(x ** 2 for x in v))

    def _cosinus_similarity(self, v1, v2):
        scalar = self._scalar_product(v1, v2)
        m1 = self._magnitude(v1)
        m2 = self._magnitude(v2)
        if m1 == 0 or m2 == 0:
            return 0.0
        else:
            return scalar / (m1 * m2)
