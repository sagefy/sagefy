module.exports = function indexRoutes(app) {
  app.get('/x', (req, res) =>
    res.json({ message: 'Welcome to the Sagefy service!' })
  )

  return app
}
