import os

# Ye script aapke folder ki saari HTML files mein automatically add ho jayegi
script_to_add = """
<script>
    // URL Masking Script
    window.addEventListener("load", function() {
        if (window.location.pathname.endsWith('.html') && window.location.pathname !== '/index.html') {
            let cleanUrl = window.location.pathname.replace('.html', '');
            window.history.replaceState(null, '', cleanUrl);
        }
    });
</script>
</body>
"""

# Current folder ki saari files par loop chalayega
for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check karega ki code pehle se toh add nahi hai (taaki double na ho jaye)
        if "URL Masking Script" not in content:
            # </body> ko replace karke uske upar apna script laga dega
            content = content.replace('</body>', script_to_add)
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
                
print("Mubarak ho bhai! Saari files 2 second mein update ho gayi.")