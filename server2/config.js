// Nota bene: For production empty this file.
//            Then copy and paste config.prod.js into this file instead.
//            Then update indicated fields.

/* eslint-disable global-require */

const baseConfig = {
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
  es: {
    host: 'elasticsearch:9200',
  },
}

if (process.env.TRAVIS) {
  module.exports = {
    ...baseConfig,
    pg: {
      host: 'localhost',
      database: 'postgres',
      user: 'postgres',
      port: 5432,
    },
    debug: true,
    test: true,
  }
} else if (process.env.NODE_ENV === 'test') {
  module.exports = {
    ...baseConfig,
    pg: {
      host: 'postgres-test',
      database: 'test',
      user: 'test',
      port: 5432,
    },
    debug: true,
    test: true,
  }
} else {
  module.exports = {
    ...baseConfig,
    pg: {
      host: 'postgres',
      database: 'sagefy',
      user: 'sagefy',
      port: 5432,
    },
    debug: true,
    test: false,
  }
}
