const { ipcMain } = require("electron")
const Database = require("../database/database")

let database = new Database(".nyanga")

function rendererEventModule() {
  ipcMain.on("load:manga-all", (event) => {
    console.log("request to load all manga")
    let mangaCollection = database.getCollection("mangaCollection")
    data = {
      manga: mangaCollection.chain().data({ removeMeta: true }).reverse()
    }

    console.log(data)
    event.sender.send("local:manga-load-all", "pong")
  })

  ipcMain.on("load:manga", (event) => {
    let mangaCollection = database.getCollection("mangaCollection")

    let checkCollection = database
      .listCollection()
      .find(({ name }) => name === "mangaCollection")

    if (checkCollection) {
      let count = mangaCollection.count()
      let data

      // debug manga count
      if (count > 3) {
        data = {
          manga: mangaCollection
            .chain()
            .limit(3)
            .data({ removeMeta: true })
            .reverse(),
          page: true
        }
      } else {
        data = {
          manga: mangaCollection.chain().data({ removeMeta: true }).reverse(),
          page: false
        }
      }
      event.sender.send("local:manga-load", data)
    } else {
      let data = {
        manga: [],
        page: false
      }

      event.sender.send("local:manga-load", data)
    }
  })

  // ipcMain.on("load:manga", (event) => {
  //   let checkCollection = database
  //     .listCollection()
  //     .find(({ name }) => name === "mangaCollection")

  //   if (checkCollection) {
  //     let mangaCollection = database.getCollection("mangaCollection")
  //     let count = mangaCollection.count()
  //     let data

  //     // debug manga count
  //     if (count > 3) {
  //       data = {
  //         manga: mangaCollection.chain().data({ removeMeta: true }).reverse(),
  //         paged: true
  //       }
  //     } else {
  //       data = {
  //         manga: mangaCollection.chain().data({ removeMeta: true }).reverse(),
  //         paged: true
  //       }
  //     }
  //     event.sender.send("local:manga-load", data)
  //   } else {
  //     let mangaCollection = database.createCollection("mangaCollection")
  //     let data = mangaCollection.chain().data({ removeMeta: true })
  //     event.sender.send("local:manga-load", data)
  //   }
  // })

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
