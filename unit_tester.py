# This file (c) Copyright 1998 - 2002 The MITRE Corporation
#
# This file is part of the Galaxy Communicator system. It is licensed
# under the conditions described in the file LICENSE in the root
# directory of the Galaxy Communicator system.

import sys, string, os

import Galaxy, GalaxyIO, TkMGalaxy
#import Galaxy, GalaxyIO, cGalaxy, TkMGalaxy

import Tkinter
from Tkinter import *

# This window will have a history pane, and a menu of what type
# of message to send. Things work like this:

# New messages which expect a reply which come in are marked
# as "pending". All administrative info that comes in with the
# new message is written back out (session info, token, server token,
# round trip). When a reply is sent, the pending message is
# discharged.

# When acting as a Hub, the unit tester can send a new message,
# a reply or an error. When acting as a server, the unit tester
# can send these as well as postpone and destroy. The four reply types
# should only be available when there's a pending new message.

# Here's what happens when you select the various elements:
# New message: a typein window pops up, with slots for administrative
# information in addition to the frame itself. Press send/cancel.
# Reply: a typein window pops up, without administrative info slots.
# Press send/cancel.
# Error: a typein window pops up for the error description. Press
# send/cancel.
# Postpone, destroy: a confirmation dialogue pops up. Press send/cancel.

# When the message is sent, it's written to the history.

# Development steps:

# (1) Implement described behavior, from Hub point of view.
# (2) Add server side (this will require a little juggling
#     in the bindings to get access at the appropriate point)
# (3) Add possibility of sending saved messages.
# (4) Add brokering w/arbitrary data.
# (5) Add file sink/source for broker.
# (6) Add menu configuration window for frame.

from TkMGalaxy import MenuBarEntry, ScrollPane, LabeledEntry, \
     CONTENTSFONT, HEADERFONT

class ConfigurableMenuBarEntry(MenuBarEntry):
    def Disable(self, entry_label):
        self.menu.entryconfigure(entry_label, state = "disabled")
    def Enable(self, entry_label):
        self.menu.entryconfigure(entry_label, state = "normal")

class ConfirmRow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self['borderwidth'] = 2
        self.okbutton = Button(self, text='OK',
                               font= HEADERFONT,
                               command=master.succeed)
        self.okbutton.pack(side='left')
        self.cancelbutton = Button(self, text='Cancel',
                                   font= HEADERFONT,
                                   command = master.fail)
        self.cancelbutton.pack(side = "left")

class ConfirmationPopup(Frame):
    def __init__(self, message):
        Frame.__init__(self, Toplevel())
        self['borderwidth'] = 2
        self['relief'] = 'ridge'
        self.pack(side='top', fill = 'both')
        self.dialogue = None
        self.master.title("Unit tester confirmation")
        self.msg = Message(self, text=message, width=200,
                           font= CONTENTSFONT,
                           justify='center')
        self.msg.pack(side = 'top')
        self.dismiss_row = ConfirmRow(self)
        self.dismiss_row.pack(side = 'top')

    def succeed(self):
        if self.dialogue is not None:
            self.dialogue.confirmation_result = 1, None
        self.master.destroy()

    def fail(self):
        if self.dialogue is not None:
            self.dialogue.confirmation_result = 0, None
        self.master.destroy()

class ConfirmationDialogue:
    def __init__(self, confirmation_window):
        self.confirmation_window = confirmation_window
        self.confirmation_result = None, None
        confirmation_window.dialogue = self
    def Confirm(self):
        self.confirmation_window.grab_set()
        self.confirmation_window.wait_window()
        return self.confirmation_result

class ConfirmationTypein(Frame):
    def __init__(self, message):
        Frame.__init__(self, Toplevel())
        self['borderwidth'] = 2
        self['relief'] = 'ridge'
        self.pack(side='top')
        self.master.title("Unit tester typein")
        self.msg = LabeledEntry(self, label_text = message,
                                entry_width = 40)
        self.msg.pack(side = 'top')
        self.msg.Enable()
        self.dismiss_row = ConfirmRow(self)
        self.dismiss_row.pack(side='top')
        self.dialogue = None

    def succeed(self):
        if self.dialogue is not None:
            self.dialogue.confirmation_result = 1, self.msg.GetValue()
        self.master.destroy()

    def fail(self):
        if self.dialogue is not None:
            self.dialogue.confirmation_result = 0, None
        self.master.destroy()

