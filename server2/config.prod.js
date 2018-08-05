module.exports = {
  debug: false,
  test: false,
  session: {
    secret: '___ UPDATE ME ___',
  },
  mail: {
    pool: true,
    secure: true,
    host: 'smtp.sparkpostmail.com',
    port: 587,
    auth: {
      user: 'SMTP_Injection',
      pass: '___ UPDATE ME ___',
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
