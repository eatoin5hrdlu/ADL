s = Server.local.boot;
s.waitForBoot{
	~prevnode = nil;
	~mport = NetAddr("127.0.0.1", NetAddr.langPort);

~files = [ "01c.wav",
	       "02c.wav",
	       "03c.wav",
	       "04c.wav",
	       "05c.wav",
	       "06c.wav",
           "07c.wav",
	       "08c.wav",
           "1ac.wav",
           "19c-old.wav"];

	~files.do({
		arg item,i; var b,p;
		b = Buffer.read(s, "/home/peter/src/sc/sounds/"++item);
		SynthDef(item, { Out.ar(0,PlayBuf.ar(1, b, BufRateScale.kr(b.bufnum), loop: 0));}).send(s);
	    OSCFunc({~adl.value(i)}, "/adl", ~mport, nil, [i]);
	});

	~adl = {
		arg which = 3;
		if(~prevnode != nil, { s.sendMsg("/n_free",~prevnode.nodeID) } );
		~prevnode = nil;
		~prevnode = Synth.new(~files[which]);
	};
}; // waitForBoot code block

