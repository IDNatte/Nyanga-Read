const { ipcMain, app } = require("electron")
const { autoUpdater } = require("electron-updater")
const { readFile } = require("fs")
const path = require("path")

const { Database } = require("../database/database")

let database = Database(".nyanga")

function rendererEventModule(win) {
  // intialize first database
  ipcMain.on("load:check-init", (event) => {
    database.get("appSettings").catch(() => {
      database
        .put({
          _id: "appSettings",
          lang: {
            langCode: "en",
            langTitle: "english"
          }
        })
        .then(() => {
          database.createIndex({
            index: {
              fields: ["bookmark_manga"],
              name: "mangadesigndoc",
              type: "json",
              ddoc: "__mangadesigndoc"
            }
          })

          database.createIndex({
            index: {
              fields: ["lastread_manga"],
              name: "readdesigndoc",
              type: "json",
              ddoc: "__readdesigndoc"
            }
          })

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
    database
      .get("appSettings")
      .then((data) => {
        event.sender.send("local:app-lang", {
          langCode: data.lang.langCode,
          langTitle: data.lang.langTitle
        })
      })
      .catch((error) => {
        let data = {
          reloadRequired: true,
          error: error
        }
        event.sender.send("app:unknown-error", data)
      })
  })

  ipcMain.on("save:app-lang", (event, language) => {
    database
      .get("appSettings")
      .then((doc) => {
        return database.put({
          _id: doc._id,
          _rev: doc._rev,
          lang: language
        })
      })
      .catch((error) => {
        let data = {
          reloadRequired: true,
          error: error
        }
        event.sender.send("app:unknown-error", data)
      })
  })

  ipcMain.on("load:manga-all", (event) => {
    database
      .allDocs({
        include_docs: true,
        startkey: "manga-",
        endkey: "manga-\ufff0"
      })
      .then((data) => {
        let manga = []

        for (let doc in data.rows) {
          manga.push({ mangaId: data.rows[doc].doc.bookmark_manga })
        }

        event.sender.send("local:manga-load-all", manga.reverse())
      })
  })

  ipcMain.on("load:manga", (event) => {
    database
      .allDocs({
        include_docs: true,
        startkey: "manga-",
        endkey: "manga-\ufff0"
      })
      .then((data) => {
        let manga = []

        for (let doc in data.rows) {
          manga.push({ mangaId: data.rows[doc].doc.bookmark_manga })
        }

        let mangaData = {
          page: data.rows.length >= 3 ? true : false,
          manga: manga.reverse().splice(0, 3)
        }

        event.sender.send("local:manga-load", mangaData)
      })
      .catch((error) => {
        let data = {
          reloadRequired: true,
          error: error
        }
        event.sender.send("app:unknown-error", data)
      })
  })

  ipcMain.on("save:manga", (event, manga) => {
    database
      .find({
        selector: { bookmark_manga: { $eq: manga.mangaId } },
        use_index: "__mangadesigndoc"
      })
      .then((data) => {
        if (data.docs.length === 0) {
          database
            .put({
              _id: `manga-${new Date().toJSON()}`,
              bookmark_manga: manga.mangaId
            })
            .then(() => {
              event.sender.send("manga:saved", "Manga Saved")
            })
            .catch((error) => {
              let data = {
                reloadRequired: true,
                error: error
              }
              event.sender.send("app:unknown-error", data)
            })
        }

        if (data.docs.length === 1) {
          event.sender.send("manga:saved", "Manga Already Saved !")
        }

        if (data.docs.length > 1) {
          event.sender.send("manga:saved", "Something feels wrong")
        }
      })
      .catch((error) => {
        let data = {
          reloadRequired: true,
          error: error
        }
        event.sender.send("app:unknown-error", data)
      })
  })

  ipcMain.on("manga:set-last-read", (event, setmanga) => {
    database
      .find({
        selector: { lastread_manga: { $eq: setmanga.manga } },
        use_index: "__readdesigndoc"
      })
      .then((data) => {
        if (data.docs.length === 0) {
          database.put({
            _id: `lastread-${new Date().toJSON()}`,
            lastread_manga: setmanga.manga,
            lastread_chapter: setmanga.chapter,
            lastread_volumeName: setmanga.volumeName,
            lastread_chapterName: setmanga.chapterName
          })
        }

        if (data.docs.length > 0) {
          const lastUpdate = data.docs.length - 1
          database.put({
            _id: data.docs[lastUpdate]._id,
            _rev: data.docs[lastUpdate]._rev,
            lastread_manga: setmanga.manga,
            lastread_chapter: setmanga.chapter,
            lastread_volumeName: setmanga.volumeName,
            lastread_chapterName: setmanga.chapterName
          })
        }
      })
      .catch((error) => {
        let data = {
          reloadRequired: true,
          error: error
        }
        event.sender.send("app:unknown-error", data)
      })
  })

  ipcMain.on("load:manga-last-read", (event, mangaId) => {
    database
      .find({
        selector: { lastread_manga: { $eq: mangaId } },
        use_index: "__readdesigndoc"
      })
      .then((data) => {
        event.sender.send("local:manga-last-read", data.docs[0])
      })
      .catch((error) => {
        let data = {
          reloadRequired: true,
          error: error
        }
        event.sender.send("app:unknown-error", data)
      })
  })
}

module.exports = rendererEventModule
