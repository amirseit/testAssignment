from tinydb import TinyDB

# Load the database
db = TinyDB("database.json")

# Access the 'templates' table
templates_table = db.table("templates")

# Print the templates
print("Current templates in the database:")
templates = templates_table.all()

# Check and print each template
if not templates:
    print("No templates found in the database.")
else:
    for template in templates:
        print(template)

def get_templates():
    """Fetch all form templates from the database."""
    # Fetch all records from the 'templates' table
    return db.table("templates").all()