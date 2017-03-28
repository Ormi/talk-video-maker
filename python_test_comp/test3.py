#!/usr/bin/env python

import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GObject, Gtk

class GTK_Main:

    def __init__(self):
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("Videotestsrc-Player")
        window.set_default_size(300, -1)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)
        self.button = Gtk.Button("Start")
        self.button.connect("clicked", self.start_stop)
        vbox.add(self.button)
        window.show_all()
        self.player = Gst.Pipeline.new("player")

        filesrc = Gst.ElementFactory.make("filesrc", "filesrc")
        filesrc.set_property("location", "slides.ts")

        sink = Gst.ElementFactory.make("xvimagesink", "video-output")
        caps = Gst.Caps.from_string("video/x-raw, width=320, height=230")
        decode = Gst.ElementFactory.make("decodebin", "decodebin")
        scale = Gst.ElementFactory.make("videoscale", "videoscale")
        convert = Gst.ElementFactory.make("videoconvert", "videoconvert")
        box = Gst.ElementFactory.make("videobox", "videobox")
        mixer = Gst.ElementFactory.make("videomixer", "videomixer")
        filter = Gst.ElementFactory.make("capsfilter", "filter")
        filter.set_property("caps", caps)


        self.player.add(filesrc)
        self.player.add(filter)
        self.player.add(decode)
        self.player.add(scale)
        self.player.add(convert)
        self.player.add(box)
        self.player.add(mixer)
        self.player.add(sink)

        filesrc.link(decode)
        decode.link(scale)
        scale.link(convert)
        convert.link(box)
        box.link(mixer)
        mixer.link(filter)
        filter.link(sink)                        

        #gst-launch-1.0 filesrc location=speaker.MTS ! decodebin ! videoscale ! videoconvert ! videobox ! videomixer ! xvimagesink    

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)


    def start_stop(self, w):
        if self.button.get_label() == "Start":
            self.button.set_label("Stop")
            self.player.set_state(Gst.State.PLAYING)
        else:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print ("Error: %s" % err, debug)
            self.button.set_label("Start")            

GObject.threads_init()
Gst.init(None)        
GTK_Main()
Gtk.main()