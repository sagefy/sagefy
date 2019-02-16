import React from 'react'
import { Link } from 'react-router-dom'
import Icon from '../components/Icon'

export default function SignUpPage() {
  // TODO if I'm already logged in, redirect instead.
  return (
    <div className="SignUpPage">
      <section>
        <h1>
          Join Sagefy <Icon i="signUp" s="xxl" />
        </h1>

        <p>
          Already have an account?{' '}
          <Link to="/log-in">
            <Icon i="logIn" /> Log In
          </Link>
          .<br />
          By signing up, you agree to our
          <Link to="/terms">
            <Icon i="terms" /> Terms of Service
          </Link>
          .
        </p>

        <form action="" method="POST">
          <p>
            <label htmlFor="name">Name</label>
            <input
              id="name"
              name="name"
              placeholder="example: Unicorn"
              type="text"
              size="40"
              autoFocus
              required
            />
          </p>
          <p>
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              placeholder="example: unicorn@example.com"
              type="email"
              size="40"
              required
            />
            <br />
            <small>
              We need your email to send notices and to reset your password.
            </small>
          </p>
          <p>
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              size="40"
              required
              pattern=".{8,}"
            />
          </p>
          <p>
            <button type="submit">
              <Icon i="signUp" /> Sign Up
            </button>
          </p>
        </form>
      </section>
    </div>
  )
}
