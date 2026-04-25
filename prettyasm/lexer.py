from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


# TODO: this forces the language to use this system for comments, which is inflexible.
# However, we want to agree on a syntax for comments regardless of the section we're in,
# so we use any // (that is not part of a string literal) as comments
# not very easy to customize what counts as a comment, but it is consistent across sections and simple to implement.
def trim_line(line: str, comment_prefix: str = "//") -> str:
	# Handle comment markers inside quoted strings.
	in_string = False
	escaped = False

	for idx, char in enumerate(line):
		if char == '"' and not escaped:
			in_string = not in_string

		if char == '\\' and not escaped:
			escaped = True
		else:
			escaped = False

		if (
			not in_string
			and char == comment_prefix[0]
			and line.startswith(comment_prefix, idx)
		):
			return line[:idx].strip()

	return line.strip()


@dataclass
class LexedFile:
	sections: Dict[str, List[str]]

	def get_section(self, section_name: str) -> List[str]:
		return self.sections.get(section_name, [])


class SectionFileLexer:
	def __init__(self, section_keyword: str = "section", comment_prefix: str = "//"):
		self.section_keyword = section_keyword
		self.comment_prefix = comment_prefix

	def clean_line(self, line: str) -> str:
		return trim_line(line, comment_prefix=self.comment_prefix)

	def section_from_line(self, line: str) -> Optional[str]:
		parts = line.split(None, 1)
		if len(parts) != 2 or parts[0] != self.section_keyword:
			return None

		section_name = parts[1].strip()
		if len(section_name) == 0:
			raise ValueError("Section header must include a section name")

		return section_name

	def lex_lines(self, lines: Iterable[str]) -> LexedFile:
		sections: Dict[str, List[str]] = {}
		active_section: Optional[str] = None

		for line_num, raw_line in enumerate(lines, start=1):
			line = self.clean_line(raw_line)
			if len(line) == 0:
				continue

			section_name = self.section_from_line(line)
			if section_name is not None:
				active_section = section_name
				if section_name not in sections:
					sections[section_name] = []
				continue

			if active_section is None:
				raise ValueError(
					f"Line {line_num}: encountered content before any section header"
				)

			sections[active_section].append(line)

		return LexedFile(sections=sections)

	def lex_file(self, filename: str) -> LexedFile:
		with open(filename, "r") as file:
			return self.lex_lines(file.readlines())
