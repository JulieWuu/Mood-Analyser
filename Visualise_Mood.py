import matplotlib.pyplot as plt
import numpy as np

from TinyDB_of_Mood import TinyDBofMood
from TinyDB_of_Mood import DONT_CARE_LIST


def draw_bar_from_dict(dictionary):
    x = np.array(list(dictionary.keys()))
    y = np.array(list(dictionary.values()))

    if len(x) > 30 or len(y) > 30:
        print("List too long: over 30 entries.")

    plt.barh(x, y)
    plt.show()


def draw_line_from_dict(dictionary, axis):
    fig, ax = plt.subplots()

    x = np.array(list(dictionary.keys()))
    y = np.array(list(dictionary.values()))

    ax.plot(x, y)
    ax.set_xlabel(axis)
    ax.set_ylabel("mood")
    ax.set_ylim(0, 1.05)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.show()


class Visualiser:

    def __init__(self):
        self.db_of_mood = TinyDBofMood("json_mood.json", "tinydb_mood.json")
        self.word_map = self.db_of_mood.count_words(DONT_CARE_LIST)

    def draw_range(self, minimum=1, maximum=400):
        count_map = {}

        for word in self.word_map.copy():
            if minimum <= self.word_map[word]["count"] <= maximum:
                count_map[word] = self.word_map[word]["count"]

        sorted_map = {k: v for k, v in sorted(count_map.items(), key=lambda item: item[1])}
        draw_bar_from_dict(sorted_map)


    def draw_density(self):
        density_map = {"2": 0, "3": 0, "4": 0, "5": 0, "6-9": 0, "10-14": 0, "15-20": 0, "20+": 0}

        for word in self.word_map.values():
            count = word["count"]
            if count == 2:
                density_map["2"] += 1
            elif count == 3:
                density_map["3"] += 1
            elif count == 4:
                density_map["4"] += 1
            elif count == 5:
                density_map["5"] += 1
            elif 6 <= count <= 9:
                density_map["6-9"] += 1
            elif 10 <= count <= 14:
                density_map["10-14"] += 1
            elif 15 <= count <= 20:
                density_map["15-20"] += 1
            else:
                density_map["20+"] += 1

        draw_bar_from_dict(density_map)

    def draw_change(self, axis : str):
        mood_table = self.db_of_mood.mood_table
        accumulative_map = {}

        try:
            for mood in mood_table:
                value = mood[axis]
                if value not in accumulative_map:
                    accumulative_map[value] = [mood["mood"]]
                else:
                    accumulative_map[value].append(mood["mood"])

        except KeyError:
            print("Axis name not found.")

        average_map = {}
        for value in accumulative_map:
            list_of_int = accumulative_map[value]
            average_map[value] = len(list_of_int) / sum(list_of_int)

        # sort average_map into key ascending order
        kl = list(average_map.keys())
        kl.sort()
        avg_map = {}
        for k in kl:
            avg_map[k] = average_map[k]

        draw_line_from_dict(avg_map, axis)


if __name__ == "__main__":
    visualiser = Visualiser()
    visualiser.draw_change("day")
