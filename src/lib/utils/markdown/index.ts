import Showdown from "showdown";

export default function markdown(content: string) {
  const shd = new Showdown.Converter({
    openLinksInNewWindow: true,
    emoji: true,
    ghMentions: true,
    ghMentionsLink: "https://gitlab.com/{u}",
    ghCodeBlocks: true
  })

  shd.setFlavor('github')
  return shd.makeHtml(content)
}