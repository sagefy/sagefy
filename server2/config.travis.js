module.exports = {
  debug: true,
  test: true,
  session: {
    secret: '5e8a2787c3824fe788bebc685787c6e4',
  },
  mail: {
    sender: 'support@sagefy.org',
    password: 'wW6Yd6jJHBVilJHX',
    username: 'SMTP_Injection',
    server: 'smtp.sparkpostmail.com',
    port: 587,
    alert: 'support@sagefy.org',
  },
  redis: {
    host: 'redis',
    port: 6379,
    logErrors: true,
  },
  pg: {
    host: 'localhost',
    database: 'postgres',
    user: 'postgres',
    port: 5432,
  },
  es: {
    host: 'elasticsearch',
    port: 9200,
  },
}
