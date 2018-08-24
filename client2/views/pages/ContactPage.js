import React from 'react'

const uvUrl = 'https://sgef.cc/feedback'

export default function ContactPage() {
  return (
    <div id="contact" className="page">
      <h1>Contact Sagefy</h1>
      <ul>
        <li>
          <strong>I have a problem with content.</strong>
          <br />Discuss it in the site, or propose removing it.
        </li>
        <li>
          <strong>I have an idea for content.</strong>
          <br />Discuss it in the site.
        </li>
        <li>
          <strong>I have an idea for the software.</strong>
          <br />Add it to our <a href={uvUrl}>feedback forum.</a>
        </li>
        <li>
          <strong>I found a bug.</strong>
          <br />Add to{' '}
          <a href="https://github.com/heiskr/sagefy/issues">Github issues</a>.
          For security issues,{' '}
          <a href="mailto:support@sagefy.org">send us an email</a>.
        </li>
        <li>
          <strong>My copyright has been violated.</strong>
          <br />
          <a href="mailto:support@sagefy.org">Send us an email</a>.
        </li>
        <li>
          <strong>I need help with my account.</strong>
          <br />
          <a href="mailto:support@sagefy.org">Send us an email</a>.
        </li>
      </ul>
    </div>
  )
}
