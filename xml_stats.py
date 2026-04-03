from miditok import REMI, TokenizerConfig
import music21
from tokenizer import get_tokenizer


def get_stats(xml_path: str, tokenizer: REMI) -> dict:
    score = music21.converter.parse(xml_path)
    stats = {}

    key_signature = score.analyze("key")

    time_signatures = set()
    tempos = set()
    notes = []  # stores list of (pitch, duration) tuples, pitch=rest for rests
    for part in score.parts:
        for measure in part.getElementsByClass(music21.stream.Measure):
            ts = measure.getTimeSignatures()
            time_signatures.add(ts)

            measure_tempos = measure.getElementsByClass(music21.tempo.MetronomeMark)
            [tempos.add(t) for t in measure_tempos]

            for e in measure.notesAndRests:
                if isinstance(e, music21.note.Note):
                    n = (e.pitch, e.quarterLength)
                    notes.append(n)
                elif isinstance(e, music21.note.Rest):
                    n = ("rest", e.quarterLength)
                    notes.append(n)

    stats["key_signature"] = key_signature
    stats["time_signatures"] = time_signatures
    stats["tempos"] = tempos
    stats["notes"] = notes

    return stats


def main():
    tokenizer = get_tokenizer()
    xml_path = r"C:\Users\whitcombp\Documents\MSOE2425\Senior\Spring\IntroDataScience\final_project\Difficulty-Classification\musicxml\1.xml"
    stats = get_stats(xml_path, tokenizer)
    print("stats:\n", stats)


if __name__ == "__main__":
    main()
