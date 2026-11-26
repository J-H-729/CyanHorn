from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable


TOKEN_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|[0-9]+|[\u4e00-\u9fff]")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


@dataclass(frozen=True)
class SearchResult:
    document_id: str
    score: float
    document: dict[str, Any]


class BM25Index:
    """Small dependency-free BM25 index for project and function retrieval."""

    def __init__(self, documents: Iterable[dict[str, Any]], *, k1: float = 1.5, b: float = 0.75):
        self.documents = list(documents)
        self.k1 = k1
        self.b = b
        self._tokens = [tokenize(self._document_text(doc)) for doc in self.documents]
        self._frequencies = [Counter(tokens) for tokens in self._tokens]
        self._document_frequency: Counter[str] = Counter()
        for frequencies in self._frequencies:
            self._document_frequency.update(frequencies.keys())
        self._average_length = sum(map(len, self._tokens)) / max(len(self._tokens), 1)

    @staticmethod
    def _document_text(document: dict[str, Any]) -> str:
        values = []
        for value in document.values():
            if isinstance(value, (list, tuple, set)):
                values.extend(str(item) for item in value)
            elif isinstance(value, dict):
                values.extend(str(item) for item in value.values())
            else:
                values.append(str(value))
        return " ".join(values)

    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        query_terms = tokenize(query)
        if not query_terms:
            return []
        document_count = len(self.documents)
        scored = []
        for index, frequencies in enumerate(self._frequencies):
            length = len(self._tokens[index])
            score = 0.0
            for term in query_terms:
                term_frequency = frequencies.get(term, 0)
                if not term_frequency:
                    continue
                df = self._document_frequency[term]
                idf = math.log(1 + (document_count - df + 0.5) / (df + 0.5))
                normalizer = 1 - self.b + self.b * length / max(self._average_length, 1)
                score += idf * (term_frequency * (self.k1 + 1)) / (term_frequency + self.k1 * normalizer)
            scored.append((score, index))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return [
            SearchResult(
                document_id=str(self.documents[index].get("project_id", index)),
                score=score,
                document=self.documents[index],
            )
            for score, index in scored[:limit]
            if score > 0
        ]

