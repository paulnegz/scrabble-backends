from PyDictionary import PyDictionary
import enchant
from functools import wraps, reduce
from time import perf_counter
from typing import Union
from fastapi import FastAPI
import uvicorn


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time, result = perf_counter(), func(*args, **kwargs)
        end_time = perf_counter()
        total_time = end_time - start_time
        # print(f'Function {func.__name__}\t{result} took {total_time:.4f} seconds')

        print(f'{func.__name__}\t took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

# dictionary = PyDictionary()
is_word = enchant.Dict("en_US")
app = FastAPI()


@app.get("/")
async def ping():
    return {"ping": "pong"}


def get_permutations(letters: str):
    words_set = set()

    def recursive(randomWord, subWord):
        for i, letter in enumerate(randomWord):
            newWord = subWord + randomWord[i:1]
            if len(newWord) > 2:
                words_set.add(newWord)
            recursive(randomWord[0:i] + randomWord[i+1:], subWord + randomWord[i:1])
    recursive(letters, "")
    return words_set


@app.get("/permutations/{letters}")
def permutations(letters: str):
    return {"permutation_set": get_permutations(letters)}


@timeit
def get_words(letters: str):
    words_set = set()

    def recursive(randomWord, subWord):
        for i, letter in enumerate(randomWord):
            newWord = subWord + randomWord[i:1]
            if len(newWord) > 2 and is_word.check(newWord):
                words_set.add(newWord)
            recursive(randomWord[0:i] + randomWord[i+1:], subWord + randomWord[i:1])
    recursive(letters, "")
    return words_set


@app.get("/words/{letters}")
def words(letters: str):
    return {"words": get_words(letters)}


@timeit
def get_define_words(permutated_words: set):
    dictionary = PyDictionary(list(permutated_words))
    meanings = dictionary.getMeanings()
    return meanings


@app.get("/scrabble/{letters}")
async def scrabble(letters: str):
    permutated_words: set = get_words(letters)
    defined_words = get_define_words(permutated_words)
    return {"solved": defined_words}


if __name__ == "__main__":
    print("mank")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    print("mankind")