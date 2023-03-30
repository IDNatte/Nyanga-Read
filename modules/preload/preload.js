const { contextBridge, ipcRenderer } = require("electron")

contextBridge.exposeInMainWorld("backendAPI", {
  // manga related
  triggerSave: (mangaId) => {
    let manga = {
      mangaId
    }
    ipcRenderer.send("save:manga", manga)
  },

  triggerMangaLoad: () => {
    ipcRenderer.send("load:manga")
  },

  triggerMangaLoadAll: () => {
    ipcRenderer.send("load:manga-all")
  },

  triggerMangaSetLastRead: (manga) => {
    ipcRenderer.send("manga:set-last-read", manga)
  },

  triggerMangaGetLastRead: (manga) => {
    ipcRenderer.send("load:manga-last-read", manga)
  },

  onMangaGetLastRead: (callback) => {
    ipcRenderer.on("local:manga-last-read", callback)
  },

  onMangaSave: (callback) => {
    ipcRenderer.on("manga:saved", callback)
  },

  onMangaLoadAll: (callback) => {
    ipcRenderer.on("local:manga-load-all", callback)
  },

  onMangaLoad: (callback) => {
    ipcRenderer.on("local:manga-load", callback)
  },
  // end of manga related

  // application related

  triggerAppFullReload: () => {
    ipcRenderer.send("load:app-full-reload")
  },

  triggerAppCheckInit: () => {
    ipcRenderer.send("load:check-init")
  },

  onAppCheckInit: (callback) => {
    ipcRenderer.on("local:check-init", callback)
  },

  triggerAppGetLanguage: () => {
    ipcRenderer.send("load:app-lang")
  },

  onGetAppLang: (callback) => {
    ipcRenderer.on("local:app-lang", callback)
  },

  triggerAppSetLanguage: (appLang) => {
    let language = {
      langCode: appLang.code,
      langTitle: appLang.title
    }

    ipcRenderer.send("save:app-lang", language)
  },

  onSetAppLanguage: (callback) => {
    ipcRenderer.on("app-lang:saved", callback)
  },

  triggerAppAbout: () => {
    ipcRenderer.send("load:app-about")
  },

  onAppAbout: (callback) => {
    ipcRenderer.on("local:app-about", callback)
  },

  triggerAppUpdate: () => {
    ipcRenderer.send("run:app-update")
  },

  triggerAppApplyUpdate: () => {
    ipcRenderer.send("run:app-apply-update")
  },

  onAppUpdate: (callback) => {
    ipcRenderer.on("app:app-update", callback)
  },

  triggreWinMinimize: () => {
    ipcRenderer.send("win:minimize")
  },

  triggreWinClose: () => {
    ipcRenderer.send("win:close")
  },

  triggerWinResize: () => {
    ipcRenderer.send("win:resize")
  },

  onAppError: (callback) => {
    ipcRenderer.on("app:unknown-error", callback)
  }

  // end of application related
})
