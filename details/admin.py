from django.contrib import admin
from .models import *

admin.site.register(comments)

class user_details_admin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone','category','date_of_joining','image',)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone','category','date_of_joining','image',)
    list_filter = ('username', 'email', 'first_name', 'last_name', 'category')
admin.site.register(user_details, user_details_admin)


class new_giveaway_admin(admin.ModelAdmin):
    list_display = ('giveaway_id','status', 'username', 'giveaway_title', 'truncated_description', 'start_date','end_date','number_of_winners')
    search_fields = ('giveaway_id','status','username', 'giveaway_title', 'truncated_description', 'start_date','end_date','number_of_winners')
    list_filter = ('giveaway_id','status','username', 'giveaway_title', 'start_date',)

    def truncated_description(self, description):
        max_chars = 40
        ret = description.description
        if len(ret) > max_chars:
            ret = ret[0:max_chars] + '...(truncated)'
        return ret
    truncated_description.short_description = 'description'

admin.site.register(new_giveaway, new_giveaway_admin)


class winners_admin(admin.ModelAdmin):
    list_display = ('giveaway_name', 'winner_name', 'winner_email', 'rank')
    search_fields = ('giveaway_name', 'winner_name', 'winner_email', 'rank')
    list_filter = ('giveaway_name', 'winner_name', 'winner_email', 'rank')
admin.site.register(winners, winners_admin)


class giveaway_rule_admin(admin.ModelAdmin):
    list_display = ('giveaway_name', 'sequence_number')
    search_fields = ('giveaway_name', 'sequence_number')
    list_filter = ('giveaway_name',)
admin.site.register(giveaway_rule,giveaway_rule_admin)


class entry_admin(admin.ModelAdmin):
    list_display = ('user','giveaway_title','giveaway_id','start_date','completed')
    search_fields = ('user','giveaway_title','giveaway_id','start_date','completed')
    list_filter = ('user','giveaway_title')
admin.site.register(entry,entry_admin)

class giveaway_analytics_admin(admin.ModelAdmin):
    list_display = ('giveaway_name', 'giveaway_id','participants_count','completed','partial')
    search_fields = ('giveaway_name', 'giveaway_id','participants_count','completed','partial')
    list_filter = ('giveaway_name','giveaway_id')
admin.site.register(giveaway_analytics,giveaway_analytics_admin)



