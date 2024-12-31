# from django.contrib import admin
# from .models import Event
from django.contrib import admin
# from .models import Registration, Event
from django.utils.html import format_html
from .models.Event import Event
from .models.Registration import Registration

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'title', 'start_time', 'end_time', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'event_id', 'description')
    # You can include the media file directly in the form
    fields = ('event_id', 'title', 'description', 'start_time', 'end_time', 'location', 'status', 'media_file', 'amount_per_person', 'amount_per_adult_guest', 'amount_per_child_guest', 'bkash_account_number', 'bkash_payment_option', 'nagad_account_number', 'nagad_payment_option', 'rocket_account_number', 'rocket_payment_option', 'bank_account_name', 'bank_account_number', 'bank_name', 'bank_branch_name', 'bank_swift_code', 'bank_routing_number', 'bank_city', 'bank_country')

admin.site.register(Event, EventAdmin)

# Define a custom admin class for Registration model
class RegistrationAdmin(admin.ModelAdmin):
    # List the fields you want to display in the admin list view
    list_display = (
        'student_id', 'full_name', 'event_id', 'total_amount', 'registration_datetime', 'approved', 'transaction_document', 'profile_picture', 'action_buttons'
    )

    # Add filters to the sidebar
    list_filter = ('approved', 'event_id')

    # Add search fields for quick searching
    search_fields = ('student_id', 'full_name', 'email', 'transaction_id')

    # Allow the admin to edit multiple records at once (bulk actions)
    actions = ['approve_registrations', 'reject_registrations']

    # Add a custom button to approve/reject directly from the list view
    def action_buttons(self, obj):
        return format_html(
            '<a class="button" href="/admin/app/registration/{}/change/">View</a>',
            obj.id
        )
    action_buttons.short_description = 'Actions'

    # Method for approving registrations in bulk
    def approve_registrations(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f'{updated} registration(s) approved.')
    approve_registrations.short_description = 'Approve selected registrations'

    # Method for rejecting registrations in bulk
    def reject_registrations(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, f'{updated} registration(s) rejected.')
    reject_registrations.short_description = 'Reject selected registrations'

    # Make sure admin can see the password field (although hashed, useful for debugging)
    readonly_fields = ('password',)

# Register the Registration model with the custom admin class
admin.site.register(Registration, RegistrationAdmin)
