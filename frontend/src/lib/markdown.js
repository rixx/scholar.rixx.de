import MarkdownIt from 'markdown-it';
import MarkdownItWikilinks from 'markdown-it-wikilinks';

const wikilinks = MarkdownItWikilinks({
  baseURL: '/t/',
  uriSuffix: '',
  makeAllLinksAbsolute: true,
})
const md = MarkdownIt().use(wikilinks)

const renderMarkdown = (text) => {
  return md.render(text)
}
export default renderMarkdown
