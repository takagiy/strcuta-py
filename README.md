<!-- Copyright (C) Yuki Takagi 2020 -->
<!-- Distributed under the Boost Software License, Version 1.0. -->
<!-- (See accompanying file LICENSE_1_0.txt or copy at -->
<!-- https://www.boost.org/LICENSE_1_0.txt) -->

# strcuta - Loading UTAU voice banks into the Python data structure

## Little example

```python
from strcuta import voicebank

renri = voicebank.load("../yaminerenri_1.5-1/闇音レンリ・連続音Ver1.5")
uta = renri.voice("u た", "F#5")

uta.write("uta_fs5.wav")
uta.overlapping().write("uta_fs5_ovl.wav")
uta.prepronounced().write("uta_fs5_pre.wav")
uta.fixed().write("uta_fs5_vc-.wav")
uta.stretchable().write("uta_fs5_-v.wav")
```

Currently, `strcuta` can load -
  * `*.wav`
  * `*.frq`
  * `oto.ini`
  * `prefix.map`.
