try:
    import sys
    from django.contrib import admin
    from django.contrib.auth.models import User
    from django.contrib.auth.admin import UserAdmin
    from .models import IndividualUser, ProfessionalUser, CorporateUser
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)


class AccountAdmin(admin.ModelAdmin):

    def emails(self, obj):
        return obj.user.email

    def name(self, obj):
        return obj.user.first_name

    list_display = ('emails', 'name', 'users_id')
    search_fields = ('user__email', 'user__first_name', 'users_id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(IndividualUser, AccountAdmin)
admin.site.register(ProfessionalUser, AccountAdmin)
admin.site.register(CorporateUser, AccountAdmin)

admin.site.site_title = 'Torus'
admin.site.site_header = 'Torus admin panel'