class TaggableScrollPane(ScrollPane):

    def Write(self, text, key = None, tag_fn = None):
        if tag_fn and key:
            if not hasattr(self, "tag_index"):
                self.tag_index = 0
            tag = "text_tag_%d" % self.tag_index
            self.tag_index = self.tag_index + 1
            start_index = self.textbox.index('end - 1 chars')
        ScrollPane.Write(self, text)
        if tag_fn and key:
            end_index = self.textbox.index('end - 1 chars')
            self.textbox.tag_add(tag, start_index, end_index)
            self.textbox.tag_bind(tag, key,
                                  lambda e, f = tag_fn, t = text: f(t, e))

class TypeinScrollPane(ScrollPane):

    def __init__(self, master, height = 12, width = 60,
                 label = '', label_justification = 'left',
                 action_button_label = None, action_button_action = None):
        ScrollPane.__init__(self, master, height, width,
                            label, label_justification,
                            action_button_label, action_button_action)
        self.textbox['state']='normal'
        self.textbox['background'] = 'white'

    def Write(self, text):
        ScrollPane.Write(self, text)
        self.textbox['state']='normal'

# If the message type is GAL_MESSAGE_MSG_TYPE, we should
# add a row for the session ID and a round trip button.
# The round trip button will be disabled if we're a hub
# and we're doing this from a modal dialogue.

class ConfirmationFrameTypein(Frame):
    def __init__(self, message, msg_type, gui, from_modal):
        Frame.__init__(self, Toplevel())
        self['borderwidth'] = 2
        self['relief'] = 'ridge'
        self.pack(side='top', fill = 'both')
        self.master.title("Unit tester typein")
        self.msg = TypeinScrollPane(self, label = message)
        self.msg.pack(side = 'top', fill = 'both', expand = 1)
        d = TaggableScrollPane(self,
                               label = "Or select a frame:")
        d.pack(side = "top", fill = 'both')
        for f in gui.frame_history:
            d.Write(f + "\n", "<Button-1>", self.MaybeUseFrame)
        # Here's where we add the line.
        if msg_type == GalaxyIO.GAL_MESSAGE_MSG_TYPE:
            p = Frame(self, borderwidth = 2, relief = 'ridge')
            p.pack(side = 'top', fill = 'x', expand = 1)
            # Do the grid for the session ID and round trip.
            session_id = gui.env.GetSessionID()
            if not session_id: session_id = ""
            self.session_entry = LabeledEntry(p, label_text = "Session ID:",
                                              entry_value = session_id)
            self.session_entry.entry['state'] = 'normal'
            # self.session_entry['borderwidth'] = 2
            # self.session_entry['relief'] = 'ridge'
            self.lock_var = IntVar()
            self.lock_entry = Checkbutton(p, text = "Lock session",
                                          font = HEADERFONT,
                                          variable = self.lock_var)
            self.round_trip_var = IntVar()
            self.round_trip_entry = Checkbutton(p, text = "Reply required",
                                                font = HEADERFONT,
                                                variable = self.round_trip_var)
            # self.round_trip_entry['borderwidth'] = 2
            # self.round_trip_entry['relief'] = 'ridge'
            self.session_entry.grid(row = 0, column = 0, sticky = 'w')
            self.session_entry.grid_columnconfigure(0, weight = '1')
            self.session_entry.grid_rowconfigure(0, weight = '1')
            self.lock_entry.grid(row = 1, column = 0, sticky = 'w')
            self.lock_entry.grid_columnconfigure(0, weight = '1')
            self.lock_entry.grid_rowconfigure(0, weight = '1')
            self.round_trip_entry.grid(row = 2, column = 0, sticky = 'w')
            self.round_trip_entry.grid_columnconfigure(0, weight = '1')
            self.round_trip_entry.grid_rowconfigure(2, weight = '1')
            if gui.as_hub and from_modal:
                self.round_trip_entry['state'] = 'disabled'
            if gui.as_hub:
                self.lock_entry['state'] = 'disabled'
        else:
            self.session_entry = None
            self.round_trip_entry = None
            self.round_trip_var = None
            self.lock_entry = None
            self.lock_var = None
        self.dismiss_row = ConfirmRow(self)
        self.dismiss_row.pack(side='top')
        self.dialogue = None

    # This is generated by mouse clicks in the history pane.
    # If there's a message typein visible, use the text.
    # Duh. The message typein is modal. Can't use it.

    def MaybeUseFrame(self, text, event):
        self.msg.Clear()
        self.msg.Write(text)

    def succeed(self):
        if self.dialogue is not None:
            f_text = self.msg.textbox.get('0.0', 'end')
            if self.session_entry:
                session = self.session_entry.GetValue()
            else:
                session = None
            if self.round_trip_var:
                round_trip = self.round_trip_var.get()
            else:
                round_trip = None
            if self.lock_var:
                lock = self.lock_var.get()
            else:
                lock = None
            self.dialogue.confirmation_result = 1, (f_text, session, round_trip, lock)
        self.master.destroy()

    def fail(self):
        if self.dialogue is not None:
            self.dialogue.confirmation_result = 0, None
        self.master.destroy()

