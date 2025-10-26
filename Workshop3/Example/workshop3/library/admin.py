from django.contrib import admin
from .models import Author, Publisher, Book

class BookInline(admin.TabularInline):     
	model = Book     
	extra = 1  

@admin.register(Author) 
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')  # Columns in list view
    search_fields = ('first_name','last_name')  # Enable search on first and last name
    ordering = ('last_name',)  # Sort by last name by default
    

@admin.register(Publisher) 
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)  # Add filters in sidebar
    inlines = [BookInline]

@admin.register(Book) 
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'publisher')
    search_fields = ('title',)
    list_filter = ('publisher', 'publish_date')
    date_hierarchy = 'publish_date'  # Drill-down by date
    raw_id_fields = ('publisher',)  # Use popup for foreign key selection
    filter_horizontal = ('authors',)  # Horizontal widget for many-to-many

    def get_authors(self, obj):
        return ", ".join([author.last_name for author in obj.authors.all()])
    get_authors.short_description = 'Authors'  # Column header

admin.site.site_header = "Library Management System"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Welcome to the Library Dashboard"