import sys,string,os
import Galaxy, GalaxyIO

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

#def __PollTimer(self):
#    response, msg_type = self.env.conn.ReadFrame(blocking = 0)
#    if response is not None:
#        # Strip the administrative information.
#        try:
#            admin_info = response[Galaxy.GAL_HUB_OPAQUE_DATA_FRAME_KEY]
#            del response[Galaxy.GAL_HUB_OPAQUE_DATA_FRAME_KEY]
#        except KeyError:
#            admin_info = None
#        if (msg_type == GalaxyIO.GAL_MESSAGE_MSG_TYPE):
#            # Update the environment object. This will
#            # decode the administrative info.
#            self.env = FakeCallEnvironment(self.env.conn, None,
#                                           admin_info = admin_info,
#                                           frame_name = response.name)
#            _DoGenericDispatch(self.env, response)
#        else:
#            self.RecordMessage(response, "Received", msg_type)
#            

def SendNewMessage(env,f_text,s_text=None,round_trip=1,lock=0):
    _SendMessage(env,GalaxyIO.GAL_MESSAGE_MSG_TYPE,f_text,s_text,round_trip,lock)

def SendReply(env):
    _SendMessage(env,GalaxyIO.GAL_REPLY_MSG_TYPE)

def SendErrorReply(env):
    env.Error(env)

def SendDestroyReply(env):
    env.DestroyToken()

def _SendMessage(env,msg_type,f_text,s_text=None,round_trip=1,lock=0):
    try:
        new_f = Galaxy.Frame(str=f_text)
    except Galaxy.FrameParsingError:
        print "Cancelled."
        sys.stdout.flush()
        raise RuntimeError
    
    if msg_type == GalaxyIO.GAL_REPLY_MSG_TYPE:
        env.Reply(new_f)
    elif msg_type == GalaxyIO.GAL_MESSAGE_MSG_TYPE:
        # Do something, not sure what yet.
        if s_text and lock:
            env.SetSession(s_text,
                                GalaxyIO.GAL_SERVER_READS_ONLY_FROM_SESSION | GalaxyIO.GAL_SESSION_WRITES_ONLY_TO_SERVER | GalaxyIO.GAL_SERVER_WRITES_ONLY_TO_SESSION)
        elif s_text:
            env.UpdateSessionID(s_text)
        # Only want to wait for the reply if we're
        # not a Hub.
        if round_trip:
            try:
                reply_f = env.DispatchFrame(new_f)
                del reply_f[Galaxy.GAL_HUB_OPAQUE_DATA_FRAME_KEY]
                return reply_f
            except GalaxyIO.DispatchError,error_frame:
                del error_frame[Galaxy.GAL_HUB_OPAQUE_DATA_FRAME_KEY]
                raise RuntimeError,error_frame
        else:
            env.WriteFrame(new_f)


    
    
def main(host,port,retry):
    
    try:
        welcome_frame = None 
    except Galaxy.FrameParsingError:
        print "Welcome frame cannot be parsed, skipping."

    c = GalaxyIO.ClientConnection(host,port,welcome_frame,connect=0)
    if not c:
        print "No server."
        sys.stdout.flush()
        return
    # Next, I need to set the verbosity I want.
    c.ostream.set_verbosity(3)
    # Finally, I need to connect.
    try:
        c.Connect(retry=retry)
        print "Connected to", host, "at port", port
        sys.stdout.flush()
        
        env = FakeCallEnvironment(c,None)
        while True:
            try:
                 #:session_id "Default" :tidx 82 
                f_text = '''{c reinitialize}'''
                print SendNewMessage(env,f_text)
                f_text = '''{c gal_be.launch_query 
                                :inframe "{
    query    {
        place    {
            name    MURRAY AND HAZELWOOD
            type    stop
        }
        type    100
    }
}\n"
                            }'''
                print SendNewMessage(env,f_text)
                break
            except RuntimeError:
                print 'SendNewMessage Error'
        env.conn.Disconnect()
        
    except:
        print "Couldn't connect to", host, "at port", port
        sys.stdout.flush()

main('localhost',18000,1)

#def conn_BE(in_frame):
#    import socket
#    
#    remote_host = 'localhost'
#    remote_port = 23456
#    
#    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#    s.connect((remote_host,remote_port)) 
#    
#    sent = s.send(in_frame)
#    if not sent:
#        raise RuntimeError("socket connection broken")
#    
##    while True:
#    chunk = s.recv(1024)
#    print chunk
#    s.close
    
#conn_BE('''{
#    query    {
#        place    {
#            name    MURRAY AND HAZELWOOD
#            type    stop
#        }
#        type    100
#    }
#}\n''')