import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import escape, linebreaks

logger = logging.getLogger(__name__)


def _build_email_card(title_badge, heading, body_table_rows, message_box=None, meta_footer="Portfolio Dispatch Engine"):
    """
    Renders a clean, high-contrast light mode card compatible across all email clients.
    """
    message_html = ""
    if message_box:
        message_html = f"""
        <tr>
            <td style="padding: 0 32px 24px 32px;">
                <div style="background-color: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #4f46e5; padding: 18px 20px;">
                    <div style="font-family: 'Courier New', Courier, monospace; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #4f46e5; margin-bottom: 8px; font-weight: 700;">
                        // MESSAGE_CONTENT
                    </div>
                    <div style="font-size: 14px; line-height: 1.6; color: #334155; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
                        {message_box}
                    </div>
                </div>
            </td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{heading}</title>
</head>
<body style="margin: 0; padding: 32px 12px; background-color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(15, 23, 42, 0.06);">
        <!-- CARD HEADER -->
        <tr>
            <td style="padding: 30px 32px 20px 32px; background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%); border-bottom: 1px solid #e2e8f0;">
                <div style="display: inline-block; padding: 4px 12px; border-radius: 999px; background-color: #e0e7ff; border: 1px solid #c7d2fe; font-family: 'Courier New', Courier, monospace; font-size: 11px; font-weight: 700; color: #4338ca; text-transform: uppercase; margin-bottom: 10px;">
                    {title_badge}
                </div>
                <h1 style="margin: 0; font-size: 22px; font-weight: 800; color: #0f172a; letter-spacing: -0.02em;">
                    {heading}
                </h1>
            </td>
        </tr>

        <!-- METADATA ROWS -->
        <tr>
            <td style="padding: 24px 32px 12px 32px;">
                <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                    {body_table_rows}
                </table>
            </td>
        </tr>

        <!-- MESSAGE CONTENT BOX -->
        {message_html}

        <!-- FOOTER -->
        <tr>
            <td style="padding: 16px 32px; background-color: #f8fafc; border-top: 1px solid #f1f5f9; text-align: center;">
                <span style="font-family: 'Courier New', Courier, monospace; font-size: 11px; color: #64748b;">
                    {meta_footer}
                </span>
            </td>
        </tr>
    </table>
</body>
</html>"""


def _build_meta_row(label, value, is_highlight=False, highlight_color="#15803d", highlight_bg="#dcfce7"):
    """
    Renders clean light mode metadata rows.
    """
    val_style = "font-size: 14px; font-weight: 600; color: #0f172a;"
    if is_highlight:
        val_style = f"display: inline-block; font-size: 12px; font-weight: 700; color: {highlight_color}; background-color: {highlight_bg}; padding: 3px 8px; border-radius: 6px; font-family: 'Courier New', Courier, monospace;"

    return f"""
    <tr>
        <td style="padding: 7px 0; width: 130px; font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; font-family: 'Courier New', Courier, monospace; vertical-align: top;">
            {label}
        </td>
        <td style="padding: 7px 0; {val_style}">
            {value}
        </td>
    </tr>
    """


def send_contact_notification(contact_message, resume_downloaded=False):
    """
    Dispatches a clean light-mode email notification for contact inquiries.
    """
    resume_status_text = "YES" if resume_downloaded else "NO"
    status_color = "#15803d" if resume_downloaded else "#64748b"
    status_bg = "#dcfce7" if resume_downloaded else "#f1f5f9"

    name = escape(contact_message.sender_name)
    email = escape(contact_message.sender_email)
    subject_text = escape(contact_message.subject or "Direct Inquiry")
    message_content = linebreaks(escape(contact_message.message))

    subject = f"Portfolio Inquiry: {contact_message.sender_name}"

    text_body = f"""[PORTFOLIO CONTACT DISPATCH]

Sender Name : {contact_message.sender_name}
Sender Email: {contact_message.sender_email}
Subject     : {contact_message.subject or 'No subject specified'}
Resume Req. : {resume_status_text}

Message:
--------------------------------------------------
{contact_message.message}
--------------------------------------------------
"""

    rows = (
        _build_meta_row("Sender", name) +
        _build_meta_row("Email", f"<a href='mailto:{email}' style='color: #4f46e5; text-decoration: none; font-weight: 600;'>{email}</a>") +
        _build_meta_row("Subject", subject_text) +
        _build_meta_row("Resume Req.", resume_status_text, is_highlight=True, highlight_color=status_color, highlight_bg=status_bg)
    )

    html_body = _build_email_card(
        title_badge="./incoming_message",
        heading="New Contact Inbound",
        body_table_rows=rows,
        message_box=message_content,
        meta_footer="Automated Portfolio Notification"
    )

    try:
        mail = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.NOTIFICATION_EMAIL],
            reply_to=[contact_message.sender_email],
        )
        mail.attach_alternative(html_body, "text/html")
        mail.send()
        return True
    except Exception as error:
        logger.error(f"Contact email dispatch failure: {error}")
        return False


def send_resume_download_notification(resume_download):
    """
    Dispatches a clean light-mode notification when a resume is downloaded.
    """
    contact = resume_download.contact_message
    download_time = resume_download.downloaded_at.strftime("%b %d, %Y — %I:%M %p")
    resume_title = escape(resume_download.resume.title)

    if contact:
        subject = f"Resume Downloaded: {contact.sender_name}"
        name = escape(contact.sender_name)
        email = escape(contact.sender_email)
        subject_text = escape(contact.subject or "No subject")
        message_content = linebreaks(escape(contact.message))

        text_body = f"""[RESUME DOWNLOAD EVENT]

Resume Title : {resume_download.resume.title}
Downloaded At: {download_time}
Associated Contact: YES

Name : {contact.sender_name}
Email: {contact.sender_email}
Subject: {contact.subject or 'No subject'}

Message:
--------------------------------------------------
{contact.message}
--------------------------------------------------
"""

        rows = (
            _build_meta_row("Document", resume_title) +
            _build_meta_row("Timestamp", download_time) +
            _build_meta_row("Sender", name) +
            _build_meta_row("Email", f"<a href='mailto:{email}' style='color: #4f46e5; text-decoration: none; font-weight: 600;'>{email}</a>") +
            _build_meta_row("Subject", subject_text)
        )

        html_body = _build_email_card(
            title_badge="./resume_event",
            heading="Resume Downloaded with Inquiry",
            body_table_rows=rows,
            message_box=message_content,
            meta_footer="Portfolio Analytics Engine"
        )
        reply_to = [contact.sender_email]

    else:
        subject = f"Portfolio Resume Downloaded: {resume_download.resume.title}"

        text_body = f"""[RESUME DOWNLOAD EVENT]

Resume Title : {resume_download.resume.title}
Downloaded At: {download_time}
Visitor Type : Anonymous Visitor
"""

        rows = (
            _build_meta_row("Document", resume_title) +
            _build_meta_row("Timestamp", download_time) +
            _build_meta_row("Visitor", "Anonymous Visitor", is_highlight=True, highlight_color="#0284c7", highlight_bg="#e0f2fe")
        )

        html_body = _build_email_card(
            title_badge="./direct_download",
            heading="Resume Downloaded",
            body_table_rows=rows,
            message_box=None,
            meta_footer="Direct Asset Download Notification"
        )
        reply_to = None

    try:
        mail = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.NOTIFICATION_EMAIL],
            reply_to=reply_to,
        )
        mail.attach_alternative(html_body, "text/html")
        mail.send()
        return True
    except Exception as error:
        logger.error(f"Resume notification email dispatch failure: {error}")
        return False