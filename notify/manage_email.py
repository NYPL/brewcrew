from pdb import set_trace

from django.core.mail import send_mail

from templated_email import get_templated_mail


def send_match_email(user_one, user_two):

    email = get_templated_mail(
        template_name = 'match',
        from_email='brewcrew@nypl.org',
        to=[user_one.email, user_two.email],
        context={
            'name_one' : user_one.name,
            'description_one' : user_one.description,
            'name_two' : user_two.name,
            'description_two' : user_two.description
        }
    )

    send_mail(email.subject, email.body, email.from_email, email.to)
