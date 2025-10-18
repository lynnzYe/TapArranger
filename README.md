# Versions

- V0.1
    - Full working demo
    - Nearest arranger
    - Problems:
        - melody tapping requirement is extremely strict
        - accompaniment cannot have non-chord tone / melodies
        - bass notes are not optimally chosen (e.g. should emphasize root more)
        - weird b9#5 notes get emphasized more, esp. bad when chord is not clear (missing root, third e.g.)
        - One melody note can't have multiple chords -> with tempo estimation you may be able to change chord context
        - or play the root hack/trick
        - left sometimes want to be ahead of the right (chord before melody)

## Major Arrangement Issues:

1. Left hand must wait for the melody
2. Cannot play passing notes
3. Arrangement does not sound professional
    - voice leading & distribution of notes
4. Not using information from the **history**
    - e.g. don't repeat a pitch too frequently
5. Not tempo estimation but beat tracking? (fails at extremely expressive passages)
6. Need to manually label melody & chord

## Major Synthesis Issues:
1. Soundfont not optimal & sometimes weird pitch modulation


## Major Experience Issues:
1. Loss of agency and authorship (low condition)

# Roger's Feedback
People can learn to play with melodic advance (don't play it late)
10~20ms okay, might solve some problem, but not too big to solve all the problems
