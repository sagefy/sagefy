/* eslint-disable max-len */
const { div, header, h1, a, p, section, h2, h3, ul, li, strong, small, span } = require('../../modules/tags')
const icon = require('../components/icon.tmpl')

module.exports = (data) => {
    const id = data.routeArgs[0]

    if (id !== 'CgDRJPfzJuTR916HdmosA3A8') { return div() }

    const cta = a(
        { href: `/sign_up?subject_id=${id}`, className: 'subjects-landing__cta' },
        icon('sign-up'),
        ' Let\'s Get Learning!'
    )

    const w = n => span({ className: 'subjects-landing__icon-wrap' }, n)

    return div(
        {
            id: 'subjects-landing',
            className: 'page',
        },
        header(
            h1('An Introduction to Electronic Music'),
            p('A small taste of the basics of electronic music. Learn the concepts behind creating and modifying sounds in an electronic music system. Learn the ideas behind the tools and systems we use to create electronic music.'),
            cta
            // TODO-2 social media sharing links
        ),
        section(
            h2('Goals'),
            h3('Who'),
            p('This subject is for anyone who wants to learn the basic ideas of electronic music systems. We will focus on computer-based systems.'),
            h3('Outcome'),
            p('You will be able to explain the basic properties of sound and hearing in a digital system. You\'ll be able to describe the basic tools of creating and modifying sounds. You\'ll have an understanding of some of the systems we use to create and edit electronic music.'),
            p('This subject does not teach how to use a particular piece of software. The ideas here will apply to any software of your choice. This subject does not detail: the artistic study of electronic music, the history of electronic music, or how western music theory applies to electronic music. These are important topics, but outside of the scope of this focused subject.'),
            h3('Requirements'),
            p('This subject does not require extra software. This subject focuses on the what and why, not how. The ideas apply to any electronic music software, such as Pure Data, Audacity, and Ardour. A background in western music theory is not required.'),
            p('A basic understanding of mathematical concepts, such as linear vs logarithmic scale, is helpful. Some physics knowledge is also helpful, but not necessary.'),
            h3('Difficulty'),
            p('Easy. Approximately 5-10 hours in length.'),
            h3('Cost'),
            p('Always free.'),
            cta
        ),
        section(
            h2('About Sagefy'),
            ul(
                { className: 'subjects-landing__about-sagefy' },
                li(w(icon('next')), ' Short, informational videos. Easy to understand.'),
                li(w(icon('learn')), ' Lots of practice questions to help you master the content.'),
                li(w(icon('settings')), ' Sagefy adapts practice questions based on your responses.'),
                li(w(icon('grow')), ' Completely self-paced.'),
                li(w(icon('subject')), ' Choose your own path.'),
                li(w(icon('fast')), ' Skip content you already know.'),
                li(w(icon('post')), ' Get support with our built-in discussions.')
            ),
            cta
        ),
        section(
            h2('What You Will Learn'),
            ul(
                li(
                    h3('Foundation'),
                    ul(
                        li(strong('Electronic Music'), ': Define electronic music and the subjects electronic music covers'),
                        li(strong('Sound Parameters'), ': Describe the basic parameters of sound: amplitude, frequency, duration, phase, and timbre.'),
                        li(strong('Human Hearing'), ': Describe common properties of human hearing, as hearing pertains to electronic music. (Frequency, Amplitude, Spatialization, Hidden Fundamental...)'),
                        li(strong('Hearing Curves'), ': Describe how hearing varies with frequency and amplitude.'),
                        li(strong('Digital Representation'), ': Describe how we represent sound digitally, including bit depth and sample rate.'),
                        li(strong('Analog to Digital'), ': Describe how we convert analog sound into digital sound. (Recording, Nyquist)'),
                        li(strong('Complex Waves'), ': Describe the composition of complex sounds.')
                    )
                ),
                li(
                    h3('Creating Sound'),
                    ul(
                        li(strong('Oscillators'), ': Describe the oscillators and basic wave forms: sine, triangle, square, and sawtooth.'),
                        li(strong('Noise'), ': Describe the types of noise: white, brown, and pink.'),
                        li(strong('Additive Synthesis'), ': Describe how multiple waves produce a single sound.'),
                        li(strong('Subtractive Synthesis'), ': Describe how we can subtract information to produce sound.'),
                        li(strong('Samplers'), ': Describe samplers.')
                    )
                ),
                li(
                    h3('Changing Sound'),
                    ul(
                        li(strong('Filters'), ': Describe the basic types of filters: low-pass, high-pass, band-reject, and band-pass.'),
                        li(strong('Modulation'), ': Describe modulation of sound signals.'),
                        li(strong('Low Frequency Oscillators'), ': Describe low-frequency oscillators.'),
                        li(strong('Modulation Effects'), ': Describe modulation effects: tremolo, chorus, flange, phase, vibrato.'),
                        li(strong('Amplitude Modifiers'), ': Describe the basic characteristics of amplitude modifiers: gain, compressors, de-essers, expanders, multi-pressors.'),
                        li(strong('Envelopes'), ': Describe how amplitude changes over time (generators: envelopes).'),
                        li(strong('Equalization'), ': Describe equalizers.'),
                        li(strong('Distortion'), ': Describe distortion and applying the effect to a signal.'),
                        li(strong('Delay'), ': Describe delay effects.'),
                        li(strong('Reverberation'), ': Describe reverberation effects.')
                    )
                ),
                li(
                    h3('Complex Techniques'),
                    ul(
                        li(strong('Fast Fourier Transform'), ': Describe the inputs, outputs, and applications of the Fast Fourier Transform.'),
                        li(strong('Spatialization'), ': Describe acoustic panning and spatialization.'),
                        li(strong('Frequency Modulation Synthesis'), small(' Coming soon!'), ': Describe frequency modulation (FM) synthesis.'),
                        li(strong('Granular Synthesis'), small(' Coming soon!'), ': Describe granular synthesis.'),
                        li(strong('Formant Synthesis'), small(' Coming soon!'), ': Describe formant synthesis.'),
                        li(strong('Physical Modeling'), small(' Coming soon!'), ': Describe physical modeling.'),
                        li(strong('Convolution'), small(' Coming soon!'), ': Describe convolution.'),
                        li(strong('Vocoding'), small(' Coming soon!'), ': Describe vocoding.')
                    )
                ),
                li(
                    h3('Systems'),
                    ul(
                        li(strong('Basic Synthesizer'), ': Describe a basic synthesizer configuration.'),
                        li(strong('Mixers'), ': Describe a mixer.'),
                        li(strong('Monophony and Polyphony'), ': Describe polyphonic synthesis.'),
                        li(strong('Musical Instrument Digital Interface'), ': Describe the basics of the MIDI protocol.'),
                        li(strong('Open Sound Control'), ': Describe the basics of the OSC protocol.')
                    )
                )
            ),
            cta
        ),
        section(
            h2('About the Instructor'),
            p('I am Kevin Heis, the founder of Sagefy. I\'m interested in real-time, algorithmic electronic music for performance and installation. I hold a Master\'s in Intermedia Music Technology from the University of Oregon. But more important, I love learning. I love to support others\' learning goals too!'),
            cta
        )
        // TODO-3 testimonals/reviews (rating)
    )
}
