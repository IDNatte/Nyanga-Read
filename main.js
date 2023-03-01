const { app, BrowserWindow } = require("electron")
const serve = require("electron-serve")

const loadURL = serve({ directory: "layout/build" })

const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600
  })

  if (process.env.APP_DEV) {
    win.loadURL("http://localhost:5173")
  } else {
    loadURL(win)
  }
}

app.whenReady().then(() => {
  createWindow()
})
