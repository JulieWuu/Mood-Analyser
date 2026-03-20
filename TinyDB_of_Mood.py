import json

from tinydb import TinyDB, Query

DONT_CARE_LIST = ["", "1", "2", "22", "3", "4", "5"]

class TinyDBofMood:

    def __init__(self, js_filename, db_filename):
        self.filename = db_filename
        self.js_filename = js_filename
        self.mood_db = TinyDB(self.filename)

        if not self.mood_db.all():
            print(f"Database is empty, loading data from {self.js_filename}.")
            self.load()
            print(self.mood_db.all())

        self.mood_table = self.mood_db.table("_default")


    def load(self):
        with open(self.js_filename, "r") as f:
            mood_dict = json.load(f)

        for record in mood_dict.values():
            self.mood_db.insert(record)


    def count_words(self, dont_cares):
        word_map = {}

        for mood in self.mood_table:
            comment = mood["comment"].lower()
            comment = (comment.replace(".", "").replace(",", "").replace("+", "").replace("-", "").replace("&", "").replace("!", "")
                       .replace('"', "").replace("'", "")).replace("?", "").replace(";", "").replace("(", "").replace(")", "")

            comment = comment.split(" ")

            for word in comment:
                if word in dont_cares:
                    continue
                if word not in word_map:
                    word_map[word] = {"count": comment.count(word),
                                      "appearance": []}
                    word_map[word]["appearance"].append(mood)

                else:
                    word_map[word]["count"] += comment.count(word)
                    word_map[word]["appearance"].append(mood)

        for word in word_map.copy():
            if word_map[word]["count"] == 1:
                word_map.pop(word)

        return word_map


    def fetch_word(self, word):
        print(self.mood_db.search(Query().comment.search(word)))

if __name__ == "__main__":
    db_of_mood = TinyDBofMood("json_mood.json", "tinydb_mood.json")

    word_map = db_of_mood.count_words(DONT_CARE_LIST)

    key_list = list(word_map.keys())
    key_list.sort()
    for key in key_list:
        print(f"{key}: {word_map[key]}")


