import React from 'react'
import { string } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Icon from './Icon'

const SKIPLIST = [
  'EU7YbwNsNzChujKZ1tt2Nx',
  '7LwhvLeJieWKhtbf1gwbrz',
  'Ly9ud9qwF5YtChwME1WVSz',
  'UuJf1CPiH8Nwp9TiGM9LaY',
  'YSU8p5GM5cF6GoU2XQacKa',
  '5J7ugiWCDrCMFrjLtctoz4',
  '6WHomZbepJtmvZt5hK9891',
  '7txPzd2aeaZceAefUeqqFb',
  '9iW9Nny13ntVgjZ1qRGLNH',
  'AZCm5r1kBFc97rMo9G1n1N',
  'SzKHxCThj3JgrYXtGsR3Ar',
  'XB5n8epNnefnwBQ7qApZS6',
  'CDfeHFEkNLsEupxHzSK6h3',
  'Diz8Vk1hTSz45x4fXQu5mA',
  'EJxduGmbZ2kEAkMfQD78s8',
  'GKLyQogbrRVq8Ji5LFfEGu',
  'KvPKVJCctfLsBd67ZjkjNw',
  'NPo3dbodZcH2oL55by8psj',
  'WxhRFu3k6EQkp9Dc5FZWSZ',
  'XMAonC2As1vfAiNyTzGAeb',
  'YPKM6hCssGm8N5GFKZAfM3',
  'Yah4rhoE8ckasNeku9LTSm',
  'DtRJb9heB6DiepNErzVP4X',
  'LKH6MZAN8J2wEQPaeje9VK',
  'LVLJM6zi4djZxhGAVRzs4D',
  'LrkaKqFXM2C9XWt8xpHnr4',
  'QYp6WJEwdQyQ9v1SAUVTEy',
  'WoFwLQ4CfsDmZ1dR22N7M2',
  'XningXkhfKQ3hiNUQgZCsY',
  '2SK9mcmzCaSKduWXnnfPLE',
  '3hiAG3TNjbYuBB3knYyZXk',
  'DnkiX8TTb14in3hhs8gM4V',
  'FUnq8iaot6fqKTRXkpzcbQ',
  'StX6iaDNmff9AEEoqb7pgM',
  'W9UmrCsnrmgPvwp8mQRuoc',
]

export default function TempHelp({ name, cardId, subjectId }) {
  if (SKIPLIST.includes(to58(subjectId)) || !name || !cardId) return <></>
  return (
    <section>
      <hr />
      <p>
        <small>
          Sagefy currently shows computer-made examples of many subjects. <br />
          <Icon i="help" s="s" /> If you want to learn about <q>{name}</q> and
          help others learn too,{' '}
          <a
            href={`/cards/${to58(cardId)}/edit?redirect=/cards/${to58(
              cardId
            )}/learn`}
          >
            <Icon i="build" s="s" /> help us by editing!
          </a>
        </small>
      </p>
    </section>
  )
}

TempHelp.propTypes = {
  name: string.isRequired,
  cardId: string.isRequired,
  subjectId: string.isRequired,
}
