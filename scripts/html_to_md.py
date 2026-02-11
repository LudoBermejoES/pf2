import os
from bs4 import BeautifulSoup
import re

def html_to_markdown(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    markdown_output = []

    # Remove style and script tags
    for s in soup(['style', 'script']):
        s.decompose()

    def _get_text_with_preserved_spaces(tag):
        # Recursively get text, preserving single spaces between elements
        parts = []
        for content in tag.contents:
            if isinstance(content, str):
                parts.append(content.strip())
            else: # It's a tag
                parts.append(content.get_text(separator=' ', strip=True))
        return re.sub(r'\s+', ' ', ' '.join(parts)).strip()

    # Convert main title (<p class="s12">) to H1
    main_title_tag = soup.find('p', class_='s12')
    if main_title_tag:
        # Clean up any bookmark anchors within the title
        for a_tag in main_title_tag.find_all('a'):
            a_tag.decompose()
        title_text = main_title_tag.get_text(strip=True)
        if title_text:
            main_title_tag.replace_with(f"# {title_text}\n\n")

    # Convert other headings
    for h_level in range(1, 7):
        for h_tag in soup.find_all(f'h{h_level}'):
            heading_text = _get_text_with_preserved_spaces(h_tag)
            heading_text = re.sub(r'<a[^>]*?>&zwnj;</a>', '', heading_text) # Remove any trailing anchor tags or zero-width spaces
            heading_text = re.sub(r'&\w+;', '', heading_text) # remove html entities
            heading_text = heading_text.strip()

            if heading_text:
                h_tag.replace_with(f"{'#' * h_level} {heading_text}\n\n")

    # Process paragraphs and custom list-like elements
    # Iterate over a reversed copy to avoid issues with modifying the list while iterating
    for p_tag in reversed(soup.find_all('p')):
        style = p_tag.get('style', '')
        # Heuristic: if a <p> tag has a link and significant left padding, treat as a list item
        is_list_item = False
        if p_tag.find('a') and 'padding-left' in style:
            match = re.search(r'padding-left: (\d+)pt', style)
            if match and int(match.group(1)) > 20: # Threshold for significant indentation
                a_tag = p_tag.find('a')
                if a_tag and a_tag.get_text(strip=True) and a_tag.get('href'):
                    link_text = a_tag.get_text(strip=True)
                    link_href = a_tag['href']
                    # Clean up text to remove potential page numbers
                    clean_text = re.sub(r'\s+Page\s+\d+', '', link_text).strip()
                    p_tag.replace_with(f"* [{clean_text}]({link_href})\n")
                    is_list_item = True
                elif p_tag.get_text(strip=True):
                    # If it has padding and no proper link, treat as a list item without link
                    p_tag.replace_with(f"* {p_tag.get_text(strip=True)}\n")
                    is_list_item = True

        if not is_list_item:
            # General paragraph conversion for remaining <p> tags
            p_text = p_tag.get_text(separator=' ', strip=True)
            p_text = re.sub(r'<a[^>]*?>&zwnj;</a>', '', p_text)
            p_text = re.sub(r'&\w+;', '', p_text) # remove html entities
            p_text = p_text.strip()

            if p_text:
                p_tag.replace_with(f"{p_text}\n\n")
            else:
                p_tag.decompose() # Remove empty paragraphs

    # Convert bold and italic (strong, em, b, i)
    for strong_tag in soup.find_all(['strong', 'b']):
        strong_tag.replace_with(f"**{strong_tag.get_text(strip=True)}**")
    for em_tag in soup.find_all(['em', 'i']):
        em_tag.replace_with(f"*{em_tag.get_text(strip=True)}*")

    # Convert links
    # This loop is specifically for standalone <a> tags that haven't been handled
    # (e.g., not part of the custom list items or decomposed already)
    for a_tag in soup.find_all('a', href=True):
        link_text = a_tag.get_text(strip=True)
        link_href = a_tag['href']
        if link_text and link_href:
            a_tag.replace_with(f"[{link_text}]({link_href})")
        elif link_href: # If no link text, just show the href
            a_tag.replace_with(f"<{link_href}>")
        else:
            a_tag.decompose() # Remove empty links

    # Convert lists (ul and ol)
    for ul_tag in soup.find_all('ul'):
        list_items = []
        for li_tag in ul_tag.find_all('li', recursive=False): # Only direct children
            item_text = li_tag.get_text(strip=True)
            if item_text:
                list_items.append(f"* {item_text}")
        if list_items:
            ul_tag.replace_with("\n".join(list_items) + "\n\n")

    for ol_tag in soup.find_all('ol'):
        list_items = []
        for i, li_tag in enumerate(ol_tag.find_all('li', recursive=False)): # Only direct children
            item_text = li_tag.get_text(strip=True)
            if item_text:
                list_items.append(f"{i+1}. {item_text}")
        if list_items:
            ol_tag.replace_with("\n".join(list_items) + "\n\n")


    # Extract the main content. This part might need adjustment based on the actual HTML structure.
    # Often content is within a <body> or a specific div.
    # For now, let's try to get everything from the body, assuming the head is already handled.
    body_content = soup.find('body')
    if body_content:
        # Convert remaining tags (like span, div without specific meaning) to their text content
        for tag in body_content.find_all(True): # True means select all tags
            if tag.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li', 'a', 'strong', 'em', 'b', 'i']:
                # Replace with just its text content if it's not a block-level element and has text
                if tag.get_text(strip=True) and tag.name not in ['html', 'body']:
                    tag.replace_with(tag.get_text())
                else:
                    tag.decompose() # Remove other tags that might just be styling containers


        markdown_output = body_content.get_text(separator='\n').strip()
    else:
        markdown_output = soup.get_text(separator='\n').strip()

    # Clean up multiple newlines and zero-width spaces
    markdown_output = re.sub(r'\n\s*\n', '\n\n', markdown_output)
    markdown_output = re.sub(r'\n{3,}', '\n\n', markdown_output)
    markdown_output = markdown_output.replace('‌', '') # Remove zero-width spaces

    return markdown_output

def main():
    input_dir = 'original/treasure_vault/chapters_html'
    output_dir = 'docs/treasure_vault_md'

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    html_files = [f for f in os.listdir(input_dir) if f.endswith('.html')]

    for html_file in html_files:
        input_path = os.path.join(input_dir, html_file)
        output_filename = os.path.splitext(html_file)[0] + '.md'
        output_path = os.path.join(output_dir, output_filename)

        print(f"Converting {input_path} to {output_path}...")

        with open(input_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        markdown_content = html_to_markdown(html_content)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

    print("Conversion complete.")

if __name__ == '__main__':
    main()
