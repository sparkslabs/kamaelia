SinOsc osc => LPF lpf => dac;
0.5 => osc.gain;
700 => lpf.freq;
OscRecv recv;
2000 => recv.port;
recv.listen();

OscEvent positionEvent;

recv.event("/UITest/position, f f") @=> positionEvent;

while (true)
{
    positionEvent => now;
    while (positionEvent.nextMsg() != 0) {
        400 + (positionEvent.getFloat() * (1000 - 400)) => osc.freq;
        400 + positionEvent.getFloat() * (1000 - 400) => lpf.freq;
    }
}
