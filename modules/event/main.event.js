const { ipcMain, app } = require("electron")
const { autoUpdater } = require("electron-updater")
const { readFile } = require("fs")
const path = require("path")

const DatabaseLegacy = require("../database/database-legacy")
const { Database } = require("../database/database")

let database = new DatabaseLegacy(".nyanga")
let db2 = Database(".nyanga")

function rendererEventModule(win) {
  // intialize first database
  ipcMain.on("load:check-init", (event) => {
    db2.createIndex({
      index: {
        fields: ["mangaId", "_id"],
        name: "mangadesigndoc",
        type: "json"
      }
    })

    db2.get("appSettings").catch(() => {
      db2
        .put({
          _id: "appSettings",
          lang: {
            langCode: "en",
            langTitle: "english"
          }
        })
        .then(() => {
          let data = {
            reloadRequired: true
          }
          event.sender.send("local:check-init", data)
        })
    })
  })

  ipcMain.on("load:app-full-reload", () => {
    app.relaunch()
    app.quit()
  })

  // event
  ipcMain.on("win:minimize", () => {
    if (!win.isMinimized()) {
      win.minimize()
    }
  })

  ipcMain.on("win:resize", () => {
    if (win.isMaximized()) {
      win.unmaximize()
    } else {
      win.maximize()
    }
  })

  ipcMain.on("win:close", () => {
    win.close()
  })

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

  ipcMain.on("load:app-lang", (event) => {
    // let dbAppSettings = database.getCollection("appSettings")

    db2.get("appSettings").then((data) => {
      // console.log(data.lang)
      event.sender.send("local:app-lang", {
        langCode: data.lang.langCode,
        langTitle: data.lang.langTitle
      })
    })

    // if (dbAppSettings) {
    //   let language = dbAppSettings
    //     .chain()
    //     .find({ settingsID: "language" })
    //     .data({ removeMeta: true })

    //   let data = language[0]
    //   event.sender.send("local:app-lang", data)
    // }
  })

  ipcMain.on("save:app-lang", (event, language) => {
    db2.get("appSettings").then((doc) => {
      return db2.put({
        _id: doc._id,
        _rev: doc._rev,
        lang: language
      })
    })
  })

  ipcMain.on("load:manga-all", (event) => {
    let mangaCollection = database.getCollection("mangaCollection")
    let data = {
      manga: mangaCollection.chain().data({ removeMeta: true }).reverse()
    }

    db2
      .allDocs({
        include_docs: true,
        startkey: "manga-",
        endkey: "manga-\ufff0"
      })
      .then((data) => {
        console.log(data.rows)
      })

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

      if (count > 3) {
        let manga = mangaCollection.chain().data({ removeMeta: true }).reverse()
        let mangaData = manga.slice(0, 3)

        data = {
          manga: mangaData,
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

    db2
      .allDocs({
        include_docs: true,
        startkey: "manga-",
        endkey: "manga-\ufff0"
      })
      .then((data) => {
        console.log(data)

        let manga = []

        for (let doc in data.rows) {
          manga.push({ mangaId: data.rows[doc].doc.mangaId })
        }

        let mangaData = {
          page: data.rows.length > 3 ? true : false,
          manga: manga.slice(0, 3).reverse()
        }

        console.log(mangaData)
      })
  })

  ipcMain.on("save:manga", (event, manga) => {
    // console.log(manga)

    // let mangaCollection = database.getCollection("mangaCollection")
    // let checkMangaId = mangaCollection.findOne({ mangaId: manga.mangaId })
    // if (!checkMangaId) {
    //   mangaCollection.insert(manga)
    //   event.sender.send("manga:saved", "Manga Saved")
    // } else {
    //   event.sender.send("manga:saved", "Manga Already Saved !")
    // }

    db2
      .find({
        selector: { mangaId: { $eq: manga.mangaId } }
      })
      .then((data) => {
        if (data.docs.length === 0) {
          db2
            .put({
              _id: `manga-${new Date().toJSON()}`,
              mangaId: manga.mangaId
            })
            .then(() => {
              event.sender.send("manga:saved", "Manga Saved")
            })
        }

        if (data.docs.length === 1) {
          event.sender.send("manga:saved", "Manga Already Saved !")
        }

        if (data.docs.length > 1) {
          event.sender.send("manga:saved", "Something feels wrong")
        }
      })
  })
}

module.exports = rendererEventModule
