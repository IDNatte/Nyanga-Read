const PouchDB = require("pouchdb")
const path = require("path")
const os = require("os")

PouchDB.plugin(require("pouchdb-adapter-node-websql"))
PouchDB.plugin(require("pouchdb-find"))

function Database(filepath) {
  const databasePath = path.join(os.homedir(), filepath)

  const database = new PouchDB(
    path.join(databasePath, "nyangaread.database.db"),
    { adapter: "websql", auto_compaction: true }
  )

  return database
}

module.exports = {
  Database
}
