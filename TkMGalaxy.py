# This file (c) Copyright 1998 - 2002 The MITRE Corporation
#
# This file is part of the Galaxy Communicator system. It is licensed
# under the conditions described in the file LICENSE in the root
# directory of the Galaxy Communicator system.

import os, sys, __main__, socket, string

import Tkinter
from Tkinter import *

########################################
#
# GUI units
#
########################################

BadLabelJustification = 'BadLabelJustification'

HEADERFONT = '-*-lucida-bold-r-normal-sans-14-140-*'
CONTENTSFONT = '-*-lucida-medium-r-normal-sans-12-120-*',

class LabeledEntry(Frame):
    def __init__(self, master, label_text,
                 entry_value = '',
                 entry_width = 20,
                 return_cmd = None,
                 label_width = None):
        Frame.__init__(self, master)
        if label_width:
            fontvar = StringVar()
            fontvar.set(label_text)
            self.label = Entry(self, relief = 'flat',
                               borderwidth = 0,
                               font = HEADERFONT, justify = 'left',
                               textvariable = fontvar,
                               width = label_width, state = 'disabled')
        else:
            self.label = Label(self, text=label_text, font= HEADERFONT)
        self.entry = Entry(self, borderwidth=2, relief='sunken',
                           font=CONTENTSFONT, width=entry_width)
        if type(entry_value) is StringType:
            self.textvar = StringVar()
        else:
            self.textvar = IntVar()
        self.textvar.set(entry_value)
        self.entry['textvariable']=self.textvar
        if return_cmd:
            self.entry.bind('<KeyPress-Return>',
                            lambda event, cmd = return_cmd, s = self: \
                            cmd(s.GetValue()))
        else:
            self.entry['state'] = 'disabled'
        self.label.pack(side = 'left')
        self.entry.pack(side = 'left', fill = 'x', expand = 1)
    def Enable(self):
        self.entry['state'] = 'normal'
    def GetValue(self):
        return self.textvar.get()
    def SetValue(self, val):
        self.textvar.set(val)

class ScrollPane(Frame):
    def __init__(self, master, height = 12, width = 60,
                 label = '', label_justification = 'left',
                 action_button_label = None, action_button_action = None):
        Frame.__init__(self, master)
        if label:
            self.labelframe = Frame(self)
            self.labelframe.pack(side = 'top', expand = 0, fill = 'x')
            self.label = Label(self.labelframe, text=label, font= HEADERFONT)
            if label_justification == 'left':
                # self.label.pack(side = 'top', anchor = 'w')
                self.label.pack(side = 'left')
                if action_button_label or action_button_action:
                    self.button = Button(self.labelframe,
                                         text = action_button_label,
                                         font = HEADERFONT,
                                         command = action_button_action)
                    self.button.pack(side = 'right')
            elif label_justification == 'right':
                # self.label.pack(side = 'top', anchor = 'e')
                self.label.pack(side = 'right')
                if action_button_label or action_button_action:
                    self.button = Button(self.labelframe,
                                         text = action_button_label,
                                         font = HEADERFONT,
                                         command = action_button_action)
                    self.button.pack(side = 'left')
            elif label_justification == 'center':
                self.label.pack(side = 'top')
            else:
                raise BadLabelJustification, label_justification
            self.textframe = Frame(self)
            self.textframe.pack(side = 'top', expand = 1, fill = 'both')
            if (action_button_label or action_button_action) and \
               label_justification == 'center':
                self.button = Button(self,
                                     text = action_button_label,
                                     font = HEADERFONT,
                                     command = action_button_action)
                self.button.pack(side = 'top')
        else:
            self.textframe = self
        self.textbox = Text(self.textframe, borderwidth=1, relief='sunken',
                            state='disabled', height=height, width=width,
                            font= CONTENTSFONT
                            )
        self.scrollbar = Scrollbar(self.textframe, borderwidth=1, relief='sunken',
                                   command=self.textbox.yview)
        self.scrollbar.pack(side = "right", fill = "y")
        self.textbox['yscrollcommand'] = self.scrollbar.set
        self.textbox.pack(side='left', expand=1, fill='both')
    def write(self, text):
        self.Write(text)
    def Write(self, text):
        self.textbox['state']='normal'
        self.textbox.insert('end', text)
        self.textbox.yview_pickplace('end')
        self.textbox['state']='disabled'
    def Clear(self):
        self.textbox['state']='normal'
        self.textbox.delete('0.0', 'end')
        self.textbox['state']='disabled'

