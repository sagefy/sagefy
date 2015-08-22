# TODO move copy to content directory
{div, h1, pre} = require('../../modules/tags')

terms = """
By using Sagefy, you agree to these terms.

This statement is effective as of February 1, 2015.

Sagefy may change this document at any time without notice.

SAGEFY IS PROVIDED AS-IS AND AS-AVAILABLE.
SAGEFY MAKES NO WARRANTIES.
SAGEFY DOES NOT OFFER WARRANTIES ON MERCHANTABILITY,
FITNESS FOR A PARTICULAR USE,
OR NON-INFRINGEMENT OF INTELLECTUAL PROPERTY.

SAGEFY IS NOT LIABLE FOR ANY DAMAGES COMING FROM USE OF SAGEFY.

Sagefy may contact you by your provided email address.

Sagefy may use cookies to keep you logged in and to personalize the service.

Sagefy may collect personally identifying information to provide services.

Sagefy may send personally identifying information to trusted
affiliates, such as Google Analytics and UserVoice.

Sagefy may disclose information to law enforcement without notice
    a) if required by law,
    b) to defend Sagefy's rights and property, or
    c) to ensure personal safety or public safety.

You cannot spam to other users of Sagefy.
You cannot impersonate any person or entity on Sagefy.
You cannot defame, harrass, abuse, threaten, or defraud
other users of Sagefy.
You cannot use Sagefy to collect information
about other users without their consent.

You cannot share a single account with multiple people.
You cannot make or use more than one account.

If you are under the age of thirteen,
you must ask a parent or guardian before using Sagefy.

You cannot interfere with security features of Sagefy.
You cannot interfere with any other user's use of Sagefy.
You cannot use any sort of automated means to access Sagefy.
You cannot bypass measures to restrict access to Sagefy.

You are solely responsible for maintaining
the confidentiality of your account and any passwords or tokens.
Sagefy is not liable for any damages resulting from
unauthorized use of your account.

Sagefy may close accounts and cancel service
in Sagefy's sole discretion.

By providing content to Sagefy, you agree you own the rights
to the content and the legal ability to provide the content.
By providing content to Sagefy, Sagefy may use this content.
No compensation will be given for user-provided content.

Sagefy may update and remove user-submitted content,
but Sagefy does not make any commitment to update content.

Sagefy is not responsible for content or agreements on
external websites, even if Sagefy links to them.

If your copyright, patent, or trademark has been violated, contact
support@sagefy.org.
Notices and counter-notices must meet statutory requirements
imposed by the Digital Millennium Copyright Act of 1998.
"""

module.exports = ->
    return div(
        {id: 'terms', className: 'col-10'}
        [
            h1('Sagefy Privacy Policy & Terms of Service')
            pre(terms)
        ]
    )
