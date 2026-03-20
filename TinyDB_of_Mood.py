import json

from tinydb import TinyDB, Query

DONT_CARE_LIST = ["", "1", "2", "22", "3", "4", "5",
                      "a", "about", "abs", "absolutely", "activities", "actually", "after", "afternoon", "again",
                      "ago", "ah", "all", "almost", "already", "also", "am", "an", "and", "another", "anymore",
                      "anymore", "anyway", "are", "around", "arrived", "as", "asked", "at",
                      "back", "bag", "be", "been", "before", "being", "believe", "better", "big", "bit", "bought",
                      "but", "buy", "buying", "by",
                      "came", "can", "cannot", "cant", "check", "choice", "clothes", "could", "couldnt",
                      "damn", "day", "days", "de", "decided", "did", "didnt", "dinner", "do", "does", "doing", "done",
                      "dont", "down",
                      "early", "enough", "enter", "even", "evening", "ever", "every", "everything", "end", "ending",
                      "falling", "feel", "feeling", "felt", "feels", "final", "finally", "finished", "finishing",
                      "first", "food", "for", "forgot", "formal", "found", "free", "from",
                      "gave", "get", "getting", "go", "going", "gone", "gonna", "got", "gotta",
                      "had", "have", "having", "here", "hour", "hours", "he", "him", "his", "how", "her", "hers",
                      "i", "ias", "idk", "if", "ill", "im", "in", "instead", "into", "irl", "is", "it", "its", "ive",
                      "just",
                      "keep", "know",
                      "la", "last", "late", "least", "like", "liked", "literally", "little", "long", "looking", "losing",
                      "lot", "love", "loving", "lunch",
                      "made", "making", "many", "me", "meet", "meeting", "might", "month", "more", "morning", "much",
                      "must", "my", "myself",
                      "n", "need", "never", "new", "next", "night", "no", "not", "now",
                      "of", "off", "oh", "on", "once", "one", "only", "open", "or", "our", "out", "over", "overall", "own",
                      "paper", "papers", "part", "past", "people", "picked",
                      "quite",
                      "ready", "really", "right",
                      "said", "say", "see", "seeing", "set", "shes", "should", "since", "skip", "skipped", "sleep", "slept",
                      "slightly", "so", "some", "someone", "soon", "spent", "stand", "start", "started", "starting", "stay",
                      "still", "stop", "stuff", "such", "suddenly", "show", "second",
                      "taking", "than", "that", "the", "them", "then", "there", "these", "thing", "things", "think", "this",
                      "tho", "though", "thought", "thoughts", "till", "time", "timed", "to", "today", "tomorrow", "tonight",
                      "too", "try", "trying", "those",
                      "uhoh", "until", "up", "use", "using",
                      "very",
                      "waiting", "wakeup", "wanna", "want", "wanted", "was", "wasnt", "way", "we", "week", "well", "went",
                      "what", "when", "where", "whole", "why", "with", "without", "woke", "would", "writing", "wrong", "wrote",
                      "yesterday", "your"]

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


