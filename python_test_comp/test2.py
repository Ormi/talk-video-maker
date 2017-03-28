import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, Gtk

# Initializing threads used by the Gst various elements
GObject.threads_init()
#Initializes the GStreamer library, setting up internal path lists, registering built-in elements, and loading standard plugins.
Gst.init(None)

class Main:
    def __init__(self):
        self.mainloop = GObject.MainLoop()
        #Creating the gst pipeline we're going to add elements to and use to play the file
        self.pipeline = Gst.Pipeline.new("mypipeline")

        #creating the filesrc element, and adding it to the pipeline
        self.filesrc = Gst.ElementFactory.make("filesrc", "filesrc")
        self.filesrc.set_property("location", "slides.ts")
        self.pipeline.add(self.filesrc)
        
        #creating and adding the decodebin element , an "automagic" element able to configure itself to decode pretty much anything
        self.decode = Gst.ElementFactory.make("decodebin", "decode")
        self.pipeline.add(self.decode)
        #connecting the decoder's "pad-added" event to a handler: the decoder doesn't yet have an output pad (a source), it's created at runtime when the decoders starts receiving some data
        self.decode.connect("pad-added", self.decode_src_created) 
        
        self.scale = Gst.ElementFactory.make("videoscale", "videoscale")
        self.pipeline.add(self.scale)

        self.convert = Gst.ElementFactory.make("videoconvert", "videoconvert")
        self.pipeline.add(self.convert)        

        self.box = Gst.ElementFactory.make("videobox", "videobox")
        self.pipeline.add(self.box)    

        self.mixer = Gst.ElementFactory.make("videomixer", "videomixer")
        self.pipeline.add(self.mixer)            

        #setting up (and adding) the alsasin, which is actually going to "play" the sound it receives
        self.sink = Gst.ElementFactory.make("xvimagesink", "xvimagesink")
        self.pipeline.add(self.sink)

        #linking elements one to another (here it's just the filesrc - > decoder link , the decoder -> sink link's going to be set up later)
        self.filesrc.link(self.decode)
        self.decode.link(self.scale)
        self.scale.link(self.convert)
        self.convert.link(self.box)
        self.box.link(self.mixer)
        self.mixer.link(self.sink)
            
    #handler taking care of linking the decoder's newly created source pad to the sink
    def decode_src_created(self, element, pad):
        pad.link(self.sink.get_static_pad("sink"))
        
    #running the shit
    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.mainloop.run()

start=Main()
start.run()