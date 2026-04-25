from miditok import REMI, TokenizerConfig
import music21
from tokenizer import get_tokenizer
import numpy as np
import os
import json
from collections import deque
from tqdm import tqdm


def count_non_waits(neighbors):
    non_waits = 0
    for n in neighbors:
        if n[0] != "rest":
            non_waits += 1
    return non_waits

def get_distance_k(notes, k):
    neighbors = deque(maxlen=k)
    distances = []
    for note in notes:
        neighbors.append(note)
        if len(neighbors) == k:
            neighbors.popleft()
        if count_non_waits(neighbors) > 2:
            distance = max(
                abs(note[0].frequency - n[0].frequency) for n in neighbors if n[0] != "rest" and note[0] != "rest"
            )
            distances.append(distance)
    return distances

def get_stats(xml_path: str, tokenizer: REMI) -> dict:
    score = music21.converter.parse(xml_path)
    stats = {}

    key_signature = score.analyze("key").sharps

    time_signatures = list()
    tempos = set()
    notes_left = []  # stores list of (pitch, duration) tuples, pitch=rest for rests
    notes_right = []  # NOTE: these are ignored as of now
    for notes, part in zip([notes_left, notes_right], score.parts):
        for measure in part.getElementsByClass(music21.stream.Measure):
            ts = measure.getTimeSignatures()[0].ratioString
            time_signatures.append(ts)

            measure_tempos = measure.recurse().getElementsByClass(
                music21.tempo.MetronomeMark
            )
            [tempos.add(t.number) for t in measure_tempos if t is not None]

            for e in measure.recurse().notesAndRests:
                if isinstance(e, music21.note.Note):
                    n = (
                        e.pitch,
                        music21.common.numberTools.numToIntOrFloat(e.quarterLength),
                    )
                    notes.append(n)
                elif isinstance(e, music21.chord.Chord):
                    for p in e.pitches:
                        notes.append((p, float(e.quarterLength)))
                elif isinstance(e, music21.note.Rest):
                    n = (
                        "rest",
                        music21.common.numberTools.numToIntOrFloat(e.quarterLength),
                    )
                    notes.append(n)
    num_measures = len(time_signatures) // 2
    time_signatures = set(time_signatures)

    pitches_left = [n[0].frequency for n in notes_left if n[0] != "rest"]
    pitches_right = [n[0].frequency for n in notes_right if n[0] != "rest"]
    durations_left = [n[1] for n in notes_left]
    durations_right = [n[1] for n in notes_right]
    note_range_left = (
        max(pitches_left) - min(pitches_left) if len(pitches_left) > 0 else None
    )
    note_range_right = (
        max(pitches_right) - min(pitches_right) if len(pitches_right) > 0 else None
    )
    num_rests_left = len([n[0] for n in notes_left if n[0] == "rest"])
    num_rests_right = len([n[0] for n in notes_right if n[0] == "rest"])
    num_accidentals_left = len(
        [n for n in notes_left if n[0] != "rest" and n[0].alter != 0]
    )
    num_accidentals_right = len(
        [n for n in notes_right if n[0] != "rest" and n[0].alter != 0]
    )
    distance_k_left = get_distance_k(notes_left, 4)
    distance_k_right = get_distance_k(notes_right, 4)

    stats["num_measures"] = num_measures
    stats["key_signature"] = key_signature
    stats["time_signatures"] = list(time_signatures)
    stats["tempos"] = list(tempos)
    stats["durations_left"] = durations_left
    stats["durations_right"] = durations_right
    stats["note_range_left"] = note_range_left
    stats["note_range_right"] = note_range_right
    stats["num_rests_left"] = num_rests_left
    stats["num_rests_right"] = num_rests_right
    stats["num_accidentals_left"] = num_accidentals_left
    stats["num_accidentals_right"] = num_accidentals_right
    stats["distance_k_left"] = distance_k_left
    stats["distance_k_right"] = distance_k_right
    print(distance_k_left)
    return stats


def main():
    results = []
    tokenizer = get_tokenizer()
    
    test_path = "C:\\Users\\stonemc\\OneDrive - Milwaukee School of Engineering\\Documents\\CSC 2621\\Final Project\\Difficulty-Classification\\musicxml\\1.xml"
    stats = get_stats(test_path, tokenizer)
    
    # for xml_path in tqdm(os.listdir("musicxml")):
    #     full_xml_path = os.path.join("musicxml", xml_path)
    #     stats = get_stats(full_xml_path, tokenizer)
    #     stats["filename"] = xml_path
    #     results.append(stats)
    #     # print(stats)


if __name__ == "__main__":
    main()