# If as_hub is true, there are a couple things that the
# unit tester can't do: first, it can't send back destroy
# or postpone replies; second, it can't send a new message
# which needs a reply (see discussion before definition of
# UnitTesterInterface).

class ModalMessageDialogue(Frame):
    def __init__(self, incoming_frame, gui):
        Frame.__init__(self, Toplevel())
        self['borderwidth'] = 2
        self['relief'] = 'ridge'
        self.pack(side='top', fill = 'both')
        self.master.title("Unit tester response window")
        self.dialogue = None
        self.original_msg = ScrollPane(self, label = "Incoming message",
                                       label_justification = "center")
        self.original_msg.Write(incoming_frame.PPrint())
        self.original_msg.pack(side = 'top')
        # Button to send a new message.
        b1 = Button(self, text = "Send new message",
                    relief = 'groove',
                    command = lambda g = gui: g.SendNewMessage(from_modal = 1))
        b1.pack(side = 'top')
        # Radiobuttons for reply type.
        self.reply_var = StringVar()
        radio_frame = Frame(self, borderwidth = 2,
                            relief = 'ridge')
        radio_frame.pack(side = 'top', fill = 'x', expand = 1)
        rb1 = Radiobutton(radio_frame, text = "Normal reply",
                          variable = self.reply_var,
                          value = "normal")
        self.grid_equal(rb1, 0, 0)
        rb2 = Radiobutton(radio_frame, text = "Error reply",
                          variable = self.reply_var,
                          value = "error")
        self.grid_equal(rb2, 0, 1)
        rb3 = Radiobutton(radio_frame, text = "Destroy reply",
                          variable = self.reply_var,
                          value = "destroy")
        self.grid_equal(rb3, 1, 0)
        if gui.as_hub:
            rb3['state'] = 'disabled'
        rb4 = Radiobutton(radio_frame, text = "Dummy reply",
                          variable = self.reply_var,
                          value = "dummy")
        self.grid_equal(rb4, 1, 1)
        self.dismiss_row = ConfirmRow(self)
        self.dismiss_row.pack(side='top')

    def grid_equal(self, win, row, col):
        win.grid(row = row, column = col, sticky = 'w')
        win.grid_columnconfigure(col, weight = '1')
        win.grid_rowconfigure(row, weight = '1')

    def Pass(self):
        pass

    def succeed(self):
        if self.dialogue is not None:
            self.dialogue.confirmation_result = 1, self.reply_var.get()
        self.master.destroy()

    def fail(self):
        if self.dialogue is not None:
            self.dialogue.confirmation_result = 0, None
        self.master.destroy()

