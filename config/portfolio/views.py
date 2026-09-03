from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction
from .services import send_telegram_notification
from django.http import HttpResponse

from .forms import ContactForm

from .models import (
    Profile,
    SocialLink,
    Experience,
    Project,
    Skill,
    Education,
    Resume,
    ContactMessage,
)


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]

    return HttpResponse(
        "\n".join(lines),
        content_type="text/plain"
    )
    
    

def home(request):

    profile = Profile.objects.filter(
        is_active=True
    ).first()

    social_links = SocialLink.objects.filter(
        is_active=True
    )

    experiences = Experience.objects.filter(
        is_active=True
    )

    projects = Project.objects.filter(
        is_active=True
    )

    skills = Skill.objects.filter(
        is_active=True
    )

    education = Education.objects.filter(
        is_active=True
    )

    resume = Resume.objects.filter(
        is_active=True
    ).first()


    # =====================================================
    # CONTACT FORM
    # =====================================================

    if request.method == "POST":

        contact_form = ContactForm(
            request.POST
        )

        if contact_form.is_valid():

            with transaction.atomic():

                contact_message = ContactMessage.objects.create(
                    sender_name=contact_form.cleaned_data["name"],
                    sender_email=contact_form.cleaned_data["email"],
                    subject=contact_form.cleaned_data["subject"],
                    message=contact_form.cleaned_data["message"],
                )

            # Database transaction is already committed here.
            # Telegram failure must not remove the saved message.

            telegram_success = send_telegram_notification(
                contact_message
            )

            if telegram_success:

                contact_message.telegram_sent = True

                contact_message.save(
                    update_fields=["telegram_sent"]
                )

            messages.success(
                request,
                "Your message has been sent successfully."
            )

            return redirect("/#contact")   

    else:

        contact_form = ContactForm()


    context = {
        "profile": profile,
        "social_links": social_links,
        "experiences": experiences,
        "projects": projects,
        "skills": skills,
        "education": education,
        "resume": resume,
        "contact_form": contact_form,
    }


    return render(
        request,
        "portfolio/home.html",
        context
    )
    
    
def error_400(request, exception):
    return render(
        request,
        "400.html",
        status=400,
    )


def error_403(request, exception):
    return render(
        request,
        "403.html",
        status=403,
    )


def error_404(request, exception):
    return render(
        request,
        "404.html",
        status=404,
    )


def error_500(request):
    return render(
        request,
        "500.html",
        status=500,
    )