import simplejson as json

from pathlib import Path
from typing import TypedDict


class Vote(TypedDict):
    id: int
    data: list[int]


class VoteResults:
    def __init__(self, database: list[Vote]):
        self.candidates: dict[int, list[list[int]]] = {
            i: [] for i in range(1, 11)}
        self.losers: set[int] = set()
        self.results: list[int] = list()
        for vote in database:
            self.candidates[vote['data'][0]].append(vote['data'])

    def get_results(self) -> int:
        while len(self.candidates) > 1:
            self.print_current()
            self.vote_round()
        winner = next(iter(self.candidates))
        print(f'{winner} победил!')
        return winner

    def print_current(self):
        for candidate in sorted(self.candidates.keys()):
            print(f'{candidate}: {len(self.candidates[candidate])}')

    def vote_round(self):
        min_count = min(len(votes) for votes in self.candidates.values())
        min_candidates = [
            i for i, votes in self.candidates.items() if len(votes) == min_count]
        loser = self.tiebreaker(min_candidates, min_count)
        print(f'{loser} проиграл!')
        self.results.append(loser)
        self.transfer_votes(loser)

    def tiebreaker(self, candidates: list[int], count: int) -> int:
        if len(candidates) == 1 or count == 0:
            return candidates[0]
        print(f'Ничья между {", ".join(map(str, candidates))}.')
        return int(input('Кто уйдет в этом раунде? '))

    def transfer_votes(self, loser: int):
        self.losers.add(loser)
        for vote in self.candidates[loser]:
            self.transfer_vote(vote)
        del self.candidates[loser]

    def transfer_vote(self, vote):
        transfer_to = self.find_available(vote)
        if transfer_to == -1:
            return
        self.candidates[transfer_to].append(vote)

    def find_available(self, vote) -> int:
        for i in vote:
            if i not in self.losers:
                return i
        return -1


def main():
    database: list[Vote] = json.loads(Path('anonymized.json').read_text())
    vote_results = VoteResults(database)
    vote_results.get_results()


if __name__ == '__main__':
    main()
