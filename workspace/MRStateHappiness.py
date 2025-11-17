from mrjob.job import MRJob
from mrjob.step import MRStep
import json
import sys

class MRStateHappiness(MRJob):

    def steps(self):
        return [
            MRStep(
                mapper_init=self.init,
                mapper=self.mapper,
                reducer=self.reducer)
        ]
    

    
    # Inicializacion del mapper para cargar el mapa de los sentimientos
    def init(self):
        self.word_map = {}
        with open('AFINN-111.txt', 'r') as f:
            for line in f:
                word, value = line.strip().split('\t')
                self.word_map[word.lower()] = value


    # Mapper: mapea cada palabra a su categoria y emite 1
    
    def mapper(self, _, line):
        tweet = json.loads(line)
        happiness = 0
        n=0
        

        if 'delete' in tweet:
            return

        user = tweet.get('user', {}) 
        if user.get('lang') != 'en':
            return

        place = tweet.get('place',{}) 

        if not place:
            return
        
        if place.get('country_code') != 'US':
            return

        for word in tweet['text'].split():
            word = word.lower()
            if word in self.word_map:
                happiness += int(self.word_map[word])
            n+=1

        # If full_name doesnt have a coma we'll ignore it so we don't get invalid state names
        full_name = place.get('full_name', '')
        if ',' not in full_name:
            return

        state = full_name.split(',')[-1].strip()

        # It's only a valid state if it is a 2 letter word.
        if len(state) != 2 or not state.isalpha():
            return

        yield state, (happiness / n)

    # Reducer: suma los conteos por categoria
    def reducer(self, state, values):
        total = 0
        count = 0
        for v in values:
            total += v
            count += 1
        if count > 0:
            # media por tweet en ese estado
            yield state, round(total / float(count),3)


if __name__ == '__main__':
    MRStateHappiness.run() 