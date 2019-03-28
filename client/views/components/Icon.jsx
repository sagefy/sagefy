import React from 'react'
import { string } from 'prop-types'
import {
  Home,
  Briefcase,
  Search,
  Share2,
  Globe,
  Youtube,
  BookOpen,
  Gift,
  Inbox,
  Mail,
  MessageCircle,
  GitHub,
  Frown,
  ThumbsUp,
  ThumbsDown,
  CheckCircle,
  Tag,
  FileText,
  UserPlus,
  LogIn,
  ArrowLeft,
  Settings,
  LogOut,
  Key,
  Map,
  // temporary home page
  Users,
  Eye,
  // default so I see somethings off
  Target,
} from 'react-feather'
import get from 'lodash.get'

const MAP = {
  // pages
  home: Home,
  terms: Briefcase,
  search: Search,
  docs: BookOpen,
  stories: Gift,
  updates: Inbox,
  contact: Mail,
  signUp: UserPlus,
  logIn: LogIn,
  settings: Settings,
  logOut: LogOut,
  password: Key,
  email: Mail,
  dashboard: Map,

  // models
  talk: MessageCircle,
  error: Frown,
  subject: Tag,
  card: FileText,

  // actions
  select: ThumbsUp,
  check: CheckCircle,
  left: ArrowLeft,

  // page specific
  adapt: Share2, // home
  open: Globe, // home
  video: Youtube, // home
  view: Eye, // home
  friends: Users, // home
  github: GitHub, // contact
  inbox: Inbox, // password, email
  popular: Users, // home
}

const SIZES = {
  s: 14,
  m: 16,
  l: 16,
  xl: 24,
  xxl: 32,
}

export default function Icon({ i, s = 'm' }) {
  return (
    <i className={`Icon icon-${i}`}>
      {React.createElement(get(MAP, i, Target), { size: get(SIZES, s) })}
    </i>
  )
}

Icon.propTypes = {
  i: string.isRequired,
  s: string,
}

Icon.defaultProps = {
  s: 'm',
}