# The way this is set up, if we receive a new message and the
# new message requires a return, we'll put up a modal dialogue to
# deal with it, no matter whether we're a Hub or server. The reason
# for this is pretty simple. If we're a server, we need to provide
# a reply, and we won't get any server loop cycles until we do, because
# we're in a server callback. If we're a Hub, the server that sent
# the message to us is waiting for a reply, and can be counted on
# not to do anything until it gets an answer back, so we don't need
# to do anything besides provide an answer.

# On the other hand, if we SEND a new message that requires a
# return, if we're a server we have to wait for the response (and
# we'll use env.DispatchFrame to handle it). If we're a Hub, we
# may very well get new messages in the process of the server
# doing its thing (and these messages may very well need a reply,
# which means we better answer them or OUR reply will never come),
# so we have to be asynchronous, just like the Hub. We'll send
# a new message and return. The behavior should look identical from
# user perspective, in terms of what s/he sees in the GUI.

# The one difference will be when we're in a modal dialogue dealing
# with a received message. In this context, if we're a Hub, we
# can't send a message which needs a reply, because this will
# result in a deadlock on the server side (it's waiting for an
# answer to ITS query, and won't process any other new messages
# until it gets the answer). If we're a server, on the other
# hand, sending a new message is no problem, as long as the Hub
# script doesn't need to consult us in the process of handling the
# new message (which is the usual deadlock case).

