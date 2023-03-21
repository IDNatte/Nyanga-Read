const { ipcMain, app } = require("electron")
const { autoUpdater } = require("electron-updater")
const { readFile } = require("fs")
const path = require("path")

const Database = require("../database/database")

let database = new Database(".nyanga")

function rendererEventModule() {
  ipcMain.on("run:app-apply-update", (event) => {
    autoUpdater.quitAndInstall()
  })

  ipcMain.on("run:app-update", (event) => {
    autoUpdater.checkForUpdates()

    autoUpdater.on("checking-for-update", () => {
      let data = {
        checking: true
      }
      event.sender.send("app:app-update", data)
    })

    autoUpdater.on("update-available", (info) => {
      let data = {
        checking: false,
        info: info,
        status: "update-available"
      }
      event.sender.send("app:app-update", data)
    })

    autoUpdater.on("update-not-available", (info) => {
      let data = {
        checking: false,
        info: info,
        status: "update-unavailable"
      }
      event.sender.send("app:app-update", data)
    })

    autoUpdater.on("error", (err) => {
      let data = {
        checking: false,
        info: err,
        status: "error"
      }
      event.sender.send("app:app-update", data)
    })

    autoUpdater.on("download-progress", () => {
      let data = {
        checking: false,
        info: "downloading update !",
        status: "downloading"
      }
      event.sender.send("app:app-update", data)
    })

    autoUpdater.on("update-downloaded", () => {
      let data = {
        checking: false,
        info: "update downloaded !",
        status: "downloaded"
      }
      event.sender.send("app:app-update", data)
    })
  })

  ipcMain.on("load:app-about", (event) => {
    readFile(
      path.join(__dirname, "../other/docs/about.md"),
      "utf-8",
      (err, data) => {
        if (err) {
          console.log(err)
          event.sender.send("local:app-about", err)
        }

        event.sender.send("local:app-about", {
          about: JSON.stringify(data),
          appVersion: app.getVersion()
        })
      }
    )
  })

  ipcMain.on("load:manga-all", (event) => {
    let mangaCollection = database.getCollection("mangaCollection")
    let data = {
      manga: mangaCollection.chain().data({ removeMeta: true }).reverse()
    }

    event.sender.send("local:manga-load-all", data)
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
