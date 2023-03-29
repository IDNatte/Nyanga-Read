const pouch = require("pouchdb")
const path = require("path")
const fs = require("fs")
const os = require("os")
pouch.plugin(require("pouchdb-adapter-node-websql"))

class DatabaseTest {
  constructor(filepath) {
    this.databasePath = path.join(os.homedir(), filepath)
    try {
      fs.readdirSync(this.databasePath)
      this.database = new pouch(
        path.join(this.databasePath, "nyangaread.database.db"),
        { adapter: "websql" }
      )
    } catch {
      fs.mkdirSync(this.databasePath, { recursive: true })
      this.database = new pouch(
        path.join(this.databasePath, "nyangaread.database.db"),
        { adapter: "websql" }
      )
    }
  }

  getInfo() {
    return this.database.info()
  }
}

module.exports = DatabaseTest
