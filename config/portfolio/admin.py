from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Profile,
    SocialLink,
    Experience,
    Project,
    Skill,
    Education,
    TrainingCourse,
    Resume,
    ContactMessage,
)


# =========================================================
# PROFILE
# =========================================================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "professional_title",
        "email",
        "profile_thumbnail",
        "is_active",
        "updated_at",
    )

    search_fields = (
        "full_name",
        "professional_title",
        "email",
        "location",
    )

    list_filter = (
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    readonly_fields = (
        "profile_image_preview",
        "updated_at",
    )

    ordering = (
        "full_name",
    )

    def profile_thumbnail(self, obj):

        if obj.profile_image:

            return format_html(
                '<img src="{}" '
                'style="width:45px;height:45px;'
                'object-fit:cover;border-radius:50%;" />',
                obj.profile_image.url,
            )

        return "-"

    profile_thumbnail.short_description = "Photo"


    def profile_image_preview(self, obj):

        if obj.profile_image:

            return format_html(
                '<img src="{}" '
                'style="max-width:250px;'
                'border-radius:12px;" />',
                obj.profile_image.url,
            )

        return "No image uploaded"

    profile_image_preview.short_description = "Profile Preview"



# =========================================================
# SOCIAL LINKS
# =========================================================

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):

    list_display = (
        "platform",
        "display_name",
        "link_preview",
        "display_order",
        "is_active",
    )

    list_filter = (
        "platform",
        "is_active",
    )

    search_fields = (
        "platform",
        "display_name",
        "url",
    )

    list_editable = (
        "display_order",
        "is_active",
    )

    ordering = (
        "display_order",
        "id",
    )

    def link_preview(self, obj):

        return format_html(
            '<a href="{}" target="_blank">'
            '<i>Open Link</i>'
            '</a>',
            obj.url,
        )

    link_preview.short_description = "Link"



# =========================================================
# EXPERIENCE
# =========================================================

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):

    list_display = (
        "job_title",
        "company_name",
        "start_date",
        "end_date",
        "currently_working",
        "display_order",
        "is_active",
    )

    search_fields = (
        "job_title",
        "company_name",
        "location",
        "description",
    )

    list_filter = (
        "currently_working",
        "is_active",
        "start_date",
    )

    list_editable = (
        "display_order",
        "is_active",
    )

    ordering = (
        "display_order",
        "-start_date",
    )



# =========================================================
# PROJECTS
# =========================================================

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "project_thumbnail",
        "title",
        "featured",
        "github_link",
        "demo_link",
        "display_order",
        "is_active",
        "updated_at",
    )

    search_fields = (
        "title",
        "short_description",
        "full_description",
        "technologies",
    )

    list_filter = (
        "featured",
        "is_active",
        "created_at",
    )

    list_editable = (
        "featured",
        "display_order",
        "is_active",
    )

    readonly_fields = (
        "project_image_preview",
        "created_at",
        "updated_at",
    )

    ordering = (
        "display_order",
        "-created_at",
    )


    def project_thumbnail(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" '
                'style="width:70px;height:45px;'
                'object-fit:cover;border-radius:6px;" />',
                obj.image.url,
            )

        return "-"

    project_thumbnail.short_description = "Image"


    def project_image_preview(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" '
                'style="max-width:350px;'
                'border-radius:12px;" />',
                obj.image.url,
            )

        return "No image uploaded"

    project_image_preview.short_description = "Project Preview"


    def github_link(self, obj):

        if obj.github_url:

            return format_html(
                '<a href="{}" '
                'target="_blank" '
                'rel="noopener noreferrer">'
                'GitHub'
                '</a>',
                obj.github_url,
            )

        return "-"

    github_link.short_description = "GitHub"


    def demo_link(self, obj):

        if obj.demo_url:

            return format_html(
                '<a href="{}" '
                'target="_blank" '
                'rel="noopener noreferrer">'
                'Live Demo'
                '</a>',
                obj.demo_url,
            )

        return "-"

    demo_link.short_description = "Demo"



# =========================================================
# SKILLS
# =========================================================

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "skills_preview",
        "display_order",
        "is_active",
    )

    search_fields = (
        "title",
        "skills",
    )

    list_editable = (
        "display_order",
        "is_active",
    )

    ordering = (
        "display_order",
        "title",
    )

    @admin.display(
        description="Skills"
    )
    def skills_preview(self, obj):

        if len(obj.skills) > 80:
            return obj.skills[:80] + "..."

        return obj.skills

# =========================================================
# EDUCATION
# =========================================================

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):

    list_display = (
        "degree",
        "institution",
        "field_of_study",
        "start_date",
        "end_date",
        "display_order",
        "is_active",
    )

    search_fields = (
        "degree",
        "institution",
        "field_of_study",
        "description",
    )

    list_filter = (
        "is_active",
        "start_date",
    )

    list_editable = (
        "display_order",
        "is_active",
    )

    ordering = (
        "display_order",
        "-start_date",
    )
    
# =========================================================
# RESUME
# =========================================================

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "resume_download",
        "is_active",
        "uploaded_at",
    )

    list_filter = (
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    readonly_fields = (
        "uploaded_at",
    )

    ordering = (
        "-uploaded_at",
    )


    def resume_download(self, obj):

        if obj.resume_file:

            return format_html(
                '<a href="{}" '
                'target="_blank">'
                'View Resume'
                '</a>',
                obj.resume_file.url,
            )

        return "-"

    resume_download.short_description = "Resume"



# =========================================================
# CONTACT MESSAGES
# =========================================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "sender_name",
        "sender_email",
        "subject",
        "created_at",
        "is_read",
        "email_sent",
    )

    list_filter = (
        "is_read",
        "email_sent",
        "created_at",
    )

    search_fields = (
        "sender_name",
        "sender_email",
        "subject",
        "message",
    )

    readonly_fields = (
        "sender_name",
        "sender_email",
        "subject",
        "message",
        "created_at",
        "email_sent",
    )

    ordering = (
        "-created_at",
    )
    

#courses
@admin.register(TrainingCourse)
class TrainingCourseAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "provider",
        "status",
        "display_order",
        "is_active",
    )

    search_fields = (
        "title",
        "provider",
        "topics",
    )

    list_filter = (
        "status",
        "is_active",
    )

    list_editable = (
        "display_order",
        "is_active",
    )

    ordering = (
        "display_order",
        "title",
    )
    



admin.site.site_header = "Portfolio Administration"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Portfolio Content Management"