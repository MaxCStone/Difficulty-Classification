from miditok import REMI, TokenizerConfig


def get_tokenizer() -> REMI:
    config = TokenizerConfig(
        pitch_range=(21, 109),  # full piano range
        beat_res={(0, 4): 8},  # uniform resolution
        num_velocities=1,  # effectively disables velocity variation
        use_velocities=False,  # we don't need velocity
        use_note_duration_programs=list(range(-1, 128)),  # durations for all tracks
        default_note_duration=0.5,
        use_tempos=True,
        num_tempos=32,
        tempo_range=(40, 250),
        log_tempos=False,
        use_time_signatures=True,
        time_signature_range={
            4: (1, 12),  # allow 1/4 to 12/4
            8: (1, 12),  # allow 1/8 to 12/8
        },
        use_chords=False,
        use_rests=False,
        use_sustain_pedals=False,
        use_pitch_bends=False,
        use_pitch_intervals=False,
        use_programs=False,
        one_token_stream_for_programs=True,
        program_changes=False,
        use_pitchdrum_tokens=False,
        encode_ids_split="bar",
        remove_duplicated_notes=True,
        delete_equal_successive_tempo_changes=True,
        delete_equal_successive_time_sig_changes=True,
        special_tokens=["PAD", "BOS", "EOS"],
        # --- Unused ---
        beat_res_rest={(0, 1): 8},
        chord_maps={},
        chord_tokens_with_root_note=False,
        chord_unknown=None,
        sustain_pedal_duration=False,
        pitch_bend_range=(-8192, 8191, 32),
        programs=list(range(-1, 128)),
        max_pitch_interval=16,
        pitch_intervals_max_time_dist=1,
        drums_pitch_range=(27, 88),
        # --- Attribute controls (disabled) ---
        ac_polyphony_track=False,
        ac_polyphony_bar=False,
        ac_polyphony_min=1,
        ac_polyphony_max=6,
        ac_pitch_class_bar=False,
        ac_note_density_track=False,
        ac_note_density_track_min=0,
        ac_note_density_track_max=18,
        ac_note_density_bar=False,
        ac_note_density_bar_max=18,
        ac_note_duration_bar=False,
        ac_note_duration_track=False,
        ac_repetition_track=False,
        ac_repetition_track_num_bins=10,
        ac_repetition_track_num_consec_bars=4,
    )

    tokenizer = REMI(config)

    return tokenizer
