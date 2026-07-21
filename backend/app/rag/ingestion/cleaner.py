import re

class DocumentCleaner:
    def clean(self, text: str) -> str:
        if not text:
            return ""

        # Normalize line breaks
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Split into lines for processing
        lines = text.split('\n')
        
        cleaned_lines = []
        for line in lines:
            # Remove excessive whitespace within the line
            line = re.sub(r'[ \t]+', ' ', line)
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            cleaned_lines.append(line)
        
        # Rejoin lines
        text = '\n'.join(cleaned_lines)
        
        # Note: Removing duplicated headers and footers perfectly is a complex heuristic.
        # For this phase, we apply a simple heuristic: if the exact same line appears 
        # at the start or end of multiple pages, we could remove it, but since we 
        # joined the text, we look for repeating lines separated by a reasonable gap.
        # Given the complexity and potential for false positives, a robust approach is needed.
        # We will implement a basic version that removes lines that are identical and 
        # appear more than 3 times (likely headers/footers in a long doc).
        # However, it's safer to avoid destroying valid repeating data.
        # We'll stick to a simple deduplication of consecutive identical lines for now,
        # or just leave it as is if it's too risky. Let's do a safe consecutive deduplication.
        
        final_lines = []
        for i, line in enumerate(cleaned_lines):
            if i > 0 and line == cleaned_lines[i-1]:
                continue
            final_lines.append(line)
            
        text = '\n'.join(final_lines)
        
        return text.strip()

cleaner = DocumentCleaner()
