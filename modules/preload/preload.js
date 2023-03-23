const { contextBridge, ipcRenderer } = require("electron")

contextBridge.exposeInMainWorld("backendAPI", {
  // manga save
  triggerSave: (mangaId) => {
    let manga = {
      mangaId
    }
    ipcRenderer.send("save:manga", manga)
  },

  onMangaSave: (callback) => {
    ipcRenderer.on("manga:saved", callback)
  },

  // end of manga save

  // manga load
  triggerMangaLoad: () => {
    ipcRenderer.send("load:manga")
  },

  triggerMangaLoadAll: () => {
    ipcRenderer.send("load:manga-all")
  },

  onMangaLoadAll: (callback) => {
    ipcRenderer.on("local:manga-load-all", callback)
  },

  onMangaLoad: (callback) => {
    ipcRenderer.on("local:manga-load", callback)
  },
  // end of manga load

  // application related
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
  }

  // end of application related
})
