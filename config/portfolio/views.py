from django.contrib import messages
from django.db import transaction
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render, redirect

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
    ResumeDownload,
    TrainingCourse,
)

from .services import (
    send_contact_notification,
    send_resume_download_notification,
)


def home(request):

    # =========================================================
    # LOAD PORTFOLIO DATA
    # =========================================================

    profile = (
        Profile.objects
        .filter(is_active=True)
        .first()
    )

    social_links = (
        SocialLink.objects
        .filter(is_active=True)
        .order_by("display_order", "id")
    )

    experiences = (
        Experience.objects
        .filter(is_active=True)
        .order_by("display_order", "-start_date")
    )

    projects = (
        Project.objects
        .filter(is_active=True)
        .order_by("display_order", "-created_at")
    )

    skills = (
        Skill.objects
        .filter(is_active=True)
        .order_by(
            "display_order",
            "title",
        )
    )

    education = (
        Education.objects
        .filter(is_active=True)
        .order_by(
            "display_order",
            "-start_date",
        )
    )

    training_courses = (
        TrainingCourse.objects
        .filter(is_active=True)
        .order_by(
            "display_order",
            "title",
        )
    )

    resume = (
        Resume.objects
        .filter(is_active=True)
        .first()
    )

    # =========================================================
    # CONTACT FORM
    # =========================================================

    if request.method == "POST":

        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():

            # -------------------------------------------------
            # CHECK RESUME CHOICE
            # -------------------------------------------------

            resume_requested = (
                contact_form.cleaned_data.get(
                    "resume_choice"
                ) == "yes"
            )

            resume_will_download = (
                resume_requested
                and resume is not None
                and bool(resume.resume_file)
            )

            # -------------------------------------------------
            # SAVE MESSAGE TO ORACLE FIRST
            # -------------------------------------------------

            with transaction.atomic():

                contact_message = (
                    ContactMessage.objects.create(
                        sender_name=(
                            contact_form.cleaned_data[
                                "name"
                            ]
                        ),
                        sender_email=(
                            contact_form.cleaned_data[
                                "email"
                            ]
                        ),
                        subject=(
                            contact_form.cleaned_data.get(
                                "subject",
                                "",
                            )
                        ),
                        message=(
                            contact_form.cleaned_data[
                                "message"
                            ]
                        ),
                    )
                )

                # ---------------------------------------------
                # LOG RESUME DOWNLOAD
                # ---------------------------------------------

                resume_download = None

                if resume_will_download:

                    resume_download = (
                        ResumeDownload.objects.create(
                            resume=resume,
                            contact_message=contact_message,
                        )
                    )

            # -------------------------------------------------
            # SEND ONE CONTACT EMAIL
            # -------------------------------------------------

            email_success = (
                send_contact_notification(
                    contact_message,
                    resume_downloaded=resume_will_download,
                )
            )

            if email_success:

                contact_message.email_sent = True

                contact_message.save(
                    update_fields=["email_sent"]
                )

                if resume_download:

                    resume_download.notification_sent = True

                    resume_download.save(
                        update_fields=[
                            "notification_sent"
                        ]
                    )

            # -------------------------------------------------
            # YES → DOWNLOAD RESUME IMMEDIATELY
            # -------------------------------------------------

            if resume_will_download:

                filename = (
                    resume.resume_file.name
                    .split("/")[-1]
                    .split("\\")[-1]
                )

                if not filename.lower().endswith(".pdf"):
                    filename += ".pdf"

                return FileResponse(
                    resume.resume_file.open("rb"),
                    as_attachment=True,
                    filename=filename,
                    content_type="application/pdf",
                )

            # -------------------------------------------------
            # USER SELECTED YES BUT NO ACTIVE RESUME EXISTS
            # -------------------------------------------------

            if resume_requested and not resume_will_download:

                messages.warning(
                    request,
                    (
                        "Your message was sent successfully, "
                        "but the resume is currently unavailable."
                    ),
                )

            else:

                messages.success(
                    request,
                    "Your message has been sent successfully.",
                )

            return redirect("/#contact")

    else:

        contact_form = ContactForm()

    # =========================================================
    # TEMPLATE CONTEXT
    # =========================================================

    context = {
        "profile": profile,
        "social_links": social_links,
        "experiences": experiences,
        "projects": projects,
        "skills": skills,
        "education": education,
        "training_courses": training_courses,
        "resume": resume,
        "contact_form": contact_form,
    }

    return render(
        request,
        "portfolio/home.html",
        context,
    )


# =============================================================
# DIRECT RESUME DOWNLOAD
# =============================================================
#
# Used by the hero Download Resume button.
#
# Contact form YES:
#     one contact email with Resume Downloaded = YES
#
# Hero download:
#     separate anonymous resume-download email
#
# =============================================================

def download_resume(request, resume_id):

    try:

        resume = Resume.objects.get(
            id=resume_id,
            is_active=True,
        )

    except Resume.DoesNotExist:

        raise Http404(
            "Resume not found."
        )

    if not resume.resume_file:

        raise Http404(
            "Resume file not found."
        )

    # ---------------------------------------------------------
    # LOG DIRECT RESUME DOWNLOAD
    # ---------------------------------------------------------

    resume_download = (
        ResumeDownload.objects.create(
            resume=resume,
            contact_message=None,
        )
    )

    # ---------------------------------------------------------
    # SEND DOWNLOAD NOTIFICATION EMAIL
    # ---------------------------------------------------------

    email_success = (
        send_resume_download_notification(
            resume_download
        )
    )

    if email_success:

        resume_download.notification_sent = True

        resume_download.save(
            update_fields=[
                "notification_sent"
            ]
        )

    # ---------------------------------------------------------
    # PREPARE PDF FILENAME
    # ---------------------------------------------------------

    filename = (
        resume.resume_file.name
        .split("/")[-1]
        .split("\\")[-1]
    )

    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"

    # ---------------------------------------------------------
    # DOWNLOAD PDF
    # ---------------------------------------------------------

    return FileResponse(
        resume.resume_file.open("rb"),
        as_attachment=True,
        filename=filename,
        content_type="application/pdf",
    )


# =============================================================
# ROBOTS.TXT
# =============================================================

def robots_txt(request):

    lines = [
        "User-agent: *",
        "Allow: /",
        (
            f"Sitemap: "
            f"{request.scheme}://"
            f"{request.get_host()}/"
            f"sitemap.xml"
        ),
    ]

    return HttpResponse(
        "\n".join(lines),
        content_type="text/plain",
    )


# =============================================================
# CUSTOM ERROR PAGES
# =============================================================

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