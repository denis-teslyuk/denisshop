from django.contrib import admin
from denisshop.models import Game, Platform, Genre, Series, Key, Review

admin.site.register(Platform)
admin.site.register(Genre)
admin.site.register(Series)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', )
    list_display_links = ('pk', )
    exclude = ('time_create', 'time_update')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'sale_price', 'release')
    list_display_links = ('title',)
    exclude = ('slug', )

@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ('key',)
    list_display_links = ('key',)
    exclude = ('slug', )


