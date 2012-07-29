from gi.repository import GObject, Gtk, Gedit
import os
import gettext

ui_str = """
<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_6">
        <menuitem name="Myplugin" action="Myplugin"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class Myplugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "Myplugin"

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self._insert_menu()

    def do_deactivate(self):
        self._remove_menu()

    def _remove_menu(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_id)
        manager.remove_action_group(self._action_group)
        self._action_group = None
        manager.ensure_update()

    def _insert_menu(self):
        manager = self.window.get_ui_manager()

	# Translate actions below, hardcoding domain here to avoid complications now
	_ = lambda s: gettext.dgettext('myplugin', s);

        self._action_group = Gtk.ActionGroup(name="GeditMypluginPluginActions")
	self._action_group.add_actions([('Myplugin', None,
	                                 _('Print'),
	                                 'F3',
	                                 _('Print to stdout'),
	                                 lambda a, w: self.do_myplugin(w.get_active_document()))],
	                                 self.window)
        manager.insert_action_group(self._action_group, -1)
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _is_word_separator(self, c):
        return not (c.isalnum() or c == '_')

    def do_myplugin(self, document):
        # Get the word at the cursor
        start = document.get_iter_at_mark(document.get_insert())
        end = start.copy()

        # If just after a word, move back into it
        c = start.get_char()
        if self._is_word_separator(c):
            start.backward_char()

        # Go backward
        while True:
            c = start.get_char()
            if not self._is_word_separator(c):
                if not start.backward_char():
                    break
            else:
                start.forward_char()
                break

        # Go forward
        while True:
            c = end.get_char()
            if not self._is_word_separator(c):
                if not end.forward_char():
                    break
            else:
                break

        if end.compare(start) > 0:
            text = document.get_text(start,end,False).strip()
            if text:
                # FIXME: We need a dbus interface for devhelp soon...
                #os.spawnlp(os.P_NOWAIT, 'devhelp', 'devhelp', '-s', text)
		#send_or_recieve(text)
		print text
		#document.set_text("Umang is a good boy")
		
