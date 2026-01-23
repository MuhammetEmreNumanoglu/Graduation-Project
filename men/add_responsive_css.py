"""
Script to add global-responsive.css to all HTML templates
"""
import os
import re

# Template directory
TEMPLATE_DIR = r"C:\Users\muham\Desktop\iyi-hisset-sistem-main\men\articles\templates\articles"

# CSS link to add
CSS_LINK = '    <link rel="stylesheet" href="{% static \'css/global-responsive.css\' %}" />'

def add_responsive_css(file_path):
    """Add global-responsive.css to an HTML file if not already present"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already added
        if 'global-responsive.css' in content:
            print(f"  ✓ Already has responsive CSS: {os.path.basename(file_path)}")
            return False
        
        # Check if file has a <head> section
        if '<head>' not in content:
            print(f"  ⚠ No <head> section found: {os.path.basename(file_path)}")
            return False
        
        # Add CSS link before </head>
        # Find the last stylesheet or before </head>
        if '</head>' in content:
            # Add before </head>
            content = content.replace('</head>', f'{CSS_LINK}\n  </head>')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Added responsive CSS to: {os.path.basename(file_path)}")
            return True
        else:
            print(f"  ⚠ Could not find </head> tag: {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error processing {os.path.basename(file_path)}: {str(e)}")
        return False

def main():
    """Main function to process all HTML files"""
    print("Adding global-responsive.css to all template files...\n")
    
    if not os.path.exists(TEMPLATE_DIR):
        print(f"Error: Template directory not found: {TEMPLATE_DIR}")
        return
    
    # Get all HTML files
    html_files = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('.html')]
    
    total = len(html_files)
    updated = 0
    
    for html_file in html_files:
        file_path = os.path.join(TEMPLATE_DIR, html_file)
        if os.path.isfile(file_path):
            if add_responsive_css(file_path):
                updated += 1
    
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Total HTML files: {total}")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {total - updated}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
