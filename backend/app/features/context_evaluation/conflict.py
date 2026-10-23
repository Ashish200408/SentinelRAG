import re
from typing import List, Tuple
from app.rag.retrieval.models import RetrievedChunk
from app.features.context_evaluation.models import ConflictResult

def extract_sentences(text: str) -> List[str]:
    # Simple sentence splitter
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return [s.strip() for s in sentences if s.strip()]

class ConflictDetector:
    def __init__(self):
        self.antonyms = [
            {"enabled", "disabled"},
            {"active", "inactive"},
            {"online", "offline"},
            {"true", "false"},
            {"high", "low"},
            {"yes", "no"},
            {"operational", "broken"},
            {"operational", "non-operational"},
            {"success", "failure"}
        ]
        
    def detect(self, query: str, chunks: List[RetrievedChunk]) -> ConflictResult:
        if not chunks or len(chunks) < 2:
            return ConflictResult(
                conflict_detected=False,
                confidence=0.0,
                reason="Not enough chunks to detect conflict.",
                conflicting_chunk_indices=[]
            )
            
        for i in range(len(chunks)):
            for j in range(i + 1, len(chunks)):
                chunk_i = chunks[i]
                chunk_j = chunks[j]
                
                sentences_i = extract_sentences(chunk_i.chunk_text)
                sentences_j = extract_sentences(chunk_j.chunk_text)
                
                for s_i in sentences_i:
                    for s_j in sentences_j:
                        conflict, reason = self._check_sentence_conflict(s_i, s_j)
                        if conflict:
                            return ConflictResult(
                                conflict_detected=True,
                                confidence=1.0,
                                reason=reason,
                                conflicting_chunk_indices=[i, j],
                                conflicting_sentences=(s_i, s_j)
                            )
                            
        return ConflictResult(
            conflict_detected=False,
            confidence=0.0,
            reason="No deterministic contradiction found between chunks.",
            conflicting_chunk_indices=[],
            conflicting_sentences=("", "")
        )
        
    def _check_sentence_conflict(self, s1: str, s2: str) -> Tuple[bool, str]:
        # Normalize
        norm_s1 = re.sub(r'[^\w\s\.]', '', s1.lower()).strip()
        norm_s2 = re.sub(r'[^\w\s\.]', '', s2.lower()).strip()
        
        if norm_s1.endswith('.'): norm_s1 = norm_s1[:-1]
        if norm_s2.endswith('.'): norm_s2 = norm_s2[:-1]
        
        words1 = norm_s1.split()
        words2 = norm_s2.split()
        
        # 1. Direct Negation
        if self._is_direct_negation(words1, words2) or self._is_direct_negation(words2, words1):
            return True, f"Explicit negation found between: '{s1}' and '{s2}'"
            
        # 2. Numeric Mismatch
        num_conflict = self._check_numeric_mismatch(norm_s1, norm_s2)
        if num_conflict:
            return True, f"Different numeric values found for the same fact: '{s1}' vs '{s2}'"
            
        # 3. Categorical Mismatch
        cat_conflict = self._check_categorical_mismatch(words1, words2)
        if cat_conflict:
            return True, f"Mutually exclusive categorical values found: '{s1}' vs '{s2}'"
            
        return False, ""
        
    def _is_direct_negation(self, words_base: List[str], words_neg: List[str]) -> bool:
        if len(words_neg) == len(words_base) + 1:
            if "not" in words_neg:
                idx = words_neg.index("not")
                without_not = words_neg[:idx] + words_neg[idx+1:]
                if without_not == words_base:
                    return True
        return False
        
    def _check_numeric_mismatch(self, s1: str, s2: str) -> bool:
        pattern = r'\b\d+(?:\.\d+)?(?=[a-zA-Z]*\b)'
        
        nums1 = re.findall(pattern, s1)
        nums2 = re.findall(pattern, s2)
        
        if not nums1 or not nums2:
            return False
            
        template1 = re.sub(pattern, '<NUM>', s1)
        template2 = re.sub(pattern, '<NUM>', s2)
        
        if template1 == template2 and nums1 != nums2:
            return True
                
        return False
        
    def _check_categorical_mismatch(self, words1: List[str], words2: List[str]) -> bool:
        if len(words1) != len(words2):
            return False
            
        diff_count = 0
        diff_w1, diff_w2 = "", ""
        
        for w1, w2 in zip(words1, words2):
            if w1 != w2:
                diff_count += 1
                diff_w1, diff_w2 = w1, w2
                
        if diff_count == 1:
            for pair in self.antonyms:
                if diff_w1 in pair and diff_w2 in pair:
                    return True
                    
        return False

conflict_detector = ConflictDetector()
