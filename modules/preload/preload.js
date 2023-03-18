const { contextBridge, ipcRenderer } = require("electron")

contextBridge.exposeInMainWorld("backendAPI", {
  triggerSave: () => ipcRenderer.invoke("save:manga")
})
