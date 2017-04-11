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

        video1 = "speaker.MTS"
        cover  = "pluto.jpg"
        video2 = "slides.ts"
        #video1 = "video2.mp4"
        #video2 = "video2.mp4"

        pipeline = ("filesrc location=%s ! decodebin name=demuxer demuxer. ! queue ! audioconvert ! audioresample ! autoaudiosink demuxer. ! queue ! videoscale ! video/x-raw,width=400, height=210 ! videoconvert ! videobox border-alpha=0 left=-1010 top=-560 ! videomixer name=mix ! xvimagesink filesrc location=%s ! jpegdec ! videoconvert ! imagefreeze ! mix. filesrc location=%s ! decodebin ! videoscale ! videoconvert ! videobox ! mix." % (video1, cover, video2))

        #filesrc = self.pipeline.get_by_name("demuxer")

        #print(pipeline)
        #creating the filesrc element, and adding it to the pipeline
        self.pipeline = Gst.parse_launch(pipeline)
            
    #handler taking care of linking the decoder's newly created source pad to the sink
    def decode_src_created(self, element, pad):
        print("Callback")
        pad.link(self.sink.get_static_pad("sink"))
        
    #running the shit
    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.mainloop.run()

start=Main()
start.run()