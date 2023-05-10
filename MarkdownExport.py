import os
import sublime
import sublime_plugin
import webbrowser
import codecs
import markdown


def save_utf8(filename, text):
    """Save to UTF8 file."""
    with codecs.open(filename, 'w', encoding='utf-8')as f:
        f.write(text)

class markdown_export_command(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            selection = sublime.Region(0, self.view.size())
            md = self.view.substr(selection)

            html = markdown.markdown(md)

            mdfile = self.view.window().active_view().file_name()
            htmlfile = os.path.splitext(mdfile)[0] + '.html'
            #sublime.error_message(htmlfile)
            save_utf8(htmlfile, html)

            webbrowser.open("file://" + htmlfile)
        except Exception as e:
            sublime.error_message("Error in GitHubMarkdownPreview package:\n\n" + str(e))
