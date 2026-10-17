# Audio Noise Reduction Project: Step-by-Step Guide

**Goal:** Reduce background noise so the voice is clearer, and measure how well each method works using a known clean reference.

**Idea:** Take a clean speech recording, add noise to it at controlled levels, then try to remove the noise with different DSP algorithms. Because the clean original is known, results can be measured with numbers, not just by listening.

---

## Project folder layout

```
Term Project/
├── audio/
│   ├── clean_speech.wav        (clean speech from Kaggle)
│   ├── noise_recording.m4a     (your iPhone noise recording)
│   ├── noise_recording.wav     (converted)
│   ├── noisy/                  (mixed files go here)
│   └── output/                 (processed files go here)
├── figures/                    (plots for the report)
├── add_noise_to_clean_audio.ipynb
└── audio_eda.ipynb
```

---

## Phase 1: Setup and data preparation

### Step 1: Set up the environment
- [ ] Python libraries installed: numpy, scipy, matplotlib, soundfile, librosa
- [ ] Optional for evaluation: `pesq` and `pystoi`
- [ ] ffmpeg installed and working (check with `ffmpeg -version` in a new terminal)
- [ ] Folders created as shown above

### Step 2: Prepare the clean speech
- [ ] Listen to `clean_speech.wav` and confirm it is clean (no background noise, no echo).
- [ ] Check its sampling rate and number of channels. Convert to **mono** if needed.
- [ ] Trim to 10 to 30 seconds of a single speaker.
- [ ] Normalize it so the peak is at 1.0 (floating point range -1 to 1).
- [ ] Write down the sampling rate. **Every other signal must match it.**

### Step 3: Prepare the noise recordings
- [ ] Convert the iPhone `.m4a` noise recording to `.wav` with ffmpeg (mono, PCM 16-bit).
- [ ] Use the **same sampling rate as the clean speech** (either set it in ffmpeg or resample in Python).
- [ ] Make sure the noise is at least as long as the speech. If it is shorter, repeat it; if longer, trim it.
- [ ] Prepare **at least three noise types**, from easy to hard:
  1. **White Gaussian noise**: generated in Python, the textbook case.
  2. **Stationary real noise**: fan, air conditioner, engine hum. Steady over time.
  3. **Non-stationary noise**: café chatter, traffic, crowd. Changes over time, so it is harder.
- Note: AAC (`.m4a`) is lossy. Mention this in the report.

---

## Phase 2: Create the noisy data

### Step 4: Mix noise at controlled SNR levels
- Choose target SNRs: **0, 5, 10 and 20 dB**.
  - 0 dB: noise as strong as the voice (very hard)
  - 20 dB: noise much weaker than the voice (mild)
- For each noise type and SNR:
  1. Measure the power of the clean speech.
  2. Scale the noise so that speech power divided by noise power matches the target SNR.
  3. Add the scaled noise to the clean speech.
- Add **1 to 2 seconds of noise only** at the start of each file. This gives a real noise-only segment for the noise estimate.
- Use a **fixed random seed** for generated noise so results can be repeated.
- With 3 noise types and 4 SNRs you will have **12 noisy files**. Save them in `audio/noisy/` with clear names, for example `white_10dB.wav`.

### Step 5: Check the noisy files
- [ ] Listen to a few files. Difficulty should clearly increase as SNR drops.
- [ ] Measure the real SNR of each file and confirm it matches the target.
- [ ] Plot the waveform and spectrogram of clean vs. noisy for one case (a good figure for the report).
- [ ] Check that no file is clipped (values beyond -1 to 1). If so, scale everything down.

---

## Phase 3: Noise reduction methods

### Step 6: Baseline with simple filters
- Apply a **highpass at about 70 Hz** and a **lowpass at about 4 to 8 kHz**.
- Use zero-phase filtering so the signal is not delayed or distorted.
- Expect a small improvement at best, especially for white noise, which covers all frequencies.
- Purpose: show why simple filters are not enough when noise overlaps the voice.

### Step 7: Get the noise estimate
Make two versions so they can be compared:
- **Ideal estimate:** the true noise you added (you know it exactly).
- **Realistic estimate:** the average spectrum of the noise-only lead-in at the start of the file.

Comparing them shows how much the estimate quality affects the result.