class UnitTesterInterface(TkMGalaxy.CommunicatorInterface):
    def __init__(self, master = None, env = None, as_hub = 0):
        TkMGalaxy.CommunicatorInterface.__init__(self, master, env)
        self.master.title("Communicator Unit Tester")
        self['borderwidth'] = 2
        self.pack(fill = 'both', expand = 1)
        self.history = ScrollPane(self,
                                  label = "Interaction history",
                                  label_justification = 'center',
                                  width = 40,
                                  height = 10)
        self.history.pack(side = 'top', anchor = 'w',
                          fill = 'both', expand = 1)
        self.button_row = Frame(self, relief = 'flat',
                                borderwidth = 2)
        self.button_row.pack(side = 'top')
        b1 = Button(self.button_row, text = "Quit",
                    relief = 'groove',
                    command = self.Quit)
        b1.pack(side = 'left')
        b2 = Button(self.button_row, text = "Send new message",
                    relief = 'groove',
                    command = self.SendNewMessage)
        b2.pack(side = 'left')
        self.env = env
        self.as_hub = as_hub

        # Register a timer poll, if you're a Hub.
        if self.as_hub:
            self.poll_timer = self.tk.createtimerhandler(100, self.__PollTimer)
        else:
            self.poll_timer = None
        self.frame_history = self.seed_frame_history

    # Receiving a new message which requires a reply
    # should provide a popup, always.
    # This is necessary in the case of the unit tester as server,
    # because nothing will happen until the dispatch function
    # callback returns (in the case of a message which
    # doesn't require a return, we can just provide a return
    # immediately). We'll maintain the same behavior when
    # the unit tester is the Hub for consistency.

    def __PollTimer(self):
        response, msg_type = self.env.conn.ReadFrame(blocking = 0)
        if response is not None:
            # Strip the administrative information.
            try:
                admin_info = response[Galaxy.GAL_HUB_OPAQUE_DATA_FRAME_KEY]
                del response[Galaxy.GAL_HUB_OPAQUE_DATA_FRAME_KEY]
            except KeyError:
                admin_info = None
            if (msg_type == GalaxyIO.GAL_MESSAGE_MSG_TYPE):
                # Update the environment object. This will
                # decode the administrative info.
                self.env = FakeCallEnvironment(self.env.conn, None,
                                               admin_info = admin_info,
                                               frame_name = response.name)
                _DoGenericDispatch(self.env, response)
            else:
                self.RecordMessage(response, "Received", msg_type)

        self.poll_timer = self.tk.createtimerhandler(100, self.__PollTimer)

    def ModalMessageReply(self, frame, just_return = 0):
        # Here, I need to pop up a modal interaction to
        # send a message reply. It should probably be seeded
        # with the incoming message. It's a different
        # dialogue than the reply dialogue.
        if just_return:
            self.RecordMessage(frame, "Sending", GalaxyIO.GAL_REPLY_MSG_TYPE)
            self.env.Reply(frame)
        else:
            yes_or_no, val = ConfirmationDialogue(ModalMessageDialogue(frame, self)).Confirm()
            # "Cancel" is like returning a dummy, as is not selecting
            # a value.
            if yes_or_no and val and (val != "dummy"):
                if val == "normal":
                    # Get reply.
                    self.SendReply()
                elif val == "error":
                    # Get error.
                    self.SendErrorReply()
                elif val == "destroy":
                    # Send destroy.
                    self.SendDestroyReply()
            else:
                # If we cancelled, or we didn't have a val, or
                # the val was "dummy", we need to send the incoming
                # frame as the reply.
                self.RecordMessage(frame, "Sending",
                                   GalaxyIO.GAL_REPLY_MSG_TYPE)
                self.env.Reply(frame)
        # So you're always guaranteed to have sent a reply.

    def SendNewMessage(self, from_modal = 0):
        self._SendMessage("Enter new message:", GalaxyIO.GAL_MESSAGE_MSG_TYPE,
                          from_modal)

    def RecordMessage(self, message, dir, mtype):
        self.history.Write(("[%s: " % dir) + MsgTypeNameTable[mtype] + "]\n")
        m = message.PPrint()
        self.history.Write(m + "\n")
        if m not in self.frame_history:
            self.frame_history.append(m)

    def _SendMessage(self, typein_prompt, msg_type, from_modal = 0):
        cur_frame_string = None
        while 1:
            d = ConfirmationDialogue(ConfirmationFrameTypein(typein_prompt, msg_type, self, from_modal))
            if cur_frame_string is not None:
                d.confirmation_window.msg.Write(cur_frame_string)
            yes_or_no, val = d.Confirm()
            if yes_or_no:
                f_text, s_text, round_trip, lock = val
                cur_frame_string = f_text
                try:
                    new_f = Galaxy.Frame(str = f_text)
                except Galaxy.FrameParsingError:
                    retry_val, ignore = ConfirmationDialogue(ConfirmationPopup("Couldn't parse the frame. Retry?")).Confirm()
                    if not retry_val:
                        print "Cancelled."
                        sys.stdout.flush()
                        return
                    else:
                        continue
                self.RecordMessage(new_f, "Sending", msg_type)
                if msg_type == GalaxyIO.GAL_REPLY_MSG_TYPE:
                    self.env.Reply(new_f)
                elif msg_type == GalaxyIO.GAL_MESSAGE_MSG_TYPE:
                    # Do something, not sure what yet.
                    if s_text and lock:
                        self.env.SetSession(s_text,
                                            GalaxyIO.GAL_SERVER_READS_ONLY_FROM_SESSION | GalaxyIO.GAL_SESSION_WRITES_ONLY_TO_SERVER | GalaxyIO.GAL_SERVER_WRITES_ONLY_TO_SESSION)
                    elif s_text:
                        self.env.UpdateSessionID(s_text)
                    # Only want to wait for the reply if we're
                    # not a Hub.
                    if round_trip and (not self.as_hub):
                        try:
                            reply_f = self.env.DispatchFrame(new_f)
                            del reply_f[Galaxy.GAL_HUB_OPAQUE_DATA_FRAME_KEY]
                            self.RecordMessage(reply_f, "Received",
                                               GalaxyIO.GAL_REPLY_MSG_TYPE)
                        except GalaxyIO.DispatchError, error_frame:
                            del error_frame[Galaxy.GAL_HUB_OPAQUE_DATA_FRAME_KEY]
                            self.RecordMessage(error_frame, "Received",
                                               GalaxyIO.GAL_ERROR_MSG_TYPE)
                    elif round_trip:
                        # We need to write a frame with the
                        # round trip set to 1. But we don't want to
                        # wait for the response. This will also only
                        # be fired when we're pretending to be a Hub,
                        # so we can use a special version of WriteFrame.
                        self.env.WriteFrame(new_f, round_trip = 1)
                    else:
                        self.env.WriteFrame(new_f)
            else:
                print "Cancelled."
                sys.stdout.flush()
            return

    def SendReply(self):
        self._SendMessage("Enter reply:", GalaxyIO.GAL_REPLY_MSG_TYPE)

    def SendErrorReply(self):
        yes_or_no, val = ConfirmationDialogue(ConfirmationTypein("Error:")).Confirm()
        self.history.Write("[Sending error reply: %s]\n" % val)
        self.env.Error(val)

    def SendPostponement(self):
        pass
        # print "Sending postponement"

    def SendDestroyReply(self):
        self.history.Write("[Sending destroy reply]\n")
        self.env.DestroyToken()

    def Quit(self, do_conn = 1):
        if self.poll_timer is not None:
            self.poll_timer.deletetimerhandler()
            self.poll_timer = None
        TkMGalaxy.CommunicatorInterface.Quit(self, do_conn)

