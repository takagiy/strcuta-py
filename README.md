<!-- Copyright (C) Yuki Takagi 2020 -->
<!-- Distributed under the Boost Software License, Version 1.0. -->
<!-- (See accompanying file LICENSE_1_0.txt or copy at -->
<!-- https://www.boost.org/LICENSE_1_0.txt) -->

# strcuta - Loading UTAU voice banks into the Python data structure [![PyPI](https://img.shields.io/pypi/v/strcuta)](https://pypi.org/project/strcuta) [![Github repository](https://img.shields.io/badge/github-repo-green)](https://github.com/takagiy/strcuta-py) [![Release history](https://img.shields.io/badge/pypi-look%20for%20early%20releases-orange)](https://pypi.org/project/strcuta/#history) [![License](https://img.shields.io/pypi/l/strcuta)](https://github.com/takagiy/strcuta-py/blob/master/LICENSE_1_0.txt)

## Little example

```python
from strcuta import voicebank

# Load the voice bank "Yamine Renri VCV ver.1.5" (Thanks to the owner :D).
renri = voicebank.load("../闇音レンリ・連続音Ver1.5")

# Resolve the spell (u-ta) and the pitch (F#5) into the voice as a wave data in
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
# Except for the preutterance
uta.intime().write("uta_intime.wav")

# Also play voices with the "sounddevice" package. (This is an optional
# feature. Install the "strcuta[play]" instead of the "strcuta" to install the
# "sounddevice" together.)
uta.play()
uta.con().play() 
```

Currently, `strcuta` can load -
  * `*.wav`
  * `*.frq`
  * `oto.ini`
  * `prefix.map`.

You can find the early releases in the [release history](https://pypi.org/project/strcuta/#history).
