from django.contrib import admin
from denisshop.models import Game, Platform, Genre, Series, Key

admin.site.register(Platform)
admin.site.register(Genre)
admin.site.register(Series)


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


