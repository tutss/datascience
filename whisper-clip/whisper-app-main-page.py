from st_pages import Page, show_pages, add_page_title

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("whisper-app.py", "Home", "🏠"),
        Page("database_items.py", "Products", ":books:"),
    ]
)