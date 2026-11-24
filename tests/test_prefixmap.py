from strcuta import prefixmap, voicebank


def load_map(tmp_path, text):
    path = tmp_path / "prefix.map"
    path.write_bytes(text.encode("cp932"))
    return prefixmap.load(path)


def test_line_with_prefix_and_suffix(tmp_path):
    # [x] When a line has a prefix and a suffix, load can map the note to both.
    # Given a line with both columns filled
    text = "C4\t強\t_hi\n"
    # When the map is loaded
    m = load_map(tmp_path, text)
    # Then the note maps to the prefix and the suffix
    assert m == {"C4": ("強", "_hi")}


def test_line_with_suffix_only(tmp_path):
    # [x] When the prefix column is empty, load can map the note to the suffix alone.
    # Given a line whose prefix column is empty
    text = "C4\t\t_hi\n"
    # When the map is loaded
    m = load_map(tmp_path, text)
    # Then the note maps to an empty prefix and the suffix
    assert m == {"C4": ("", "_hi")}


def test_line_with_missing_columns(tmp_path):
    # [x] When a line stops before the suffix column, load can treat the missing columns as empty.
    # Given a line with only a prefix and a line with only the note
    text = "C4\t強\nD4\n"
    # When the map is loaded
    m = load_map(tmp_path, text)
    # Then the missing columns are empty
    assert m == {"C4": ("強", ""), "D4": ("", "")}


def test_blank_lines_and_crlf(tmp_path):
    # [x] When the file has blank lines and CRLF line endings, load can skip the blank lines.
    # Given CRLF lines with a blank line between them
    text = "C4\t\t_lo\r\n\r\nD4\t\t_hi\r\n"
    # When the map is loaded
    m = load_map(tmp_path, text)
    # Then only the two notes are mapped, without the line endings
    assert m == {"C4": ("", "_lo"), "D4": ("", "_hi")}


def test_resolve_puts_prefix_before_spell_and_suffix_after():
    # [x] When a note has a prefix and a suffix, resolve can put the prefix before the spell and the suffix after it.
    # Given a voice bank whose note C4 has a prefix and a suffix
    bank = voicebank.Type(rootdir=".", otos={}, prefixes={"C4": ("強", "_hi")})
    # When a spell is resolved at C4
    alias = bank.resolve("a か", "C4")
    # Then the alias is prefix + spell + suffix
    assert alias == "強a か_hi"
