import os
import re

INPUT_DIR = "original/kingmaker/capitulos"

REPLACEMENTS = {
    "’": "'",
    "‘": "'",
    "“": '"',
    "”": '"',
    "–": "-",
    "—": "--",
    "…": "...",
    "â€™": "'",  
    "â€œ": '"',  
    "â€": '"',  
    "â€”": "--", 
    "â€“": "-",
    "â€¦": "...",
    "Â": "",
}

def clean_text(text):
    for k, v in REPLACEMENTS.items():
        text = text.replace(k, v)
    return text

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Basic Cleanup
    content = clean_text(content)

    # 2. Fix specific merged headers
    # e.g. "unsaid.AMIRI" -> "unsaid.\n\n## AMIRI"
    content = re.sub(r'([a-z]\.)([A-Z]{3,})', r'\1\n\n## \2', content)

    # 3. Aggressive Sidebar Removal
    # Remove the recurring sidebar text that might be malformed
    # "CHAPTER 1 ... Companions ... Weather" or similar artifacts
    # Pattern seems to be lines containing "CHAPTER 1" and "Companions"
    content = re.sub(r'(?i).*CHAPTER 1.*Companions.*', '', content)
    content = re.sub(r'(?i).*Companions.*Amiri.*Ekundayo.*', '', content)
    # Also "Chapter 2 Camping" or "Chapter 3 Weather" if they appear as sidebar artifacts (usually at end of file or page)
    # But be careful not to delete the actual chapter headers if they look like that.
    # The artifacts usually have weird spacing "7Chapter 1Chapter 1" or "Weather120"
    content = re.sub(r'\d+Chapter \d+Chapter \d+', '', content)

    lines = content.splitlines()
    new_lines = []
    buffer = []

    for i, line in enumerate(lines):
        line = line.strip()

        if not line:
            if buffer:
                new_lines.append(" ".join(buffer))
                buffer = []
            new_lines.append("") 
            continue
            
        # Skip pure page numbers
        if re.match(r'^\d+$', line):
            continue

        # Check for Stat Block keywords
        # Bold specific keywords
        # Also handles lines starting with these keywords
        keywords = ["Critical Success", "Success", "Failure", "Critical Failure", 
                    "Trigger", "Requirements", "Prerequisites", "Frequency", "Cost", "Stage \d"]
        for kw in keywords:
            if re.match(fr'^{kw}\b', line):
                 line = re.sub(fr'^({kw})', r'**\1**', line)
                 break

        # Check if Header
        is_header = False
        is_stat_header = False
        
        # Already marked header
        if line.startswith("##"):
            is_header = True
            # Don't title case it blindly if it's already processed, but we can clean it
            # Remove ##, title case, add back?
            # Or just append and continue
            if buffer:
                new_lines.append(" ".join(buffer))
                buffer = []
            new_lines.append(line)
            continue
            
        # Heuristic for new headers
        if line.isupper() and len(line) > 2 and len(line) < 100:
             # Exclude HP lines or stat headers that might be uppercase
             if not line.startswith("HP") and "CREATURE" not in line:
                 is_header = True

        # Stat Block Headers (Name Level) -> ## Name Level
        # e.g. "AMIRI CREATURE 1"
        if re.search(r'\bCREATURE \d+', line):
            is_header = True
            is_stat_header = True
            
        # Stat lines
        is_stat_line = False
        if re.match(r'^(Str|Dex|Con|Int|Wis|Cha|Fort|Ref|Will|Perception|Skills|Languages|Items|AC|HP|Speed|Melee|Ranged|Spells)\b', line):
            is_stat_line = True
            # Exception: "HP" is all caps, so it might have triggered header logic if I wasn't careful
            is_header = False 

        if is_header:
            if buffer:
                new_lines.append(" ".join(buffer))
                buffer = []
            
            # Formatting the header
            if is_stat_header:
                # Keep mostly uppercase or Title Case? 
                # "AMIRI CREATURE 1" -> "## Amiri Creature 1"
                new_lines.append(f"## {line.title()}")
            else:
                new_lines.append(f"## {line.title()}")

        elif is_stat_line:
            if buffer:
                new_lines.append(" ".join(buffer))
                buffer = []
            
            # Format HP line specifically?
            # "HP 22" -> "* **HP** 22"
            if line.startswith("HP"):
                line = line.replace("HP", "**HP**", 1)
            
            # "AC 18; Fort..." -> "* **AC** 18; **Fort**..."
            if line.startswith("AC"):
                 line = line.replace("AC", "**AC**", 1)
                 line = line.replace("Fort", "**Fort**")
                 line = line.replace("Ref", "**Ref**")
                 line = line.replace("Will", "**Will**")

            new_lines.append(f"* {line}")

        else:
            # Regular text line
            # Merge hyphenated lines
            if buffer:
                prev = buffer[-1]
                if prev.endswith("-") and not prev.endswith("--"): # Don't merge em-dashes
                    # Heuristic: Join without space
                    buffer[-1] = prev[:-1] + line
                else:
                    buffer.append(line)
            else:
                buffer.append(line)

    if buffer:
        new_lines.append(" ".join(buffer))
    
    result = "\n".join(new_lines)
    
    # Post-processing
    result = re.sub(r' +', ' ', result)
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result

if __name__ == "__main__":
    files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.md')])
    for filename in files:
        path = os.path.join(INPUT_DIR, filename)
        print(f"Processing {filename}...")
        try:
            new_content = process_file(path)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("Done.")
