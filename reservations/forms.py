from django import forms

from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "guest_name",
            "guest_email",
            "party_size",
            "reservation_time",
            "occasion_note",
        ]
        widgets = {
            "reservation_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "occasion_note": forms.Textarea(attrs={"rows": 4}),
        }


class MenuImportForm(forms.Form):
    menu_url = forms.URLField(
        label="Menu preview URL",
        widget=forms.URLInput(attrs={"placeholder": "https://example.com/private-menu.txt"}),
    )