# We probably need to implement a fake call environment
# for the Hub side. This will mirror the message set of
# the real GalaxyIO.CallEnvironment exactly.

# I'd like to use it for the server too, but that won't
# work, because the REAL C environment needs to be
# updated when replies are sent. So I have a problem
# in the server case, figuring out how to print out
# the frames that are actually sent. I can get access
# to the frames which are really typed in, but the
# postpone, destroy, and error frames won't be visible.
# For consistency, then, I should never make them visible,
# or any of the other administrative information.

class FakeCallEnvironment:

    def __init__(self, conn, env, create_p = 0,
                 admin_info = None, frame_name = None):
        # I need to have env and create_p here for compatibility
        # with the real CallEnvironment, and in particular
        # with the call to CallEnvironmentSeed.
        self.conn = conn
        self.return_satisfied = 0
        if admin_info is not None:
            self.info_frame = admin_info
        else:
            self.info_frame = Galaxy.Frame(type = Galaxy.GAL_FRAME,
                                           name = "admin_info")
        self.frame_name = frame_name

    def GetSessionID(self):
        if self.info_frame is not None:
            try:
                return self.info_frame[Galaxy.GAL_SESSION_ID_FRAME_KEY]
            except KeyError:
                return None
        else:
            return None

    def UpdateSessionID(self, id):
        self.info_frame[Galaxy.GAL_SESSION_ID_FRAME_KEY] = id

    def ReturnRequired(self):
        try:
            return self.info_frame[Galaxy.GAL_ROUND_TRIP_FRAME_KEY]
        except:
            return 0

    def _AdministerNewMessage(self, frame):
        f = Galaxy.Frame(type = Galaxy.GAL_CLAUSE,
                         name = "admin_info")
        if self.info_frame.has_key(Galaxy.GAL_SESSION_ID_FRAME_KEY):
            f[Galaxy.GAL_SESSION_ID_FRAME_KEY] = self.info_frame[Galaxy.GAL_SESSION_ID_FRAME_KEY]
        frame[Galaxy.GAL_HUB_OPAQUE_DATA_FRAME_KEY] = f

    def DispatchFrame(self, out_frame):
        self._AdministerNewMessage(out_frame)
        return self.conn.DispatchFrame(out_frame)

    # skipping DispatchFrameWithContinuation for now

    def WriteFrame(self, out_frame, round_trip = 0):
        self._AdministerNewMessage(out_frame)
        if round_trip:
            out_frame[Galaxy.GAL_HUB_OPAQUE_DATA_FRAME_KEY][Galaxy.GAL_ROUND_TRIP_FRAME_KEY] = 1
        self.conn.WriteFrame(out_frame)

    def _AdministerReply(self, out_frame, update_frame_name = 0):
        if out_frame is not None:
            out_frame[Galaxy.GAL_HUB_OPAQUE_DATA_FRAME_KEY] = self.info_frame
            if update_frame_name and (self.frame_name is not None):
                out_frame.name = self.frame_name

    def DestroyToken(self):
        if not self.return_satisfied:
            f = Galaxy.Frame(type = Galaxy.GAL_CLAUSE,
                             name = "destroy")
            self._AdministerReply(f)
            self.conn.WriteMessage(f, GalaxyIO.GAL_DESTROY_MSG_TYPE)
            self.return_satisfied = 1

    def Reply(self, out_frame):
        if not self.return_satisfied:
            self._AdministerReply(out_frame, update_frame_name = 1)
            self.conn.WriteMessage(out_frame, GalaxyIO.GAL_REPLY_MSG_TYPE)
            self.return_satisfied = 1

    def Error(self, description, errno = GalaxyIO.GAL_APPLICATION_ERROR):
        if not self.return_satisfied:
            f = Galaxy.Frame(type = Galaxy.GAL_CLAUSE,
                             name = "system_error")
            f[Galaxy.GAL_ERROR_NUMBER_FRAME_KEY] = errno
            f[Galaxy.GAL_ERROR_DESCRIPTION_FRAME_KEY] = description
            self._AdministerReply(f)
            self.conn.WriteMessage(f, GalaxyIO.GAL_ERROR_MSG_TYPE)
            self.return_satisfied = 1

    # Skipping GetSessionProperties, GetServerProperties,
    # ModifySessionProperties, ModifyServerProperties, SetSession

