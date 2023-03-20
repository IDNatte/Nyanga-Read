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

  // end of manga load
  triggerMangaLoad: () => {
    ipcRenderer.send("load:manga")
  },

  onMangaLoad: (callback) => {
    ipcRenderer.on("local:manga-load", callback)
  }
  // end of manga load
})
