#!/usr/bin/env python

import sys, os
import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GObject, Gtk

class GTK_Main:

        # self.player = Gst.Pipeline.new("player")
        # source = Gst.ElementFactory.make("filesrc", "file-source")
        # decoder = Gst.ElementFactory.make("decodebin", "decider-bin")        
        # scale = Gst.ElementFactory.make("videoscale", "video-scaler")
        # caps = Gst.Caps.from_string("video/x-raw, width=400, height=200")
        # conv = Gst.ElementFactory.make("videoconvert", "colorspace-converter")
        # # alpha
        # box = Gst.ElementFactory.make("videobox", "video-box")
        # mixer = Gst.ElementFactory.make("videomixer", "video-mixer")
        # sink = Gst.ElementFactory.make("xvimagesink", "video-output")

        # self.player.add(source)
        # self.player.add(decoder)
        # self.player.add(scale)
        # self.player.add(conv)        
        # self.player.add(box)
        # self.player.add(mixer)        
        # self.player.add(sink)

        # source.link(decoder)
        # decoder.link(scale)
        # scale.link(conv)
        # conv.link(box)
        # box.link(mixer)
        # mixer.link(sink)    

    def __init__(self):
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("Videotestsrc-Player")
        window.set_default_size(300, -1)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)

        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, False, True, 0)

        self.button = Gtk.Button("Start")
        self.button.connect("clicked", self.start_stop)
        vbox.add(self.button)
        window.show_all()

        # self.player = Gst.Pipeline.new("player")
        # source = Gst.ElementFactory.make("videotestsrc", "video-source")
        # sink = Gst.ElementFactory.make("xvimagesink", "video-output")
        # caps = Gst.Caps.from_string("video/x-raw, width=320, height=230")
        # filter = Gst.ElementFactory.make("capsfilter", "filter")
        # filter.set_property("caps", caps)

        self.player = Gst.Pipeline.new("player")
        source = Gst.ElementFactory.make("filesrc", "file-source")
        decoder = Gst.ElementFactory.make("decodebin", "decider-bin")        
        scale = Gst.ElementFactory.make("videoscale", "video-scaler")
        #caps = Gst.Caps.from_string("video/x-raw, width=400, height=200")
        conv = Gst.ElementFactory.make("videoconvert", "colorspace-converter")
        # alpha
        box = Gst.ElementFactory.make("videobox", "video-box")
        mixer = Gst.ElementFactory.make("videomixer", "video-mixer")
        sink = Gst.ElementFactory.make("xvimagesink", "video-output")

        # self.player.add(source)
        # self.player.add(filter)
        # self.player.add(sink)

        self.player.add(source)
        self.player.add(decoder)
        self.player.add(scale)
        self.player.add(conv)        
        self.player.add(box)
        self.player.add(mixer)        
        self.player.add(sink)
        # for ele in [source, decoder, scale, audioconv, conv, box, mixer, sink]:
        #     self.player.add(ele)        

        # source.link(filter)
        # filter.link(sink)

        source.link(decoder)
        decoder.link(scale)
        scale.link(conv)
        conv.link(box)
        box.link(mixer)
        mixer.link(sink)      

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            filepath = self.entry.get_text().strip()
            if os.path.isfile(filepath):
                filepath = os.path.realpath(filepath)
                self.button.set_label("Stop")
                self.player.get_by_name("file-source").set_property("location", filepath)
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
            self.button.set_label("Start")
            err, debug = message.parse_error()
            print ("Error: %s" % err, debug)

GObject.threads_init()
Gst.init(None)        
GTK_Main()
Gtk.main()