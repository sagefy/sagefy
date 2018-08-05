module.exports = {
  debug: false,
  test: false,
  session: {
    secret: '5e8a2787c3824fe788bebc685787c6e4',
  },
  mail: {
    pool: true,
    secure: true,
    host: 'smtp.sparkpostmail.com',
    port: 587,
    auth: {
      user: 'SMTP_Injection',
      pass: 'wW6Yd6jJHBVilJHX',
    },
  },
  redis: {
    host: 'redis',
    port: 6379,
    logErrors: true,
  },
  pg: {
    host: 'postgres',
    database: 'sagefy',
    user: 'sagefy',
    port: 5432,
  },
  es: {
    host: 'elasticsearch',
    port: 9200,
  },
}