def _DoGenericDispatch(env, frame, just_return = 0):
    env.conn.gui.RecordMessage(frame, "Received",
                               GalaxyIO.GAL_MESSAGE_MSG_TYPE)
    # This is the "dispatch function". If there's no GUI, we're
    # sort of toast. All the reply information will be updated
    # in the interface there.
    if env.ReturnRequired():
        # You're always guaranteed to have sent a reply.
        env.conn.gui.ModalMessageReply(frame, just_return = just_return)
    return None

# Here's the server we'll use.

class UnitTesterServer(TkMGalaxy.Server):
    def __init__(self, host, port, retry, ignore_reinitialize,
                 validate = 0,
                 session_id = None,
                 server_locations_file = None,
                 conn_class = TkMGalaxy.Connection):
        if retry:
            flags = GalaxyIO.GAL_HUB_CLIENT_CONNECT_FAILURE_RETRY | \
                    GalaxyIO.GAL_HUB_CLIENT_DISCONNECT_RETRY
        else:
            flags = GalaxyIO.GAL_HUB_CLIENT_CONNECT_FAILURE_SHUTDOWN | \
                    GalaxyIO.GAL_HUB_CLIENT_DISCONNECT_SHUTDOWN
        TkMGalaxy.Server.__init__(self, [], "<unit_tester>",
                                  0, 3, 0, 1, validate,
                                  GalaxyIO.GAL_HUB_CLIENT | flags,
                                  ("%s:%d" % (host, port)),
                                  None, None, None,
                                  GalaxyIO.CallEnvironment,
                                  conn_class,
                                  UnitTesterInterface)
        self.debug = 1
        self.ignore_reinitialize = ignore_reinitialize

    # These functions override the dispatch function access.

    def _ListDispatchFnSigs(self):
        return []

    def _GenericDispatch(self, env, frame):
        # I need to check whether we're ignoring reinitialize.
        # That will only happen the first time it's called for
        # any connection.
        if self.ignore_reinitialize and \
           ((not hasattr(env.conn, "reinitialize_done")) or \
            (env.conn.reinitialize_done == 0)):
            # If this is the first call to reinitialize (that is,
            # during connection time) and we're supposed to
            # ignore it, just return None.
            env.conn.reinitialize_done = 1
            return _DoGenericDispatch(env, frame, just_return = 1)
        else:
            return _DoGenericDispatch(env, frame)

    def _SelectDispatchFn(self, op_name):
        return lambda frame, env, s = self: s._CallDispatchFn(s._GenericDispatch, frame, env), None

    def CreateConnection(self, c_conn):
        TkMGalaxy.Server.CreateConnection(self, c_conn)
        # I want to shut off the verbosity after the connection is made.
        # self.ostream.set_verbosity(0)

def main_server(host, port, retry, ignore_reinitialize, stypes):
    s = UnitTesterServer(host, port, retry, ignore_reinitialize)
    for t in stypes:
        s.AddServiceType(t)
    s.RunServer()

