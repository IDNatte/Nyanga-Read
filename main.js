const { app, BrowserWindow } = require("electron")
const serve = require("electron-serve")
const path = require("path")

const eventHandle = require("./modules/event/main.event")
const loadURL = serve({ directory: "layout/build" })

function UpsertKeyValue(obj, keyToChange, value) {
  const keyToChangeLower = keyToChange.toLowerCase()
  for (const key of Object.keys(obj)) {
    if (key.toLowerCase() === keyToChangeLower) {
      // Reassign old key
      obj[key] = value
      // Done
      return
    }
  }
  // Insert at end instead
  obj[keyToChange] = value
}

const createWindow = () => {
  const win = new BrowserWindow({
    width: 1024,
    minWidth: 1024,
    height: 700,
    minHeight: 700,
    autoHideMenuBar: true,
    frame: false,
    webPreferences: {
      preload: path.join(__dirname, "modules/preload/preload.js")
    }
  })

  if (process.env.APP_DEV) {
    win.loadURL("http://localhost:5173")
  } else {
    loadURL(win)
  }

  win.webContents.session.webRequest.onBeforeSendHeaders(
    (details, callback) => {
      const { requestHeaders } = details
      UpsertKeyValue(requestHeaders, "Access-Control-Allow-Origin", ["*"])
      callback({ requestHeaders })
    }
  )

  win.webContents.session.webRequest.onHeadersReceived((details, callback) => {
    const { responseHeaders } = details
    UpsertKeyValue(responseHeaders, "Access-Control-Allow-Origin", ["*"])
    UpsertKeyValue(responseHeaders, "Access-Control-Allow-Headers", ["*"])
    callback({
      responseHeaders
    })
  })

  win.setTitle("Read Nyanga")

  // window event handler
  eventHandle(win)

  // debug
  // testdb()
  // let db = new database('.nyanga')
  // db.database.
  // test.getInfo().then((info) => {
  //   console.log(info)
  // })
}

app.whenReady().then(() => {
  createWindow()
})
