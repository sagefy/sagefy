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
  ArrowRightCircle,
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
  ThumbsUp,
  List,
  DownloadCloud,
  Users,
  Target,
  ChevronsDown,
  ChevronsUp,
  ChevronsLeft,
  ChevronsRight,
  User,
  MessageSquare,
  AlignLeft,
  Edit,
  Calendar,
  Facebook,
  Twitter,
  Linkedin,
  Heart,
  Star,
  PlusCircle,
} from 'react-feather'
import get from 'lodash.get'

function SagefyIcon({ size = 24 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      className="feather feather-sagefy"
    >
      <circle cx="12" cy="4" r="2" />
      <circle cx="12" cy="14" r="8" />
      <path d="M9.768 14.134l6.062-3.5M8.17 17.366l6.062-3.5" />
      {/* SOURCE -- optimized with svgo
        <g transform="rotate(-30 12 14)">
          <line x1="10" x2="17" y1="13" y2="13" />
          <line x1="7" x2="14" y1="15" y2="15" />
        </g> */}
    </svg>
  )
}

SagefyIcon.propTypes = {
  size: string.isRequired,
}

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
  choice: List,
  page: FileText,
  video: Youtube,
  embed: DownloadCloud,
  child: ChevronsDown,
  parent: ChevronsUp,
  before: ChevronsLeft,
  after: ChevronsRight,
  user: User,
  topic: MessageSquare,
  post: AlignLeft,
  sagefy: SagefyIcon,

  // actions
  select: ArrowRightCircle,
  check: CheckCircle,
  left: ArrowLeft,
  cheer: ThumbsUp,
  create: PlusCircle,
  edit: Edit,
  history: Calendar,
  build: Heart,

  // page specific
  adapt: Share2, // home
  open: Globe, // home
  github: GitHub, // contact
  inbox: Inbox, // password, email
  popular: Users, // home
  facebook: Facebook, // subject complete
  twitter: Twitter, // subject complete
  linkedin: Linkedin, // subject complete
  star: Star, // subject complete
}

const SIZES = {
  s: 14,
  m: 16,
  h3: 16,
  h2: 24,
  h1: 32,
}

export default function Icon({ i, s = 'm', ...props }) {
  return (
    <i className="Icon" {...props}>
      {React.createElement(get(MAP, i, Target), {
        size: get(SIZES, s),
        /* Set in CSS instead */
        fill: undefined,
        stroke: undefined,
        strokeWidth: undefined,
        strokeLinecap: undefined,
        strokeLinejoin: undefined,
        /* Not required for inline SVG https://stackoverflow.com/a/34249810 */
        xmlns: undefined,
      })}
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
