import json
from heapq import nlargest
from multiprocessing.dummy import Pool

from scipy import spatial
from sklearn.feature_extraction.text import CountVectorizer


class Analyzer:

    @staticmethod
    def find_similar(vacancy_words, count=10):
        data = Analyzer._get_data()

        vacansies_ids = [key for key in data]
        vacansies_words = [data[key] for key in data]
        vacansies_count = len(vacansies_words)
        del data

        vacansies_words.append(vacancy_words)

        vectorizer = CountVectorizer()

        document_term_matrix = vectorizer.fit_transform(vacansies_words)
        del vacansies_words

        cosine_distances = Analyzer._get_cosine_distances(
            document_term_matrix.toarray()[:vacansies_count],
            document_term_matrix.toarray()[vacansies_count]
        )

        similar_vacansies_ids = [cosine_distances.index(n) for n in nlargest(count, cosine_distances)]

        return [vacansies_ids[n] for n in similar_vacansies_ids]


    @staticmethod
    def _get_data():
        with open("vacansies.json", "r") as f:
            return json.loads(f.read())

    @staticmethod
    def _get_cosine_distances(vectors, distance_with):
        pool = Pool(4)

        cosine_distances = pool.map(
            lambda x: Analyzer._get_cosine_distance(
                distance_with,
                x
            ),
            vectors
        )

        pool.close()
        pool.join()

        return cosine_distances

    @staticmethod
    def _get_cosine_distance(vector_1, vector_2):
        return 1 - spatial.distance.cosine(vector_1, vector_2)