UnknownMenuType = 'UnknownMenuType'

class MyMenu(Menu):
    def __init__(self, master, vals_dict):
        Menu.__init__(self, master, font= CONTENTSFONT, tearoff=0)
        for key, val in vals_dict.items():
            type, trueval = val
            if type == 'command':
                self.add('command', label = key,
                         command = lambda com = trueval: com())
            elif type == 'cascade':
                self.add('cascade', label = key,
                         menu = MyMenu(self, trueval))
            else:
                raise UnknownMenuType

class MenuBarEntry(Menubutton):
    def __init__(self, master, text, vals_dict):
        Menubutton.__init__(self, master, font = CONTENTSFONT,
                            text = text)
        self.menu = MyMenu(self, vals_dict)
        self['menu'] = self.menu

class Error(Frame):
    def __init__(self, master, error_string):
        self.master = master

        Frame.__init__(self, master)
        self['borderwidth'] = 2
        self['relief'] = 'ridge'
        self.pack(side='top')
        self.master.title('You should know...')

        self.msg = Message(self, text=error_string, width=200,
                           font= CONTENTSFONT,
                           justify='center')
        self.msg.pack(side = 'top')
        self.dismiss_row = Frame(self)
        self.dismiss_row.pack(side='top')
        self.dismiss_row['borderwidth'] = 2
        self.CLOSE = Button(self.dismiss_row, text='OK',
                            font= HEADERFONT,
                            command=self.close_cmd)
        self.CLOSE.pack(side='left')
        self.pack(fill = 'both')

    def close_cmd(self):
        self.master.destroy()

########################################
#
# Tk connection object
#
########################################

import GalaxyIO, SLSUtil, MGalaxy

class Connection(GalaxyIO.Connection):
    def __init__(self, server, c_conn):
        GalaxyIO.Connection.__init__(self, server, c_conn)

        # SAM 10/27/00: Up to now, I've been creating the GUI and
        # giving it a connection to work with, but the fact of the
        # matter is that we can't really initialize interfaces
        # (or shouldn't, actually) until we get an environment
        # in reinitialize.

        # In order to create the connection, we need to create
        # a "seed" environment. No session ID yet.
        env_seed = GalaxyIO.CallEnvironmentSeed(self, self.server.env_class)
        self.gui = self.server.gui_class(master = Toplevel(),
                                         env = env_seed)

    def _Disconnect(self, force_destroy = 0):

        if force_destroy and self.c_conn:
            GalaxyIO.Connection._Disconnect(self, force_destroy = force_destroy)
        elif not self.disconnected:
            if self.gui:
                self.gui.Quit(do_conn = 0)
                self.gui = None
            GalaxyIO.Connection._Disconnect(self, force_destroy = force_destroy)

    def _CallDispatchFn(self, fn, py_frame, py_env):
        # Make sure you update the environment in the
        # gui class every time a dispatch function is called.
        if self.gui:
            self.gui.env = py_env
        return GalaxyIO.Connection._CallDispatchFn(self, fn, py_frame, py_env)


# The gui class must support the Quit method.

class CommunicatorInterface(Frame):
    def __init__(self, master = None, env = None):
        Frame.__init__(self, master)
        self.env = env
    def Quit(self, do_conn = 1):
        if self.env and do_conn:
            self.env.conn.Disconnect()
        self.master.destroy()

# Minor annoyance: when I type a SIGINT, the signal isn't delivered
# until after the next Hub contacts the server. It doesn't matter
# if I type a ctl-C or if I kill -INT the process from another
# shell. How does the wish executable deal with this? It looks
# like this is the way the Python tkinter mainloop is programmed.
# It looks like if I generate an event, it will interrupt itself.

