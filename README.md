<!-- Copyright (C) Yuki Takagi 2020 -->
<!-- Distributed under the Boost Software License, Version 1.0. -->
<!-- (See accompanying file LICENSE_1_0.txt or copy at -->
<!-- https://www.boost.org/LICENSE_1_0.txt) -->

# strcuta - Loading UTAU voice banks into the Python data structure

## Little example

```python
from strcuta import voicebank

renri = voicebank.load("../闇音レンリ・連続音Ver1.5")
uta = renri.voice("u た", "F#5")

uta.write("uta_fs5.wav")
uta.ovl().write("uta_fs5_ovl.wav")
uta.pre().write("uta_fs5_pre.wav")
# fixed() or con()
uta.fixed().write("uta_fs5_vc-.wav")
# stretchable() or vow()
uta.stretchable().write("uta_fs5_-v.wav")

# play voice with the sounddevice package
uta.play()
uta.ovl().play()
```

Currently, `strcuta` can load -
  * `*.wav`
  * `*.frq`
  * `oto.ini`
  * `prefix.map`.
