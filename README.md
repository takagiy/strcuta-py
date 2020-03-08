<!-- Copyright (C) Yuki Takagi 2020 -->
<!-- Distributed under the Boost Software License, Version 1.0. -->
<!-- (See accompanying file LICENSE_1_0.txt or copy at -->
<!-- https://www.boost.org/LICENSE_1_0.txt) -->

# strcuta - Loading UTAU voice banks into the Python data structure

## Little example

```
from strcuta import voicebank

# Load the voice bank "Yamine Renri VCV ver.1.5" (Thanks to the owner :D).
renri = voicebank.load("../闇音レンリ・連続音Ver1.5")

# Resolve the spell (u-ta) and the pitch (F#4) into the voice as a wave data in
# accordance with the "oto.ini"s and the "prefix.map".
uta = renri.voice("u た", "F#5")

# Save the data with the WAVE format.
uta.write("uta_fs5.wav")

# Cut the specific segment of the voice and then save it.
# "Overlap"
uta.ovl().write("uta_ovl.wav")
# "Preutterance"
uta.pre().write("uta_pre.wav")
# "Consonant". con() or fixed()
uta.con().write("uta_vc-.wav")
# "Vowel". vow() or stretchable()
uta.vow().write("uta_-v.wav")
# Exepct for the preutterance
uta.intime().write("uta_intime.wav")

# Also play voices with the "sounddevice" package.
uta.play()
uta.con().play() 
```

Currently, `strcuta` can load -
  * `*.wav`
  * `*.frq`
  * `oto.ini`
  * `prefix.map`.