def main_hub(host, port, retry, welcome_frame):
    # I want the connection to be silent. This requires
    # some gymnastics. I need not to connect initially.
    c = GalaxyIO.ClientConnection(host, port, welcome_frame,
                                  connect = 0)
    if not c:
        print "No server."
        sys.stdout.flush()
        return
    # Next, I need to set the verbosity I want.
    c.ostream.set_verbosity(0)
    # Finally, I need to connect.
    try:
        c.Connect(retry = retry)
        print "Connected to", host, "at port", port
        sys.stdout.flush()
        tester = UnitTesterInterface(env = FakeCallEnvironment(c, None),
                                     as_hub = 1)
        c.gui = tester
        tester.mainloop()
    except GalaxyIO.ClientConnectionError:
        print "Couldn't connect to", host, "at port", port
        sys.stdout.flush()

# The unit tester can't exactly use DispatchFrame,
# since new messages are discarded. This doesn't work
# well with servers which send new messages instead of
# returning, like the double server...

MsgTypeNameTable = {GalaxyIO.GAL_MESSAGE_MSG_TYPE: "new message",
                    GalaxyIO.GAL_REPLY_MSG_TYPE: "reply message",
                    GalaxyIO.GAL_ERROR_MSG_TYPE: "error message",
                    GalaxyIO.GAL_POSTPONE_MSG_TYPE: "postpone message",
                    GalaxyIO.GAL_DESTROY_MSG_TYPE: "destroy message"}

def Usage():
    print "Usage: unit_tester --as_hub [--retry] [--frames file] host port [welcome_frame]"
    print "       unit_tester --as_server [--retry] [--frames file] [--ignore_reinitialize] [--service_type t]+ host port"
    sys.exit(1)

import getopt
optlist, args = getopt.getopt(sys.argv[1:], "",
                              ['service_type=', 'retry', "frames=",
                               'as_hub', 'as_server', 'ignore_reinitialize'])

if len(args) < 2 or len(args) > 3:
    Usage()
host = args[0]
try:
    port = string.atoi(args[1])
except:
    Usage()
how = None
stypes = []
retry = 0
frame_list = []
ignore_reinitialize = 0
for key, value in optlist:
    if key in ["--as_hub", "--as_server"]:
        if how is not None:
            print "One of --as_hub or --as_server must be specified."
            Usage()
        how = key
    elif key == "--service_type":
        stypes.append(value)
    elif key == "--retry":
        retry = 1
    elif key == "--ignore_reinitialize":
        ignore_reinitialize = 1
    elif key == "--frames":
        try:
            fp = open(value, "r")
            s = fp.read()
            fp.close()
            f_list, ignore = Galaxy._read_irp_value(s)
            if type(f_list) is not type([]):
                print "Couldn't parse frame file (should be list of frames). Skipping."
            else:
                for e in f_list:
                    if Galaxy.GetObjectType(e) is not Galaxy.GAL_FRAME:
                        print "Element of frame file list is not frame. Skipping."
                    else:
                        frame_list.append(e.PPrint())
        except IOError:
            print "Couldn't read frame file. Skipping."
if how is None:
    print "One of --as_hub or --as_server must be specified."
    Usage()

if (how == "--as_hub") and stypes:
    print "Ignoring service types as Hub."
if (how == "--as_server") and (not stypes):
    Usage()
welcome_frame = None
if len(args) == 3:
    if how == "--as_server":
        print "Ignoring welcome frame as server."
    else:
        try:
            welcome_frame = Galaxy.Frame(str = sys.argv[3])
        except Galaxy.FrameParsingError:
            print "Welcome frame cannot be parsed, skipping."

sys.stdout.flush()

# I hate global variables, so I'm going to add the frame
# list as a class variable to the UnitTesterInterface (I can't
# really pass it in in the server case).

UnitTesterInterface.seed_frame_history = frame_list

if how == "--as_hub":
    main_hub(host, port, retry, welcome_frame)
elif how == "--as_server":
    main_server(host, port, retry, ignore_reinitialize, stypes)