### Step 8: Spectral subtraction (main method)
1. Cut the signal into short overlapping frames (about 20 to 32 ms, 50 to 75% overlap) using a Hann window.
2. Compute the STFT and split it into **magnitude** and **phase**.
3. Subtract the noise magnitude estimate from each frame, scaled by an **over-subtraction factor**.
4. Apply a **spectral floor** so magnitudes never go negative.
5. Combine the new magnitude with the original noisy phase and apply the inverse STFT.

### Step 9: Wiener filter (second method)
1. Use the same STFT setup as Step 8.
2. For each time-frequency point, estimate how strong the speech is compared with the noise.
3. Convert that into a gain between 0 and 1 (near 1 where speech dominates, near 0 where noise dominates).
4. Multiply the STFT by the gain and apply the inverse STFT.
- It is gentler than spectral subtraction and usually produces fewer artifacts ("musical noise").

### Step 10: Optional third method
Choose one if time allows:
- **Adaptive noise tracking:** keep updating the noise estimate over time. Helps with non-stationary noise.
- **Wavelet denoising:** a different approach, good for comparison.
- **`noisereduce` library:** as an outside reference to compare against your own implementation.

---

## Phase 4: Tuning and evaluation

### Step 11: Tune the parameters
Use one mid-difficulty file (for example white noise at 5 dB) and change one setting at a time:
- **Over-subtraction factor:** try 1, 2, 3. Higher removes more noise but damages the voice and creates watery artifacts.
- **Spectral floor:** try 0.01 to 0.1. A small nonzero floor reduces artifacts.
- **Frame size:** try 256, 512, 1024 samples. Larger gives better frequency detail, smaller gives better time detail.

Pick one final setting (by ear and by score) and **use it for all files** so the comparison is fair.

### Step 12: Measure the results
Compare every output with the **clean original**:
- **SNR improvement (dB):** output SNR minus input SNR. This is the main number.
- **PESQ** (optional): estimated speech quality.
- **STOI** (optional): estimated speech intelligibility.
- **Spectrograms** before and after.
- **Listening notes:** play at equal loudness, with headphones.

### Step 13: Build the comparison
Make a results table: rows are methods (original, simple filter, spectral subtraction, Wiener, optional third), columns are noise type and SNR, values are SNR improvement. Look for patterns:
- Which method works best for white noise vs. real noise?
- How does performance change as SNR drops?
- Does steady noise work better than changing noise?
- Where does the voice get damaged, or where does musical noise appear?

---

## Phase 5: Real recording and report

### Step 14: Test on your original iPhone recording
- Apply the best method and settings to `hci_audio_record.wav`.
- There is no clean reference, so judge it by spectrograms and listening only.
- For the noise estimate, use a separate noise-only clip recorded in the same place, or the quietest frames of the recording.
- Report it honestly as a demonstration, not a measurement.

### Step 15: Write the report
1. **Introduction:** the problem and the goal.
2. **Data:** clean speech source, noise types, SNR levels, and the `.m4a` to `.wav` conversion (AAC is lossy).
3. **Analysis:** spectrum findings from the iPhone recording (no mains hum, little energy at the extremes, noise overlapping the voice band).
4. **Methods:** each algorithm, its parameters, and why they were chosen.
5. **Results:** table, spectrograms, SNR improvements.
6. **Discussion:** strengths and weaknesses, musical noise, stationary vs. non-stationary behavior.
7. **Real recording demo.**
8. **Conclusion and limitations:** single microphone, noise estimate errors, ideas for improvement.

---

## Suggested schedule

| Stage | Steps | Time |
|---|---|---|
| Setup and data | 1 to 5 | 1 to 2 days |
| Methods | 6 to 10 | 2 to 3 days |
| Tuning and evaluation | 11 to 13 | 1 to 2 days |
| Real recording and report | 14 to 15 | 2 days |

---

## Tips

- Start with **white noise at 10 dB**. Get everything working there, then expand to the other cases.
- Always compare audio at the **same loudness**, otherwise the louder one sounds better.
- Quote file paths that contain spaces and use forward slashes (`/`).
- Save figures as you go. You will need them for the report.
- Keep a fixed random seed so your results are repeatable.
- Waveform plots hide small changes. Use spectrograms and the difference signal (original minus processed) to see what an algorithm actually did.

---

## Progress checklist

- [ ] Phase 1: clean speech and noise files prepared, same sampling rate
- [ ] Phase 2: 12 noisy files created and checked
- [ ] Phase 3: baseline, spectral subtraction and Wiener filter working
- [ ] Phase 4: parameters tuned, results table complete
- [ ] Phase 5: iPhone recording tested, report written