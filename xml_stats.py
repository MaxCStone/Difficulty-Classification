from miditok import REMI, TokenizerConfig
import music21
from tokenizer import get_tokenizer
import numpy as np
import os
import json
from tqdm import tqdm


def get_stats(xml_path: str, tokenizer: REMI) -> dict:
    score = music21.converter.parse(xml_path)
    stats = {}

    key_signature = score.analyze("key").sharps

    time_signatures = set()
    tempos = set()
    notes_left = []  # stores list of (pitch, duration) tuples, pitch=rest for rests
    notes_right = []  # NOTE: these are ignored as of now
    for notes, part in zip([notes_left, notes_right], score.parts):
        for measure in part.getElementsByClass(music21.stream.Measure):
            ts = measure.getTimeSignatures()[0].ratioString
            time_signatures.add(ts)

            measure_tempos = measure.getElementsByClass(music21.tempo.MetronomeMark)
            [tempos.add(t.number) for t in measure_tempos if t is not None]

            for e in measure.notesAndRests:
                if isinstance(e, music21.note.Note):
                    n = (
                        e.pitch,
                        music21.common.numberTools.numToIntOrFloat(e.quarterLength),
                    )
                    notes.append(n)
                elif isinstance(e, music21.note.Rest):
                    n = (
                        "rest",
                        music21.common.numberTools.numToIntOrFloat(e.quarterLength),
                    )
                    notes.append(n)
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

    return stats


def main():
    results = []
    tokenizer = get_tokenizer()
    for xml_path in tqdm(os.listdir("musicxml")):
        full_xml_path = os.path.join("musicxml", xml_path)
        stats = get_stats(full_xml_path, tokenizer)
        stats["filename"] = xml_path
        results.append(stats)
        # print(stats)

    with open("stats.json", "w") as fp:
        json.dump(results, fp, indent=4)


if __name__ == "__main__":
    main()