class Server(GalaxyIO.Server):
    def __init__(self, in_args, server_name = "<unknown>",
                 default_port = 0,
                 verbosity = -1,
                 require_port = 0,
                 maxconns = 1,
                 validate = 0,
                 server_listen_status = GalaxyIO.GAL_CONNECTION_LISTENER,
                 client_pair_string = None,
                 session_id = None,
                 server_locations_file = None,
                 slf_name = None,
                 env_class = GalaxyIO.CallEnvironment,
                 conn_class = Connection,
                 gui_class = CommunicatorInterface):
        Tkinter._default_root = None
        self.gui_class = gui_class
        self.gui_root = None
        self.pending_file_handlers = []
        self.poll_timer = None
        self.client_timer = None
        self.fd_objs = []
        self.filehandler_available = -1
        self.timer_dict = {}
        GalaxyIO.Server.__init__(self, in_args, server_name,
                                 default_port, verbosity,
                                 require_port, maxconns,
                                 validate, server_listen_status,
                                 client_pair_string, session_id,
                                 server_locations_file,
                                 slf_name,
                                 env_class)
        self.conn_class = conn_class

    def __PollTimer(self):
        for py_conn in self.conns.values():
            py_conn.PollConnection()
        self.poll_timer = self.gui_root.tk.createtimerhandler(100, self.__PollTimer)

    def __ClientTimer(self):
        self.PollClients()
        self.client_timer = self.gui_root.tk.createtimerhandler(1000, self.__ClientTimer)

    def _ExitLoop(self):
        # The server is now destroyed. Just in case this happens as the
        # result of a callback, we want to make sure that the
        # callback ends cleanly. So I'll set a timer handler to quit.
        self.gui_root.tk.createtimerhandler(1, lambda s = self: s.Quit())

    def _ServerLoop(self):
        self.gui_root = Tkinter.Tk()
        self.gui_root.withdraw()
        # createfilehandler only exists on some platforms.
        # e.g., not on Windows.
        if hasattr(self.gui_root.tk, "createfilehandler"):
            self.filehandler_available = 1
        else:
            self.filehandler_available = 0
        # In addition to the file descriptor callbacks, we
        # need a timer callback to handle the polls for
        # the listener-in-Hub stuff and for checking the
        # connection socket queues. In addition, the fact
        # that the timer happens will also allow us to
        # catch signals.
        self.poll_timer = self.gui_root.tk.createtimerhandler(100, self.__PollTimer)
        if self.ServerIsClient():
            self.client_timer = self.gui_root.tk.createtimerhandler(1000, self.__ClientTimer)
        if self.pending_file_handlers:
            for obj, sock, dir in self.pending_file_handlers:
                self._TkRegister(obj, sock, dir)
        self.pending_file_handlers = []
        self.gui_root.mainloop()

    def Quit(self, *args):
        if self.poll_timer:
            self.poll_timer.deletetimerhandler()
            self.poll_timer = None
        if self.client_timer:
            self.client_timer.deletetimerhandler()
            self.client_timer = None
        for obj in self.fd_objs[:]:
            obj.Disconnect()
            self.fd_objs.remove(obj)
        if self.gui_root:
            self.gui_root.destroy()
            self.gui_root = None
        apply(GalaxyIO.Server.Quit, (self,) + args)

    def ReaderRegister(self, obj, sock):
        self._TkRegister(obj, sock, Tkinter.READABLE)

    def _TkRegister(self, obj, sock, direction):
        if self.gui_root:
            if self.filehandler_available:
                self.gui_root.tk.createfilehandler(sock, direction,
                                                   lambda s, m, o = obj: o.Callback())
            else:
                if self.timer_dict.has_key(sock):
                    self.timer_dict[sock].deletetimerhandler()
                    del self.timer_dict[sock]
                self.timer_dict[sock] = self.gui_root.tk.createtimerhandler(25, lambda s = self, o = obj, so = sock: s._TimerCallback(o, so))
            self.fd_objs.append(obj)
        else: self.pending_file_handlers.append((obj, sock, direction))

    def _TimerCallback(self, obj, sock):
        obj.Callback()
        # If Unregister was called, this key would
        # be gone. If it's still here, reset the poll.
        if self.timer_dict.has_key(sock):
            self.timer_dict[sock] = self.gui_root.tk.createtimerhandler(25, lambda s = self, o = obj, so = sock: s._TimerCallback(o, so))

    def WriterRegister(self, obj, sock):
        self._TkRegister(obj, sock, Tkinter.WRITABLE)

    def ReaderUnregister(self, sock):
        self._TkUnregister(sock)

    def WriterUnregister(self, sock):
        self._TkUnregister(sock)

    def _TkUnregister(self, sock):
        if self.gui_root:
            if self.filehandler_available:
                try:
                    self.gui_root.tk.deletefilehandler(sock)
                except: pass
            else:
                if self.timer_dict.has_key(sock):
                    self.timer_dict[sock].deletetimerhandler()
                    del self.timer_dict[sock]
