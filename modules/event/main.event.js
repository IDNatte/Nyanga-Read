const { ipcMain } = require("electron")
const Database = require("../database/database")

let database = new Database(".nyanga")

function rendererEventModule() {
  ipcMain.on("load:manga", (event) => {
    let checkCollection = database
      .listCollection()
      .find(({ name }) => name === "mangaCollection")

    if (checkCollection) {
      let mangaCollection = database.getCollection("mangaCollection")
      let data = mangaCollection.chain().data()
      event.sender.send("local:manga-load", data)
    } else {
      let mangaCollection = database.createCollection("mangaCollection")
      let data = mangaCollection.chain().data()
      event.sender.send("local:manga-load", data)
    }
  })

  ipcMain.on("save:manga", (event, manga) => {
    let mangaCollection = database.getCollection("mangaCollection")
    let checkMangaId = mangaCollection.findOne({ mangaId: manga.mangaId })
    if (!checkMangaId) {
      mangaCollection.insert(manga)
      event.sender.send("manga:saved", "Manga Saved")
    } else {
      event.sender.send("manga:saved", "Manga Already Saved !")
    }
  })
}

module.exports = rendererEventModule
